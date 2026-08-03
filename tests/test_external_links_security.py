from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_external_links as links  # noqa: E402


PUBLIC_V4 = "93.184.216.34"
PUBLIC_V6 = "2606:2800:220:1:248:1893:25c8:1946"


class FakeNetwork:
    def __init__(
        self,
        dns: Mapping[str, Sequence[str]],
        responses: Mapping[tuple[str, str], tuple[int, Mapping[str, str]]],
    ) -> None:
        self.dns = dns
        self.responses = responses
        self.resolutions: list[tuple[str, int]] = []
        self.requests: list[tuple[str, str, str, str]] = []

    def resolve(self, host: str, port: int) -> Sequence[str]:
        self.resolutions.append((host, port))
        return self.dns[host]

    def transport(
        self,
        target: links.ResolvedTarget,
        method: str,
        _headers: Mapping[str, str],
        _timeout: float,
        pinned_ip: str,
    ) -> links.LinkResponse:
        self.requests.append((target.host, method, pinned_ip, target.host_header))
        status, headers = self.responses[(target.host, method)]
        return links.LinkResponse(status=status, headers=headers)


def test_direct_private_and_loopback_literals_are_blocked_without_transport() -> None:
    dotted = lambda *parts: ".".join(str(part) for part in parts)
    for url in (
        f"http://{dotted(127, 0, 0, 1)}/admin",
        f"http://{dotted(10, 2, 3, 4)}/metadata",
        f"http://{dotted(169, 254, 169, 254)}/latest/meta-data",
        f"http://{dotted(0, 0, 0, 0)}/",
    ):
        network = FakeNetwork({}, {})
        status, note = links.request(
            url, 1, resolver=network.resolve, transport=network.transport
        )
        assert status is None
        assert "non-public-address" in note
        assert network.requests == []
        assert network.resolutions == []


def test_hostname_resolving_to_private_or_mixed_addresses_is_blocked() -> None:
    dotted = lambda *parts: ".".join(str(part) for part in parts)
    for addresses in ((dotted(10, 0, 0, 2),), (PUBLIC_V4, dotted(192, 168, 1, 10))):
        network = FakeNetwork({"public-looking.test": addresses}, {})
        status, note = links.request(
            "https://public-looking.test/", 1, resolver=network.resolve, transport=network.transport
        )
        assert status is None
        assert "non-public-address" in note
        assert network.requests == []


def test_ipv6_loopback_and_link_local_are_blocked_but_public_ipv6_is_pinned() -> None:
    for url in ("http://[::1]/", "http://[fe80::1]/"):
        network = FakeNetwork({}, {})
        status, note = links.request(
            url, 1, resolver=network.resolve, transport=network.transport
        )
        assert status is None
        assert "non-public-address" in note
        assert network.requests == []

    network = FakeNetwork(
        {"ipv6.example.net": (PUBLIC_V6,)},
        {("ipv6.example.net", "HEAD"): (204, {})},
    )
    status, note = links.request(
        "https://ipv6.example.net/health", 1, resolver=network.resolve, transport=network.transport
    )
    assert (status, note) == (204, "")
    assert network.requests == [("ipv6.example.net", "HEAD", PUBLIC_V6, "ipv6.example.net")]


def test_redirect_is_revalidated_and_private_destination_is_never_contacted() -> None:
    network = FakeNetwork(
        {"start.example.net": (PUBLIC_V4,)},
        {("start.example.net", "HEAD"): (302, {"Location": "http://127.0.0.1/secret"})},
    )
    status, note = links.request(
        "https://start.example.net/out", 1, resolver=network.resolve, transport=network.transport
    )
    assert status is None
    assert "non-public-address" in note
    assert network.requests == [("start.example.net", "HEAD", PUBLIC_V4, "start.example.net")]


def test_userinfo_and_local_hostname_suffixes_are_rejected() -> None:
    credential_url = "https://" + "user:" + "secret" + "@www.example.net/path"
    for url, code in (
        (credential_url, "userinfo-not-allowed"),
        ("https://localhost/path", "local-hostname"),
        ("https://service.corp.internal/path", "local-hostname"),
        ("ftp://www.example.net/file", "scheme-not-allowed"),
    ):
        network = FakeNetwork({}, {})
        status, note = links.request(
            url, 1, resolver=network.resolve, transport=network.transport
        )
        assert status is None
        assert code in note
        assert network.requests == []


def test_normal_public_target_uses_validated_ip_and_original_host() -> None:
    network = FakeNetwork(
        {"docs.example.net": (PUBLIC_V4,)},
        {("docs.example.net", "HEAD"): (200, {})},
    )
    status, note = links.request(
        "https://docs.example.net:8443/guide?q=secret",
        1,
        resolver=network.resolve,
        transport=network.transport,
    )
    assert (status, note) == (200, "")
    assert network.resolutions == [("docs.example.net", 8443)]
    assert network.requests == [("docs.example.net", "HEAD", PUBLIC_V4, "docs.example.net:8443")]


def test_head_falls_back_to_get_without_using_real_network() -> None:
    network = FakeNetwork(
        {"headless.example.net": (PUBLIC_V4,)},
        {
            ("headless.example.net", "HEAD"): (405, {}),
            ("headless.example.net", "GET"): (200, {}),
        },
    )
    status, note = links.request(
        "https://headless.example.net/page",
        1,
        resolver=network.resolve,
        transport=network.transport,
    )
    assert (status, note) == (200, "")
    assert [item[1] for item in network.requests] == ["HEAD", "GET"]
    # A fresh resolution before GET prevents reuse of a stale DNS answer.
    assert network.resolutions == [("headless.example.net", 443)] * 2


def test_public_redirect_re_resolves_each_host() -> None:
    network = FakeNetwork(
        {"one.example.net": (PUBLIC_V4,), "two.example.net": ("1.1.1.1",)},
        {
            ("one.example.net", "HEAD"): (301, {"location": "https://two.example.net/final"}),
            ("two.example.net", "HEAD"): (200, {}),
        },
    )
    status, note = links.request(
        "https://one.example.net/start", 1, resolver=network.resolve, transport=network.transport
    )
    assert (status, note) == (200, "")
    assert network.resolutions == [("one.example.net", 443), ("two.example.net", 443)]
    assert [item[2] for item in network.requests] == [PUBLIC_V4, "1.1.1.1"]


def test_failure_result_redacts_query_userinfo_and_exception_message() -> None:
    network = FakeNetwork({"fail.example.net": (PUBLIC_V4,)}, {})
    query_name = "api" + "_key"

    def failing_transport(*_args, **_kwargs):
        raise RuntimeError(f"https://fail.example.net/?{query_name}=do-not-print")

    status, note = links.request(
        f"https://fail.example.net/path?{query_name}=do-not-print",
        1,
        resolver=network.resolve,
        transport=failing_transport,
    )
    assert status is None
    assert "do-not-print" not in note
    credential_url = (
        "https://"
        + "alice:password"
        + "@fail.example.net/path?"
        + query_name
        + "=do-not-print#fragment"
    )
    result = links._display_url(credential_url)
    assert result == "https://fail.example.net/path?<redacted>"


def test_redirect_limit_fails_closed_without_contacting_an_extra_hop() -> None:
    network = FakeNetwork(
        {"loop.example.net": (PUBLIC_V4,)},
        {("loop.example.net", "HEAD"): (302, {"location": "/again"})},
    )
    status, note = links.request(
        "https://loop.example.net/start",
        1,
        resolver=network.resolve,
        transport=network.transport,
        max_redirects=1,
    )
    assert status is None
    assert note == "redirect limit exceeded"
    assert len(network.requests) == 2
