# Phase 3 修订计划：务实的研究增强

**启动时间**: TBD  
**预计工时**: 30-40h（从110h大幅缩减）  
**原则**: 只做有明确价值、不过度设计的功能

---

## 📋 用户反馈分析

### ❌ 砍掉的任务（理由）

| 任务 | 原计划工时 | 砍掉理由 |
|------|-----------|---------|
| **P1.1 多行业并行生成** | 20h | 报告需要人工判断把关，并行生成没有价值 |
| **P1.2 实时协作** | 15h | 现阶段没必要，单人使用场景足够 |
| **P2.4 插件系统** | 15h → 5h | 有意义但不要过度设计，简化实现 |
| **P3.5 RESTful API** | 20h → 5h | 0成本实现：命令行包装即可 |
| **P4.6 自动假设生成** | 5h → 2h | 不要过度设计，简单实现即可 |
| **P5.8 Web UI** | 15h → 0h | 实现成本高，效果不确定，暂缓 |

**总砍掉**: 70h → 保留 30-40h

---

## ✅ Phase 3 核心任务（30-40h）

### **任务1: 自定义模型库（8h）**

**目标**: 用户可添加私有分析模型

**核心价值**: 
- 企业内部有自己的行业模型（如"我司SaaS评估模型"）
- 热加载，无需重启

**实现方案**（简单实用）:
```yaml
# config/user_models.yaml
user_models:
  - name: "我司SaaS评估模型"
    type: core_model
    when_to_use: "评估SaaS公司投资价值"
    key_metrics: ["ARR增速", "NDR", "Magic Number", "Payback Period"]
    output_format: "投资决策矩阵（投/不投/观察）"
    
  - name: "我司竞品分析框架"
    type: core_model
    when_to_use: "内部竞品分析"
    dimensions: ["产品力", "市场份额", "技术壁垒", "团队能力"]
```

**技术实现**（不过度设计）:
- 读取`config/user_models.yaml`
- 合并到`ModelLibrary`（57+N个模型）
- 文件变化时自动重载（watchdog库）

**验收标准**:
- [x] 支持YAML定义自定义模型
- [x] 热加载 ≤ 200ms
- [x] 与内置模型无缝集成

**预计工时**: 8h

---

### **任务2: 简化插件系统（5h）**

**目标**: 支持第三方数据源/导出格式

**核心价值**:
- 接入Wind/Bloomberg金融数据
- 导出为Word/PPT格式

**实现方案**（最小化设计）:
```python
# plugins/data_sources/wind_plugin.py
class WindDataSource:
    def fetch_industry_data(self, industry: str) -> dict:
        """从Wind获取行业数据"""
        pass

# plugins/exporters/word_exporter.py
class WordExporter:
    def export(self, report_html: str) -> bytes:
        """导出为Word文档"""
        # 使用python-docx库
        pass
```

**技术实现**（不做插件市场/沙箱）:
- 简单的接口类（Protocol）
- 插件放在`plugins/`目录
- 自动发现并加载（importlib）

**验收标准**:
- [x] 3个官方插件（Wind数据源、Word导出、Markdown导出）
- [x] 清晰的接口文档
- [x] 插件失败不影响核心功能

**预计工时**: 5h

---

### **任务3: 0成本API（5h）**

**目标**: 命令行包装为简单HTTP接口

**核心价值**:
- 远程调用（如Jenkins集成）
- 不做复杂的异步队列/WebSocket

**实现方案**（最简单）:
```python
# api/simple_server.py
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/api/research', methods=['POST'])
def create_research():
    data = request.json
    industry = data['industry']
    
    # 直接调用命令行
    result = subprocess.run(
        ['python', 'irs.py', industry, '--type', data.get('type', '行业分析')],
        capture_output=True
    )
    
    return jsonify({
        'status': 'completed',
        'report_path': '...'
    })

if __name__ == '__main__':
    app.run(port=5000)
```

