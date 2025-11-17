import os.path
from time import sleep

import live2d.v3 as live2d
import pyautogui
from pyopengltk import OpenGLFrame

import resources


class live2d_frame(OpenGLFrame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.model = None

    def initgl(self):
        """Initalize gl states when the frame is created"""
        if self.model:
            del self.model
        live2d.dispose()

        live2d.init()
        live2d.glInit()

        self.model = live2d.LAppModel()
        if live2d.LIVE2D_VERSION == 2:
            self.model.LoadModelJson(os.path.join(resources.RESOURCES_DIRECTORY, "v2/hibiki/hibiki.model.json"))
        else:
            self.model.LoadModelJson(os.path.join(resources.RESOURCES_DIRECTORY, "v3/huohuo/huohuo.model3.json"))
        self.update_idletasks()
        self.model.Resize(self.height, self.width)
        self.model.SetScale(1)

    def redraw(self):
        # """Render a single frame"""
        live2d.clearBuffer()

        screen_x, screen_y = pyautogui.position()
        x = screen_x - self.winfo_rootx()
        y = screen_y - self.winfo_rooty()

        self.model.Update()
        self.model.Drag(x, y)
        self.model.Draw()
        # # 控制帧率
        sleep(1 / 240)
