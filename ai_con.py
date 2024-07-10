from openai import OpenAI
from config import API_KEY_PROXY

client = OpenAI(
    api_key=API_KEY_PROXY,
    base_url="https://api.proxyapi.ru/openai/v1",
)


def chat_with_gpt():
    print("Добро пожаловать в чат с нейросетью! Введите 'exit' для выхода.")

    conversation_history = []

    while True:
        user_input = input("Вы: ")
        if user_input.lower() == "exit":
            print("Завершение чата. До свидания!")
            break

        conversation_history.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106", messages=conversation_history
        )

        answer = response.choices[0].message.content

        print(f"GPT: {answer}")

        conversation_history.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    chat_with_gpt()
