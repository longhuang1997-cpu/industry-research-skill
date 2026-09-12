---
name: industry-research
description: AI驱动的咨询级行业研究 - 分析行业时自动调用
version: 1.0.0
author: Refactored 2026-09-12
---

# Industry Research Skill

当用户询问行业研究相关问题时，自动调用此Skill生成专业分析报告。

## 触发场景

以下场景自动触发：
- 用户说"帮我研究【行业名】"
- 用户说"分析【行业名】行业"
- 用户说"【行业名】市场怎么样"
- 用户询问行业政策、竞争、商业模式等

## 调用方式

### 对话示例1：简单调用
```
用户：帮我研究医疗陪护行业

Claude执行：
cd /path/to/industry-research-skill
python irs.py "医疗陪护"

输出报告路径给用户
```

### 对话示例2：指定重点
```
用户：帮我研究AI芯片，重点看政策和竞争

Claude执行：
cd /path/to/industry-research-skill
python irs.py "AI芯片" --intent "重点看政策和竞争"

输出报告路径给用户
```

### 对话示例3：精确指定维度
```
用户：分析智能陪护机器人的政策环境、进入壁垒和风险

Claude执行：
cd /path/to/industry-research-skill
python irs.py "智能陪护机器人" --dimensions 政策环境,进入壁垒,风险分析

输出报告路径给用户
```

## 技术实现

### 入口文件
- **主入口**：`irs.py`
- **工作目录**：`/path/to/industry-research-skill`（安装路径）

### 参数映射

| 用户自然语言 | 命令行参数 |
|------------|-----------|
| "帮我研究【行业】" | `python irs.py "行业"` |
| "重点看XX和YY" | `--intent "重点看XX和YY"` |
| "分析XX、YY、ZZ" | `--dimensions XX,YY,ZZ` |
| "详细分析" | `--mode full` |
| "快速版" | `--mode quick`（默认） |

### 意图理解关键词

Claude应该识别这些关键词并转换为dimensions参数：

| 用户说 | dimensions参数 |
|-------|---------------|
| "政策"、"监管" | 政策环境 |
| "市场规模"、"多大" | 市场规模 |
| "商业模式"、"怎么赚钱" | 商业模式 |
| "竞争"、"对手" | 竞争格局 |
| "壁垒"、"门槛" | 进入壁垒 |
| "风险"、"挑战" | 风险分析 |

---

---

## 核心特性

### ✅ 自动意图理解
- 用户自然语言 → 自动转换为结构化参数
- "重点看政策和竞争" → `--intent "重点看政策和竞争"`
- 支持模糊表达，Skill内部有意图解析

### ✅ 动态工作流
- 按需生成研究流程（不做冗余分析）
- 自动解析依赖关系（竞争格局依赖市场规模）
- 最小化时间成本

### ✅ 咨询级分析
- BCG/麦肯锡分析标准
- 使用PEST、Porter、四方决策链等框架
- 必须包含具体数字和可执行建议

---

## 支持的分析维度

| 维度关键词 | dimensions值 | 分析框架 | 时长 |
|----------|-------------|---------|------|
| "政策"、"监管" | 政策环境 | PEST-P | 8分钟 |
| "市场"、"规模" | 市场规模 | Top-down + Bottom-up | 8分钟 |
| "商业模式"、"盈利" | 商业模式 | 四方决策链 | 10分钟 |
| "竞争"、"对手" | 竞争格局 | Porter五力 | 10分钟 |
| "壁垒"、"门槛" | 进入壁垒 | 五大壁垒 | 8分钟 |
| "风险"、"挑战" | 风险分析 | PESTEL | 8分钟 |

**必需维度**：行业画像、战略建议（自动补充）

---

## 输出格式

### 执行过程
```
[Step 1] 解析用户意图...
   识别维度: 政策环境, 竞争格局
   
[Step 2] 生成研究工作流...
   工作流: 5个步骤, 预计 38 分钟
   
[Step 3] 执行AI分析...
   [1/5] 分析 行业画像... [OK] (质量: 0.85)
   [2/5] 分析 政策环境... [OK] (质量: 0.78)
   [3/5] 分析 市场规模... [OK] (质量: 0.82)
   [4/5] 分析 竞争格局... [OK] (质量: 0.80)
   [5/5] 分析 战略建议... [OK] (质量: 0.88)
   
[Step 4] 质量检查...
   平均质量分: 0.83
   [OK] 质量检查通过
   
[Step 5] 生成专业报告...
   [OK] 报告已生成: output/医疗陪护_20260912_220145.html
```

