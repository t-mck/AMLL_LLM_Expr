# pip install openai
# https://platform.openai.com/docs/api-reference/introduction
# https://platform.openai.com/api-keys
# https://platform.openai.com/docs/guides/rate-limits/usage-tiers?context=tier-free

from openai import OpenAI

client = OpenAI(api_key="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")

stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user",
               "content": "Say this is a test duderino"}]
    # ,
    # stream=True
)

output = stream.choices[0].message.content
print(output)

# for chunk in stream:
#     if chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content, end="")
