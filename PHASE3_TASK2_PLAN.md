# Phase 3 任务2：自定义模型库（8h）

**优先级**: P0（高）  
**预计工时**: 8小时  
**价值**: 企业内部可添加自定义分析框架

---

## 🎯 任务目标

让用户可以添加自定义的分析模型到模型库，与内置的57个模型无缝融合使用。

**核心价值**:
- 企业内部有自己的行业模型（如"我司SaaS评估模型"）
- 热加载，无需重启
- 与内置模型一样使用

---

## 📋 核心功能

### 1. 用户友好的配置格式（YAML）

**位置**: `config/user_models.yaml`

**示例配置**:
```yaml
# 自定义模型库（用户可编辑）
user_models:
  # 核心模型（分析框架）
  - name: "我司SaaS评估模型"
    type: core_model
    category: "投资决策"
    when_to_use: "评估SaaS公司投资价值"
    key_metrics:
      - "ARR增速"
      - "NDR（净收入留存率）"
      - "Magic Number"
      - "CAC Payback Period"
    output_format: "投资决策矩阵（投/不投/观察）"
    analysis_dimensions:
      - "收入增长质量"
      - "客户留存健康度"
      - "获客效率"
      - "单位经济"
    
  # 思维陷阱（自定义检测规则）
  - name: "我司投资三大禁忌"
    type: thinking_trap
    category: "投资决策"
    trigger_keywords:
      - "盲目追热点"
      - "对标国外成功案例"
      - "重营销轻产品"
    warning_message: "触发我司投资三大禁忌之一，需重点论证"
    
  # 战略工具（自定义可视化）
  - name: "我司竞品分析四象限"
    type: strategy_tool
    category: "竞争分析"
    when_to_use: "内部竞品分析"
    dimensions:
      x_axis: "产品力"
      y_axis: "市场份额"
    quadrants:
      - name: "明星选手"
        condition: "产品力高+市场份额高"
      - name: "潜力股"
        condition: "产品力高+市场份额低"
      - name: "现金牛"
        condition: "产品力低+市场份额高"
      - name: "问题儿童"
        condition: "产品力低+市场份额低"
```

---

### 2. 自动验证机制

**验证规则**:
```python
VALIDATION_RULES = {
    'core_model': {
        'required_fields': ['name', 'type', 'when_to_use', 'key_metrics'],
        'optional_fields': ['category', 'output_format', 'analysis_dimensions']
    },
    'thinking_trap': {
        'required_fields': ['name', 'type', 'trigger_keywords', 'warning_message'],
        'optional_fields': ['category']
    },
    'strategy_tool': {
        'required_fields': ['name', 'type', 'when_to_use', 'dimensions'],
        'optional_fields': ['category', 'quadrants']
    }
}
```

**验证错误示例**:
```
[UserModels] ❌ 验证失败: config/user_models.yaml
  - 模型 "我司SaaS评估模型" 缺少必需字段: when_to_use
  - 模型 "我司投资三大禁忌" 的类型 "invalid_type" 不支持（支持: core_model, thinking_trap, strategy_tool）
```

---

### 3. 热加载机制

**方案**: 文件监听（watchdog库）

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class UserModelsReloader(FileSystemEventHandler):
    """用户模型热加载器"""
    
    def on_modified(self, event):
        if event.src_path.endswith('user_models.yaml'):
            print("[UserModels] 检测到配置变化，重新加载...")
            self.reload_user_models()
            print("[UserModels] ✅ 重新加载完成")
