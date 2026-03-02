"""
诊断 Tushare Token 问题
"""
import tushare as ts

token = "c79b2dba9b1bfc2698f74e650dca03edd0b9398ee038bb97d0285fa5"

print("=" * 60)
print("Tushare Token 诊断")
print("=" * 60)
print(f"Token 长度: {len(token)}")
print(f"Token 前10位: {token[:10]}")
print(f"Token 后10位: {token[-10:]}")
print()

# 尝试设置 token
ts.set_token(token)

# 尝试创建 pro_api
try:
    pro = ts.pro_api()
    print("✅ pro_api() 创建成功")

    # 尝试调用一个简单的接口
    print("\n测试调用 trade_cal 接口...")
    df = pro.trade_cal(exchange='SSE', start_date='20260101', end_date='20260110')
    print(f"✅ 调用成功，返回 {len(df)} 条数据")
    print(df.head())

except Exception as e:
    print(f"❌ 调用失败: {e}")
    print("\n可能的原因：")
    print("1. Token 不正确或不完整")
    print("2. Token 未激活（需要注册后等待）")
    print("3. Token 权限不足（需要积分）")
    print("4. 网络问题")

    print("\n解决方案：")
    print("1. 访问 https://tushare.pro/register 重新注册")
    print("2. 登录后在个人中心获取正确的 Token")
    print("3. 或使用 AkShare（免费，无需 Token）")
