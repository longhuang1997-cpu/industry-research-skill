# Industry Research Skill - 使用示例

**版本**: v3.2  
**日期**: 2026-01-09

---

## 📚 目录

1. [零API完整分析（推荐）](#零api完整分析)
2. [交互式研究（新增）](#交互式研究)
3. [自动化分析（需要API）](#自动化分析)
4. [自定义模型库](#自定义模型库)

---

## 🎯 零API完整分析

**适用场景**: WorkBuddy在对话中研究 / 其他Agent集成 / 企业内部AI能力沉淀

**核心优势**: 不需要任何API密钥，所有Agent都可以调用

### 方式1: 直接使用PromptOnlyOrchestrator

```python
from core.prompt_only_orchestrator import PromptOnlyOrchestrator

# 初始化（无需API密钥）
orch = PromptOnlyOrchestrator(mode='quick')

# 1. 获取研究任务清单
tasks = orch.get_research_tasks(
    industry='医疗陪护',
    dimensions=['政策环境', '市场规模', '商业模式']
)

# 2. Agent逐个执行任务
results = []
for task in tasks:
    # 用你自己的AI能力执行Prompt
    content = your_agent.analyze(task['prompt'])
    
    # 评估质量
    quality_score = task['assess_quality'](content)
    
    results.append({
        'dimension': task['dimension'],
        'content': content,
        'quality_score': quality_score
    })

# 3. 生成专业报告
report = orch.generate_report(
    industry='医疗陪护',
    analysis_results=results,
    export_formats=['word', 'markdown']  # 可选
)

print(f"✅ 报告已生成：{report['path']}")
```

**输出**:
- HTML报告（桌面/industry_research_reports/）
- Word/Markdown（可选）
- 含6类型×16框架方法论
- 假设-证据-结论三段式
- 质量评估报告

---

## 🎤 交互式研究（新增v3.2）

**适用场景**: 不确定研究范围，需要逐步澄清需求

**核心优势**: 多轮对话、需求澄清、中期回顾、动态调整

### 完整对话示例

```python
from core.interactive_session import InteractiveResearchSession

# 初始化交互式会话（零API模式）
session = InteractiveResearchSession(backend='prompt_only')

# ========== 第一轮：用户提问 ==========
user_msg = "帮我研究医疗陪护行业"
response = session.chat(user_msg)

print(response['message'])
# 输出：你研究【医疗陪护】的目的是什么？
# 选项：
#   1. 🚀 市场进入可行性
#   2. 💰 投资尽调
#   3. ⚔️ 竞争分析
#   4. 📊 行业概览
#   5. 🎯 自定义

# ========== 第二轮：选择目的 ==========
response = session.chat("market_entry")

print(response['message'])
# 输出：基于「市场进入可行性」，我推荐分析以下维度：
# - 市场规模
# - 进入壁垒
# - 竞争格局
# - 单位经济
# - 风险分析
# 
# 选项：
#   1. ✅ 全部分析（预计40分钟）
#   2. 🎯 我来选择部分
#   3. ⚡ 快速版（3-4个核心维度）

# ========== 第三轮：确认维度 ==========
response = session.chat("all")

print(f"{response['message']}")
# 输出：已生成5个分析任务，请Agent逐个执行

tasks = response['tasks']
print(f"任务清单：{len(tasks)}个")

# ========== 第四轮：Agent执行分析 ==========
for task in tasks:
    print(f"\n正在分析：{task['dimension']}...")
    
    # 用你的AI能力执行
    content = your_agent.analyze(task['prompt'])
    
    # 提交结果
    progress = session.submit_result(
        dimension=task['dimension'],
        content=content
    )
    
    print(progress['message'])
    # 输出：✅ 市场规模 分析完成 (1/5)
    
    # 中期回顾（自动触发，完成一半时）
    if progress['type'] == 'review':
        print("\n📊 中期回顾：")
        print(progress['message'])
        
        # 关键发现
        for finding in progress['key_findings']:
            print(f"  - {finding['dimension']}: {finding['summary']}")
        
        # 用户决定
        user_choice = input("继续按计划 / 调整维度 / 生成报告？(continue/adjust/finish): ")
        continue_response = session.chat(user_choice)

# ========== 第五轮：生成报告 ==========
# 全部完成后自动生成报告
if progress['type'] == 'complete':
    print(f"\n✅ {progress['message']}")
    print(f"报告路径：{progress['report_path']}")
```

### 简化版（适合WorkBuddy集成）

```python
# WorkBuddy内部实现

def research_industry_interactive(user_query: str):
    """交互式行业研究"""
    session = InteractiveResearchSession(backend='prompt_only')
    
    # 第一轮
    response = session.chat(user_query)
    if response['type'] == 'question':
        # 追问用户
        return format_question(response)
    
    # 后续轮次由用户回复驱动
    # ...
    
    # Agent执行任务
    if response['type'] == 'tasks':
        results = []
        for task in response['tasks']:
            content = self.analyze_with_web_search(task['prompt'])
            session.submit_result(task['dimension'], content)
        
        # 获取最终报告
        return session.state['report_path']
```

---

## 🤖 自动化分析（需要API）

**适用场景**: 有API密钥，希望全自动执行

**核心优势**: 一键生成，无需手动执行

```python
from core.orchestrator import Orchestrator

# 初始化（需要API密钥）
orch = Orchestrator(mode='quick')

# 一键执行
result = orch.run(
    industry='医疗陪护',
    user_params={
        'dimensions': ['政策环境', '市场规模', '竞争格局'],
        'intent': '我想评估这个市场是否值得进入'  # 可选：自然语言意图
    }
)

print(f"✅ 分析完成")
print(f"报告路径：{result['path']}")
print(f"质量评分：{result['quality']['avg_quality']:.2f}")
```

---

## 🔧 自定义模型库

**适用场景**: 企业有自己的分析框架，需要沉淀

**核心优势**: 显性化方法论，标准化流程

### 创建自定义模型

**文件**: `config/user_models/custom_framework.yaml`

```yaml
name: 丹田能源业务评估框架
description: 评估物业公司是否应该切入能源业务
version: 1.0.0
author: 黄林
created_at: 2026-01-09

# 使用条件
applicable_when:
  - 物业公司转型
  - 能源业务评估
  - 新业务论证

# 分析框架
framework:
  step1:
    name: 机会识别
    questions:
      - 政策是否支持？（双碳目标、地方补贴）
      - 市场空间多大？（既有物业面积×能源改造渗透率）
      - 业主支付意愿？（节能效益分享 vs 自费改造）
    
  step2:
    name: 能力匹配
    questions:
      - 物业公司有哪些优势？（场地、客户关系、运维）
      - 缺少哪些能力？（技术、资金、案例）
      - 获取成本多高？（自建 vs 合作 vs 收购）
    
  step3:
    name: 商业模式
    questions:
      - 收费模式？（EMC分享 / 托管 / 一次性改造）
      - 单位经济？（单项目回本周期、IRR）
      - 规模化路径？（单项目 → 区域复制 → 平台化）
    
  step4:
    name: 风险与退出
    questions:
      - 核心风险？（技术风险、回款风险、政策变化）
      - 如何对冲？（保险、担保、分段收款）
      - 退出机制？（止损条件、资产处置）

# 输出判据
output_criteria:
  should_enter:
    - 市场空间 > 100亿
    - 单位经济回本周期 < 5年
    - 核心能力可获取
    - 风险可控
  
  should_not_enter:
    - 政策不确定性高
    - 单位经济不成立
    - 核心能力缺口大且无法获取
  
  partnership_conditions:
    - 优先合作：技术/资金互补，风险共担
    - 慎重自建：避免重资产陷阱

# 常见误用
common_mistakes:
  - 只看市场大，不算单位经济
  - 只看政策好，不看执行力度
  - 低估能力缺口，高估自建速度
```

### 使用自定义模型

```python
from core.orchestrator import Orchestrator

orch = Orchestrator()

# 使用自定义模型
result = orch.run(
    industry='物业能源业务',
    user_params={
        'custom_model': '丹田能源业务评估框架'
    }
)
```

---

## 📊 对比：三种使用方式

| 维度 | 零API | 交互式 | 自动化 |
|------|-------|--------|--------|
| **需要API** | ❌ | ❌ | ✅ |
| **交互提问** | ❌ | ✅ | ❌ |
| **执行方式** | Agent手动执行 | Agent手动执行 | 自动执行 |
| **灵活性** | 中 | 高 | 低 |
| **适合场景** | 简单快速分析 | 复杂需求澄清 | 批量自动化 |
| **学习成本** | 低 | 中 | 低 |

---

## 🎓 最佳实践

### 1. 选择合适的模式

**零API模式** - 适合：
- WorkBuddy在对话中临时研究
- 其他Agent快速集成
- 没有API密钥的环境

**交互式模式** - 适合：
- 需求不明确，需要逐步澄清
- 希望根据中期发现调整方向
- 用户希望参与决策

**自动化模式** - 适合：
- 需求明确，维度固定
- 批量生成报告
- 有API密钥且希望节省时间

### 2. 质量控制

**必须做**:
- ✅ 使用假设-证据-结论三段式
- ✅ 标注数据来源
- ✅ 反面证据检验
- ✅ 质量评估（每章>0.7分）

**避免**:
- ❌ 只看正面，忽略反面
- ❌ 数据无溯源
- ❌ 假设未明确
- ❌ 结论不回答核心问题

### 3. 数据溯源

```python
# 好的实践
content = """
市场规模：2024年约800亿元（宽口径，含陪诊）[来源: 《2025医疗陪护白皮书》]
预计2025年突破1000亿元 [来源: 时代财经 2025-07]

⚠️ 口径说明：白皮书未严格区分陪护/陪诊，存在口径泡沫风险
"""

# 不好的实践
content = """
市场规模很大，约几百亿
```

### 4. 反面证据检验

```python
# 每个结论都要问：
# 1. 有什么证据反驳这个结论？
# 2. 在什么情况下这个结论不成立？
# 3. 我有没有忽略哪些反面案例？

# 示例
正面结论：政府大力推动长护险，行业前景乐观
反面证据：
  - 某地试点3年后暂停（财政压力）
  - 下沉市场覆盖率<5%（支付意愿不足）
  - 机构利润率普遍<10%（补贴不足以覆盖成本）
综合判断：政策方向正确，但执行力度和持续性存在不确定性
```

---

## 🔗 相关文档

- [零API完整分析指南](ZERO_API_FULL_ANALYSIS_GUIDE.md)
- [方法论框架说明](README.md)
- [v3.2更新日志](CHANGELOG_v3.2.md)

---

**🎉 所有Agent都可以调用Industry Research Skill做完整分析了！**
