"""
框架选择器：根据行业特征自动选择分析框架

基于4象限分类法:
- 象限1: 政府主导+高监管
- 象限2: 政策驱动+混合支付（如医疗陪护）
- 象限3: B端支付+轻监管
- 象限4: 市场主导+低监管
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional


class FrameworkSelector:
    """
    框架选择器（增强版）

    根据行业特征自动选择最适合的分析框架组合

    新功能:
    - 自动集成用户自定义框架
    - 支持按行业推荐自定义框架
    - 框架优先级：用户自定义 > 内置框架
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        初始化框架选择器

        Args:
            config_path: 决策树配置文件路径（可选）
        """
        if config_path is None:
            config_path = Path(__file__).parent / 'framework_decision_tree.yaml'

        with open(config_path, 'r', encoding='utf-8') as f:
            self.tree = yaml.safe_load(f)

        # 加载用户自定义框架
        from .custom_framework_builder import CustomFrameworkBuilder
        self.custom_builder = CustomFrameworkBuilder()
        self.custom_frameworks = self.custom_builder.list_custom_frameworks()

    def classify_industry(self,
                         industry_name: str,
                         user_answers: Optional[Dict] = None) -> str:
        """
        将行业分类到4个象限之一

        Args:
            industry_name: 行业名称（如"医疗陪护"）
            user_answers: 用户填写的行业特征（可选）

        Returns:
            quadrant: 象限标识 (quadrant_1/2/3/4)
        """
        # Step 1: 检查是否为已知行业
        for quadrant_key, quadrant in self.tree['framework_decision_tree'].items():
            if quadrant_key.startswith('quadrant_'):
                if industry_name in quadrant.get('examples', []):
                    print(f"[FrameworkSelector] Identified known industry: {quadrant_key}")
                    return quadrant_key

        # Step 2: 未知行业，通过用户回答分类
        if user_answers:
            policy_sensitivity = user_answers.get('policy_sensitivity', 'low')
            payment_model = user_answers.get('payment_model', 'C端')

            if policy_sensitivity == 'high' and payment_model == '政府':
                return 'quadrant_1_gov_dominant'
            elif policy_sensitivity == 'high' and payment_model == '混合':
                return 'quadrant_2_policy_driven'
            elif policy_sensitivity == 'low' and payment_model == 'B端':
                return 'quadrant_3_b2b'
            else:
                return 'quadrant_4_market_driven'

        # Step 3: 默认返回最通用的象限4
        print("[WARNING] Unknown industry, using default quadrant 4 (market-driven)")
        return 'quadrant_4_market_driven'

    def select_frameworks(self,
                         industry_name: str,
                         user_answers: Optional[Dict] = None,
                         custom_framework_id: Optional[str] = None) -> List[Dict]:
        """
        自动选择适用的分析框架（增强版）

        Args:
            industry_name: 行业名称
            user_answers: 用户填写的行业特征（可选）
            custom_framework_id: 指定使用的自定义框架ID（可选）

        Returns:
            frameworks: 框架列表，按权重排序
                [{'name': 'PEST分析', 'weight': '30%', 'focus': '...'}, ...]

        优先级:
        1. 用户明确指定的自定义框架
        2. 适用于该行业的自定义框架
        3. 内置框架（基于4象限）
        """
        all_frameworks = []

        # 1. 优先级1：用户明确指定的自定义框架
        if custom_framework_id:
            custom_fw = self.custom_builder.get_framework(custom_framework_id)
            if custom_fw:
                print(f"\n[FrameworkSelector] Using specified custom framework: {custom_fw['framework_name']}")
                return self._convert_custom_framework(custom_fw)
            else:
                print(f"[WARNING] Custom framework {custom_framework_id} not found, falling back...")

        # 2. 优先级2：查找适用于该行业的自定义框架
        matching_custom = []
        for fw in self.custom_frameworks:
            fw_def = self.custom_builder.get_framework(fw['framework_id'])
            if fw_def and industry_name in fw_def.get('applicable_industries', []):
                matching_custom.append(fw_def)

        if matching_custom:
            print(f"\n[FrameworkSelector] Found {len(matching_custom)} custom framework(s) for {industry_name}")
            for fw in matching_custom:
                print(f"  - {fw['framework_name']} (自定义)")

            # 返回自定义框架 + 内置框架（混合）
            custom_converted = []
            for fw in matching_custom:
                custom_converted.extend(self._convert_custom_framework(fw))

            # 同时加载内置框架（权重降低）
            quadrant = self.classify_industry(industry_name, user_answers)
            builtin_frameworks = self.tree['framework_decision_tree'][quadrant]['frameworks']

            # 合并：自定义框架保持原权重，内置框架权重×0.5
            for fw in builtin_frameworks:
                fw_copy = fw.copy()
                original_weight = float(fw_copy['weight'].rstrip('%'))
                fw_copy['weight'] = f"{original_weight * 0.5:.0f}%"
                fw_copy['name'] = f"{fw_copy['name']}（内置）"
                custom_converted.append(fw_copy)

            return sorted(custom_converted,
                         key=lambda x: float(x['weight'].rstrip('%')),
                         reverse=True)

        # 3. 优先级3：使用内置框架
        quadrant = self.classify_industry(industry_name, user_answers)
        frameworks = self.tree['framework_decision_tree'][quadrant]['frameworks']

        # 按权重排序
        sorted_frameworks = sorted(
            frameworks,
            key=lambda x: float(x['weight'].rstrip('%')),
            reverse=True
        )

        print(f"\n[FrameworkSelector] Selected {len(sorted_frameworks)} built-in frameworks for {industry_name}:")
        for fw in sorted_frameworks:
            print(f"  - {fw['name']} (权重{fw['weight']})")

        return sorted_frameworks

    def _convert_custom_framework(self, custom_fw: Dict) -> List[Dict]:
        """
        将自定义框架转换为标准格式

        Args:
            custom_fw: 自定义框架定义

        Returns:
            frameworks: 标准格式的框架列表
        """
        converted = []

        for dim in custom_fw.get('dimensions', []):
            converted.append({
                'name': f"{custom_fw['framework_name']}-{dim['name']}",
                'weight': dim['weight'],
                'focus': dim.get('focus', ''),
                'key_questions': dim.get('key_questions', []),
                'custom': True,
                'framework_id': custom_fw['framework_id']
            })

        return converted

    def list_available_frameworks(self, industry_name: Optional[str] = None) -> Dict:
        """
        列出所有可用的框架（内置+自定义）

        Args:
            industry_name: 行业名称（可选，用于筛选）

        Returns:
            frameworks: {'custom': [...], 'builtin': [...]}
        """
        result = {
            'custom': [],
            'builtin': []
        }

        # 自定义框架
        for fw in self.custom_frameworks:
            fw_def = self.custom_builder.get_framework(fw['framework_id'])
            if industry_name:
                if industry_name in fw_def.get('applicable_industries', []):
                    result['custom'].append(fw)
            else:
                result['custom'].append(fw)

        # 内置框架（从4个象限提取）
        for quadrant_key, quadrant in self.tree['framework_decision_tree'].items():
            if quadrant_key.startswith('quadrant_'):
                for fw in quadrant['frameworks']:
                    if fw not in result['builtin']:
                        result['builtin'].append({
                            'name': fw['name'],
                            'weight': fw['weight'],
                            'quadrant': quadrant_key
                        })

        return result

    def create_custom_framework_interactive(self):
        """
        交互式创建自定义框架（快捷入口）

        Returns:
            framework_def: 创建的框架定义
        """
        return self.custom_builder.create_framework_interactive()

    def get_key_questions(self, industry_name: str) -> List[str]:
        """
        获取关键问题清单

        Args:
            industry_name: 行业名称

        Returns:
            questions: 关键问题列表
        """
        quadrant = self.classify_industry(industry_name)
        return self.tree['framework_decision_tree'][quadrant]['key_questions']


def main():
    """测试框架选择器"""
    selector = FrameworkSelector()

    # 测试: 医疗陪护（已知行业）
    print("="*60)
    print("测试1: 医疗陪护（已知行业）")
    print("="*60)
    frameworks = selector.select_frameworks('医疗陪护')

    print("\n关键问题:")
    questions = selector.get_key_questions('医疗陪护')
    for i, q in enumerate(questions, 1):
        print(f"  {i}. {q}")

    # 测试: 未知行业
    print("\n" + "="*60)
    print("测试2: 月子中心（未知行业，需要用户回答）")
    print("="*60)
    user_input = {
        'policy_sensitivity': 'high',
        'payment_model': '混合'
    }
    frameworks = selector.select_frameworks('月子中心', user_input)


if __name__ == '__main__':
    main()