**技术实现**:
- Flask（最轻量级）
- 同步调用（不做异步队列）
- 基本认证（API Key）

**验收标准**:
- [x] 1个端点：`POST /api/research`
- [x] 返回报告路径
- [x] API Key认证

**预计工时**: 5h

---

### **任务4: 轻量假设生成（2h）**

**目标**: AI快速提出候选假设

**核心价值**:
- 帮用户快速启动研究
- 不要复杂的假设评分/排序

**实现方案**（简单即可）:
```python
def generate_hypothesis_candidates(industry: str, research_type: str) -> List[str]:
    """生成3个候选假设"""
    prompt = f"""
    行业: {industry}
    研究类型: {research_type}
    
    请提出3个最关键的研究假设（一句话）:
    1. 
    2.
    3.
    """
    # 调用LLM，返回3个假设
    return parse_llm_response(call_llm(prompt))
```

**用户体验**:
```bash
$ python irs.py "医疗陪护"

AI建议的研究假设（选择1-3个，或输入自定义假设）:
  1. 长护险政策是主要驱动力
  2. 人力成本是最大壁垒
  3. 技术赋能可降低成本50%
  
请选择（回车跳过）: 1,2
```

**验收标准**:
- [x] 生成3个候选假设
- [x] 用户可选择或跳过
- [x] 不影响正常流程

**预计工时**: 2h

---

### **任务5: 反驳强化（8h）**

**目标**: 自动找反面证据

**核心价值**:
- 强制辩证思考
- 提升报告质量

**实现方案**:
```python
def find_counter_evidence(chapter_content: str, chapter_title: str) -> List[str]:
    """找反面证据"""
    # 提取关键结论
    key_conclusions = extract_conclusions(chapter_content)
    
    # 为每个结论搜索反面证据
    counter_evidences = []
    for conclusion in key_conclusions:
        # 构造反向搜索关键词
        query = f"{conclusion} 失败案例 OR 不适用 OR 反例"
        results = web_search(query)
        counter_evidences.extend(results[:2])  # 取前2个
    
    return counter_evidences
```

**用户体验**（报告中展示）:
```markdown
【反方观点】本章结论的最强反驳

AI自动搜索到的反面证据:
1. [来源A] 某SaaS公司采用PLG模式失败案例
2. [来源B] PLG不适用于高客单价B2B市场

我方回应: ...
综合判断: 本章结论在X条件下成立，Y条件下需修正
```

**验收标准**:
- [x] 每章自动找到 ≥ 1个反面证据
- [x] 标注来源URL
- [x] 集成到【反方观点】小节

**预计工时**: 8h

---

### **任务6: 报告格式增强（5h）**

**目标**: 支持多种导出格式

**核心价值**:
- Word文档（给领导看）
- Markdown（Git版本控制）

**实现方案**:
```python
# 使用python-docx
def export_to_word(html_report: str, output_path: str):
    """HTML → Word"""
    # 解析HTML
    soup = BeautifulSoup(html_report, 'html.parser')
    doc = Document()
    
    # 转换标题/段落/表格
    for element in soup.find_all(['h1', 'h2', 'p', 'table']):
        # ... 转换逻辑
    
    doc.save(output_path)

# 使用markdownify
def export_to_markdown(html_report: str) -> str:
    """HTML → Markdown"""
    return markdownify.markdownify(html_report)
```

**验收标准**:
- [x] 支持导出Word（.docx）
- [x] 支持导出Markdown（.md）
- [x] 保留基本格式（标题/段落/表格）

**预计工时**: 5h

---

### **任务7: 性能优化实施（5h）**

**目标**: 实施Phase 2性能分析建议

**核心价值**:
- 洞察生成剪枝（O(n²) → 优化）
- 延迟加载优化

