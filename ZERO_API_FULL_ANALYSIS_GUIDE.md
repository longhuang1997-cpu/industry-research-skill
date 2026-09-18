# 零API完整分析 - 使用指南

**最后更新**: 2026-01-09  
**版本**: v3.2 (零API完整分析版)

---

## 🎯 核心理念

**完整分析，不需要API** ——Skill负责方法论+流程控制+报告生成，Agent负责执行分析。

### 架构对比

**原版（需要API）**:
```
用户 → Skill → 调用Anthropic API → 返回分析 → 生成报告
           ↑
        需要API密钥
```

**零API版（不需要API）**:
```
用户 → Skill生成任务清单(Prompt列表) → Agent执行分析 → Skill生成报告
           ↑                                ↑
        无需API密钥                    调用方Agent的能力
```

---

## 🚀 快速开始

### 方式1: 在Python中使用

```python
from core.prompt_only_orchestrator import PromptOnlyOrchestrator

# 初始化（无需API密钥）
orch = PromptOnlyOrchestrator(mode='quick')  # quick/standard/deep

# Step 1: 获取研究任务清单
tasks = orch.get_research_tasks(
    industry='医疗陪护',
    dimensions=['政策环境', '市场规模', '商业模式']  # 可选，不指定则使用默认
)

# Step 2: 逐个执行分析（用你自己的Agent能力）
results = []
for task in tasks:
    # 真实场景：用你的Agent执行Prompt
    content = your_agent.analyze(task['prompt'])
    
    # 评估质量
    quality_score = task['assess_quality'](content)
    
    results.append({
        'dimension': task['dimension'],
        'content': content,
        'quality_score': quality_score
    })

# Step 3: 生成专业报告
report = orch.generate_report(
    industry='医疗陪护',
    analysis_results=results,
    export_formats=['word', 'markdown']  # 可选：多格式导出
)

print(f"报告路径: {report['path']}")
```

### 方式2: 在对话中使用（WorkBuddy/Claude Code）

**用户**: "帮我研究医疗陪护行业"

**WorkBuddy**:
```python
# 内部流程（用户看不见）

# 1. 获取任务清单
from core.prompt_only_orchestrator import PromptOnlyOrchestrator
orch = PromptOnlyOrchestrator()
tasks = orch.get_research_tasks('医疗陪护')

# 2. 逐个执行（用我自己的能力）
results = []
for task in tasks:
    # 展示进度
    print(f"正在分析 {task['dimension']}...")
    
    # 用我的联网检索+分析能力
    content = self.analyze_with_web_search(
        prompt=task['prompt'],
        hypothesis=task['hypothesis'],
        evidence_needed=task['evidence_needed']
    )
    
    results.append({
        'dimension': task['dimension'],
        'content': content,
        'quality_score': task['assess_quality'](content)
    })

# 3. 询问用户是否生成报告
if user_wants_report:
    report = orch.generate_report('医疗陪护', results)
    print(f"报告已生成: {report['path']}")
else:
    # 直接在对话中展示结果
    for result in results:
        print(f"## {result['dimension']}")
        print(result['content'])
```

---

## 📦 核心组件

### 1. PromptOnlyEngine

**职责**: 生成分析Prompt，不调用API

```python
from core.prompt_only_engine import PromptOnlyEngine

engine = PromptOnlyEngine()

# 获取所有分析Prompt
prompts = engine.get_analysis_prompts(
    industry='医疗陪护',
    dimensions=['政策环境', '市场规模'],
    research_type='行业分析'  # 6种类型可选
)

# 获取单个维度的Prompt
prompt_info = engine.get_single_dimension_prompt(
    industry='医疗陪护',
    dimension='政策环境',
    context={}  # 前序分析结果
)
```

### 2. PromptOnlyOrchestrator

**职责**: 流程控制+质量检查+报告生成

```python
from core.prompt_only_orchestrator import PromptOnlyOrchestrator

orch = PromptOnlyOrchestrator(mode='standard')

# 获取任务清单
tasks = orch.get_research_tasks('医疗陪护')

# 生成报告
report = orch.generate_report('医疗陪护', results)

# 快速生成研究指南（纯Prompt，不执行分析）
guide = orch.quick_start('医疗陪护')
```

