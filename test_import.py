"""测试框架选择器导入"""

try:
    from knowledge.frameworks import FrameworkSelector
    print("SUCCESS: FrameworkSelector imported successfully")

    # 尝试实例化
    selector = FrameworkSelector()
    print("SUCCESS: FrameworkSelector instantiated successfully")

    # 检查自定义框架是否加载
    print(f"Custom frameworks loaded: {len(selector.custom_frameworks)}")

    print("\nAll tests passed!")

except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
