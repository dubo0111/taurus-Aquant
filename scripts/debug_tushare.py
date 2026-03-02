"""
调试 Tushare 连接
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import tushare as ts
import tushare.pro.client as client
from src.utils.config import settings

print("=" * 60)
print("调试 Tushare 连接")
print("=" * 60)

# 1. 检查配置
print("\n1. 检查配置：")
print(f"   TUSHARE_TOKEN: {settings.TUSHARE_TOKEN[:20]}...")
print(f"   TUSHARE_API_URL: {settings.TUSHARE_API_URL}")

# 2. 方法1：用户的原始代码
print("\n2. 测试用户原始代码：")
try:
    client.DataApi._DataApi__http_url = "http://tushare.xyz"
    pro1 = ts.pro_api('fa3b68af8c489154bbdf4253203193f23be1e3640b11f86e0088c7d5')
    df1 = pro1.daily_basic(**{"limit": 5}, fields=["ts_code", "trade_date", "close"])
    print(f"   ✅ 成功（用户代码）：{len(df1)} 条数据")
    print(df1)
except Exception as e:
    print(f"   ❌ 失败（用户代码）：{e}")

# 3. 方法2：使用配置
print("\n3. 测试使用配置：")
try:
    # 先设置 URL
    if settings.TUSHARE_API_URL:
        client.DataApi._DataApi__http_url = settings.TUSHARE_API_URL
        print(f"   已设置 API URL: {settings.TUSHARE_API_URL}")

    # 再创建 pro_api
    pro2 = ts.pro_api(settings.TUSHARE_TOKEN)
    df2 = pro2.daily_basic(**{"limit": 5}, fields=["ts_code", "trade_date", "close"])
    print(f"   ✅ 成功（使用配置）：{len(df2)} 条数据")
    print(df2)
except Exception as e:
    print(f"   ❌ 失败（使用配置）：{e}")
    import traceback
    traceback.print_exc()

# 4. 检查 token 是否一致
print("\n4. 检查 token：")
user_token = 'fa3b68af8c489154bbdf4253203193f23be1e3640b11f86e0088c7d5'
config_token = settings.TUSHARE_TOKEN
print(f"   用户代码中的 token: {user_token}")
print(f"   .env 中的 token:    {config_token}")
print(f"   是否一致: {'✅ 是' if user_token == config_token else '❌ 否'}")
