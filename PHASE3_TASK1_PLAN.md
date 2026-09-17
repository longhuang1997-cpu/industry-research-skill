# Phase 3 任务1：反驳强化（8h）

**优先级**: P0（最高）  
**预计工时**: 8小时  
**价值**: 提升报告质量，强制辩证思考

---

## 🎯 任务目标

为每个章节自动搜索反面证据，强制辩证思考，提升报告可信度。

---

## 📋 核心功能

### 1. 反面证据搜索

**输入**: 章节内容 + 章节标题  
**输出**: ≥1个反面证据（含来源URL）

**搜索策略**:
```python
def find_counter_evidence(chapter_content: str, chapter_title: str) -> List[Dict]:
    """
    找反面证据
    
    Returns:
        [
            {
                'source': 'https://...',
                'title': '某公司PLG模式失败案例',
                'snippet': '...',
                'relevance': 0.85
            },
            ...
        ]
    """
    # Step 1: 提取关键结论
    key_conclusions = extract_key_conclusions(chapter_content)
    
    # Step 2: 为每个结论构造反向搜索
    counter_evidences = []
    for conclusion in key_conclusions:
        # 构造反向关键词
        queries = generate_counter_queries(conclusion)
        # 搜索
        for query in queries:
            results = web_search(query)
            counter_evidences.extend(results[:2])  # 每个结论取2个
    
    # Step 3: 去重 + 相关度排序
    unique_evidences = deduplicate(counter_evidences)
    sorted_evidences = sort_by_relevance(unique_evidences)
    
    return sorted_evidences[:3]  # 返回Top 3
```

---

### 2. 反向关键词生成

**核心模板**:
```python
COUNTER_QUERY_TEMPLATES = [
    "{conclusion} 失败案例",
    "{conclusion} 反例",
    "{conclusion} 不适用",
    "{conclusion} 局限性",
    "{conclusion} 风险",
    "为什么{conclusion}不成立",
]

def generate_counter_queries(conclusion: str) -> List[str]:
    """生成反向搜索关键词"""
    queries = []
    for template in COUNTER_QUERY_TEMPLATES:
        queries.append(template.format(conclusion=conclusion))
    return queries
```

**示例**:
```
结论: "SaaS公司应采用PLG模式"

反向关键词:
- "PLG模式 失败案例"
- "PLG模式 反例"
- "PLG模式 不适用"
- "为什么PLG模式不成立"
```

---

### 3. 关键结论提取

**方法1: LLM提取**（准确，慢）
```python
def extract_key_conclusions_llm(chapter_content: str) -> List[str]:
    """用LLM提取关键结论"""
    prompt = f"""
    请从以下章节中提取3个最关键的结论（一句话）:
    
    {chapter_content}
    
    格式:
    1. 结论1
    2. 结论2
    3. 结论3
    """
    response = call_llm(prompt)
    return parse_list(response)
```

**方法2: 规则提取**（快速，粗糙）
```python
def extract_key_conclusions_rule(chapter_content: str) -> List[str]:
    """用规则提取关键结论"""
    conclusions = []
    
    # 查找"建议"、"应该"、"因此"等关键词后的句子
    patterns = [
        r"建议[:：](.+?)。",
        r"应该(.+?)。",
        r"因此[,，](.+?)。",
        r"结论[:：](.+?)。",
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, chapter_content)
        conclusions.extend(matches)
    
    return conclusions[:3]  # 最多3个
```

**推荐**: 方法2（规则提取），快速且足够用

---

### 4. 集成到【反方观点】小节

**现有结构**:
```markdown
## 政策环境分析

### 核心发现
政府推动长护险试点，覆盖1.45亿人...

### 【反方观点】本章结论的最强反驳
（目前由LLM生成）
- 反驳点：...
- 我方回应：...
```

**增强后**:
```markdown
### 【反方观点】本章结论的最强反驳

**AI自动搜索到的反面证据**:
1. [来源A](https://...) 某地长护险试点失败案例
   > 试点3年后因财政压力暂停，覆盖率降至20%
   
2. [来源B](https://...) 长护险在下沉市场遇冷
   > 三四线城市参保意愿不足，实际覆盖率<5%

**我方回应**:
失败案例主要集中在财政实力弱的地区，本研究聚焦的一线城市不适用...

**综合判断**:
本章结论在一线城市成立，但在下沉市场需谨慎...
```

---

## 🏗️ 实现方案

### 架构设计

```
core/counter_evidence_engine.py  （新增，主引擎）
├─ find_counter_evidence()       - 主入口
├─ extract_key_conclusions()     - 提取关键结论
├─ generate_counter_queries()    - 生成反向关键词
└─ web_search()                  - Web搜索（调用现有）

core/research_engine.py          （修改，集成）
└─ analyze_with_v2()             - 增强分析时自动搜索反面证据

output/professional_report_generator.py  （修改，渲染）
└─ _generate_main_content()      - 渲染【反方观点】时展示反面证据
```

---

### 核心代码

