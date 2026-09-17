# 自定义模型库使用指南

**版本**: v1.0  
**更新日期**: 2026-09-17  
**适用人群**: 企业内部用户、高级用户

---

## 📖 概述

Industry Research Skill允许企业内部添加自定义的分析模型，与内置的57个模型无缝融合使用。

**核心价值**:
- ✅ 沉淀企业内部方法论（如"我司SaaS评估模型"）
- ✅ 自定义思维陷阱检测（如"投资三大禁忌"）
- ✅ 定制战略工具/可视化（如"竞品四象限"）
- ✅ 热加载，无需重启（修改后≤1秒生效）

---

## 🚀 快速开始

### 步骤1: 编辑配置文件

打开 `config/user_models.yaml`，添加你的模型：

```yaml
user_models:
  - name: "我司行业评估模型"
    type: core_model
    when_to_use: "评估新进入行业时使用"
    key_metrics:
      - "市场规模"
      - "增长率"
      - "竞争格局"
```

### 步骤2: 保存文件

保存后，系统会自动验证并加载（热加载，≤1秒）。

### 步骤3: 使用模型

在研究分析中，自定义模型会自动被推荐使用（与内置模型一样）。

---

## 📝 配置格式

### 支持的模型类型

| 类型 | 说明 | 适用场景 |
|------|------|---------|
| `core_model` | 核心分析模型 | 行业评估、公司分析、投资决策 |
| `thinking_trap` | 思维陷阱检测 | 自动检测逻辑谬误、投资禁忌 |
| `strategy_tool` | 战略工具/可视化 | 竞品分析、战略规划 |

---

### 类型1: 核心分析模型（core_model）

**必需字段**:
- `name`: 模型名称（唯一标识）
- `type`: 固定为 `core_model`
- `when_to_use`: 何时使用（一句话说明）
- `key_metrics`: 关键指标（列表）

**可选字段**:
- `category`: 类别（如"投资决策"、"行业分析"）
- `output_format`: 输出格式
- `analysis_dimensions`: 分析维度（列表）
- `use_cases`: 使用场景（列表）

**示例**:
```yaml
- name: "我司SaaS评估模型"
  type: core_model
  category: "投资决策"
  when_to_use: "评估SaaS公司投资价值"
  
  key_metrics:
    - "ARR增速"
    - "NDR（净收入留存率）"
    - "Magic Number"
    - "CAC Payback Period"
    - "Rule of 40"
  
  output_format: "投资决策矩阵（投/不投/观察）"
  
  analysis_dimensions:
    - "收入增长质量"
    - "客户留存健康度"
    - "获客效率"
    - "单位经济"
  
  use_cases:
    - "尽调阶段快速判断"
    - "投后管理定期复盘"
```

---

### 类型2: 思维陷阱检测（thinking_trap）

**必需字段**:
- `name`: 陷阱名称
- `type`: 固定为 `thinking_trap`
- `trigger_keywords`: 触发关键词（列表）
- `warning_message`: 警告信息

**可选字段**:
- `category`: 类别
- `counter_path`: 反驳路径（如何化解）

**示例**:
```yaml
- name: "我司投资三大禁忌"
  type: thinking_trap
  category: "投资决策"
  
  trigger_keywords:
    - "对标Uber"
    - "美国已验证"
    - "重营销轻产品"
    - "盲目追热点"
  
  warning_message: |
    ⚠️ 触发我司投资三大禁忌之一：
    1. 盲目对标国外（中美差异巨大）
    2. 重营销轻产品（违背长期价值）
    3. 盲目追热点（缺乏护城河）
    
    需重点论证中国市场差异、产品力、护城河。
  
  counter_path: |
    补充：
    1. 中美市场对比分析
    2. 产品力验证（NPS数据）
    3. 护城河分析
```

---

### 类型3: 战略工具/可视化（strategy_tool）

**必需字段**:
- `name`: 工具名称
- `type`: 固定为 `strategy_tool`
- `when_to_use`: 何时使用
- `dimensions`: 维度定义（字典，必须包含`x_axis`和`y_axis`）

**可选字段**:
- `category`: 类别
- `quadrants`: 四象限定义（列表）
- `data_sources`: 数据来源
- `output_format`: 输出格式

**示例**:
```yaml
- name: "我司竞品分析四象限"
  type: strategy_tool
  category: "竞争分析"
  when_to_use: "内部竞品分析"
  
  dimensions:
    x_axis: "产品力"
    y_axis: "市场份额"
  
  quadrants:
    - name: "明星选手"
      position: "右上"
      condition: "产品力高 + 市场份额高"
      strategy: "重点关注"
    
    - name: "潜力股"
      position: "右下"
      condition: "产品力高 + 市场份额低"
      strategy: "长期观察"
  
  data_sources:
    - "艾瑞/易观报告"
    - "客户访谈"
  
  output_format: "四象限散点图 + 战略建议"
```

