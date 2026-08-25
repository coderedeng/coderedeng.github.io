---
title: YC开源QM：把编码Agent变成"公司同事"的多玩家协作框架，三周14K星
cover: /img/cover42.png
date: 2026-08-25 15:30:00
last_modified_at: 2026-08-25 15:30:00
sticky: false
categories:
- Tech前沿
tags:
- AI前沿
- 开源项目
---

## 背景：个人助理很好，但公司需要的是"同事"

Claude Code、Codex、OpenCode 这类编码 Agent 已经证明了一个事实：给足权限和上下文，模型可以独立跑完一个工程任务。但它们的形态几乎都是**单人工具**——你的终端、你的凭据、你的会话。当一家创业公司想让整个团队都用上 Agent 时，问题立刻涌现：

- 每个人的 Agent 配置互相隔离，经验无法沉淀；
- 共享一个 Agent？权限和记忆全搅在一起，谁改坏了都不知道；
- Slack 里 @一下就能干活的需求，本地 CLI 根本接不住。

7月29日，YC（Y Combinator）开源了 **QM**——"multiplayer agent harness for work"。**三周时间 14,000+ Star、MIT 协议**，定位非常明确：不是给个人的助理，而是给公司的同事系统。

## 核心设计：每个人一个隔离工作区，每个房间一套共享状态

QM 的基本单元是 **scope（作用域）**——每个人、每个 Slack 频道/项目都有自己的 scope，各自拥有独立的：

- 记忆（memory）与文件空间
- keychain 视图与登录态服务
- 权限策略与 cron 任务
- 持久化沙箱（durable sandbox）——Agent 装的工具会一直装着，下次接着用

个人 scope 让你把 Agent 调成"自己的"，共享 scope 让团队在频道和项目里协作。同一套身份和配置在 **Slack 和 Web UI 之间无缝携带**：早上在 Slack 频道里布置的任务，下午可以在网页端继续跟进。

架构上是一个无头核心（headless core）+ 可选插件的模型：

```
Postgres（会话 · 记忆 · 队列）
        │
Headless Core: API / 身份 / 策略 / 调度器
        ├── Agent Loop（Pi、OpenCode、Codex、Claude Code 任选）
        └── Per-scope Sandbox（文件 · 工具 · 登录态服务）

Web UI / Admin Panel / Public Portal —— 核心 HTTP API 上的可选插件
Slack —— 进程内插件，由 core 直接启动和监督
```

核心用 TypeScript + Fastify 跑在 Node 上，Slack 侧用 Bolt。所有"公司特定"的东西——组织配置、自定义工具与技能、沙箱镜像、基础设施——都放在一个 **deployment directory** 里，由 `qm` CLI 校验和部署。每个底座（harness、会话存储、沙箱、记忆）都在接口后面，生产实现可以整体替换。

## Harness 无关：Pi、OpenCode、Codex、Claude Code 驱动同一个核心

QM 最反"厂商锁定"的设计是 **harness 可插拔**：Agent loop 层面对 Pi、OpenCode、Codex、Claude Code 一视同仁，管理员在组织层面决定哪些 harness 和模型可用。部署不绑定任何单一供应商——今天全公司用 Claude Code，下个月部分团队切 Codex，只是配置变更而不是迁移工程。

配套的能力面也很完整：

- **共享 Skills**：技能按 scope 归属、可按授权分享，管理员可将其提升到全组织，还支持从 git 仓库导入 skill pack；
- **后台工作**：cron、watch、入站 webhook 让 Agent 在没人盯着的时候继续干活——定时整理收件箱（自动打标签 + 起草回复）、监控 CI、跟踪项目频道里的进展都是官方示例场景；
- **内部 Web App**：Agent 可以搭一个内部应用并发布给指定的人，数据保持更新。

## 安全模型：三档姿态 + 不可绕过的硬规则

多玩家意味着权限必须分层。QM 沿用了本地编码 Agent 的哲学——**Agent 以所服务之人的身份和凭据行动，一切操作可审计**——并在其上提供组织级安全姿态：

- **Strict**：除两个白名单工具外，每次 harness 工具调用都暂停等待人工批准；
- **Auto（默认）**：分类器先对带来源标签的外部数据和工具结果做筛查，再交给模型，筛查器本身可替换成自研的；
- **Dangerous**：不筛查、不暂停——但预声明的命令策略（递归删除、破坏性 SQL 等硬拒绝规则）在每一档下都生效，包括 Dangerous。

对要上生产的团队来说，"最危险档位也有不可绕过的底线"这个设计比单纯的开关更让人放心。

## 影响与展望

QM 踩中的是 Agent 落地的下一个断层：**从"个人生产力工具"到"组织基础设施"**。过去半年大家争论的是单个 Agent 能不能干活，现在的问题是——当十个人、十个频道同时用 Agent，记忆怎么隔离、经验怎么共享、权限怎么审计、账单怎么算？QM 给出的答案是一套 scope 化的状态管理 + 可插拔的 harness 层 + Slack 原生入口。

由 YC 亲自下场开源也值得玩味：作为最懂创业公司工作流的机构，它选择把"多玩家 Agent 协作框架"做成 MIT 协议的基础设施，而不是内部工具——这等于向整个生态宣告了它的判断：**Agent 的终局形态是组织成员，不是个人玩具**。

接下来值得观察两点：一是 harness 可插拔层会不会成为事实标准（类似 LLM 界的 OpenAI-compatible API）；二是 scope 化的记忆/权限模型能否经受住真实团队的规模考验。三周 14K 星说明这个方向的需求已经压不住了。

**参考链接：**
- GitHub: https://github.com/yc-software/qm
- YC 官网: https://www.ycombinator.com
