"""
测试自动读取Claude Code settings.json的功能
"""

from execution.consulting_ai_analyzer import ConsultingAIAnalyzer

print("="*60)
print("测试: 自动读取Claude Code配置")
print("="*60)

# 不传入任何参数，看能否自动读取settings.json
analyzer = ConsultingAIAnalyzer()

print(f"\nAPI密钥状态: {'已加载' if analyzer.api_key else '未加载'}")
print(f"Base URL: {analyzer.base_url if analyzer.base_url else '未设置'}")
print(f"模型: {analyzer.model}")

if analyzer.api_key:
    # 如果成功读取，尝试生成一个简单的行业画像
    print("\n正在测试AI分析能力...")
    try:
        profile = analyzer._analyze_industry_profile('医疗陪护')
        print(f"\n行业画像生成成功！")
        print(f"内容: {profile['summary'][:100]}...")
    except Exception as e:
        print(f"\nAPI调用失败: {str(e)}")
else:
    print("\n⚠️ 未能自动加载API密钥")
    print("请检查 ~/.claude/settings.json 是否存在")

print("\n" + "="*60)
