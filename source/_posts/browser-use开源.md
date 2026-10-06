---
title: Browser-Use开源：GitHub 11万星浏览器智能体，如何接管你的整个网页
cover: /img/cover42.png
date: 2026-10-06 10:00:00
categories:
- Tech前沿
tags:
- AI前沿
- Browser-Use
- 开源项目
---

## 一、当"会用浏览器"成为智能体的第一技能

过去两年，AI 智能体（Agent）的能力边界一直在向上突破：从纯文本对话到代码生成，再到终端操作与多步骤推理。然而几乎所有旗舰模型都忽略了一个最基础、最高频的场景——**网页本身**。我们每天的工作流里，仍有海量任务发生在浏览器中：登录后台填表、跨站点抓取数据、走一遍完整的下单流程、自动化 QA 测试。这些动作对 LLM 而言曾是"黑盒"，因为它看不到 DOM、点不动按钮、也读不懂页面结构。

**Browser-Use** 正是为此而生的开源项目。它的口号很直白："Make websites accessible for AI agents"——让大语言模型像人一样使用浏览器：打开网页、点击按钮、输入文字、填写表单，你只需描述任务，它自己完成。截至 2026 年 10 月，该项目在 GitHub 上已突破 **11.7 万 Star**（MIT 协议），成为全站 Star 数最高的开源项目之一，并被 Claude Code、Codex、Cursor、OpenClaw 等多个智能体选为默认浏览器工具。

## 二、它到底能做什么？

Browser-Use 的核心是一个"感知—决策—执行"的闭环循环：

1. **感知**：通过 Chromium 的 CDP（Chrome DevTools Protocol）驱动真实浏览器，抓取页面 HTML 与可交互元素列表；
2. **决策**：将页面状态交给 LLM，由模型判断下一步该点击哪个元素、输入什么内容；
3. **执行**：调用浏览器动作工具完成操作，观察页面是否变化；
4. **循环**：重复上述过程，直到任务完成或达到失败上限。

这种设计的关键在于——它不依赖固定的 CSS 选择器（那会在网站改版后失效），而是让模型基于**当前页面的实际内容**做决策，因此对前端变动具有天然鲁棒性。

一个最小示例仅需几行：

```python
import asyncio
from browser_use import Agent, ChatBrowserUse

async def main():
    agent = Agent(
        task="找到 GitHub 上 browser-use 仓库的 Star 数量",
        llm=ChatBrowserUse(model='openai/gpt-5.5'),
    )
    history = await agent.run()
    print(history.final_result())

asyncio.run(main())
```

## 三、技术拆解：为什么它能登顶榜单？

Browser-Use 提供两类接入方式。**CLI** 适合已拥有智能体的场景——安装一次 skill，即可让既有 Agent 替你完成浏览器任务；**Python 库**则面向需要在代码中规模化自动化的人群（定时抓取、并发监控、QA）。

其内置工具链覆盖了网页交互的完整语义：

- **导航与控制**：`search`、`navigate`、`go_back`、`wait`
- **交互**：`click`（按索引点击）、`input`、`upload_file`、`scroll`、`send_keys`
- **内容提取**：`extract`（LLM 抽取页面信息）、`evaluate`（执行自定义 JS，处理 shadow DOM）
- **文件操作**：`write_file`、`read_file`、`replace_file`
- **收尾**：`done`

在模型选择上，官方专门优化了 **ChatBrowserUse()**——针对浏览器任务微调，平均比其他模型快 3–5 倍且准确率领先。它通过 provider 前缀统一接入各家模型（`anthropic/claude-sonnet-4-6`、`google/gemini-3-pro`），一个 `BROWSER_USE_API_KEY` 即可打通所有后端。

真正让它脱颖而出的，是官方在 **Odysseys 排行榜**上的表现：在 200 个长程网页任务的评测中，Browser-Use 以 **87.4% 的平均完成率登顶**，领先于 OpenAI、Anthropic、Google 和微软的 computer-use 智能体。该榜单专门衡量"跨多个网站、需数十步操作"的真实场景，正是 Browser-Use 的主场。

2026 年推出的 **Browser Use 0.13** 引入了基于 Rust 核心的 beta agent，架构升级为 `Python API → Rust core → Browser harness → Web task done`：Rust 侧提供与编程智能体类似的真实浏览器动作空间、持久化工具和"恢复循环"（recovery loops），在速度与稳定性上进一步拉齐了与闭源方案的差距。

## 四、影响与未来展望

Browser-Use 的意义在于它把"网页操作"从脆弱的脚本自动化，升级为**可泛化、可推理的智能体能力**。当网站改版、表单结构变化时，传统 Selenium 脚本会大面积崩溃，而 Browser-Use 让模型重新"看懂"页面后再行动——这正是 agentic 范式相对于传统自动化的本质跃迁。

对行业而言，三条趋势值得关注：

1. **浏览器成为智能体的标准输入输出设备**。正如终端曾是编码 Agent 的战场，浏览器正成为通用 Agent 的新交互界面。
2. **"开源模型 + 专用微调"路线跑通**。bu-* 系列开源预览模型的推出，证明低成本本地模型也能在特定任务上逼近闭源精度。
3. **云化基础设施补全最后一公里**。官方推出的 $0.02/小时云端浏览器，内置隐身指纹、验证码求解与住宅代理轮换，解决了本地运行 Chrome 内存占用高、并发难管理的工程痛点。

当然，挑战依然存在：长程任务的可靠性仍受模型推理稳定性制约，反爬与验证码对抗是一场持久战，而大规模并行的资源消耗也需要专门的云基础设施来承接。但对开发者而言，Browser-Use 已经给出了一个几乎零门槛的答案——**你不再需要自己写选择器和等待逻辑，只需告诉 AI 你想做什么**。

当智能体开始真正"使用"网页而非仅仅"阅读"文本，我们或许正站在 Agent 从实验室走向真实工作流的临界点上。而 Browser-Use，正是这道门最显眼的那把钥匙。
