import dotenv
import os
from groq import Groq

dotenv.load_dotenv()



client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "search online and give me details of josephat oyondi",
        }
    ],
    model="gemma2-9b-it",
)

print(chat_completion.choices[0].message.content)