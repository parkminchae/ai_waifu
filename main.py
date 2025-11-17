import dotenv

from scripts.gpt import conf, get_gpt
from scripts.gui import App

dotenv.load_dotenv()

chat_log = []
model = conf["model"]


def callback(text, q):
    global chat_log
    chat_log += [{"role": "user", "content": text}]
    text_gen = get_gpt(model, chat_log)
    chat_log += [{"role": "assistant", "content": text_gen}]
    print(text_gen)
    q.put(text_gen)


def main():
    app = App(callback)
    app.run()


if __name__ == "__main__":
    main()