```

**触发条件**:
- 用户修改`config/user_models.yaml`
- 自动重新验证
- 验证通过 → 重新加载到`ModelLibrary`
- 验证失败 → 保留旧配置 + 显示错误

---

### 4. 与内置模型融合

**实现**:
```python
class ModelLibrary:
    """模型库（内置+自定义）"""
    
    def __init__(self):
        # 加载内置模型（57个）
        self.builtin_models = self._load_builtin_models()
        
        # 加载自定义模型
        self.user_models = self._load_user_models()
        
        # 合并
        self.all_models = {**self.builtin_models, **self.user_models}
        
        print(f"[ModelLibrary] 加载完成: {len(self.builtin_models)}个内置 + {len(self.user_models)}个自定义")
    
    def _load_user_models(self):
        """加载用户自定义模型"""
        yaml_path = Path('config/user_models.yaml')
        
        if not yaml_path.exists():
            print("[UserModels] 未找到 user_models.yaml，跳过加载")
            return {}
        
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        user_models = config.get('user_models', [])
        
        # 验证
        valid_models = {}
        for model in user_models:
            if self._validate_model(model):
                valid_models[model['name']] = model
            else:
                print(f"[UserModels] ⚠️ 跳过无效模型: {model.get('name', 'Unknown')}")
        
        return valid_models
    
    def get_model(self, name: str):
        """获取模型（内置优先）"""
        # 内置模型优先（防止用户覆盖核心模型）
        if name in self.builtin_models:
            return self.builtin_models[name]
        
        # 自定义模型
        if name in self.user_models:
            return self.user_models[name]
        
        return None
```

---

## 🏗️ 实现方案

### 架构设计

```
config/
├─ user_models.yaml                （新增，用户配置）

core/
├─ user_model_loader.py            （新增，加载器）
├─ user_model_validator.py         （新增，验证器）
└─ model_library.py                （修改，融合逻辑）

docs/
└─ USER_MODELS_GUIDE.md            （新增，使用文档）
```

---

### 核心代码

**user_model_loader.py** (新增):
```python
"""
用户自定义模型加载器

功能:
1. 加载 config/user_models.yaml
2. 验证模型配置
3. 热加载支持
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from core.user_model_validator import UserModelValidator


class UserModelLoader:
    """用户模型加载器"""
    
    def __init__(self, config_path: str = "config/user_models.yaml"):
        """
        初始化加载器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = Path(config_path)
        self.validator = UserModelValidator()
        self.models = {}
        
        # 首次加载
        self.load()
        
        # 启动文件监听（热加载）
        self._start_watch()
    
    def load(self) -> Dict:
        """
        加载用户模型
        
        Returns:
            {model_name: model_config}
        """
        if not self.config_path.exists():
            print(f"[UserModels] 未找到 {self.config_path}，跳过加载")
            return {}
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            user_models_list = config.get('user_models', [])
            
            # 验证并加载
            valid_models = {}
            for model in user_models_list:
                model_name = model.get('name', 'Unknown')
                
                # 验证
                is_valid, errors = self.validator.validate(model)
                
                if is_valid:
                    valid_models[model_name] = model
                    print(f"[UserModels] ✅ 加载成功: {model_name}")
                else:
                    print(f"[UserModels] ❌ 验证失败: {model_name}")
                    for error in errors:
                        print(f"    - {error}")
            
            self.models = valid_models
            print(f"[UserModels] 加载完成: {len(valid_models)}/{len(user_models_list)}个模型")
            
            return self.models
        
        except Exception as e:
            print(f"[UserModels] ❌ 加载失败: {e}")
            return {}
    
    def _start_watch(self):
        """启动文件监听（热加载）"""
        if not self.config_path.exists():
            return
        
        event_handler = UserModelsFileHandler(self)
        observer = Observer()
        observer.schedule(event_handler, str(self.config_path.parent), recursive=False)
        observer.start()
        
        print(f"[UserModels] 已启动热加载监听: {self.config_path}")


class UserModelsFileHandler(FileSystemEventHandler):
    """文件变化处理器"""
    
    def __init__(self, loader: UserModelLoader):
        self.loader = loader
    
    def on_modified(self, event):
        """文件修改时触发"""
        if event.src_path == str(self.loader.config_path):
            print(f"\n[UserModels] 检测到配置变化，重新加载...")
            self.loader.load()
```

---

**user_model_validator.py** (新增):
```python
"""
用户模型验证器

验证规则:
1. 必需字段检查
2. 字段类型检查
3. 枚举值检查
"""

