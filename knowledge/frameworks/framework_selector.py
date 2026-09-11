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
    框架选择器

    根据行业特征自动选择最适合的分析框架组合
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
                         user_answers: Optional[Dict] = None) -> List[Dict]:
        """
        自动选择适用的分析框架

        Args:
            industry_name: 行业名称
            user_answers: 用户填写的行业特征（可选）

        Returns:
            frameworks: 框架列表，按权重排序
                [{'name': 'PEST分析', 'weight': '30%', 'focus': '...'}, ...]
        """
        quadrant = self.classify_industry(industry_name, user_answers)
        frameworks = self.tree['framework_decision_tree'][quadrant]['frameworks']

        # 按权重排序
        sorted_frameworks = sorted(
            frameworks,
            key=lambda x: float(x['weight'].rstrip('%')),
            reverse=True
        )

        print(f"\n[FrameworkSelector] Selected {len(sorted_frameworks)} frameworks for {industry_name}:")
        for fw in sorted_frameworks:
            print(f"  - {fw['name']} (权重{fw['weight']})")

        return sorted_frameworks

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
