# 验证记录

发布版本：`1.0.0`。检查日期：2026-09-21。

## 格式与分发

| 检查 | 结果与范围 |
| --- | --- |
| Agent Skills 规范 | `skills-ref validate skills/learn-with-ai` 通过；上游固定到 `69ef37e9424c0a7ea9dd2293b559e43ec8176379` |
| Anthropic 校验器 | 官方 `quick_validate.py` 返回 `Skill is valid!`；上游固定到 `34040c9c568585f6929bedeaad110ad08f079624` |
| 可移植前言 | 仅使用标准 `name`、`description`、`license`、`metadata`；描述不超过 200 字符，避免不同 Claude 文档中的限制差异 |
| 本地引用 | 所有相对资源链接可解析，未越出技能目录 |
| 安装包 | 单个 `learn-with-ai/` 根目录、七个文件，含许可证，无本机绝对路径或符号链接 |
| ZIP 验证 | 解压后再次运行参考校验；与源目录逐文件字节一致，SHA-256 校验通过 |
| 独立静态审阅 | 发布目录、安装说明、打包脚本、校验脚本和 CI 未发现实质问题 |

规范依据：[Agent Skills](https://agentskills.io/specification)、[Anthropic Skills](https://github.com/anthropics/skills)、[Claude 自定义 Skill](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)。`skills-ref` 是规范方提供的参考校验实现，不是产品认证。

## 行为检查

2026-09-13 的前一版本经过七个边界场景与一次四轮学习流程模拟，检查了计划与执行分离、示范与独立完成分离、真实时间间隔、删除记录时保留事实准确性、缺失文件、口述与实测区分，以及换助手后从保存记录接续。

本次发布保留十步主体及原有五个支持文件，新增许可/版本元数据，以及没有文件工具时的聊天记录交付方式。旧测试属于前一版本的历史证据，没有被描述为本次所有宿主的运行测试。

对新增行为执行了一次独立模拟：只做第 8 步、允许查资料但禁止解题提示、出题后立刻暂停、宿主没有文件保存工具。实际输出完成了目标约定和一道待答题，未泄露答案，保留“尚未检验”，交付可复制的记录并明确“尚未保存到文件”。

可复查输入与实际输出：[无文件工具的模拟](../evals/no-write-host.md)。

## 宿主与效果边界

| 宿主 | 已验证范围 |
| --- | --- |
| Codex | 前述独立模拟与本次无文件工具模拟在 Codex 子代理环境完成；不是所有 Codex 客户端版本的发现测试 |
| Claude Code | CLI 2.1.278 在临时项目 `.claude/skills/learn-with-ai` 中发现了 Skill，初始化的 `skills` 与 `slash_commands` 均包含 `learn-with-ai`；随后隔离配置下认证失败，未产生实际 Skill 调用或教学回答 |
| Claude 网页端 | 已核对官方上传格式与 ZIP 内容；未登录其他账户完成网页上传测试 |
| Gemini CLI | 安装方式依据官方文档；本机未安装 Gemini CLI，未执行宿主运行测试 |
| 其他 Agent | 仅声明开放格式兼容；需宿主支持 Agent Skills 或手动加载文件 |

合成学习者输入只验证助手行为。没有进行真实用户长期记忆追踪、迁移效果实验或效率提升实验，不承诺倍速学习效果。

Claude Code 宿主检查只允许 `Read`、`Skill`，禁用外部 MCP，使用临时项目设置且不持久保存会话。实际结果为退出码 1、`authentication_failed` / `Not logged in`，没有模型 token 消耗。此次证明了目录发现，不能据此声称 Claude 模型已经执行通过；没有为完成测试修改用户登录或服务配置。

## 重跑

在仓库根目录按 README 安装开发依赖后执行：

```bash
skills-ref validate skills/learn-with-ai
python scripts/package.py
python scripts/validate.py --archive dist/learn-with-ai-v1.0.0.zip
```

GitHub Actions 的实时结果见仓库 Actions 页面；CI 验证结构与分发，不自动进行需要模型服务的行为测试。
