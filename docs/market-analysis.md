# Codex / Claude Agent Skill 市场热度分析与选题推导

> 数据采集时间：2026-10-19。安装量来自 skills.sh 公开榜单，插件生态信息来自
> anthropics/skills、anthropics/claude-plugins-official、openai/plugins。
> 部分中文媒体的 star 数据口径不一，本文只采用可交叉验证的部分，并在文中标注。

---

## 1. 一句话结论

当前 Skill 市场的流量不奖励“更强的提示词”，而奖励三种东西：

1. **入口**：帮用户决定“该装什么”的元技能（find-skills 累计约 390 万安装）；
2. **可验证的产物**：装完能立刻产出文档、页面、视频、代码变更的技能；
3. **可订阅的作者方法论**：用户装的不是单个功能，而是某个工程师的工作方式。

`skill-forge` 的选题，就是把 1 和 2 合并：**把用户刚做完的一次真实工作，反向蒸馏成可发布、可验证、可安装的 Skill 资产。**

---

## 2. 市场热度快照（skills.sh，2026-10-19）

| 排名 | Skill | 发布方 | 累计安装 | 类型 |
|---|---|---|---|---|
| 1 | find-skills | vercel-labs | 3.9M | 入口 / 元技能 |
| 2 | grill-me | mattpocock | 1.4M | 需求澄清 |
| 3 | grill-with-docs | mattpocock | 1.2M | 需求澄清 |
| 4 | agent-browser | vercel-labs | 1.2M | 浏览器自动化 |
| 5 | improve-codebase-architecture | mattpocock | 1.1M | 代码质量 |
| 6 | tdd | mattpocock | 1.1M | 工程流程 |
| 7 | hyperframes-cli | heygen-com | 1.1M | 视频生成 |
| 8 | hyperframes | heygen-com | 1.1M | 视频生成 |
| 9 | setup-matt-pocock-skills | mattpocock | 1.0M | 套件安装器 |
| 10 | handoff | mattpocock | 1.0M | 多 Agent 协作 |
| 11 | frontend-design | anthropics | 1.0M | 设计 / 前端 |
| 12 | reddit-automation | flowkit-labs | 994K | 增长自动化 |
| 13 | triage | mattpocock | 962K | Issue 治理 |
| 14 | prototype | mattpocock | 958K | 原型 |
| 17 | grilling | mattpocock | 941K | 需求澄清（真正的方法论） |
| 31 | lark-doc | open.feishu.cn | 783K | 平台集成（飞书全家桶合计 17.9M） |
| 78 | azure-diagnostics | microsoft | 561K | 云平台（Azure 全家桶合计 7.3M） |
| 170 | skill-creator | anthropics | 409K | 造 Skill 的 Skill |
| 257 | writing-great-skills | mattpocock | 307K | Skill 写作方法论 |
| 284 | write-a-skill | mattpocock | 220K | 造 Skill 的 Skill |
| — | caveman / caveman-compress | juliusbrussee | 580K / 403K | Token 压缩 |

### 从榜单直接读出的四个事实

**事实一：入口型产品赢家通吃。**
find-skills 的安装量是第二名的 2.8 倍。它本身不解决任何业务问题，只负责“告诉你该装什么”。
安装它之后会带出更多安装，形成自我强化的分发飞轮。

**事实二：个人方法论可以规模化。**
Matt Pocock 一人占据 Top 30 中的 10+ 席，合计超过 2.7M 安装。
用户安装 `setup-matt-pocock-skills` 的本质是“订阅这个人”，而不是“需要这个功能”。

**事实三：企业套件靠平台绑定冲量，但单品留存弱。**
飞书 20+ 个 `lark-*` 技能合计 17.9M，微软 Azure 全家桶 7.3M。
这是“已经用这个平台的人顺手装”，不是“技能本身出圈”。个人开发者无法复制这条路径。

**事实四：造 Skill 的需求已被验证，但产品形态仍停留在“从零手写”。**
- skill-creator（Anthropic 官方）：409K
- writing-great-skills（Matt）：307K
- write-a-skill（Matt）：220K

三者都在教用户“如何写一个 Skill”，输入是用户的**口述与想象**。
没有人解决更难、更高频的问题：**我刚刚已经做成了一件事，怎么把它沉淀下来？**

### 竞品复核（2026-10-19）

