async page => {
  const origin = page.url().replace(/\/+$/, "");
  const homeUrl = `${origin}/`;
  const checks = [];
  const failures = [];
  const consoleMessages = [];
  const pageErrors = [];
  const requestFailures = [];
  const externalRequests = [];
  const httpErrors = [];

  const record = (name, passed, detail) => {
    checks.push({ name, passed, detail });
    if (!passed) failures.push(`${name}: ${detail}`);
  };

  page.on("console", message => {
    consoleMessages.push({ type: message.type(), text: message.text() });
  });
  page.on("pageerror", error => pageErrors.push(String(error)));
  page.on("requestfailed", request => {
    requestFailures.push({
      url: request.url(),
      error: request.failure()?.errorText || "unknown",
    });
  });
  page.on("request", request => {
    const url = request.url();
    if (/^(data|blob):/.test(url)) return;
    if (url !== origin && !url.startsWith(`${origin}/`)) externalRequests.push(url);
  });
  page.on("response", response => {
    if (response.status() >= 400) {
      httpErrors.push({ status: response.status(), url: response.url() });
    }
  });

  page.setDefaultTimeout(15000);
  page.setDefaultNavigationTimeout(20000);
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.emulateMedia({ colorScheme: "light", reducedMotion: "reduce" });
  await page.goto(homeUrl, { waitUntil: "networkidle" });
  await page.evaluate(() => localStorage.clear());
  await page.goto(homeUrl, { waitUntil: "networkidle" });

  const viewport = page.viewportSize();
  record(
    "PC 视口为 1440×1000",
    viewport?.width === 1440 && viewport?.height === 1000,
    JSON.stringify(viewport),
  );

  const homeTitle = await page.title();
  const homeHeading = await page.locator("h1").first().innerText();
  record(
    "首页标题与主标题可见",
    homeTitle.includes("FlowAgentic 培训与操作 Playbook") &&
      homeHeading.includes("FlowAgentic 培训与操作 Playbook"),
    `${homeTitle} | ${homeHeading}`,
  );

  const homeMermaidScripts = await page.locator(
    'script[src*="assets/vendor/mermaid.min.js"]',
  ).count();
  record(
    "非图表首页不加载 Mermaid",
    homeMermaidScripts === 0,
    `script_count=${homeMermaidScripts}`,
  );

  const initialTheme = await page.locator("body").getAttribute("data-md-color-scheme");
  record("浅色主题为默认值", initialTheme === "default", String(initialTheme));
  await page.evaluate(() => document.getElementById("__palette_1")?.click());
  await page.waitForFunction(
    () => document.body.getAttribute("data-md-color-scheme") === "slate",
  );
  const toggledTheme = await page.locator("body").getAttribute("data-md-color-scheme");
  record("主题切换可用", toggledTheme === "slate", String(toggledTheme));

  await page.evaluate(() => document.querySelector("label[for=__search]")?.click());
  const searchInput = page.locator('[data-md-component="search-query"]');
  await searchInput.click();
  await searchInput.pressSequentially("OpenAI Assistant", { delay: 20 });
  await page.locator(".md-search-result__item").first().waitFor({ state: "visible" });
  const searchText = await page.locator(".md-search-result__list").innerText();
  record(
    "中文搜索可检索英文白名单术语",
    searchText.includes("OpenAI Assistant"),
    searchText.slice(0, 240),
  );

  await page.goto(`${origin}/09-tools-mcp/`, { waitUntil: "networkidle" });
  const migrationHeading = page.getByRole("heading", {
    name: "旧 Token 迁移与重新启用",
  });
  record(
    "MCP 旧 Token 迁移章节可见",
    await migrationHeading.isVisible(),
    await migrationHeading.innerText(),
  );

  const pdfResponse = await page.request.get(
    `${origin}/assets/downloads/flowagentic-playbook.pdf`,
  );
  const pdfBody = await pdfResponse.body();
  const pdfType = pdfResponse.headers()["content-type"] || "";
  record(
    "中文 PDF 可下载且格式有效",
    pdfResponse.ok() &&
      pdfType.toLowerCase().includes("application/pdf") &&
      pdfBody.length > 1_000_000 &&
      pdfBody.subarray(0, 5).toString() === "%PDF-",
    `status=${pdfResponse.status()} type=${pdfType} bytes=${pdfBody.length}`,
  );

  await page.goto(`${origin}/404.html`, { waitUntil: "networkidle" });
  const notFoundHeading = await page.getByRole("heading", { level: 1 }).innerText();
  record(
    "404 页面为中文并可访问",
    notFoundHeading.trim() === "页面未找到",
    notFoundHeading,
  );

  await page.goto(`${origin}/01-system/`, { waitUntil: "networkidle" });
  const diagram = page.locator("div.mermaid").first();
  await diagram.waitFor({ state: "visible" });
  const diagramBox = await diagram.boundingBox();
  const unrenderedDiagrams = await page.locator("pre.mermaid").count();
  const mermaidScripts = await page.locator(
    'script[src*="assets/vendor/mermaid.min.js"]',
  ).count();
  record(
    "系统数据流图完成渲染",
    Boolean(
      diagramBox &&
        diagramBox.height > 50 &&
        diagramBox.width > 100 &&
        unrenderedDiagrams === 0
    ),
    JSON.stringify({ diagramBox, unrenderedDiagrams }),
  );
  record(
    "图表页仅加载一份自托管 Mermaid",
    mermaidScripts === 1,
    `script_count=${mermaidScripts}`,
  );

  const userAgent = await page.evaluate(() => navigator.userAgent);
  const isFirefox = userAgent.includes("Firefox/");
  const consoleErrors = consoleMessages.filter(item => item.type === "error");
  const consoleWarnings = consoleMessages.filter(item =>
    item.type === "warning" || item.type === "warn",
  );
  const unexpectedWarnings = consoleWarnings.filter(item =>
    !(isFirefox && item.text.includes("unreachable code after return statement")),
  );
  record(
    "控制台无错误和意外警告",
    consoleErrors.length === 0 &&
      pageErrors.length === 0 &&
      unexpectedWarnings.length === 0,
    JSON.stringify({ consoleErrors, pageErrors, unexpectedWarnings }),
  );
  record(
    "页面请求无外联、失败或 HTTP 错误",
    externalRequests.length === 0 &&
      requestFailures.length === 0 &&
      httpErrors.length === 0,
    JSON.stringify({ externalRequests, requestFailures, httpErrors }),
  );

  const summary = {
    status: failures.length ? "failed" : "passed",
    browser: isFirefox ? "firefox" : "chrome",
    userAgent,
    origin,
    checks,
    allowedWarnings: consoleWarnings.filter(item => !unexpectedWarnings.includes(item)),
    failures,
  };
  if (failures.length) {
    throw new Error(`Playbook browser smoke failed\n${JSON.stringify(summary, null, 2)}`);
  }
  return summary;
}
