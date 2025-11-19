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
    motion: str


def get_gpt(chat_log=None):
    if chat_log is None:
        chat_log = []
    response = client.responses.parse(
        model=model,
        input=[
            {"role": "system", "content": conf["persona_prompt"]},
            {
                "role": "assistant",
                "content": "한글로 대답."
                + "표현(expression)은 화남 'angry', 슬플떄 'cry', 삐졌을때 or 의심: 'white_eyes', 배개 안기 'baozhen', 필요없을 경우에는 'Noexp'"
                + "할수있는 모션(motion)은 두리번거리기 'haoqi', 쓰러지는척 'keshui', 백기 흔들기 or 항복 : 'qizi'"
                + ", 배개안고 얼굴 비비기: 'zhentou', 도리도리 or 강한 부정 or 머리 흔들기 or 강한 거부: 'yaotou', 없을때는 'Nomotion",
            },
        ]
        + chat_log,
        text_format=CalendarEvent,
    )

    return response.output_parsed
