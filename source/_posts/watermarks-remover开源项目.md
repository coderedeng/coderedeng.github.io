---
title: watermarks-remover：一键清除Claude、Gemini等AI水印的开源利器，750星引爆隐私讨论
index_img: /img/cover42.png
date: 2026-08-12 16:30:00
categories:
- 热门开源项目
tags:
- AI水印
- Claude
- SynthID
- C2PA
- 隐私保护
---

# watermarks-remover：一键清除Claude、Gemini等AI水印的开源利器，750星引爆隐私讨论

> **GitHub 热度**：753 stars · Python · Agent Skill + CLI 工具  
> **创建时间**：2026年8月11日（仅2天）  
> **作者**：guillaumemeyer  

在AI生成内容泛滥的今天，一个看似小众却直击痛点的项目正在GitHub上迅速走红——**watermarks-remover**。这个开源项目用不到一周的时间就斩获了750+ stars，成为近期最热门的隐私保护工具之一。

它的目标只有一个：**清除你拥有的内容中所有厂商的AI水印和来源标记**。Claude 的不可见 Unicode 字符、Gemini 的 SynthID 文本统计水印、OpenAI 的 C2PA 文件元数据——它一视同仁，全部清理。

## 为什么需要"去水印"？

过去两年，各大 AI 厂商纷纷推出了内容溯源方案：

- **Claude**（Anthropic）在生成的文本中嵌入不可见的 Unicode 字符和特殊空格，用于标记"这是 Claude 写的"
- **Gemini / SynthID-Text**（Google DeepMind）采用统计采样水印——通过选择特定 token 的分布来编码来源信息
- **OpenAI** 则倾向于使用 C2PA（Content Credentials）标准，在文件元数据中嵌入生成者信息

这些方案初衷是好的：防止深度伪造、标记 AI 生成内容。但对普通用户来说，问题在于——**当你自己拥有这份内容时，为什么还要保留厂商的"签名"？**

一位开发者在 Reddit 上吐槽："我用 Claude 写了一封邮件，结果收件人收到的是带不可见字符的垃圾邮件格式。"这种尴尬场景正在越来越多地出现。

## watermarks-remover 的工作原理：三层防御体系

watermarks-remover 的设计非常精巧，它把水印清除分为三个层次，每层针对不同类型的标记：

### Layer A：Unicode 清理（确定性脚本）

这是最基础也最有效的一层。Claude 等模型在生成文本时会混入以下不可见字符：
- **零宽空格**（ZWSP, U+200B）
- **双向控制符**（Bidi marks）
- **标签字符**（Tag characters）
- **异体选择器**和特殊空格

watermarks-remover 提供 `clean_text.py` 脚本，用纯 Python stdlib 即可运行：

```bash
python3 clean_text.py draft.md -o draft.cleaned.md --stats
```

它会输出清理前后的统计对比——比如"移除了 23 个零宽空格和 5 个双向控制符"。这种确定性方法不会改变文本的可见内容，只是把那些藏在背后的标记字符全部剥离。

### Layer B：统计水印重写（Agent + 可选模型）

这一层更复杂。SynthID-Text 等方案不是靠隐藏字符，而是通过**token 选择分布**来编码信息——也就是说，即使你把所有不可见字符都删了，文本本身仍然携带着"我是 Gemini 生成的"信号。

watermarks-remover 的 Layer B 采用了一种"重写攻击"策略：用另一个模型（推荐非来源模型）对文本进行改写，从而破坏原有的统计分布。它提供了多种后端选项：

```bash
# 仅打印提示词（无需模型）
python3 rewrite_text.py draft.md --backend print-prompt --strength paraphrase

# 使用本地 Ollama 模型重写
WATERMARKS_REWRITE_BACKEND=ollama WATERMARKS_REWRITE_MODEL=llama3.2 \
  python3 rewrite_text.py draft.md -o draft.rewritten.md
```

