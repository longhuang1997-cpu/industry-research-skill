"""
用户模型验证器 - Phase 3 任务2

功能:
1. 验证用户自定义模型配置
2. 必需字段检查
3. 字段类型检查
4. 枚举值检查

作者: Claude Opus 5
日期: 2026-09-17
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
        if 'key_metrics' in model:
            if not isinstance(model['key_metrics'], list):
                errors.append("key_metrics 必须是列表")
            elif len(model['key_metrics']) == 0:
                errors.append("key_metrics 不能为空")

        # analysis_dimensions 如果存在，必须是列表
        if 'analysis_dimensions' in model:
            if not isinstance(model['analysis_dimensions'], list):
                errors.append("analysis_dimensions 必须是列表")

        return errors

    def _validate_thinking_trap(self, model: Dict) -> List[str]:
        """验证思维陷阱"""
        errors = []

        # trigger_keywords 必须是列表
        if 'trigger_keywords' in model:
            if not isinstance(model['trigger_keywords'], list):
                errors.append("trigger_keywords 必须是列表")
            elif len(model['trigger_keywords']) == 0:
                errors.append("trigger_keywords 不能为空")

        return errors

    def _validate_strategy_tool(self, model: Dict) -> List[str]:
        """验证战略工具"""
        errors = []

        # dimensions 必须是字典
        if 'dimensions' in model:
            if not isinstance(model['dimensions'], dict):
                errors.append("dimensions 必须是字典")
            else:
                # 检查是否有 x_axis 和 y_axis
                if 'x_axis' not in model['dimensions']:
                    errors.append("dimensions 缺少 x_axis")
                if 'y_axis' not in model['dimensions']:
                    errors.append("dimensions 缺少 y_axis")

        # quadrants 如果存在，必须是列表
        if 'quadrants' in model:
            if not isinstance(model['quadrants'], list):
                errors.append("quadrants 必须是列表")
            else:
                # 检查每个象限是否有 name 和 condition
                for i, quad in enumerate(model['quadrants'], 1):
                    if not isinstance(quad, dict):
                        errors.append(f"quadrants[{i}] 必须是字典")
                        continue
                    if 'name' not in quad:
                        errors.append(f"quadrants[{i}] 缺少 name")
                    if 'condition' not in quad:
                        errors.append(f"quadrants[{i}] 缺少 condition")

        return errors


# ==================== 测试代码 ====================

if __name__ == '__main__':
    print("=" * 60)
    print("用户模型验证器 - 单元测试")
    print("=" * 60)

    validator = UserModelValidator()

    # 测试1: 有效的核心模型
    test_core_model = {
        'name': '测试SaaS模型',
        'type': 'core_model',
        'when_to_use': '评估SaaS公司',
        'key_metrics': ['ARR', 'NDR', 'Magic Number']
    }

    is_valid, errors = validator.validate(test_core_model)
    print(f"\n测试1 - 有效核心模型: {'✅ 通过' if is_valid else '❌ 失败'}")
    if errors:
        for error in errors:
            print(f"  - {error}")

    # 测试2: 缺少必需字段
    test_invalid_model = {
        'name': '无效模型',
        'type': 'core_model'
        # 缺少 when_to_use 和 key_metrics
    }

    is_valid, errors = validator.validate(test_invalid_model)
    print(f"\n测试2 - 缺少必需字段: {'✅ 检测到错误' if not is_valid else '❌ 未检测到'}")
    if errors:
        for error in errors:
            print(f"  - {error}")

    # 测试3: 有效的思维陷阱
    test_thinking_trap = {
        'name': '投资禁忌',
        'type': 'thinking_trap',
        'trigger_keywords': ['对标Uber', '烧钱'],
        'warning_message': '触发投资禁忌'
    }

    is_valid, errors = validator.validate(test_thinking_trap)
    print(f"\n测试3 - 有效思维陷阱: {'✅ 通过' if is_valid else '❌ 失败'}")
    if errors:
        for error in errors:
            print(f"  - {error}")

    # 测试4: 有效的战略工具
    test_strategy_tool = {
        'name': '竞品四象限',
        'type': 'strategy_tool',
        'when_to_use': '竞品分析',
        'dimensions': {
            'x_axis': '产品力',
            'y_axis': '市场份额'
        }
    }

    is_valid, errors = validator.validate(test_strategy_tool)
    print(f"\n测试4 - 有效战略工具: {'✅ 通过' if is_valid else '❌ 失败'}")
    if errors:
        for error in errors:
            print(f"  - {error}")

    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)
