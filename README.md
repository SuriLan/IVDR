# IVDR Classification Agent Skill

An AI Agent Skill designed to assist with EU IVDR (In Vitro Diagnostic Regulation) medical device classification and matching suitable codes.

一个专为 AI 智能体（Agent）设计的技能，用于协助进行欧盟 IVDR（体外诊断医疗器械法规）的分类，并匹配适用的分类代码。

---

## 📖 项目简介 (Introduction)

本项目包含了一套结构化的提示词（Prompt）和法规参考知识，可以“教会”大语言模型（如豆包、Kimi、ChatGPT 等）如何按照欧盟 IVDR 规则对医疗器械进行分类。

## 🚀 如何在国内 AI 工具中使用？(How to use in domestic AI agents)

如果你使用的是 **豆包、Kimi、通义千问、智谱清言** 等国内 AI 助手，不需要懂代码，按照以下 3 步即可使用：

### 第一步：下载技能文件
1. 点击页面右上角的绿色 **`Code`** 按钮。
2. 选择 **`Download ZIP`** 下载压缩包。
3. 解压下载的压缩包到你的电脑上。

### 第二步：上传核心文件给 AI
打开你常用的 AI 助手（如豆包），新建一个对话，然后做两件事：
1. **上传文件**：把解压出来的 `SKILL.md` 文件（以及 `references` 文件夹里你觉得有用的 PDF 或文档）拖拽上传到对话框里。
2. **发送指令**：复制下面这句话发给 AI：
   > “请仔细阅读我上传的 `SKILL.md` 文件，你现在是一位欧盟 IVDR 法规专家。请按照该文件中的规则和说明来回答我的问题。准备好了请回复‘已就绪’。”

### 第三步：开始提问
AI 回复“已就绪”后，你就可以直接把产品描述发给它了，例如：
> “我有一个产品，用于检测人体血液中的 HIV 病毒核酸，属于哪一类？请帮我匹配代码。”

---

## 💻 开发者使用方式 (For Developers)

If you are using command-line tools or AI coding assistants (like Cursor, Claude Code, GitHub Copilot), you can install this skill directly:

```bash
# 使用通用安装命令
npx skills add SuriLan/IVDR

# 或者使用 GitHub CLI
gh skill install SuriLan/IVDR