项目文档明确建议：**不要用 Claude 去改写 Claude 生成的文本**——否则可能重新注入水印。推荐使用非来源模型，比如本地部署的 Llama、Qwen 等开源模型。

### Layer C：文件元数据清理（C2PA / EXIF）

对于图片、PDF、DOCX 等文件，watermarks-remover 可以剥离 C2PA 内容凭证、EXIF 信息、XMP 元数据等。支持格式包括 PNG、JPEG、SVG、PDF、DOCX、ODT、HTML、Markdown：

```bash
python3 clean_file.py photo.png -o photo.cleaned.png
python3 clean_file.py notes.docx -o notes.cleaned.docx
```

对于 PDF，它推荐使用 `exiftool` 工具进行更彻底的清理（可选依赖）。

## 为什么这个项目能迅速走红？

**1. 切中了"AI 水印泛滥"的痛点。**  
从 Claude 到 Gemini 再到 OpenAI，几乎所有主流 AI 厂商都在推自己的内容标记方案。用户被各种不可见字符和元数据搞得不胜其烦——watermarks-remover 提供了一个统一的解决方案。

**2. Agent Skill 集成方式非常巧妙。**  
项目设计为 Grok Build / 本地项目的 agent skill（`.grok/skills/remove-ai-marks`），可以直接通过 `/remove-ai-marks` 命令调用。这意味着它不只是命令行工具，而是可以嵌入到 AI 工作流中的"技能"——当你用 Claude 写文档时，随时可以一键清理水印。

**3. 诚实的免责声明。**  
项目 README 中明确写道："在厂商公开检测器和密钥之前，没有任何工具能诚实地保证'这一定无法通过官方检查'。报告必须区分可验证的和尽力而为的工作。"这种坦诚反而赢得了社区的信任——它不承诺100%清除所有水印（比如像素级 SynthID 媒体水印），而是清晰列出哪些能做、哪些做不到。

**4. 多厂商覆盖。**  
从 Claude 到 Gemini/SynthID，再到 OpenAI 和开源 LLM 的 Kirchenbauer 式水印，watermarks-remover 几乎覆盖了当前所有主流 AI 标记方案。这种"一劳永逸"的设计对跨平台用户极具吸引力。

## 实际使用场景

**个人内容所有权：**  
用 Claude 写了一篇博客文章，发布前需要清除所有不可见字符和来源标记——否则搜索引擎可能会把那些零宽空格当成垃圾信号。

**隐私保护：**  
在分享文档之前，确保不包含任何 AI 厂商的追踪信息。对于法律文件、合同等敏感内容尤为重要。

**跨平台协作：**  
团队中有人用 Claude，有人用 Gemini，最终交付的文件需要统一"干净"——watermarks-remover 可以标准化输出。

## 局限性与未来展望

项目文档坦诚地列出了当前无法处理的场景：
- **像素级水印**（如 SynthID 媒体水印）不在范围内
- **C2PA 软绑定**（内容中的水印可重新链接远程凭证）无法清除
- **训练后门**也不在清理范围

这些限制是诚实的——目前业界也没有通用的解决方案。但 Layer A + Layer B + 文件元数据清理的组合，已经覆盖了绝大多数日常使用场景。

## 结语

watermarks-remover 的出现反映了 AI 时代一个日益尖锐的问题：**谁拥有你生成的内容？** 当 Claude、Gemini、OpenAI 都在你的文本中留下"签名"时，用户需要一种简单的方式来拿回控制权。这个项目用不到一周的时间就获得了750+ stars，说明这个需求是真实且迫切的。

如果你经常使用 AI 生成内容并担心隐私问题，不妨试试 watermarks-remover——它可能是你今年夏天最值得关注的开源工具之一。

---

**项目地址**：[github.com/guillaumemeyer/watermarks-remover](https://github.com/guillaumemeyer/watermarks-remover)  
**参考来源**：项目 README、Anthropic Claude 水印说明、Google SynthID-Text 论文、C2PA 标准文档