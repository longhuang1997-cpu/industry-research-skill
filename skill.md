---
name: industry-research
description: AI驱动的咨询级行业研究 - 快速模式70分钟 | 全量模式3-5小时
version: 0.4.0
author: Based on consulting methodology
---

# 使用方法

## 对话调用（推荐）

直接在对话中说：
```
帮我研究一下【医疗陪护】行业
```

或使用skill命令：
```
/industry-research 医疗陪护
/industry-research 医疗陪护 --mode full
```

## 命令行调用

```bash
python irs.py "医疗陪护"
python irs.py "医疗陪护" --mode full
```

## 参数说明

- `行业名称`：必需，如"医疗陪护"、"金融科技"、"在线教育"
- `--mode`：可选
  - `quick`（默认）：快速模式，70分钟，完整流程
  - `full`：全量模式，3-5小时，深度研究+3个人工决策点

## 工作流程

### Quick模式（70分钟）
1. **数据收集** - 联网搜索 + Tier分级
2. **框架分析 + AI分析** - 5个框架 + 咨询级AI洞察
3. **图表生成** - 7种专业图表
4. **专业报告** - 麦肯锡风格HTML
5. **质量检查** - 5维度质检
6. **打包交付**

### Full模式（3-5小时）
- 所有Quick模式内容
- 扩展分析维度（竞争格局、进入壁垒）
- 3个人工决策点
- 更深度的数据收集

## 交付物

- 📊 **7种专业图表**：金字塔、瀑布图、饼图、时间线、散点矩阵、折线图、雷达图
- 📄 **专业HTML报告**：封面 + 执行摘要 + 主体分析 + 附录
- 📈 **真实数据支撑**：Web搜索 + Tier 1数据源
- 🧠 **AI咨询洞察**：政策、市场、商业模式、竞争、壁垒
- ✅ **质量保证**：5维度质检通过

## 依赖

- Python 3.8+
- anthropic >= 0.18.0
- matplotlib >= 3.5.0
- pyyaml >= 6.0
- requests >= 2.28.0

## 主控架构

主程序入口：`orchestrator/orchestrator.py`

调用链：
```
用户请求 → Orchestrator (主控)
  ↓
知识层 (FrameworkSelector + DataSourceSelector)
  ↓
执行层 (DataCollector + FrameworkApplier + ConsultingAIAnalyzer + ChartGenerator)
  ↓
输出层 (QualityChecker + ProfessionalReportGenerator + Packager)
```

## 配置

配置文件：`skill_config.yaml`

关键配置：
- `model`: 留空自动检测当前会话模型，或手动指定
- `api_key`: 留空从settings.json读取
- `base_url`: 可选，用于中转站

## 示例

**快速研究（对话）**：
> 帮我研究一下医疗陪护行业

**深度研究（对话）**：
> 帮我深度研究医疗陪护行业，使用全量模式

**命令行**：
```bash
python irs.py "医疗陪护"
python irs.py "金融科技" --mode full
```
