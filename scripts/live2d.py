import os.path
from time import sleep

import live2d.v3 as live2d
import pyautogui
import scipy.io.wavfile
import sounddevice as sd
from live2d.utils.lipsync import WavHandler
from pyopengltk import OpenGLFrame

import resources

wavHandler = WavHandler()
lipSyncN = 3


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

        self.model.SetAutoBlinkEnable(True)

    def start_tts(self, audio_path):
        v_samplerate, v_data = scipy.io.wavfile.read(audio_path)
        sd.play(v_data, v_samplerate)
        wavHandler.Start(audio_path)
        sd.wait()

    def redraw(self):
        # """Render a single frame"""
        live2d.clearBuffer()

        screen_x, screen_y = pyautogui.position()
        x = screen_x - self.winfo_rootx()
        y = screen_y - self.winfo_rooty() + 150

        self.model.Update()
        if wavHandler.Update():  # 获取 wav 下一帧片段的响度（Rms），如果没有下一帧片段则为False（音频已播放完毕）
            self.model.SetParameterValue("ParamMouthOpenY", wavHandler.GetRms() * lipSyncN)
        self.model.Drag(x, y)
        self.model.Draw()

        sleep(1 / 240)

    def setexpression(self, text):
        self.model.ResetExpression()
        self.model.SetExpression(text)

    def setmotion(self, text):
        self.model.StartRandomMotion(text)

    def resetexpression(self):
        self.model.ResetExpression()