`npx skills find skill-forge` 返回的同名与近似条目：

| Skill | 安装量 | 定位 | 与我们的关系 |
|---|---|---|---|
| browser-act/skills@browser-act-skill-forge | 85.2K | 浏览器自动化场景 | 名称近似，场景不同 |
| sanyuan0704/sanyuan-skills@skill-forge | 4.1K | Skill 写作规范（token 成本铁律） | 直接相邻，但输入是写作规范，不是已完成工作流 |
| ngmeyer/skills@skillforge | 311 | 同名近似 | 长尾 |
| yujunzhixue/github-skill-forge | 152 | GitHub 场景 | 场景不同 |

结论：`skill-forge` 不是空白词，存在 4.1K 量级的相邻竞品。差异化不在“教你写 skill”，
而在“从已完成工作流反向蒸馏 + 可执行审计 + 双市场打包”。因此保留名称，
并在 description 中强化 `evidence-backed` 与 `already-completed`。

---

## 3. 播客案例拆解：Treg 的 Codex 插件为什么能改变增长曲线

节目：十字路口《新的创业机会，正在 Claude Code 和 Codex 周围长出来》
shownotes 关键节点：`00:14:42 一个 Codex 插件，意外改变了增长曲线`、`00:18:04 Agent 最常买什么工具？`、`00:20:13 浏览器抓不到的数据，就是工具市场的价值`、`00:21:57 Treg 为什么更像 Costco？`

结合公开资料，Treg 的路径可以还原为：

| 阶段 | 产品 | 结果 | 教训 |
|---|---|---|---|
| 1 | SuperDesign（设计 Agent） | 6000+ GitHub Star | 模型能力一升级，应用层被吞噬 |
| 2 | 增长 Agent | 收入不稳 | 垂直 Agent 陷入“绝境” |
| 3 | Treg（Agent 工具注册中心） | 一个 Codex 插件改变增长曲线 | 站在平台肩膀上，卖“工具层” |

Treg 卖的到底是什么：

- 不是 prompt，不是 Agent，而是 **Agent 干活时必须调用的外部能力**：SEO、社交、广告、电商、enriched 数据；
- 聚合 60+ 提供商、2600–3600 个 API 端点，一个 token 统一计费；
- 分发形态是 **plugin**（`/plugin install treg@treg`，或 `npx skills add superdesigndev/treg -s treg`），一次安装，持续调用；
- 商业模型像 Costco：不靠单个工具溢价，靠会员/按量调用形成复购。

### 这个案例真正可复用的三点

1. **卖“必经之路”，不卖“可选功能”。**
   Agent 只要干活就要调工具。工具层是必经之路，提示词不是。
2. **用安装门槛极低的壳，装一个持续产生价值的内核。**
   插件只是壳，内核是数据与调用。壳负责获客，内核负责留存。
3. **把“一次成交”变成“持续计费”。**
   纯 Skill 没有复购，但“每次生成都要跑的验证/发布流程”有复购。

### 不能直接照搬的地方

Treg 需要真实的数据供应商、计费系统、法务与账号体系，个人开发者无法复制。
但它的**结构**可以复制：**一个极低门槛的入口 + 一个每次使用都产生新资产的引擎。**

---

## 4. 高流量 Skill 的通用公式

把榜单拆成可操作的变量：

```
安装量 ≈ 受众规模 × 触发频率 × 安装门槛的倒数 × 传播系数 × 作者信任
```

| 变量 | 高分做法 | 低分做法 |
|---|---|---|
| 受众规模 | 所有用 Claude/Codex 的人 | 只服务某个小众框架 |
| 触发频率 | 每天都会发生（写代码、发版、写文档） | 一年一次（迁移、审计） |
| 安装门槛 | 一条命令、零依赖、纯 Markdown | 要配 API Key、要装数据库 |
| 传播系数 | 产出物自带署名与分享价值 | 用完没有任何痕迹 |
| 作者信任 | 有真实工程案例、可验证 | 只有一段“你是一名专家” |

### 五类已被验证的高流量形态

| 形态 | 代表 | 为什么有效 | 个人可复制性 |
|---|---|---|---|
| 入口型 | find-skills | 解决“不知道装什么” | 高，但已有霸主 |
| 方法论型 | mattpocock 全系 | 订阅作者的工作方式 | 中，需要长期声誉 |
| 交付物型 | frontend-design、hyperframes | 装完立刻有产物 | 高 |
| 平台绑定型 | lark-*、azure-* | 存量用户顺手装 | 低 |
| 成本/治理型 | caveman、triage | 直接省钱、省时间 | 高，仍在早期 |

