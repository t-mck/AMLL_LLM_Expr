# pip install openai

from openai import OpenAI

client = OpenAI(api_key="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", base_url="https://chat.openai.com/g/g-aEgASz9fP-llm-math-1")

stream = client.chat.completions.create(
    model="LLM_Math_1",
    messages=[{"role": "user", "content": "Say this is a test"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")