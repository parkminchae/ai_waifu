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
def get_gpt(model, chat_log=None):
    if chat_log is None:
        chat_log = []
    message = [
        {"role": "system", "content": conf["persona_prompt"]},
        {"role": "assistant", "content": "한글로 대답"},
    ] + chat_log
    result = client.chat.completions.create(model=model, messages=message).choices[0].message.content
    return result
