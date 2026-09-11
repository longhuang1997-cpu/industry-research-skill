# Industry Research Skill

AI辅助行业研究自动化工具 - 从数据收集到报告生成的完整解决方案

## 项目概述

Industry Research Skill是一个基于Python的自动化行业研究系统，能够在70分钟内生成专业的行业研究报告（快速模式）或3-5小时内生成深度研究报告（全量模式）。

### 核心特性

- **智能框架选择**：基于4象限分类法自动选择最合适的分析框架
- **自动数据收集**：集成Web搜索，自动收集Tier 1高质量数据源
- **7种专业图表**：金字塔图、瀑布图、对比饼图、时间线图、散点图、趋势图、雷达图
- **3种行业配色**：医疗、金融、科技行业专用配色方案
- **5维质量检查**：数据来源、财务模型、图表质量、逻辑一致性、HTML格式
- **双模式运行**：快速模式（70分钟）和全量模式（3-5小时）

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 快速模式（70分钟）

```bash
python orchestrator/orchestrator.py "医疗陪护" --mode quick
```

输出：
- 4-6张核心图表（SVG格式）
- 1页执行摘要（HTML）
- Tier 1数据覆盖率报告

### 全量模式（3-5小时）

```bash
python orchestrator/orchestrator.py "医疗陪护" --mode full
```

输出：
- 6+张完整图表
- 6章节完整报告
- 3个人工决策点
- 详细数据来源清单

## 项目结构

```
industry-research-skill/
├── orchestrator/              # 主控层
│   └── orchestrator.py       # 流程编排（快速/全量模式）
├── knowledge/                 # 知识层
│   ├── frameworks/           # 分析框架
│   │   ├── framework_selector.py        # 框架选择器
│   │   └── framework_decision_tree.yaml # 框架决策树
│   └── data_sources/         # 数据源
│       ├── data_source_selector.py      # 数据源选择器
│       └── data_source_tree.yaml        # 数据源树
├── execution/                 # 执行层
│   ├── charts/               # 图表生成器（7种）
│   │   ├── pyramid.py        # 金字塔图
│   │   ├── waterfall.py      # 瀑布图
│   │   ├── comparison_pie.py # 对比饼图
│   │   ├── timeline.py       # 时间线图
│   │   ├── scatter_matrix.py # 散点矩阵图
│   │   ├── line_chart.py     # 趋势图
│   │   └── radar_chart.py    # 雷达图
│   ├── styles/               # 配色方案
│   │   └── colors.py         # 3种行业配色
│   ├── data_collector.py     # 数据收集器
│   ├── framework_applier.py  # 框架应用器
│   └── chart_generator.py    # 图表生成统一接口
├── output/                    # 输出层
│   ├── quality_checker.py    # 5维质量检查
│   ├── report_generator.py   # HTML报告生成
│   └── packaging.py          # 交付物打包
├── utils/                     # 工具模块
│   ├── web_search_utils.py   # Web搜索工具
│   ├── file_utils.py         # 文件工具
│   ├── yaml_loader.py        # YAML加载器
│   └── logger.py             # 日志工具
├── config.yaml               # 配置文件
├── requirements.txt          # 依赖清单
└── README.md                 # 项目文档
```

## 核心功能

### 1. 智能框架选择

基于4象限分类自动选择分析框架：

- **象限1**（政府主导+高监管）：医疗陪护、养老服务
- **象限2**（政府主导+低监管）：公共交通、市政服务
- **象限3**（市场主导+高监管）：金融科技、网约车
- **象限4**（市场主导+低监管）：电商、社交媒体

每个象限匹配不同的分析框架组合。

### 2. 自动数据收集

**Tier分级系统：**
- **Tier 1**：政府官网、统计局（覆盖率目标≥60%）
- **Tier 2**：行业协会、券商研报
- **Tier 3**：媒体报道、企业年报

**功能：**
- 批量搜索（支持8+个关键词）
- 自动去重
- 来源可追溯性

### 3. 7种专业图表

| 图表类型 | 用途 | 适用场景 |
|---------|------|---------|
| 金字塔图 | 行业结构分层 | 市场规模分层、用户分级 |
| 瀑布图 | 单位经济模型 | 成本拆解、利润分析 |
| 对比饼图 | 支付结构演进 | 现状vs目标对比 |
| 时间线图 | 政策演进 | 历史事件、里程碑 |
| 散点矩阵图 | 竞争格局 | 企业定位、市场格局 |
| 趋势图 | 市场规模趋势 | 时间序列数据 |
| 雷达图 | PEST分析 | 多维度对比 |

### 4. 5种分析框架

| 框架 | 权重 | 适用场景 |
|------|------|---------|
| PEST分析 | 30% | 政策驱动型行业 |
| 行业链分析 | 25% | 供应链结构 |
| 四方决策链 | 25% | 多方决策场景 |
| 单位经济模型 | 15% | 盈利能力分析 |
| 波特五力 | 5% | 竞争格局分析 |

### 5. 双模式运行

#### 快速模式（70分钟）

6个关键步骤：
1. 数据收集（10分钟）
2. 框架分析（15分钟）
3. 快速可视化（20分钟）
4. 执行摘要（10分钟）
5. 质量检查（10分钟）
6. 打包交付（5分钟）

#### 全量模式（3-5小时）

