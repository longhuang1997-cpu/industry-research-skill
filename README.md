# Industry Research Skill

> **AI驱动的行业研究工具** - 用咨询公司标准快速生成行业洞察

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/longhuang1997-cpu/industry-research-skill)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

## 🎯 这个Skill是什么？

**Industry Research Skill** 能够在10-40分钟内，生成一份咨询公司水准的行业研究报告。

**怎么用？**
在Claude对话中说：
```
帮我研究【你的行业】
```
就这么简单！

**适合谁用？**
- 📊 **投资人** - 快速了解目标行业，辅助投资决策
- 🚀 **创业者** - 市场进入评估，商业模式验证
- 💼 **战略规划** - 企业进入新市场前的全面调研
- 🎓 **咨询顾问** - 快速生成行业分析框架底稿

---

## ✨ 核心特点

### 1. 咨询级分析框架
使用BCG/麦肯锡的分析方法：
- **PEST框架** - 政策环境分析
- **Porter五力模型** - 竞争格局分析
- **四方决策链** - 商业模式分析
- **单位经济模型** - 盈利能力评估

### 2. 智能动态流程
- 🎯 自然语言描述需求："重点看政策和竞争"
- ⚡ 自动生成最小研究流程（按需分析，不做冗余工作）
- 🔗 智能依赖解析（例如：竞争格局分析会先做市场规模）

### 3. 质量保证
- ✅ 每个分析必须包含具体数字
- ✅ 自动质量评分（≥0.7为合格）
- ✅ 给出可执行的战略建议

---

## 🚀 快速开始

### 最简单的方式：对话调用（推荐）✨

**在Claude对话中直接说**：
```
帮我研究医疗陪护行业
```

或者更具体：
```
帮我研究医疗陪护，重点看政策和竞争，快速版
```

**就这么简单！** Claude会自动调用Skill生成报告。

---

### 安装Skill（首次使用）

#### 步骤1：克隆项目
```bash
git clone https://github.com/longhuang1997-cpu/industry-research-skill.git
cd industry-research-skill
```

#### 步骤2：安装依赖
```bash
pip install -r requirements.txt
```

#### 步骤3：配置API密钥
```bash
# 方式1：环境变量
export ANTHROPIC_API_KEY="your-api-key"

# 方式2：编辑config.yaml
api_key: "your-api-key"
```

#### 步骤4：安装到Claude
将`skill.md`文件放到Claude的skills目录（具体路径参考Claude文档）

**安装后**，在任何Claude对话中说"帮我研究XX行业"即可使用。

---

### 命令行调用（可选，适合技术用户）

如果你熟悉Python，也可以直接命令行：

```bash
# 最简单
python irs.py "医疗陪护"

# 自然语言指定重点
python irs.py "医疗陪护" --intent "重点看政策和竞争"

# 精确指定维度
python irs.py "医疗陪护" --dimensions 政策环境,市场规模,商业模式

# 全量深度模式
python irs.py "医疗陪护" --mode full
```

**但对于普通用户，强烈推荐对话方式！**

---

## 📊 支持的分析维度

| 维度 | 说明 | 分析框架 | 时长 |
|------|------|---------|------|
| **行业画像** | 3句话概括行业特征 | - | 2分钟 |
| **政策环境** | 识别政策驱动因素和影响 | PEST-P | 8分钟 |
| **市场规模** | 估算市场规模和增长率 | Top-down + Bottom-up | 8分钟 |
| **商业模式** | 分析盈利模式和单位经济 | 四方决策链 | 10分钟 |
| **竞争格局** | 评估行业竞争强度 | Porter五力 | 10分钟 |
| **进入壁垒** | 识别市场进入门槛 | 五大壁垒 | 8分钟 |
| **风险分析** | 评估主要风险和应对策略 | PESTEL | 8分钟 |
| **战略建议** | 给出可执行的进入策略 | - | 10分钟 |

**动态流程**：工具会自动选择必需维度，并根据依赖关系排序。

---

## 💡 使用场景

### 在Claude对话中直接使用

#### 场景1：投资尽调
```
你：帮我研究AI芯片行业，投资视角，重点看市场规模和竞争格局

Claude：[调用Industry Research Skill]
正在分析...
已生成报告：AI芯片行业研究报告.html
- 市场容量：2024年约500亿美元，CAGR 25%
- 主要玩家：英伟达（60%）、AMD（15%）、Intel（10%）
- 投资机会：边缘AI芯片、高性能推理芯片
```