---

## ✅ 验证规则

系统会自动验证配置，常见错误：

### 错误1: 缺少必需字段
```
❌ 模型 "我司SaaS模型" 缺少必需字段: when_to_use
```

**解决**: 添加缺失的字段。

---

### 错误2: 类型不支持
```
❌ 不支持的类型: my_custom_type（支持: core_model, thinking_trap, strategy_tool）
```

**解决**: 使用支持的类型之一。

---

### 错误3: 字段类型错误
```
❌ key_metrics 必须是列表
```

**解决**: 检查字段类型，例如：
```yaml
# ❌ 错误
key_metrics: "ARR, NDR"

# ✅ 正确
key_metrics:
  - "ARR"
  - "NDR"
```

---

## 🔥 热加载

**自动触发**:
- 修改 `config/user_models.yaml`
- 保存文件
- 系统自动检测变化
- 重新验证
- 验证通过 → 重新加载（≤1秒）
- 验证失败 → 保留旧配置 + 显示错误

**控制台输出示例**:
```
[UserModels] 🔄 检测到配置变化，重新加载...
[UserModels] ✅ 我司SaaS评估模型
[UserModels] ✅ 我司投资三大禁忌
[UserModels] 加载完成: 2/2个模型有效
[UserModels] ➕ 新增 1 个模型
```

---

## 🎯 最佳实践

### 1. 命名规范
- ✅ 使用清晰的名称：`"我司SaaS评估模型"`
- ❌ 避免模糊命名：`"模型1"`、`"test"`

### 2. 文档化
- 添加详细的 `when_to_use`
- 列出所有 `key_metrics`
- 说明 `output_format`

### 3. 测试验证
1. 添加新模型
2. 保存文件
3. 检查控制台输出（是否有错误）
4. 运行一次分析测试

### 4. 版本控制
- 将 `config/user_models.yaml` 纳入Git
- 记录每次修改的原因
- 团队共享配置

### 5. 安全
- 不要在配置中存储敏感信息（API密钥、密码）
- 定期审查自定义模型

---

## ❓ 常见问题

### Q1: 自定义模型会覆盖内置模型吗？
**A**: 不会。内置模型优先级更高，自定义模型只是补充。

---

### Q2: 热加载需要重启系统吗？
**A**: 不需要。修改配置文件后自动生效（≤1秒）。

---

### Q3: 如何禁用某个自定义模型？
**A**: 两种方法：
1. 从配置文件中删除
2. 在模型前加 `#` 注释掉

---

### Q4: 支持多少个自定义模型？
**A**: 理论上无限制，但建议≤20个（保持简洁）。

---

### Q5: 自定义模型会影响性能吗？
**A**: 影响极小（<100ms），延迟加载设计。

---

### Q6: 如何分享自定义模型？
**A**: 复制 `config/user_models.yaml` 到其他项目即可。

---

### Q7: 验证失败怎么办？
**A**: 
1. 查看控制台错误信息
2. 对照本文档的配置格式
3. 修正后保存（自动重新加载）

---

## 📚 进阶用法

### 团队协作配置

**方案1: 共享配置文件**
```bash
# 团队共享同一个 config/user_models.yaml
git add config/user_models.yaml
git commit -m "新增我司SaaS评估模型"
git push
```

**方案2: 分层配置（TODO）**
```yaml
# 基础配置（团队共享）
base_models:
  - ...

# 个人配置（个人扩展）
personal_models:
  - ...
```

---

### 条件触发（思维陷阱）

```yaml
- name: "我司投资门槛"
  type: thinking_trap
  trigger_keywords:
    - "市场规模<10亿"
    - "增长率<30%"
  warning_message: |
    ⚠️ 未达到我司投资门槛：
    - 市场规模≥10亿
    - 增长率≥30%
```

---

## 🛠️ 故障排查

### 问题1: 配置文件不存在
```
[UserModels] ℹ️  未找到 user_models.yaml，跳过加载
```

**解决**: 创建 `config/user_models.yaml` 文件。

---

### 问题2: YAML格式错误
```
[UserModels] ❌ YAML解析失败: ...
```

**解决**: 
1. 使用YAML验证工具（https://www.yamllint.com/）
2. 检查缩进（必须用空格，不能用Tab）
3. 检查引号、冒号

---

### 问题3: 热加载不工作
```
[UserModels] ⚠️  未安装 watchdog，热加载功能不可用
```

**解决**: 
```bash
pip install watchdog
```

---

## 📞 技术支持

**问题反馈**: 在项目仓库提Issue  
**功能建议**: 欢迎提Pull Request

---

## 📜 附录

### 完整配置示例

参见: `config/user_models.yaml`

### 内置模型列表

参见: Phase 2文档 - 57个内置模型

---

**最后更新**: 2026-09-17  
**版本**: v1.0  
**作者**: Industry Research Skill Team