5个深度阶段 + 3个人工决策点：
1. **Phase 1**: 深度数据收集 → **决策点1**：数据来源确认
2. **Phase 2**: 深度框架分析
3. **Phase 3**: 完整图表生成（6+张）
4. **Phase 4**: 完整报告生成 → **决策点2**：洞察深度自检
5. **Phase 5**: 质量检查和打包 → **决策点3**：最终质量把关

## 使用示例

### 示例1：研究医疗陪护行业

```python
from orchestrator.orchestrator import IndustryResearchOrchestrator

# 初始化
orchestrator = IndustryResearchOrchestrator(mode='quick')

# 运行研究
result = orchestrator.run(
    industry_name='医疗陪护',
    user_params={
        'industry': '医疗陪护',
        'web_search': True,
        'mode': 'quick'
    }
)

print(f"Status: {result['status']}")
print(f"Charts: {result['charts']}")
print(f"Tier 1 Coverage: {result['tier1_coverage']:.1%}")
```

### 示例2：生成单个图表

```python
from execution.charts.pyramid import PyramidChart

# 准备数据
data = {
    'title': '医疗陪护行业结构金字塔',
    'layers': [
        {'label': '高端市场', 'value': 630, 'unit': '亿元'},
        {'label': '中端市场', 'value': 470, 'unit': '亿元'},
        {'label': '基础市场', 'value': 210, 'unit': '亿元'}
    ]
}

# 生成图表
chart = PyramidChart('医疗陪护行业结构', industry='medical')
chart.save(data, 'output/pyramid.svg')
```

## 配置说明

`config.yaml` 主要配置项：

```yaml
skill:
  name: industry-research
  version: 0.1.0-alpha
  mode: quick  # quick | full

paths:
  skill_root: "."
  output_dir: "./output"
  charts_dir: "./output/charts"

quality:
  tier1_coverage_threshold: 0.6
  min_charts: 3
  max_execution_time: 7200  # seconds
```

## 依赖清单

- `matplotlib>=3.5.0` - 图表生成
- `pyyaml>=6.0` - YAML配置解析
- `requests>=2.28.0` - HTTP请求
- `pillow>=9.0.0` - 图像处理
- `numpy>=1.21.0` - 数值计算
- `pandas>=1.3.0` - 数据处理
- `jinja2>=3.0.0` - HTML模板

## 开发路线图

### 已完成（v0.1.0-alpha）

- [x] 7种核心图表生成器
- [x] 3种行业配色方案
- [x] 5种分析框架应用
- [x] 自动数据收集（Web搜索集成）
- [x] 5维质量检查
- [x] HTML报告生成
- [x] 快速模式和全量模式
- [x] 3个人工决策点

### 计划中（v0.2.0-beta）

- [ ] 真实的人工决策点UI（弹出对话框）
- [ ] PDF报告生成（替代HTML）
- [ ] 更多行业预设（10+行业）
- [ ] 自定义框架权重
- [ ] 数据缓存机制
- [ ] 性能优化（并行处理）

### 未来规划（v1.0.0）

- [ ] Claude Code Skill集成
- [ ] 多语言支持（英文、日文）
- [ ] 云端部署版本
- [ ] API接口
- [ ] Web UI

## 测试

### 运行单元测试

```bash
# 测试图表生成器
python execution/charts/pyramid.py
python execution/charts/waterfall.py
python execution/charts/line_chart.py
python execution/charts/radar_chart.py

# 测试框架应用器
python execution/framework_applier.py

# 测试质量检查器
python output/quality_checker.py

# 测试报告生成器
python output/report_generator.py
```

### 端到端测试

```bash
# 快速模式
python orchestrator/orchestrator.py "医疗陪护" --mode quick

# 全量模式
python orchestrator/orchestrator.py "医疗陪护" --mode full
```

## 性能指标

| 指标 | 快速模式 | 全量模式 |
|------|---------|---------|
| 执行时间 | 70分钟 | 3-5小时 |
| 图表数量 | 4-6张 | 6+张 |
| 报告章节 | 1页摘要 | 6个章节 |
| Tier 1覆盖率 | ≥60% | ≥80% |
| 质量检查 | 自动 | 自动+人工 |

## 常见问题

**Q: Windows上中文显示乱码怎么办？**  
A: 系统已处理了所有emoji字符，使用纯ASCII输出。如果仍有乱码，请确保终端编码设置为UTF-8。

**Q: 图表生成失败怎么办？**  
A: 系统采用容错设计，单个图表失败不会影响整体流程。查看控制台的`[SKIP]`消息了解失败原因。

**Q: 如何添加新的行业？**  
A: 编辑`knowledge/frameworks/framework_decision_tree.yaml`，在对应象限下添加行业名称和特征关键词。

**Q: 如何自定义图表配色？**  
A: 在`execution/styles/colors.py`中创建新的配色方案类，继承`ColorScheme`基类。

**Q: 支持哪些数据源？**  
A: 当前支持Web搜索（集成Tier分级），未来将支持API接口、数据库导入等。

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

- 项目地址：`C:\Users\huangl265\projects\industry-research-skill`
- 文档版本：v0.1.0-alpha
- 最后更新：2026-09-11

---

**Industry Research Skill - 让行业研究自动化，专注于洞察而非执行**
