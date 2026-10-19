# 发布与冷启动手册

> 目标：把 `skill-forge` 从本地目录变成一个能被搜索、安装、审核、传播的公开资产。
>
> 当前状态（2026-10-19）：已发布到 <https://github.com/YaBoom/skill-forge>，
> v1.0.0 Release 已创建，8 个 topics 已设置，`npx skills add YaBoom/skill-forge -l`
> 已验证能识别 1 个 skill。`python scripts/preflight.py` 20/20 通过。
>
> 仍需你本人操作：Claude 官方表单提交（涉及账号登录与对外身份声明）；
> Codex 官方 `openai/plugins` 是 curated 集合，没有公开提交通道。

---

## 0. 先认清三条通道的现实

| 通道 | 现实门槛 | 你能得到什么 | 建议顺序 |
|---|---|---|---|
| GitHub + skills.sh | 零门槛，push 即可 | 真实安装量、榜单曝光、issue 反馈 | 第 1 天 |
| Claude 官方目录 | 提交表单 + 安全扫描 + 人工审核 | 品牌背书、`/plugin install` 直达 | 第 2–4 周 |
| Codex 官方插件库 | `openai/plugins` 是 curated 集合，PR 需审核 | Codex 内置曝光 | 第 2–4 周 |

注意两个事实：

1. `openai/skills` 已标记 deprecated，Codex 现在的官方示例仓库是 `openai/plugins`。
2. 官方目录不是“发布即上架”，没有 L2 的真实安装数据，L3 通过率很低。
   所以先把 skills.sh 跑出数据，再拿数据去申请官方目录。

---

## 1. 发布前最后验收

在本机执行：

```powershell
cd D:\workspaceForZhu\ai-code-pro\claude-codex-tools
python scripts/preflight.py
```

必须看到 `20/20 checks passed`。

再做一次真实触发测试（Claude Code 或 Codex 中）：

```text
把我们现在做的这个发布流程沉淀成一个 skill。
```

预期：模型加载 `skill-forge`，先产出证据台账与评分卡，而不是直接写一段提示词。
如果它没有加载，说明 `description` 需要按目标模型再调，先改描述再发布。

---

## 2. 推到 GitHub **[已完成]**

仓库已创建：<https://github.com/YaBoom/skill-forge>

首次提交：`c512f85 feat: add skill-forge for Claude Code and Codex`

Release：<https://github.com/YaBoom/skill-forge/releases/tag/v1.0.0>

以下命令保留作为换机或重建仓库时的参考：

```powershell
git init
git add .
git commit -m "feat: add skill-forge for Claude Code and Codex"
git branch -M main
gh repo create YaBoom/skill-forge --public --source=. --remote=origin --push
```

没有 `gh` CLI 就在 GitHub 网页新建空仓库，然后：

```powershell
git remote add origin https://github.com/YaBoom/skill-forge.git
git push -u origin main
```

提交身份已确认使用 `YaBoom <15007105273@163.com>`，无需再配置。

---

## 3. 上架 skills.sh

push 之后：

1. 打开 `https://skills.sh/YaBoom/skill-forge`，确认是否已被索引。
2. 本地验证安装：

```powershell
npx skills add YaBoom/skill-forge -s skill-forge -g -y
```

3. 验证后检查安装目录是否出现 `skill-forge/SKILL.md`。
4. 若未被索引，在仓库 README 顶部保留 `## Install` 段与 `npx skills add` 命令，
   等待抓取或通过 skills.sh 页面提交收录。

skills.sh 的关键指标是**累计安装量**，不是 star。安装量来自真实用户执行
`npx skills add`，所以发布文案要直接给命令，不要只给仓库链接。

---

## 4. 提交 Claude 官方目录 **[你]**

入口：`https://claude.com/marketplace`，按页面指引提交 external plugin。
审核流程：提交 → 自动安全扫描 → 人工审核 → 通过后手动选择上线时间。

提交时使用以下英文材料（可直接复制）：

**Plugin name**

```text
skill-forge
```

**Short description**

```text
Turn a workflow you just finished into a tested, publish-ready Agent Skill.
```

**Long description**

```text
Skill Forge harvests evidence from the current session, git history, and project
files, distills it into a portable procedure, scores it against eight quality gates,
and packages the result for Claude Code, Codex, Cursor, and skills.sh. Every run
returns a scorecard, an evidence ledger, trigger tests, and a publish plan, so a skill
cannot ship on vibes alone.
```

**Category**

```text
development
```

**审核前自查**

- `name` 一旦发布不可修改，确认就是 `skill-forge`。
- 仓库里没有密钥、绝对路径、客户名。
- `SKILL.md` 能独立触发，审核员不需要读 README 才能用。
- 版本号 `1.0.0` 与 manifest 一致。

---

## 5. 提交 Codex 官方插件库 **[你]**

`openai/plugins` 是 curated 集合。标准做法：

```powershell
gh repo fork openai/plugins --clone
```

在 fork 中新增：