---

## 5. 选题矩阵：为什么是 skill-forge

对 6 个候选方向按 5 个维度打分（1–5 分，总分 25）：

| 方向 | 受众规模 | 触发频率 | 竞争强度（越高越好） | 传播系数 | 差异化 | 总分 |
|---|---|---|---|---|---|---|
| skill 体检 / 治理 | 5 | 3 | 5 | 4 | 4 | 21 |
| **工作流蒸馏成 Skill** | **5** | **5** | **5** | **5** | **5** | **25** |
| Token / 上下文压缩 | 5 | 5 | 2 | 3 | 2 | 17 |
| 设计审美 | 4 | 4 | 2 | 5 | 2 | 17 |
| 中文去 AI 味 | 3 | 4 | 3 | 4 | 3 | 17 |
| 垂直科研 | 2 | 3 | 3 | 3 | 4 | 15 |

**选择“工作流蒸馏成 Skill”的五条理由：**

1. **触发频率最高**：用户每完成一次有价值的任务，就是一次触发机会。
2. **竞争仍未被占据**：现有产品（skill-creator / write-a-skill / sanyuan skill-forge）
   的输入都是“口述、想象或写作规范”，没有产品把“刚做完的事”作为第一输入。
3. **产出物即传播物**：生成的每个 Skill 都带 `Built with skill-forge` 元数据，
   形成“用得越多 → 产出越多 → 曝光越多”的回流。
4. **跨生态天然成立**：Skill 是 Claude、Codex、Cursor 共同采纳的开放标准，
   一次生成可以打包进三个市场。
5. **可验证，不像玄学**：触发测试、token 预算、安全扫描都能给出分数与报告，
   用户愿意晒分数，媒体愿意引用。

### 与官方 skill-creator 的差异

| 维度 | skill-creator（官方） | skill-forge |
|---|---|---|
| 输入 | 用户口述需求 | 真实会话、git diff、命令历史、项目文件 |
| 方法 | 访谈 → 起草 | 采集 → 蒸馏 → 门禁 → 生成 → 验证 |
| 输出 | 一个 SKILL.md | Skill + 双市场 manifest + 触发测试 + 评分卡 |
| 质量保证 | 靠作者经验 | 8 道门禁 + 可执行审计脚本 |
| 发布 | 用户自己处理 | 内置 Claude / Codex / skills.sh 三条发布路径 |

---

## 6. 分发与“官方市场”的真实路径

必须区分“事实市场”和“官方目录”：

| 层级 | 渠道 | 门槛 | 谁能进 | 预期 |
|---|---|---|---|---|
| L1 | 本地 `~/.claude/skills`、`~/.codex/skills` | 零 | 所有人 | 自用 |
| L2 | GitHub + `npx skills add owner/repo` | 零 | 所有人 | 安装量、榜单 |
| L3 | 自建 Claude / Codex marketplace | 低 | 所有人 | 团队分发 |
| L4 | Claude 官方目录 `claude-plugins-official` | 高 | 审核通过的第三方 | 品牌背书 |
| L5 | Codex 官方 `openai/plugins` | 高 | 官方 curated | 品牌背书 |

关键事实（2026-10 核实）：

- `openai/skills` 已在 README 标记 **deprecated**，Codex 的当前示例仓库是 `openai/plugins`；
- Claude 第三方插件通过官方提交表单进入 `external_plugins`，需通过质量与安全审核；
- skills.sh 是当前安装量最大的事实分发层，`npx skills add` 是通用安装命令。

**现实策略：先用 L2 拿安装量与反馈，再用数据去申请 L4/L5。**
没有 L2 的数据，直接冲官方目录的通过率极低。

---

## 7. 结论

`skill-forge` 不是一个“写 Skill 的提示词”，而是一条**从真实工作到可分发资产的生产线**：

- 对个人：把一次性经验变成可复用资产；
- 对团队：把 SOP 变成可版本化的插件；
- 对生态：持续产出新的高质量 Skill，反哺市场。

下一步见仓库根目录 `README.md` 与 `plugins/skill-forge/skills/skill-forge/SKILL.md`。