---

## 🎓 使用场景

### 场景1: WorkBuddy在对话中研究

**优势**:
- ✅ 不需要外部API密钥
- ✅ 用我（WorkBuddy）的联网检索能力
- ✅ 在对话中实时展示进度
- ✅ 灵活调整分析深度

**流程**:
```
用户提问 → 获取任务清单 → 逐个执行(用我的能力) → 实时展示结果 → 可选生成报告
```

### 场景2: 其他Agent集成方法论

**优势**:
- ✅ 快速获得"咨询级"研究框架
- ✅ 6类型×16框架自动匹配
- ✅ 假设-证据-结论三段式
- ✅ 质量评估+报告生成

**流程**:
```
Agent调用Skill → 获取Prompt列表 → 用自己的能力执行 → 返回结果给Skill → 生成报告
```

### 场景3: 企业内部AI能力沉淀

**优势**:
- ✅ 方法论显性化（6类型×16框架清单）
- ✅ 流程标准化（5步故事线）
- ✅ 质量保证（数字核验+反面检验）
- ✅ 可视化报告（HTML/Word/Markdown）

**流程**:
```
员工提出研究需求 → 企业AI Agent调用Skill → 生成任务清单 → AI执行 → 输出报告
```

---

## 📊 任务清单结构

每个任务包含：

```python
{
    'step': 1,                      # 第几步
    'total': 5,                     # 总共几步
    'dimension': '政策环境',         # 分析维度
    'time': 8,                      # 预计时间(分钟)
    'prompt': '完整的分析Prompt',   # Agent要执行的Prompt
    'hypothesis': '核心假设',        # 假设-证据-结论框架
    'evidence_needed': {            # 需要的证据
        'required': ['关键证据1', '关键证据2'],
        'supporting': ['支撑证据'],
        'counter': ['反驳证据']
    },
    'conclusion_format': '结论格式',  # 结论要求
    'needs_internal_data': False,    # 是否需要内部数据
    'internal_data_desc': '',        # 内部数据说明
    'context': {},                   # 上下文（前序结果）
    'assess_quality': <function>     # 质量评估函数
}
```

---

## 🔧 高级用法

### 1. 自定义分析维度

```python
# 不使用默认维度，自己指定
tasks = orch.get_research_tasks(
    industry='新能源汽车',
    dimensions=[
        '技术趋势',      # 自定义维度
        '竞争格局',
        '供应链分析',   # 自定义维度
        '商业模式'
    ],
    research_type='行业分析'
)
```

### 2. 多种研究类型

```python
# 6种研究类型可选
research_types = [
    '行业分析',           # 通用行业研究
    '公司对标',           # 对标分析
    '投资尽调',           # 投资决策
    '战略指导',           # 战略规划
    '市场进入可行性',     # 新市场评估
    '合作评估'            # 合作决策
]

tasks = orch.get_research_tasks(
    industry='企业服务SaaS',
    research_type='公司对标'  # 会自动匹配对应的分析维度
)
```

### 3. 质量检查

```python
# Skill提供质量检查
quality_check = orch.engine.check_quality(results)

print(f"平均质量分: {quality_check['avg_quality']:.2f}")
print(f"检查结果: {'通过' if quality_check['passed'] else '有问题'}")

if quality_check['issues']:
    print("问题:")
    for issue in quality_check['issues']:
        print(f"  - {issue}")
    
    print("建议:")
    for suggestion in quality_check['suggestions']:
        print(f"  - {suggestion}")
```

### 4. 多格式导出

```python
# 生成报告时指定导出格式
report = orch.generate_report(
    industry='医疗陪护',
    analysis_results=results,
    export_formats=['word', 'markdown']  # HTML自动生成
)

# 查看导出文件
if 'exported_files' in report:
    for fmt, path in report['exported_files'].items():
        print(f"{fmt.upper()}: {path}")
```

---

## 💡 最佳实践

### 1. 渐进式分析

