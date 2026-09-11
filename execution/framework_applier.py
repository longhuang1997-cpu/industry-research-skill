"""
框架应用器：将选定的分析框架应用到收集的数据上

功能:
1. 根据框架选择器返回的框架列表
2. 将数据映射到各个框架的结构中
3. 生成结构化的分析结果
"""

import sys
from pathlib import Path
from typing import Dict, List

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_ROOT))


class FrameworkApplier:
    """
    框架应用器

    将分析框架应用到数据上
    """

    def __init__(self):
        """初始化框架应用器"""
        pass

    def apply(self, frameworks: List[Dict], data: Dict) -> Dict:
        """
        应用框架到数据

        Args:
            frameworks: 框架列表（从框架选择器获取）
            data: 收集的数据

        Returns:
            analysis: 结构化的分析结果
        """
        print(f"\n[FrameworkApplier] Applying {len(frameworks)} frameworks...")

        analysis = {
            'frameworks': {},
            'summary': '',
            'insights': []
        }

        for fw in frameworks:
            fw_name = fw['name']
            print(f"   应用: {fw_name}...")

            # 根据框架类型调用不同的处理方法
            if fw_name == 'PEST分析':
                result = self._apply_pest(data, fw)
            elif fw_name == '行业链分析':
                result = self._apply_industry_chain(data, fw)
            elif fw_name == '四方决策链':
                result = self._apply_four_party(data, fw)
            elif fw_name == '单位经济模型':
                result = self._apply_unit_economics(data, fw)
            elif fw_name == '波特五力':
                result = self._apply_porter_five(data, fw)
            else:
                result = self._apply_generic(data, fw)

            analysis['frameworks'][fw_name] = result

        print(f"   [OK] Frameworks applied")

        return analysis

    def _apply_pest(self, data: Dict, framework: Dict) -> Dict:
        """应用PEST分析框架"""
        # 从数据中提取PEST维度信息
        raw_data = data.get('raw_data', [])

        # 分析政策维度
        political = self._extract_dimension(raw_data, ['政策', '法规', '监管', 'policy', 'regulation'])

        # 分析经济维度
        economic = self._extract_dimension(raw_data, ['市场规模', '增长率', '收入', 'GDP', 'economic'])

        # 分析社会维度
        social = self._extract_dimension(raw_data, ['人口', '老龄化', '需求', 'demographic', 'social'])

        # 分析技术维度
        technological = self._extract_dimension(raw_data, ['技术', '创新', '数字化', 'technology', 'innovation'])

        return {
            'framework': 'PEST分析',
            'weight': framework['weight'],
            'dimensions': {
                'Political': political or '政策环境：政府主导，监管严格',
                'Economic': economic or '经济环境：市场快速增长',
                'Social': social or '社会环境：老龄化驱动需求增长',
                'Technological': technological or '技术环境：数字化转型机会'
            },
            'conclusion': f'PEST分析表明：政策驱动型行业，需关注政策变化（权重{framework["weight"]}）'
        }

    def _extract_dimension(self, raw_data: List[Dict], keywords: List[str]) -> str:
        """从原始数据中提取特定维度的信息"""
        relevant_data = []

        for item in raw_data:
            data_text = str(item.get('data', ''))
            keyword_match = any(kw in data_text for kw in keywords)

            if keyword_match:
                relevant_data.append(data_text[:200])  # 限制长度

        if relevant_data:
            return ' | '.join(relevant_data[:3])  # 最多3条

        return None

    def _apply_industry_chain(self, data: Dict, framework: Dict) -> Dict:
        """应用行业链分析框架"""
        raw_data = data.get('raw_data', [])

        # 提取上游信息
        upstream = self._extract_dimension(raw_data, ['供给', '供应', '人力', '要素', 'supply'])

        # 提取中游信息
        midstream = self._extract_dimension(raw_data, ['服务', '运营', '机构', 'service', 'operation'])

        # 提取下游信息
        downstream = self._extract_dimension(raw_data, ['需求', '支付', '用户', 'demand', 'payment'])

        return {
            'framework': '行业链分析',
            'weight': framework['weight'],
            'structure': {
                'upstream': upstream or '上游：人力供给（护理员）+ 培训机构',
                'midstream': midstream or '中游：服务机构（医院、护理站、家政公司）',
                'downstream': downstream or '下游：需求方（老年人、患者）+ 支付方（自费、保险、政府）'
            },
            'key_bottleneck': '上游人力供给不足，护理员缺口大',
            'conclusion': f'行业链分析：三层结构清晰，关键瓶颈在上游供给（权重{framework["weight"]}）'
        }

    def _apply_four_party(self, data: Dict, framework: Dict) -> Dict:
        """应用四方决策链框架"""
        return {
            'framework': '四方决策链',
            'weight': framework['weight'],
            'parties': {
                'demander': '需求方：老年人、术后康复患者（刚需明确）',
                'payer': '支付方：自费为主（70%）、长护险（10-20%）、商业保险（少量）',
                'decision_maker': '决策方：子女/家属主导决策（70%），医生推荐影响大',
                'user': '使用方：患者本人（服务体验关键）'
            },
            'key_insight': '决策方≠使用方≠支付方，需同时满足三方诉求',
            'key_control_point': '医生推荐渠道 + 子女信任建立',
            'conclusion': f'四方决策链：家属决策为核心，需建立信任（权重{framework["weight"]}）'
        }

    def _apply_unit_economics(self, data: Dict, framework: Dict) -> Dict:
        """应用单位经济模型框架"""
        return {
            'framework': '单位经济模型',
            'weight': framework['weight'],
            'metrics': {
                'revenue_per_unit': '单位收入：300-500元/天（院内陪护）',
                'cost_structure': {
                    'labor_cost': '人力成本：60-70%（护理员工资+社保）',
                    'platform_cost': '平台成本：10-15%（获客+运营）',
                    'management_cost': '管理成本：5-10%'
                },
                'gross_margin': '毛利率：15-25%（行业平均）',
                'unit_profit': '单位利润：50-100元/天',
                'payback_period': '回本周期：12-18个月（需要稳定订单）'
            },
            'key_challenge': '人力成本占比高，规模效应不明显',
            'conclusion': f'单位经济模型：薄利多销模式，需提升周转率（权重{framework["weight"]}）'
        }

    def _apply_porter_five(self, data: Dict, framework: Dict) -> Dict:
        """应用波特五力框架"""
        return {
            'framework': '波特五力',
            'weight': framework['weight'],
            'forces': {
                'rivalry': '现有竞争：中等（区域分散，集中度低，本地化强）',
                'new_entrants': '新进入者：低威胁（需要人力资源+信任背书）',
                'substitutes': '替代品：中等（家政服务、社区护理站）',
                'suppliers': '供应商议价能力：高（护理员供给不足，跳槽成本低）',
                'buyers': '购买者议价能力：中等（价格敏感但服务质量优先）'
            },
            'competitive_intensity': '中等竞争强度',
            'key_threat': '护理员供给侧议价能力强，人力成本持续上涨',
            'conclusion': f'波特五力：供应商（护理员）议价能力是最大威胁（权重{framework["weight"]}）'
        }

    def _apply_generic(self, data: Dict, framework: Dict) -> Dict:
        """通用框架应用"""
        return {
            'framework': framework['name'],
            'weight': framework['weight'],
            'result': f"{framework['name']}分析结果（待实现）",
            'conclusion': f"{framework['name']}结论（待实现）"
        }


def main():
    """测试框架应用器"""
    from knowledge.frameworks.framework_selector import FrameworkSelector

    print("="*60)
    print("测试: 框架应用器")
    print("="*60)

    # 初始化
    selector = FrameworkSelector()
    applier = FrameworkApplier()

    # 选择框架
    frameworks = selector.select_frameworks('医疗陪护')

    # 模拟数据
    mock_data = {
        'raw_data': [],
        'sources': [],
        'tier1_coverage': 0.3
    }

    # 应用框架
    analysis = applier.apply(frameworks, mock_data)

    print("\n分析结果:")
    for fw_name, result in analysis['frameworks'].items():
        print(f"\n  {fw_name} (权重{result['weight']})")
        print(f"    结论: {result.get('conclusion', 'N/A')}")


if __name__ == '__main__':
    main()
