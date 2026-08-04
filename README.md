# FlowAgentic 培训与操作 Playbook

这是一个与 FlowAgentic 产品源码完全独立的公开培训站点工程，面向新手使用者、流程搭建者、二次开发者和管理员／运维人员。站点基于 MkDocs Material，使用 mike 管理版本，并同时生成 GitHub Pages 站点和中文 PDF。

当前状态是“完整工作草案”。基线逻辑来自 Flowise `3.1.3` 和已合并、主分支 CI 通过的源码提交 `96f6ae464f7f4757883a5ba6bec26ca951b4da4d`。正式截图和公开发布仍必须等待这一精确提交完成生产部署与中文 PC 端验收，并通过截图脱敏和其余外部门禁。

## 本地运行

需要 Python `3.12`、Node.js `22`、[uv](https://docs.astral.sh/uv/) 和 Chrome／Firefox。

```bash
uv sync --frozen --all-groups
uv run python scripts/vendor_assets.py
uv run python scripts/validate_all.py
uv run pyright
uv run pytest -q
uv run mkdocs serve
```

查看当前机器可读发布状态：

```bash
uv run python scripts/release_readiness.py
```

严格构建站点和 PDF：

```bash
uv run mkdocs build --strict
uv run python scripts/build_pdf.py \
  --site-dir site \
  --output output/pdf/flowagentic-playbook.pdf \
  --tmp-dir tmp/pdfs
uv run python scripts/validate_pdf.py output/pdf/flowagentic-playbook.pdf
uv run python scripts/validate_public_artifacts.py \
  --site-dir site \
  --pdf output/pdf/flowagentic-playbook.pdf
```

完成构建和 PDF 生成后，以固定版本的 Playwright CLI 在 Chrome 与 Firefox 重放静态站主链：

```bash
npm ci
bash scripts/playwright_cli.sh install-browser chrome
bash scripts/playwright_cli.sh install-browser firefox
npm run browser:smoke
```

浏览器脚本固定使用 `1440×1000` 视口，验证首页、主题、搜索、MCP 迁移章节、Mermaid、404、PDF、控制台和外联请求。它只证明当前构建制品在本地浏览器可运行，不构成 FlowAgentic 产品生产环境的 PC 验收、正式截图或 GitHub Pages 发布证据。

Linux CI 会安装 `fonts-noto-cjk`。本地生成发布级 PDF 前，也必须安装 Noto Sans CJK，并增加 `--require-noto`。

## 发布模型

- PR 和 `main` 分支提交只验证并上传预览制品，不会更新公开站。
- 本地、PR 和 `main` 预览不启用版本切换器，避免在尚未生成 mike 版本树时请求不存在的 `versions.json`。
- 只有手动触发“发布版本”工作流才会写入独立的 `gh-pages` 分支；构建验证使用只读权限，并把同一份已验证 mike 静态树同时封装为 Pages 制品。受 `github-pages` 环境保护的写权限 Job 先对该树执行一次提交和一次推送，再由 `actions/deploy-pages` 部署完全相同的制品。
- 发布版本名必须为 `flowagentic-<产品版本>-<7 至 12 位短 SHA>`，并与 40 位发布 SHA 一致。
- 中文验收门禁和截图门禁都必须显式为 `passed`，确认词必须为 `publish`。
- 工作流输入还必须与 `data/release.yml`、截图基线、截图计划和截图 manifest 相互一致；只修改手动输入无法绕过仓库内证据绑定。
- 九道外部门禁使用代码固定的证据 ID；每个回执都必须绑定 `data/evidence/` 中的公开安全制品并由 CI 重算摘要。Provider 成功还必须通过信任清单中的外部 Ed25519 隔离执行器验签，本仓库不保存签名私钥。
- Pages 必须保持 `workflow` 构建模式，并把根目录来源绑定到独立 `gh-pages` 发布留档分支；单独推送分支不构成部署证据，只有 `actions/deploy-pages` 成功、部署记录和公开 URL 冒烟同时通过才可宣称发布。
- 发布工作流只使用 GitHub 自动签发的 `GITHUB_TOKEN` 与短期 OIDC 身份；不得配置或复用产品源码仓库的部署密钥。
- 仓库采用单维护者治理：`main` 启用管理员同样受约束的分支保护，所有变更必须经过 PR 和必需状态检查；由于 GitHub 禁止作者批准自己的 PR，批准数固定为 0。`github-pages` 环境仍必须经过人工审批。

独立公开仓库已经接入 [zjgulai/flowagentic-training-playbook](https://github.com/zjgulai/flowagentic-training-playbook)。`main` 必须经过 PR 和“站点、PDF 与内容门禁”检查；单维护者模式不把管理员身份或自动检查伪装成独立人工批准。`github-pages` 环境必须经过人工审批。`gh-pages` 已完成不含入口页的基础设施引导，Pages 保持 `workflow` 模式且部署记录仍为 0；该分支当前不是正式站点，公开 URL 返回 404。

同版本隔离培训环境的基础运行验收已经通过；在生产 G1、正式截图门禁和安全提供的 Provider 凭据到位前，仍不执行正式截图、Provider 实验或公开发布。

### 独立 GitHub 仓库接入门禁

收到用户指定的空仓库 URL 后，先运行纯 GET 的接入检查。`intake` 阶段要求仓库公开、独立、空白、处于启用状态，且当前操作者具有管理员权限：

```bash
uv run python scripts/github_repository_readiness.py \
  --repository OWNER/REPO \
  --phase intake \
  --output tmp/github-repository-intake.json
```

完成独立历史的首次推送、`gh-pages` 引导、Pages 来源、`github-pages` 环境人工审批，以及 `main` 的单维护者 PR 和必需状态检查配置后，再运行发布阶段审计：

```bash
uv run python scripts/github_repository_readiness.py \
  --repository OWNER/REPO \
  --phase release \
  --governance-mode solo-maintainer \
  --output tmp/github-repository-release.json
```

该工具只调用 GitHub GET API，不会创建仓库、添加 remote、推送分支、修改保护规则、部署 Pages 或更新 `data/release.yml`。检查通过只代表“可生成待人工复核的门禁材料”，不能代替人工回执，也不能单独证明 GitHub Pages 已发布。

## 独立性与隐私

```bash
uv run python scripts/check_independence.py
```

检查会拒绝 submodule/gitlink、嵌套 Git 历史、产品源码仓库远端、跨仓库可复用发布工作流和常见部署密钥文件。站点不启用分析、遥测或第三方字体；Mermaid 运行时脚本以固定版本和哈希自托管。

公开仓库不得包含真实账号、邮箱、域名、IP、Token、Cookie、资源 ID、生产拓扑、备份恢复命令或回执。所有课程数据必须为合成数据。

## 许可

- 原创正文与培训材料：[CC BY-NC-SA 4.0](LICENSE-CONTENT)
- 示例代码与本仓库自动化脚本：[MIT](LICENSE-CODE)

第三方产品界面、商标和研究来源不因本仓库的许可声明而改变其原有权利归属。
