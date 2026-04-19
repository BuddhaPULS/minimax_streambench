from openai import OpenAI

clenti = OpenAI()

response = clenti.chat.completions.create(
    model="MiniMax-M2.7",
    messages=[
        {
            "role": "user",
            "content": [
                {"type":"text",
                 "text":"What is agent Harness?"}]
        }
    ],
    max_tokens=500
)

print(response.choices[0].message.content)
print(response.usage)