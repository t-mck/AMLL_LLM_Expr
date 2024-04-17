import anthropic
import yaml

with open('claude_session_api.yaml') as rf:
        API_KEY = yaml.safe_load(rf)['api_key']


client = anthropic.Anthropic(
    api_key=API_KEY,
)
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)
print(message.content)