### 返回给用户
```
✓ 行业研究完成！

报告路径: output/医疗陪护_20260912_220145.html
平均质量分: 0.83
执行时间: 38分钟

报告包含：
- 行业画像（3句话概括）
- 政策环境分析（PEST-P框架）
- 市场规模分析（Top-down + Bottom-up）
- 竞争格局分析（Porter五力）
- 战略建议（可执行方案）
```

---

## 故障处理

### 常见问题

**1. API密钥未配置**
```
错误: ANTHROPIC_API_KEY not found
解决: export ANTHROPIC_API_KEY="your-key"
或编辑 config.yaml
```

**2. 依赖未安装**
```
错误: ModuleNotFoundError: No module named 'anthropic'
解决: pip install -r requirements.txt
```

**3. 工作目录错误**
```
错误: irs.py not found
解决: 确保Claude当前目录在 industry-research-skill/
cd /path/to/industry-research-skill
```

**4. 分析质量偏低**
```
警告: 某个维度质量分 < 0.6
处理: Skill会自动重试，无需人工干预
```

---

## 扩展能力

### 自建MCP数据源（可选）

Skill默认使用Claude的Web搜索能力，已足够大部分场景。

**何时需要自建MCP？**
- 有付费数据订阅（Wind、企查查、Bloomberg）
- 长期研究特定行业（需要专业数据库）
- 接入公司内部系统（内部BI、CRM数据）

**参考文档**：`mcp/README.md`

---

---

## 技术架构（供开发者参考）

### 核心流程
```
用户对话
  ↓
Claude识别触发词
  ↓
执行: python irs.py "行业" [--intent "意图" | --dimensions 维度列表]
  ↓
irs.py (入口转发)
  ↓
core/orchestrator.py (流程编排)
  ↓
core/research_engine.py (AI引擎)
  ├─ parse_intent() - 意图理解
  ├─ create_workflow() - 动态工作流
  ├─ analyze() - AI分析（8个Prompt模板）
  └─ check_quality() - 质量检查
  ↓
生成HTML报告
  ↓
返回报告路径给用户
```

### 设计原则
- **代码做编排**（流程控制、依赖解析、质量评分）
- **AI做推理**（行业分析、框架应用、战略建议）
- **Prompt工程 > 复杂脚本**（用Prompt注入框架知识）
- **按需生成 > 固定模板**（动态工作流）

### 依赖
- Python 3.8+
- anthropic >= 0.18.0
- pyyaml >= 6.0

---

## Claude调用示例（完整流程）

### 示例1：用户说"帮我研究医疗陪护"

```python
# Claude内部执行（自动）
import subprocess
import os

# 切换到Skill目录
os.chdir('/path/to/industry-research-skill')

# 执行Skill
result = subprocess.run(
    ['python', 'irs.py', '医疗陪护'],
    capture_output=True,
    text=True
)

# 解析输出，获取报告路径
report_path = extract_report_path(result.stdout)

# 返回给用户
print(f"✓ 行业研究完成！\n报告路径: {report_path}")
```

### 示例2：用户说"研究AI芯片，重点看政策和竞争"

```python
# Claude内部执行（自动）
os.chdir('/path/to/industry-research-skill')

result = subprocess.run(
    ['python', 'irs.py', 'AI芯片', '--intent', '重点看政策和竞争'],
    capture_output=True,
    text=True
)

report_path = extract_report_path(result.stdout)
print(f"✓ 行业研究完成！\n报告路径: {report_path}")
```

---

## 开发者备注

### Skill安装路径
- 默认：`~/.claude/skills/industry-research-skill/`
- 或用户指定路径

### 执行权限
- 确保irs.py有执行权限
- 确保Claude有权限访问Skill目录

### 输出目录
- 默认：`output/`（相对于Skill根目录）
- 报告命名：`{行业}_{时间戳}.html`

---

**设计理念**：让AI做AI擅长的事（推理），用脚本做脚本擅长的事（编排）。