```python
# 不用一次获取所有任务，可以逐步深入
# Step 1: 快速画像
quick_tasks = orch.get_research_tasks(
    industry='医疗陪护',
    dimensions=['行业画像']  # 只要概况
)

# Step 2: 用户确认后，深入分析
if user_wants_more:
    deep_tasks = orch.get_research_tasks(
        industry='医疗陪护',
        dimensions=['政策环境', '市场规模', '商业模式', '竞争格局']
    )
```

### 2. 上下文传递

```python
# 后续维度的分析，可以传递前序结果作为上下文
context = {}

for task in tasks:
    # 执行分析
    content = agent.analyze(task['prompt'])
    
    # 更新上下文（供后续任务使用）
    context[task['dimension']] = content
    
    # 后续任务可以看到前面的分析结果
    # 例如："商业模式"分析可以引用"市场规模"的数据
```

### 3. 灵活调整质量评分

```python
# Skill提供的质量评估函数
quality_score = task['assess_quality'](content)

# 你也可以自己实现更严格的评分
def my_quality_check(content):
    score = 0.0
    
    # 检查是否有数字+单位
    if re.search(r'\d+\s*(亿元|万人|%)', content):
        score += 0.4
    
    # 检查是否有数据来源
    if '来源:' in content or '数据来源' in content:
        score += 0.3
    
    # 检查是否有结论
    if '结论' in content or '建议' in content:
        score += 0.3
    
    return score
```

---

## 🎯 与原版对比

| 维度 | 原版（需要API） | 零API版 |
|------|----------------|---------|
| **API依赖** | ❌ 需要Anthropic API密钥 | ✅ 不需要API |
| **分析能力** | Claude API | 调用方Agent能力 |
| **灵活性** | 固定流程 | 灵活调整 |
| **实时交互** | ❌ 批量执行 | ✅ 可以逐步展示 |
| **成本** | API调用费用 | 零成本 |
| **方法论** | ✅ 6类型×16框架 | ✅ 完全保留 |
| **报告生成** | ✅ HTML/Word/Markdown | ✅ 完全保留 |
| **质量检查** | ✅ 自动评分 | ✅ 完全保留 |

---

## 🔍 FAQ

### Q1: 零API版和Mock模式有什么区别？

**Mock模式**:
- 返回方法论框架（模板）
- 不执行真实分析
- 用于演示/教学

**零API版**:
- 返回完整的Prompt
- Agent执行真实分析
- 用于生产环境

### Q2: 如果我有API密钥，还能用零API版吗？

可以！零API版是**补充**不是**替代**：

- **有API密钥**: 用原版orchestrator.py（自动化执行）
- **无API密钥**: 用prompt_only_orchestrator.py（手动或Agent执行）
- **混合使用**: 部分维度用API，部分手动

### Q3: 零API版的报告质量如何？

**报告质量取决于**:
1. Agent的分析能力（谁执行Prompt）
2. 数据来源（Agent能否联网检索）
3. 方法论应用（Skill保证框架正确）

**Skill保证**:
- ✅ 方法论框架正确（6类型×16框架）
- ✅ 假设-证据-结论三段式
- ✅ 质量评估标准
- ✅ 报告排版专业

### Q4: 如何在企业内部推广？

**推荐路径**:

1. **第一阶段**: 演示方法论价值
   - 用quick_start()生成研究指南
   - 展示6类型×16框架清单
   - 不需要任何API

2. **第二阶段**: 试点项目
   - 选1-2个业务场景
   - 用零API版集成到现有AI Agent
   - 验证报告质量

3. **第三阶段**: 全面推广
   - 沉淀到企业AI能力库
   - 培训团队使用方法论
   - 建立企业自定义框架（Phase 3已支持）

---

## 📚 延伸阅读

- [ZERO_DEPENDENCY_FIXES.md](./ZERO_DEPENDENCY_FIXES.md) - 零依赖修复说明
- [examples/zero_api_full_analysis.py](./examples/zero_api_full_analysis.py) - 完整使用示例
- [skill.md](./skill.md) - Skill原始文档（方法论详解）

---

**🎉 现在，所有Agent都可以调用Industry Research Skill了！**

**核心价值**: 不是更强的AI，而是**方法论显性化 + 流程标准化 + 质量保证**
