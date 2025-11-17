import os

import dotenv
import yaml
from openai import OpenAI

dotenv.load_dotenv()

conf_path = "./config.yaml"

with open(conf_path, "rt", encoding="UTF8") as c:
    raw = c.read()


exp = os.path.expandvars(raw)
conf = yaml.safe_load(exp)

client = OpenAI(api_key=conf["key"])


# gpt 출력
def translate(model, text=""):
    message = [
        {"role": "system", "content": "일본어로 번역해줘"},
        {"role": "user", "content": text},
    ]
    result = client.chat.completions.create(model=model, messages=message).choices[0].message.content
    return result
