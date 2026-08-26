---
title: CopilotKit开源OpenBot：每个AI同事一台独立电脑，动作先审批后执行
cover: /img/cover42.png
date: 2026-08-26 07:35:00
last_modified_at: 2026-08-26 07:35:00
sticky: false
categories:
- Tech前沿
tags:
- AI前沿
- 开源项目
---

## 背景：Agent 能干活了，但"敢不敢给它权限"成了新瓶颈

编码 Agent 已经证明模型可以独立跑完工程任务，接下来企业最关心的问题只有一个：**能不能把真实的工作和真实的凭据交给它？** 浏览器登录态、公司文件、内部系统——这些才是 Agent 价值的主体，也是安全团队最警惕的部分。

8月17日，CopilotKit（AG-UI 协议背后的团队）开源了 **OpenBot**：一个"AI 同事"平台。**9 天时间 2,900+ Star、MIT 协议**。它的定位一句话就能说清——每个 AI 同事都有一台自己的电脑：独立的浏览器（含独立登录态）、独立的文件空间、只授予它需要的工具，而且**每一个动作在发生前被决策、发生后被记录**。

## 核心设计：一台"专属电脑" + 一个统一网关

OpenBot 里 Bot 和人的关系不是"调用 API"，而是"同事协作"。每个 Bot 是一个 AG-UI 端点（开放协议，不绑定任何框架），接入后自动获得自己的频道、自己的屏幕——你可以在 Web UI 上**看着它操作浏览器**，它做到不该独自决定的事时你可以接管方向盘，处理完再交还给它。

安全架构是整套系统的灵魂：Bot 对电脑、文件、MCP server、组件做的**任何**操作都经过同一个网关（gateway），由它决策并留痕。官方示例里可以直接打开 `/admin/audit` 查看完整审计流，在 `/admin/boundaries` 加一条 deny 规则后重试同样的浏览器动作——被拦下。这就是"能用你的工具"和"值得信任地用你的工具"的区别。

部署形态对自托管友好：Docker Compose 拉起全部组件（应用、API、Bot 驱动的浏览器、PostgreSQL），数据落在自己的库里，**模型完全自选**——不捆绑任何模型厂商。示例包内置三个 Bot（General Assistant / Knowledge / Risk Analyst），它们是配置而不是代码，改个 YAML 就能定义新同事。

## Bring Any AG-UI Agent：框架无关的"同事入职"流程

OpenBot 最开放的设计是 **BYO agent**：任何会说 AG-UI（agent-to-user 交互开放协议）的端点都能接入，无论它跑在 LangGraph、自研框架还是手写代码上。"入职"一个新同事不需要改平台代码——端点一接，频道、屏幕、权限边界就都配好了。

快速上手也很直接：

```bash
# 1. 克隆后配置 .env（单用户模式默认开启，适合本地体验）
git clone https://github.com/CopilotKit/OpenBot && cd OpenBot
cp .env.example .env   # OPENBOT_SINGLE_USER=true 让所有请求视为同一管理员

# 2. 一键启动：Docker 服务 + 迁移 + API(3001) + App(3010) + 健康检查
scripts/start.sh

# 3. 打开 /bot，试试：
#    "Open news.ycombinator.com and tell me the top story."
```

生产部署则是一个镜像搞定（应用、API、浏览器、可选内嵌 Postgres），`EMBEDDED_POSTGRES=off` 时指向已有数据库即可。需要 CopilotKit Intelligence 的 license key（有免费档，也可自托管）和一个模型 API key——PoC Bot 用 OpenAI，LangGraph Bot 支持 OpenAI/Anthropic/Google。

## 影响与展望

OpenBot 踩中的是 Agent 企业化的关键断层：**从"演示能干活"到"生产敢授权"**。它的三个设计选择值得记住：

1. **动作网关化**——所有副作用（浏览器、文件、MCP）收敛到一个可决策、可审计的 choke point，而不是散落在各框架里；
2. **身份隔离**——每个 Bot 独立浏览器登录态和文件空间，权限按 Bot 粒度授予，出问题时爆炸半径可控;
3. **协议先行**——AG-UI 作为 agent-to-user 交互层，让"同事"可以来自任何框架，平台不锁定生态。

需要泼的冷水也明确：项目自标 **Alpha**，官方直言"expect rough edges and bugs"；单用户模式只适合本地体验，多租户、SSO、细粒度 RBAC 这些企业刚需还得等后续版本。但方向已经很清楚——当 Agent 开始持有真实凭据，"先审批后执行 + 全程留痕"会从加分项变成准入门槛。OpenBot 把这个门槛做成了开源基础设施，9 天近 3K 星说明企业侧的等待是真实的。

**参考链接：**
- GitHub: https://github.com/CopilotKit/OpenBot
- 官网: https://www.copilotkit.ai/openbot
- AG-UI 协议: https://github.com/ag-ui-protocol/ag-ui
