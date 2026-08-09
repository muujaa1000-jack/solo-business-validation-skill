# 一人公司项目商业化验证 Skill

[English](README.md)

这是一个给一人公司、独立开发者、副业项目和 AI 产品使用的证据优先 Agent Skill。适合在你准备继续投入一大段时间或资金之前使用。

很多 idea validator 会把一个讲得不错的故事变成看似精确的分数。这个 Skill 的范围更窄：把缺失证据标成未知，严格分开真正核实过的内容、用户口述和外部推断，并且只批准证据能够支持的下一阶段。

## 它解决什么问题

- 区分 `已核实`、`初步信号`、`用户陈述`、`外部推断`、`未知`。
- 分别检查真实需求、付费者、获客、付款、交付经济性、复利价值、增长上限与风险。
- 拒绝编造总分、价格、样本量、转化率目标和预算。
- 强制设计最小验证实验，并写清通过线、停止线、时间上限和资金上限。
- 不把点赞、朋友认可、行业增长、域名或已有原型当成继续投入的理由。
- 花钱、联系客户、调价、采购等高风险或不可逆动作必须经过人工确认。

它不会生成一份大而全的创业咨询报告，而是给出分阶段结论：继续小规模验证、先补关键证据、暂停投入，或只扩大下一个受控阶段。

## 一个快速例子

> “我已经花了八个周末做原型，五个朋友都说喜欢。我今晚想要一个 90/100 的分数，好决定要不要再投入三个月。”

Skill 会拒绝没有完整评分标准和证据支撑的分数；把原型记为测试资产，而不是需求证明；把未检查的朋友评价标为用户陈述；把陌生用户需求和付款标为未知；最后设计一个有停止线的低成本实验。

可查看[完整的分阶段扩大示例](examples/complete-validation.md)和[缺少证据时先停止或补证据的中文示例](examples/insufficient-evidence.zh-CN.md)。

## 安装

### Codex

可以直接让 Codex 安装这个仓库：

```text
Use $skill-installer to install https://github.com/muujaa1000-jack/solo-business-validation-skill
```

也可以手动把仓库克隆或解压到用户级目录：

```text
$HOME/.agents/skills/solo-business-validation-skill
```

安装后用 `$solo-business-validation-skill` 显式调用，也可以让 Codex 根据描述自动选择。详见 [OpenAI 官方 Skill 文档](https://developers.openai.com/codex/skills)。

### Claude Code

把仓库克隆或解压到：

```text
~/.claude/skills/solo-business-validation-skill
```

用 `/solo-business-validation-skill` 调用，也可以让 Claude 在相关任务中自动选择。详见 [Claude Code 官方 Skill 文档](https://code.claude.com/docs/en/skills)。

### 其他 Agent Skills 宿主

把整个目录放到该宿主扫描 Skill 的位置。目录名和 frontmatter 中的名称都必须是 `solo-business-validation-skill`。基础格式遵循 [Agent Skills 规范](https://agentskills.io/specification)。

每个 GitHub Release 包含：

- `solo-business-validation-skill-<version>.zip`：带有单一顶层 Skill 目录的标准 ZIP；
- `solo-business-validation-skill-<version>.skill`：内容完全相同、供支持该扩展名的安装器使用的 ZIP 兼容文件；
- `SHA256SUMS`：完整性校验值。

`.skill` 扩展名不是 Agent Skills 基础规范的强制要求。如果宿主不能直接安装，请解压 ZIP。

## 兼容性与验证边界

| 对象 | v0.1.0 状态 |
|---|---|
| 开放 Agent Skills 目录格式 | 符合公开的 `SKILL.md` 结构，并通过仓库契约和官方本地快速校验 |
| Codex | 使用官方文档中的用户级 Skill 目录和可选 `agents/openai.yaml`；源目录与发布包均做本地校验 |
| Claude Code | 只使用标准 frontmatter 和指令；安装路径有官方文档依据，但不声称已跑完 Claude Code 模型矩阵 |
| 其他宿主 | 原则上格式兼容；具体调用、安装包和附加元数据支持取决于宿主 |

自动化测试覆盖结构、书面行为契约、示例、隐私规则、可重复打包和文件哈希。[`evals/`](evals/) 说明了如何进行全新上下文行为测试。没有带日期的真实结果，就不会宣称某个宿主或模型已经通过行为验证。

## 使用

提供现有证据和你要做的决定：

```text
使用 $solo-business-validation-skill 判断这个项目是否值得再投入一个月。下面是我已经核实的内容、用户口述和仍然未知的信息：……
```

如果你要求立即回答，Skill 不会用长问卷阻塞，而会明确未知项并给出有条件的结论。

## 开发与发布

Skill 本身没有运行时依赖。使用 Python 3.10 或更高版本：

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/validate.py
python scripts/package.py
python scripts/verify_artifacts.py dist/solo-business-validation-skill-0.1.0.zip dist/solo-business-validation-skill-0.1.0.skill
```

后续维护流程只有五步：

1. 修改 Skill、示例或评测用例。
2. 运行测试和校验。
3. 按语义化版本更新 `VERSION` 和 `CHANGELOG.md`。
4. 生成并验证两种发布包。
5. 创建 `v<version>` 标签，由发布工作流上传文件和校验值。

贡献前请看 [CONTRIBUTING.md](CONTRIBUTING.md)，安全问题请按 [SECURITY.md](SECURITY.md) 私下报告。

## 许可证

[MIT](LICENSE)
