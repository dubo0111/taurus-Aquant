from zai import ZaiClient, ZhipuAiClient

# For Chinese users, create the ZhipuAiClient
client = ZhipuAiClient(api_key="bf7a17b28b4342a38607198705b99cec.HhoOB3Uhjsdwsisg", base_url="https://open.bigmodel.cn/api/paas/v4/")

# Create chat completion
response = client.chat.completions.create(
    model="glm-4.7-flash",  # or "glm-5" if you have access
    messages=[
        {"role": "user", "content": "Hello, Z.ai!"}
    ]
)
print(response.choices[0].message.content)