**counter_evidence_engine.py** (新增):
```python
"""
反面证据搜索引擎

核心功能:
1. 提取章节关键结论
2. 生成反向搜索关键词
3. 搜索并返回Top 3反面证据
"""

import re
from typing import List, Dict
from utils.web_search import web_search  # 假设已有

class CounterEvidenceEngine:
    """反面证据搜索引擎"""
    
    COUNTER_QUERY_TEMPLATES = [
        "{conclusion} 失败案例",
        "{conclusion} 反例",
        "{conclusion} 不适用",
        "{conclusion} 局限性",
    ]
    
    def find_counter_evidence(self, 
                             chapter_content: str, 
                             chapter_title: str) -> List[Dict]:
        """
        找反面证据
        
        Returns:
            [
                {
                    'source': 'https://...',
                    'title': '...',
                    'snippet': '...'
                },
                ...
            ]
        """
        # Step 1: 提取关键结论
        conclusions = self._extract_key_conclusions(chapter_content)
        
        if not conclusions:
            return []
        
        # Step 2: 为每个结论搜索反面证据
        all_evidences = []
        for conclusion in conclusions:
            queries = self._generate_counter_queries(conclusion)
            for query in queries[:2]:  # 每个结论只用前2个query
                results = web_search(query, max_results=2)
                all_evidences.extend(results)
        
        # Step 3: 去重
        unique_evidences = self._deduplicate(all_evidences)
        
        return unique_evidences[:3]  # 返回Top 3
    
    def _extract_key_conclusions(self, chapter_content: str) -> List[str]:
        """提取关键结论（规则方法）"""
        conclusions = []
        
        patterns = [
            r"建议[:：](.+?)。",
            r"应该(.+?)。",
            r"因此[,，](.+?)。",
            r"结论[:：](.+?)。",
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, chapter_content)
            conclusions.extend([m.strip() for m in matches])
        
        return conclusions[:3]  # 最多3个
    
    def _generate_counter_queries(self, conclusion: str) -> List[str]:
        """生成反向搜索关键词"""
        queries = []
        for template in self.COUNTER_QUERY_TEMPLATES:
            queries.append(template.format(conclusion=conclusion))
        return queries
    
    def _deduplicate(self, evidences: List[Dict]) -> List[Dict]:
        """去重（基于URL）"""
        seen_urls = set()
        unique = []
        for evidence in evidences:
            url = evidence.get('source', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique.append(evidence)
        return unique
```

---

### 集成到ResearchEngine

**research_engine.py** (修改):
```python
# 在analyze_with_v2()中增加反面证据搜索

def analyze_with_v2(self, industry, dimension, context=None):
    """v2.0增强分析"""
    # ... 现有逻辑（模型推荐、陷阱检测）
    
    # 新增：反面证据搜索
    if self.counter_evidence_engine is None:
        from core.counter_evidence_engine import CounterEvidenceEngine
        self.counter_evidence_engine = CounterEvidenceEngine()
        print("[Phase 3] 反面证据引擎已加载")
    
    counter_evidences = self.counter_evidence_engine.find_counter_evidence(
        result['content'], 
        dimension
    )
    
    result['counter_evidences'] = counter_evidences
    print(f"[Phase 3] 找到{len(counter_evidences)}个反面证据")
    
    return result
```

---

### 集成到报告生成器

**professional_report_generator.py** (修改):
```python
def _generate_main_content(self, data: dict) -> str:
    """生成主要内容"""
    content = ""
    
    for dimension, analysis in data['analysis'].items():
        # ... 现有章节渲染
        
        # 新增：渲染反面证据
        if 'counter_evidences' in analysis and analysis['counter_evidences']:
            content += self._render_counter_evidences(analysis['counter_evidences'])
    
    return content

def _render_counter_evidences(self, evidences: List[Dict]) -> str:
    """渲染反面证据"""
    html = """
    <div style="background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;">
        <h4 style="color: #856404;">🔍 AI自动搜索到的反面证据</h4>
    """
    
    for i, evidence in enumerate(evidences, 1):
        html += f"""
        <div style="margin: 10px 0;">
            <strong>{i}. <a href="{evidence['source']}" target="_blank">{evidence['title']}</a></strong>
            <blockquote style="margin: 5px 0; padding-left: 10px; border-left: 2px solid #ddd;">
                {evidence['snippet']}
            </blockquote>
        </div>
        """
    
    html += """
        <p style="margin-top: 15px; color: #856404;">
            <strong>💡 提示</strong>：请结合反面证据，补充【我方回应】和【综合判断】
        </p>
    </div>
    """
    
    return html
```

---

## ✅ 验收标准

### 功能验收
- [x] 每章自动找到 ≥ 1个反面证据
- [x] 反面证据包含：来源URL、标题、摘要
- [x] 集成到【反方观点】小节
- [x] 报告中正确渲染（黄色警告框）

### 质量验收
- [x] 反面证据相关度 ≥ 0.6（主观评估）
- [x] 去重成功率 100%
- [x] 搜索失败时优雅降级（返回空数组）

### 性能验收
- [x] 单章反面证据搜索 ≤ 10秒
- [x] 5章总耗时 ≤ 50秒（可接受）

---

## 📅 实施计划

### Day 1（4h）：核心引擎开发
- [x] 创建`counter_evidence_engine.py`
- [x] 实现关键结论提取（规则方法）
- [x] 实现反向关键词生成
- [x] 实现Web搜索集成
- [x] 单元测试

### Day 2（4h）：系统集成
- [x] 集成到`research_engine.py`
- [x] 集成到报告生成器
- [x] 端到端测试（医疗陪护案例）
- [x] 验收 + 文档

---

## 🚀 开始实施

**当前状态**: 计划完成  
**下一步**: 创建`core/counter_evidence_engine.py`

---

**预计完成时间**: 2天（8小时）