#### 场景2：市场进入评估
```
你：我想做智能陪护机器人，帮我评估市场进入的可行性

Claude：[调用Industry Research Skill]
正在分析政策环境、进入壁垒、风险...
已生成评估报告
- 政策支持度：★★★★☆（国家养老政策支持）
- 进入门槛：中等（需要医疗器械认证）
- 主要风险：技术成熟度、用户接受度
- 建议策略：先做ToB医院市场，再拓展ToC家庭
```

#### 场景3：商业模式验证
```
你：上门护理服务的商业模式能跑通吗？帮我算算账

Claude：[调用Industry Research Skill]
正在分析商业模式、市场规模、竞争格局...
已生成分析报告
- 单位经济：客单价300元，毛利率40%
- 市场空间：2024年预计200亿，增长率30%
- 盈利模型：需要单城市3000+订单/月才能盈亏平衡
- 竞争格局：区域竞争为主，CR5<20%
```

---

## 🚀 快速开始

### 对于普通用户（推荐）

**直接在Claude对话中说**：
```
帮我研究【你的行业】
```

就这么简单！Claude会自动调用这个Skill。

### 对于开发者（安装Skill）

如果你是第一次使用，需要安装：

```bash
# 1. 克隆Skill
git clone https://github.com/longhuang1997-cpu/industry-research-skill.git

# 2. 安装到Claude
# (具体步骤参考skill.md)

# 3. 配置API
export ANTHROPIC_API_KEY="your-key"
```

安装后，在任何对话中说"帮我研究XX行业"即可使用。

### 对于技术用户（命令行调用）

如果你熟悉Python，也可以直接命令行调用：

```bash
python irs.py "AI芯片" --intent "投资视角"
```

但**不推荐普通用户使用命令行**，对话方式更简单。

---

## 🏗️ 技术架构

```
irs.py (入口)
  ↓
core/orchestrator.py (流程编排)
  ↓
core/research_engine.py (AI引擎)
  ├─ 意图理解 → 自然语言转结构化参数
  ├─ 动态工作流 → 按需生成+依赖解析
  ├─ AI分析 → 8个Prompt模板（咨询框架）
  └─ 质量检查 → 自动评分
```

### 为什么这样设计？

**混合策略**：代码做编排，AI做推理

| 模块 | 实现方式 | 理由 |
|------|---------|------|
| 流程控制 | Python代码 | 快速、稳定、免费 |
| 依赖解析 | 拓扑排序算法 | 100%准确 |
| **行业分析** | **AI + Prompt工程** | **擅长推理和生成** ⭐ |
| 质量评分 | 规则检查 | 确定性判断 |

**核心优势**：
- ⚡ 性能好：简单规则用代码（0.001秒 vs AI的1秒）
- 💰 成本低：避免不必要的API调用
- 🎯 准确性：关键推理交给AI，算法交给代码

---

## 🔧 配置

### API密钥

支持多种配置方式：

```bash
# 方式1：环境变量
export ANTHROPIC_API_KEY="your-key"

# 方式2：config.yaml
api_key: "your-key"
model: "claude-sonnet-4-20250514"
```

### 自定义分析维度

编辑 `core/research_engine.py`：

```python
DIMENSIONS = {
    '你的维度': {
        'time': 8,  # 预计耗时（分钟）
        'dependencies': ['行业画像'],  # 依赖关系
        'prompt_template': 'your_template'
    }
}
```

---

## 📚 高级用法

### 扩展MCP数据源（可选）

如果你有付费数据订阅（如Wind、企查查），可以自建MCP扩展：

```bash
mcp/
  └── your_datasource/
      ├── server.py
      └── config.yaml
```

参考：`mcp/README.md`

**注意**：工具默认使用Claude的Web搜索能力，大部分场景已足够。

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

**特别欢迎**：
- 新的分析维度和Prompt模板
- 行业特定的分析框架
- 报告样式优化

---

## 📄 License

MIT License - 可自由使用、修改和商业化

---

## 🔗 相关资源

- **项目主页**：https://github.com/longhuang1997-cpu/industry-research-skill
- **技术文档**：`REFACTOR_NOTES.md`
- **Skill集成**：`skill.md`

---

## ❓ 常见问题

### Q: 需要什么样的API？
A: Claude API（Sonnet或Opus模型），支持Anthropic官方API和兼容接口。

### Q: 分析质量如何？
A: 使用咨询公司的分析框架，包含具体数字和案例。质量分≥0.7的分析通过验证。

### Q: 可以分析哪些行业？
A: 任何行业。工具使用通用分析框架，AI会根据行业特点自动调整。

### Q: 支持中文吗？
A: 完全支持中文输入和输出，也支持英文。

### Q: 需要多久？
A: 快速模式10-20分钟，全量模式40-60分钟，取决于选择的维度数量。

---

**用AI推理替代脚本复杂度 - 让行业研究更简单！** 🚀
