# learn-with-ai · AI 学习实践

[![Validate skill](https://github.com/ShengjiaCui/learn-with-ai/actions/workflows/validate.yml/badge.svg)](https://github.com/ShengjiaCui/learn-with-ai/actions/workflows/validate.yml)

围绕一项真正想完成的任务，用 AI 研究、规划、练习、纠错，并留下下次能继续的学习记录。

A portable Agent Skill for outcome-based learning: ten steps, evidence-aware practice, and resumable learning records. Instructions are written in Chinese; the skill follows the learner's language.

**目标能验收，学习有证据，下次能接续。** 符合 [Agent Skills 开放格式](https://agentskills.io/specification)，沿用 Anthropic 的 `SKILL.md` 结构。核心内容不依赖特定模型、API、MCP 服务或运行时。格式兼容不等于所有宿主都已运行实测；详见 [验证说明](docs/VALIDATION.md)。

## 安装

先下载仓库，以下文件复制命令在仓库根目录运行（macOS / Linux）：

```bash
git clone https://github.com/ShengjiaCui/learn-with-ai.git
cd learn-with-ai
```

只安装 `skills/learn-with-ai/` 这一整个目录。目标位置已有同名 Skill 时先备份并明确替换，避免把不同版本混在一起。

### Claude Code

```bash
mkdir -p ~/.claude/skills
cp -R skills/learn-with-ai ~/.claude/skills/
```

新建会话，使用 `/learn-with-ai`，或说“使用 learn-with-ai 带我学习……”。从旧版本升级时整目录替换，然后新开会话：Claude Code 会在会话内缓存已加载的 Skill 正文，替换文件的当轮调用仍可能拿到旧内容。项目级安装可改为项目内的 `.claude/skills/`。依据：[Claude Code Skills 文档](https://code.claude.com/docs/en/skills)。

### Codex 与支持共享技能目录的 Agent

```bash
mkdir -p ~/.agents/skills
cp -R skills/learn-with-ai ~/.agents/skills/
```

在 Codex 中使用 `$learn-with-ai`；也可以安装到项目内的 `.agents/skills/`。不要在多个被同一宿主扫描的目录重复安装同名版本。`agents/openai.yaml` 是可选的 Codex 界面元数据，其他宿主无需解析它。依据：[Codex 技能文档](https://learn.chatgpt.com/docs/build-skills)。

### Gemini CLI

```bash
gemini skills install https://github.com/ShengjiaCui/learn-with-ai.git --path skills/learn-with-ai
gemini skills list
```

随后在对话中指定使用 `learn-with-ai`。Gemini CLI 也支持上面的 `.agents/skills/` 目录方式，二选一即可。依据：[Gemini CLI Skills 文档](https://geminicli.com/docs/cli/skills/)。

### Claude 网页端 / 桌面端

在 [Releases](https://github.com/ShengjiaCui/learn-with-ai/releases) 下载最新版本附带的 **`learn-with-ai-v<版本号>.zip`**，按 [Claude 官方上传说明](https://support.claude.com/en/articles/12512180-use-skills-in-claude) 在技能设置中上传。是否可用取决于账户和组织设置。

请选择发布附件中的专用 ZIP；GitHub 自动生成的 “Source code (zip)” 是仓库源码，目录结构不同。专用 ZIP 的顶层只有 `learn-with-ai/`，其下直接是 `SKILL.md` 与资源。

### 其他 Agent

若宿主支持 Agent Skills，将完整 `learn-with-ai/` 放入该宿主文档指定的技能目录。若不支持自动发现，可让它阅读 `SKILL.md` 并按需读取相对引用的文件；这种方式是手动加载。文件保存与跨会话恢复仍需要宿主具备文件能力或用户提供记录。

## 怎么用

```text
使用 learn-with-ai，带我学习 Python 数据清洗。
我会基本语法，希望能独立处理一份包含缺失值和重复记录的 CSV。
今天有 30 分钟，材料是我提供的文件。先明确验收标准，再开始。
```

其他入口：

- “按完整十步带我学这个主题。”
- “只做第 8 步，考考我；一次一题，等我回答再反馈。”
- “今天只要学习计划，不开始测试。”
- “把本轮记录保存到 `learning/python-csv.md`；下次从待答题继续。”
- “读取 `learning/python-csv.md`，继续上次学习。”

出题后会等待你的回答。看过答案、提示后完成、独立完成会分别记录；一次答对不会被当成长期掌握。没有写入文件的工具时，会给出可复制的接续记录。

## 十步框架

1. 五视角 STORM
2. 矛盾图谱
3. 综合简报
4. 同行评审自检
5. 资源筛选
6. 学习阶梯
7. 2 小时啃下核心 20%
8. 考到我崩溃
9. 费曼循环
10. 一页速查表

这些是沿用的步骤名称；实际时间、难度和练习数量服从学习任务。“2 小时”“20%”及来源书名中的效率说法不是效果保证。支持从指定步骤开始、暂停和直接讲解。

## 文件结构

```text
skills/learn-with-ai/
├── SKILL.md
├── LICENSE
├── agents/openai.yaml
├── references/
│   ├── ten-step-workflow.md
│   ├── practice-and-resume.md
│   ├── evidence-review.md
│   └── worked-example.md
└── assets/learning-record.md
```

`worked-example.md` 是一段从出题、答错、提示到留下记录的合成示范，供 Agent 在不确定一轮练习该怎么进行时参照。`learning-record.md` 开头的“最小接续记录”用于单轮学习或只在聊天里交付的场合，完整模板留给跨多次的持续跟进。

仓库根目录的开发脚本、验证说明和 CI 不会装入技能包。学习记录由使用者保存在自己指定的位置，不应提交到本仓库。

## 验证与打包

仅维护仓库时需要 Python 3.11+ 与开发依赖；使用 Skill 不需要安装它们。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
skills-ref validate skills/learn-with-ai
python scripts/package.py
python scripts/validate.py --built
```

`--built` 按 `SKILL.md` 中的版本号检查 `dist/` 下刚打出的 ZIP，发版时只需改一处版本号；也可以用 `--archive <路径>` 检查任意一个已下载的发布包。`skills-ref` 是规范维护方的参考校验器，依赖固定到一个已审查的提交。打包脚本生成 ZIP 和 SHA-256 校验文件；CI 会校验格式、资源链接、许可一致性及压缩包内容。Windows 可使用 `.venv\Scripts\Activate.ps1` 激活环境，其余 Python 命令相同。

## 来源与许可

框架受到爱AI的大刘《用Claude、Codex、Workbuddy 10倍速学习任何知识（轻科技）》启发，[原书入口](https://weread.qq.com/web/reader/552323d0813abbc5cg01570e)。本仓库提供原创实践指令与模板，不包含原书全文、截图或付费笔记；来源归属在 Skill 内保留。

仓库原创内容采用 [MIT License](LICENSE)。外部来源、书籍和各产品名称归其权利人所有，不纳入本仓库的许可授予。本项目不是 Anthropic、OpenAI 或 Google 的官方技能或认证产品。