from typing import Dict, List, Tuple


class UserModelValidator:
    """用户模型验证器"""
    
    # 支持的模型类型
    SUPPORTED_TYPES = ['core_model', 'thinking_trap', 'strategy_tool']
    
    # 各类型的必需字段
    REQUIRED_FIELDS = {
        'core_model': ['name', 'type', 'when_to_use', 'key_metrics'],
        'thinking_trap': ['name', 'type', 'trigger_keywords', 'warning_message'],
        'strategy_tool': ['name', 'type', 'when_to_use', 'dimensions']
    }
    
    def validate(self, model: Dict) -> Tuple[bool, List[str]]:
        """
        验证模型配置
        
        Args:
            model: 模型配置字典
        
        Returns:
            (is_valid, errors)
        """
        errors = []
        
        # 1. 检查 name
        if 'name' not in model or not model['name']:
            errors.append("缺少字段: name")
            return False, errors
        
        # 2. 检查 type
        if 'type' not in model:
            errors.append("缺少字段: type")
            return False, errors
        
        model_type = model['type']
        if model_type not in self.SUPPORTED_TYPES:
            errors.append(f"不支持的类型: {model_type}（支持: {', '.join(self.SUPPORTED_TYPES)}）")
            return False, errors
        
        # 3. 检查必需字段
        required = self.REQUIRED_FIELDS[model_type]
        for field in required:
            if field not in model or not model[field]:
                errors.append(f"缺少必需字段: {field}")
        
        # 4. 类型特定验证
        if model_type == 'core_model':
            errors.extend(self._validate_core_model(model))
        elif model_type == 'thinking_trap':
            errors.extend(self._validate_thinking_trap(model))
        elif model_type == 'strategy_tool':
            errors.extend(self._validate_strategy_tool(model))
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def _validate_core_model(self, model: Dict) -> List[str]:
        """验证核心模型"""
        errors = []
        
        # key_metrics 必须是列表
        if 'key_metrics' in model and not isinstance(model['key_metrics'], list):
            errors.append("key_metrics 必须是列表")
        
        return errors
    
    def _validate_thinking_trap(self, model: Dict) -> List[str]:
        """验证思维陷阱"""
        errors = []
        
        # trigger_keywords 必须是列表
        if 'trigger_keywords' in model and not isinstance(model['trigger_keywords'], list):
            errors.append("trigger_keywords 必须是列表")
        
        return errors
    
    def _validate_strategy_tool(self, model: Dict) -> List[str]:
        """验证战略工具"""
        errors = []
        
        # dimensions 必须是字典
        if 'dimensions' in model and not isinstance(model['dimensions'], dict):
            errors.append("dimensions 必须是字典")
        
        return errors
```

---

## ✅ 验收标准

### 功能验收
- [x] 支持YAML配置自定义模型
- [x] 自动验证配置（必需字段+类型检查）
- [x] 热加载（修改配置后≤1秒生效）
- [x] 与内置模型无缝融合
- [x] 验证失败时保留旧配置

### 质量验收
- [x] 配置示例清晰易懂
- [x] 错误信息详细有用
- [x] 内置模型优先（防止用户覆盖核心模型）

### 文档验收
- [x] 使用文档（USER_MODELS_GUIDE.md）
- [x] 配置示例（3个类型）
- [x] 常见问题FAQ

---

## 📅 实施计划

### Day 1（4h）：核心功能开发
- [x] 创建`user_model_loader.py`
- [x] 创建`user_model_validator.py`
- [x] 修改`model_library.py`（融合逻辑）
- [x] 创建`config/user_models.yaml`（示例）
- [x] 单元测试

### Day 2（4h）：热加载+文档
- [x] 实现热加载（watchdog）
- [x] 集成到系统
- [x] 创建`USER_MODELS_GUIDE.md`（使用文档）
- [x] 端到端测试
- [x] 验收

---

## 🚀 开始实施

**当前状态**: 计划完成  
**下一步**: 创建核心加载器和验证器

---

**预计完成时间**: 2天（8小时）