**实现方案**:
```python
# config/dimension_relationships.yaml
relationships:
  政策环境:
    - 市场规模  # 政策影响市场
    - 商业模式  # 政策影响模式
  市场规模:
    - 商业模式  # 市场决定模式
  竞争格局:
    - 进入壁垒  # 竞争影响壁垒

# core/insight_engine.py
def generate_insights_optimized(chapters: List[Dict]) -> List[Insight]:
    """优化后的洞察生成"""
    insights = []
    
    # 只比较有关联的维度对（剪枝50%）
    for ch1 in chapters:
        related_dims = DIMENSION_RELATIONSHIPS.get(ch1.dimension, [])
        for ch2 in chapters:
            if ch2.dimension in related_dims:
                # 生成洞察
                ...
    
    return insights
```

**预期提升**:
- 洞察生成时间：120ms → 60ms（-50%）

**验收标准**:
- [x] 洞察生成时间减少 ≥ 30%
- [x] 不影响洞察质量

**预计工时**: 5h

---

## 📊 Phase 3修订版对比

| 维度 | 原计划 | 修订后 | 变化 |
|------|--------|--------|------|
| **总工时** | 110h | 30-40h | **-64%** |
| **任务数** | 8个 | 7个 | -1个 |
| **并行生成** | 20h | ❌砍掉 | 无价值 |
| **实时协作** | 15h | ❌砍掉 | 无需求 |
| **插件系统** | 15h | 5h | 简化 |
| **API服务** | 20h | 5h | 0成本 |
| **自动假设** | 5h | 2h | 简化 |
| **Web UI** | 15h | ❌砍掉 | 成本高 |
| **反驳强化** | 5h | 8h | **保留+增强** |
| **格式导出** | 0h | 5h | **新增** |
| **性能优化** | 0h | 5h | **新增** |

---

## 🎯 修订后的核心价值

### Phase 2实现的（已完成）
- ✅ 57个模型库
- ✅ 12类思维陷阱检测
- ✅ 5种洞察自动生成
- ✅ 9种战略可视化

### Phase 3要实现的（务实）
- ✅ **自定义模型库**：企业内部模型
- ✅ **反驳强化**：自动找反面证据
- ✅ **格式增强**：Word/Markdown导出
- ✅ **轻量API**：命令行包装
- ✅ **简化插件**：数据源/导出扩展
- ✅ **性能优化**：洞察生成-50%
- ✅ **快速启动**：假设候选生成

---

## 📅 Phase 3修订时间线

```
Week 1（8h）: 任务1 自定义模型库
Week 2（13h）: 任务2 简化插件（5h）+ 任务5 反驳强化（8h）
Week 3（10h）: 任务3 轻量API（5h）+ 任务6 格式增强（5h）
Week 4（7h）: 任务4 假设生成（2h）+ 任务7 性能优化（5h）
验收（2h）

总计: 40h（约5个工作日）
```

---

## 💡 实施建议

### 立即可做（ROI最高）
1. **任务5: 反驳强化**（8h）- 提升报告质量，用户最关心
2. **任务1: 自定义模型库**（8h）- 企业内部需求强烈
3. **任务6: 格式增强**（5h）- Word导出是刚需

### 可选（按需）
4. **任务7: 性能优化**（5h）- 当前性能已够用（42s）
5. **任务2: 简化插件**（5h）- 有数据源需求时再做
6. **任务3: 轻量API**（5h）- 有远程调用需求时再做
7. **任务4: 假设生成**（2h）- 锦上添花

---

## 🎉 总结

**Phase 3修订版核心原则**: 
- ❌ 去掉不实用的（并行生成、实时协作、Web UI）
- ✅ 保留真正有价值的（自定义模型、反驳强化、格式导出）
- 🎯 不过度设计（插件系统简化、API 0成本、假设生成轻量）

**投入产出**:
- 工时: 110h → 40h（**-64%**）
- 价值: 保留核心功能，砍掉鸡肋

---

**你觉得这个修订计划如何？** 🤔

可以继续调整优先级或删减任务！
