"""
意图解析器：从自然语言中提取研究需求

将用户的自然语言描述转换为WorkflowEngine可理解的参数
"""

import re
from typing import Dict, List, Optional


class IntentParser:
    """
    解析用户意图，提取研究维度和深度

    示例：
    "帮我研究医疗陪护，重点看政策环境和竞争格局，快速版"
    → dimensions=['政策环境', '竞争格局'], depth='快速'
    """

    def __init__(self):
        """初始化意图解析器"""

        # 维度关键词映射
        self.dimension_keywords = {
            '政策环境': ['政策', '监管', '法规', '政府', '支持', '补贴', '长护险'],
            '市场规模': ['市场', '规模', '增长', '体量', '空间', '多大', '市场有多大'],
            '商业模式': ['商业模式', '盈利', '赚钱', '变现', '收费', '单位经济'],
            '竞争格局': ['竞争', '对手', '玩家', '格局', '谁在做', '竞争激烈'],
            '进入壁垒': ['壁垒', '门槛', '难度', '好不好进', '容易进入'],
            '产业链': ['产业链', '上下游', '供应链', '链条'],
            '风险分析': ['风险', '问题', '挑战', '困难', '担心'],
            '机会识别': ['机会', '趋势', '红利', '潜力', '前景']
        }

        # 深度关键词映射
        self.depth_keywords = {
            '快速': ['快速', '快', '简单', '大概', '粗略', '10分钟', '十分钟'],
            '标准': ['标准', '正常', '常规', '30分钟', '三十分钟'],
            '深度': ['深度', '深入', '详细', '全面', '完整', '60分钟', '一小时']
        }

        # 视角关键词（扩展功能）
        self.perspective_keywords = {
            '创业者': ['创业', '创始人', '我想做', '想进入'],
            '投资人': ['投资', '投资人', '值不值得投', '回报'],
            '咨询顾问': ['咨询', '分析', '客观']
        }

    def parse(self, user_input: str) -> Dict:
        """
        解析用户输入

        Args:
            user_input: 用户的自然语言输入

        Returns:
            parsed_params: 解析后的参数字典
        """
        result = {
            'dimensions': self._extract_dimensions(user_input),
            'depth': self._extract_depth(user_input),
            'perspective': self._extract_perspective(user_input)
        }

        return result

    def _extract_dimensions(self, text: str) -> List[str]:
        """
        提取用户想分析的维度

        Args:
            text: 用户输入文本

        Returns:
            dimensions: 维度列表
        """
        matched_dimensions = []

        for dimension, keywords in self.dimension_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    if dimension not in matched_dimensions:
                        matched_dimensions.append(dimension)
                    break

        return matched_dimensions

    def _extract_depth(self, text: str) -> Optional[str]:
        """
        提取研究深度

        Args:
            text: 用户输入文本

        Returns:
            depth: '快速' / '标准' / '深度' / None
        """
        for depth, keywords in self.depth_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return depth

        return None

    def _extract_perspective(self, text: str) -> Optional[str]:
        """
        提取用户视角

        Args:
            text: 用户输入文本

        Returns:
            perspective: '创业者' / '投资人' / '咨询顾问' / None
        """
        for perspective, keywords in self.perspective_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return perspective

        return None

    def format_as_user_params(self, parsed_intent: Dict) -> Dict:
        """
        将解析结果转换为orchestrator的user_params格式

        Args:
            parsed_intent: 解析后的意图

        Returns:
            user_params: orchestrator可理解的参数
        """
        user_params = {}

        if parsed_intent['dimensions']:
            user_params['dimensions'] = parsed_intent['dimensions']

        if parsed_intent['depth']:
            user_params['depth'] = parsed_intent['depth']

        if parsed_intent['perspective']:
            user_params['perspective'] = parsed_intent['perspective']

        return user_params


def test_parser():
    """测试意图解析器"""
    parser = IntentParser()

    test_cases = [
        "帮我研究医疗陪护，重点看政策环境和竞争格局，快速版",
        "我想进入养老行业，想知道市场有多大，竞争激不激烈",
        "从投资人视角，深度分析在线教育的商业模式和风险",
        "快速看一下金融科技的政策支持情况"
    ]

    print("="*60)
    print("意图解析器测试")
    print("="*60)

    for i, case in enumerate(test_cases, 1):
        print(f"\n[测试{i}] {case}")
        result = parser.parse(case)
        print(f"维度: {result['dimensions']}")
        print(f"深度: {result['depth']}")
        print(f"视角: {result['perspective']}")

        user_params = parser.format_as_user_params(result)
        print(f"转换后: {user_params}")


if __name__ == '__main__':
    test_parser()
