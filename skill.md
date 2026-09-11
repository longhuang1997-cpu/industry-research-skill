---
name: industry-research
description: AI辅助行业研究自动化 - 快速模式70分钟 | 全量模式3-5小时
version: 0.1.0-alpha
author: Based on medical care case study
---

# 使用方法

```bash
/industry-research [行业名称] [--mode quick|full]
```

## 示例

```bash
# 快速模式（默认）
/industry-research 医疗陪护

# 全量模式
/industry-research 医疗陪护 --mode full

# 带其他参数
/industry-research 医疗陪护 --mode quick --web-search yes
```

## 参数说明

- `行业名称`：必需，如"医疗陪护"、"养老服务"
- `--mode`：可选，quick（快速模式，70分钟）或 full（全量模式，3-5小时），默认quick
- `--web-search`：可选，yes或no，默认yes

## 依赖

- Python 3.8+
- matplotlib >= 3.5.0
- pyyaml >= 6.0
- requests >= 2.28.0

## 入口

主程序入口：`orchestrator/orchestrator.py`
