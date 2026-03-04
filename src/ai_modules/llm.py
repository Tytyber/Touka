from openai import OpenAI
import config
import asyncio

MODEL = "arcee-ai/trinity-large-preview:free"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=config.OR_TOKEN,
)

user_histories = {}  # {(guild_id, user_id): [messages]}


async def generate_response(guild_id: int, user_id: int, text: str):
    key = (guild_id, user_id)

    if key not in user_histories:
        user_histories[key] = [
            {
                "role": "system",
                "content": config.LLM_PROMT
            }
        ]

    user_histories[key].append({
        "role": "user",
        "content": text
    })

    loop = asyncio.get_running_loop()

    # 🔥 ВАЖНО: выносим блокирующий вызов
    response = await loop.run_in_executor(
        None,
        lambda: client.chat.completions.create(
            model=MODEL,
            messages=user_histories[key],
            extra_body={"reasoning": {"enabled": True}}
        )
    )

    message = response.choices[0].message

    user_histories[key].append({
        "role": "assistant",
        "content": message.content
    })

    if len(user_histories[key]) > 20:
        user_histories[key] = (
            user_histories[key][:1] +
            user_histories[key][-18:]
        )
    print("Регистрация команды /say")
    return message.content