```text
plugins/skill-forge/
├── .codex-plugin/plugin.json
├── skills/skill-forge/...
└── README.md
```

在 `.agents/plugins/marketplace.json` 的 `plugins` 数组追加：

```json
{
  "name": "skill-forge",
  "source": { "source": "local", "path": "./plugins/skill-forge" },
  "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
  "category": "Developer Tools"
}
```

PR 标题与说明：

```text
Add skill-forge plugin

Skill Forge turns a completed workflow into a tested, publish-ready Agent Skill.
It provides an eight-gate quality scorecard, trigger tests, and dual packaging for
Claude Code and Codex. No credentials, no network calls, no bundled binaries.
```

如果维护者只接受官方合作方插件，就把这份 PR 当作公开记录，主战场放回 skills.sh。

---

## 6. 冷启动内容策略

### 核心叙事（不要写成“我做了个 Skill”）

> 我拆了 skills.sh 上安装量最高的 30 个 Skill，发现大多数新 Skill 死于同一件事：
> 不是功能不够强，而是**根本不会被触发**，或者只在自己的仓库里能用。
> 所以我把“从一次真实工作流蒸馏出可发布 Skill”做成了一个 Skill。

这个叙事同时具备：数据、冲突、可验证方法、明确产物。

### 渠道与节奏

| 天 | 渠道 | 内容 | 目标 |
|---|---|---|---|
| D0 | GitHub + skills.sh | 仓库、README、安装命令 | 可安装 |
| D1 | X / LinkedIn | 8 门禁图 + 一条命令 | 首批安装 |
| D2 | Reddit r/ClaudeAI、r/CodexAI | “Why your skill never triggers” 复盘 | 讨论与 issue |
| D3 | Hacker News `Show HN` | 数据 + 方法，不放广告 | 长尾流量 |
| D4 | 掘金 / 少数派 / V2EX | 中文完整拆解（可直接用 `docs/market-analysis.md`） | 中文圈扩散 |
| D7 | 小红书 / 公众号 | “我如何把 3 小时的一次性工作变成可复用资产” | 非开发者受众 |

### 发布文案（英文，可直接用）

```text
Most Agent Skills fail for one reason: they never trigger.

I analyzed the top 30 skills on skills.sh. The winners are entry points
(find-skills, 3.9M), verifiable deliverables (frontend-design, 1M), or a
subscribable methodology (mattpocock, 10+ slots).

Almost nobody solves the harder problem: I just finished a workflow — how do I
turn it into something publishable?

So I built skill-forge:
→ harvests evidence from the session, git history, and repo
→ distills 7 elements (trigger, inputs, steps, decisions, failures, verification, output)
→ scores 8 quality gates (release needs 13/16, safety must be 2)
→ generates SKILL.md + references + assets + scripts
→ packages for Claude Code, Codex, Cursor, and skills.sh

One command:
npx skills add YaBoom/skill-forge -s skill-forge -g -y

Repo: https://github.com/YaBoom/skill-forge
```

### 中文文案（可直接用）

```text
我扒了 skills.sh 安装量最高的 30 个 Skill，发现一个反常识的事实：
排第一的 find-skills 有 390 万安装，它本身不解决任何业务问题，
只负责告诉你“该装什么”。

真正稀缺的不是又一个提示词，而是把“我刚做完的一次工作”变成可复用资产的能力。

所以我做了 skill-forge：
· 从会话、git 历史、项目文件里采集证据
· 蒸馏成 7 个要素：触发、输入、步骤、分支、失败、验证、产物
· 过 8 道质量门禁，低于 13/16 不允许发布
· 自动生成 Claude Code / Codex 双市场安装包

一条命令：
npx skills add YaBoom/skill-forge -s skill-forge -g -y
```

---

## 7. 发布后 14 天的指标与动作

| 指标 | 看什么 | 低于预期时做什么 |
|---|---|---|
| 安装量 | skills.sh 页面 | 改 README 第一屏，把命令提前；补 3 个真实案例 |
| 触发率 | 用户反馈“装了没反应” | 重写 `description`，增加用户原话触发词 |
| Issue 类型 | 安装失败 / 触发失败 / 质量建议 | 安装失败优先修，触发失败次之 |
| Star | GitHub | 不追 star，追安装；star 只影响开发者信任 |
| 官方审核 | 表单状态 | 被拒时要求具体原因，逐条修复后再提交 |

### 版本节奏

- `1.0.x`：修触发词、修安装路径、补示例。
- `1.1.0`：新增 3–5 个场景配方（PR review、迁移、发布、文档、数据清洗）。
- `2.0.0`：支持团队级 marketplace 与 CI 校验。

---

## 8. 现在需要你决定的 3 件事

1. GitHub 仓库名是否用 `skill-forge`（影响所有安装命令与官方提交）。
2. 是否现在执行 `git init` + 首次 commit + push（我可以代跑，但需要你确认）。
3. 官方目录由你提交还是我生成完整表单草稿后你粘贴（涉及你的账号登录）。

确认后，我可以继续完成 commit、发布文案配图、以及首个场景配方的示例。
