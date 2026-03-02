"""
直接使用用户提供的代码测试
"""
import tushare as ts
import tushare.pro.client as client

# 按照用户的示例代码
client.DataApi._DataApi__http_url = "http://tushare.xyz"  # 一定要加上这行代码
pro = ts.pro_api('fa3b68af8c489154bbdf4253203193f23be1e3640b11f86e0088c7d5')

print("=" * 60)
print("测试 Tushare Token（用户示例）")
print("=" * 60)

try:
    # 用户提供的示例
    df = pro.daily_basic(**{"limit": 20}, fields=["ts_code", "trade_date", "close", "pb", "ps"])
    print(f"✅ 成功获取 {len(df)} 条数据")
    print(df)

    print("\n" + "=" * 60)
    print("🎉 Token 有效！")
    print("=" * 60)

except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
