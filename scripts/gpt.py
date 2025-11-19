import os

import dotenv
import yaml
from openai import OpenAI
from pydantic import BaseModel

dotenv.load_dotenv()

conf_path = "./config.yaml"

with open(conf_path, "rt", encoding="UTF8") as c:
    raw = c.read()


exp = os.path.expandvars(raw)
conf = yaml.safe_load(exp)

client = OpenAI(api_key=conf["key"])
model = conf["model"]


class CalendarEvent(BaseModel):
    contents: str
    expression: str


def get_gpt(chat_log=None):
    if chat_log is None:
        chat_log = []
    response = client.responses.parse(
        model=model,
        input=[
            {"role": "system", "content": conf["persona_prompt"]},
            {
                "role": "assistant",
                "content": "한글로 대답하고 모션은 화났을때 'angry', 슬플떄 'cry', 삐졌을떄 'white_eyes', 항복 'qizi1' 으로 해줘.",
            },
        ]
        + chat_log,
        text_format=CalendarEvent,
    )

    return response.output_parsed
