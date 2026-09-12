"""
对话集成辅助函数

帮助Claude在对话中理解用户意图并调用行业研究
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent
sys.path.insert(0, str(SKILL_ROOT))


def parse_and_research(user_input: str, industry: str = None):
    """
    从自然语言中解析意图并执行研究

    Args:
        user_input: 用户的自然语言输入
        industry: 行业名称（如果已从user_input中提取）

    Returns:
        result: 研究结果

    使用示例：
        用户说："帮我研究医疗陪护行业，重点看政策和竞争，快速版"
        → parse_and_research(user_input, industry="医疗陪护")
    """
    from orchestrator.intent_parser import IntentParser
    from irs import run_research

    # 如果没有明确的行业名称，尝试从输入中提取
    if not industry:
        industry = extract_industry_name(user_input)
        if not industry:
            return {
                'status': 'error',
                'message': '未能识别行业名称，请明确指定行业'
            }

    # 解析用户意图
    parser = IntentParser()
    intent = parser.parse(user_input)

    # 转换为user_params
    user_params = parser.format_as_user_params(intent)

    # 显示解析结果（可选）
    print("\n💡 理解您的需求:")
    if user_params.get('dimensions'):
        print(f"   分析维度: {', '.join(user_params['dimensions'])}")
    else:
        print(f"   分析维度: 标准维度（政策环境、市场规模、商业模式）")

    if user_params.get('depth'):
        print(f"   研究深度: {user_params['depth']}")
    else:
        print(f"   研究深度: 标准（约30分钟）")

    if user_params.get('perspective'):
        print(f"   分析视角: {user_params['perspective']}")

    print()

    # 执行研究
    result = run_research(industry, user_params)

    return result


def extract_industry_name(user_input: str) -> str:
    """
    从用户输入中提取行业名称

    Args:
        user_input: 用户输入

    Returns:
        industry: 行业名称（如果找到）

    示例：
        "帮我研究医疗陪护行业" → "医疗陪护"
        "分析一下在线教育" → "在线教育"
    """
    import re

    # 常见行业研究触发词
    patterns = [
        r'研究(.{2,10})行业',
        r'分析(.{2,10})行业',
        r'看看(.{2,10})行业',
        r'研究(.{2,10})',
        r'分析(.{2,10})',
        r'了解(.{2,10})的',
    ]

    for pattern in patterns:
        match = re.search(pattern, user_input)
        if match:
            industry = match.group(1).strip()
            # 去除常见修饰词
            industry = industry.replace('一下', '').replace('看', '').strip()
            if industry and len(industry) >= 2:
                return industry

    return None


def should_trigger_research(user_input: str) -> bool:
    """
    判断用户输入是否触发行业研究

    Args:
        user_input: 用户输入

    Returns:
        bool: 是否应该触发行业研究
    """
    # 行业研究关键词
    research_keywords = [
        '研究', '分析', '调研', '了解',
        '行业', '市场', '政策', '竞争',
        '值不值得', '机会', '趋势', '前景'
    ]

    # 至少包含一个关键词
    return any(keyword in user_input for keyword in research_keywords)


# 示例使用
def example_usage():
    """示例：如何在对话中使用"""
    print("="*60)
    print("对话集成示例")
    print("="*60)

    # 场景1：完整的自然语言输入
    print("\n[场景1] 用户说：")
    print('"帮我研究医疗陪护行业，重点看政策支不支持，还有竞争激不激烈，快速看一下就行"')
    print("\nClaude应该调用：")
    print('parse_and_research(user_input, industry="医疗陪护")')

    # 场景2：简单的研究请求
    print("\n[场景2] 用户说：")
    print('"我想了解一下养老行业"')
    print("\nClaude应该调用：")
    print('parse_and_research(user_input)  # 自动提取行业名称')

    # 场景3：追问式对话
    print("\n[场景3] 用户说：")
    print('"市场规模有多大？"')
    print("\nClaude应该：")
    print('直接回答（基于之前的研究结果，已在对话上下文中）')

    print("\n" + "="*60)


if __name__ == '__main__':
    example_usage()
