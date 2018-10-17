# -*- coding:UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import wx
#import wx.lib.sized_controls as sc


class GoTr(object):
    def __init__(self):
        pass

    def getHTMLText(self, url):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            return r.text
        except:
            print("Get HTML Text Failed!")
            return 0

    def google_translate_EtoC(self, to_translate, from_language="en", to_language="ch-CN"):
        #根据参数生产提交的网址
        base_url = "https://translate.google.cn/m?hl={}&sl={}&ie=UTF-8&q={}"
        url = base_url.format(to_language, from_language, to_translate)
        
        #获取网页
        html = self.getHTMLText(url)
        if html:
            soup = BeautifulSoup(html, "html.parser")
        
        #解析网页得到翻译结果   
        try:
            result = soup.find_all("div", {"class":"t0"})[0].text
        except:
            print("Translation Failed!")
            result = ""
            
        return result

    def google_translate_CtoE(self, to_translate, from_language="ch-CN", to_language="en"):
        #根据参数生产提交的网址
        base_url = "https://translate.google.cn/m?hl={}&sl={}&ie=UTF-8&q={}"
        url = base_url.format(to_language, from_language, to_translate)
        
        #获取网页
        html = self.getHTMLText(url)
        if html:
            soup = BeautifulSoup(html, "html.parser")

        #解析网页得到翻译结果   
        try:
            result = soup.find_all("div", {"class":"t0"})[0].text
        except:
            print("Translation Failed!")
            result = ""

        return result


class GoTrPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.GoTranslator = GoTr()

        #中文StaticText控件
        self.cLabel = wx.StaticText(self, label="原文: ")
        #中文TextCtrl控件
        self.cContent = wx.TextCtrl(self, -1, size=(500, 250),
                               style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_NOHIDESEL)
        #中文文本控件操作按钮
        self.buttonCSelectAll = wx.Button(self, -1, "全选")
        self.Bind(wx.EVT_BUTTON, self.OnButtonCSelectAll, self.buttonCSelectAll)
        self.buttonCClear = wx.Button(self, -1, "清除")
        self.Bind(wx.EVT_BUTTON, self.OnButtonCClear, self.buttonCClear)
        self.buttonCCopy = wx.Button(self, -1, "复制")
        self.Bind(wx.EVT_BUTTON, self.OnButtonCCopy, self.buttonCCopy)
        self.buttonCPaste = wx.Button(self, -1, "粘贴")
        self.Bind(wx.EVT_BUTTON, self.OnButtonCPaste, self.buttonCPaste)

        self.buttonCBoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonCBoxSizer.Add(self.buttonCSelectAll, 0, wx.ALL, 5)
        self.buttonCBoxSizer.Add(self.buttonCClear,     0, wx.ALL, 5)
        self.buttonCBoxSizer.Add(self.buttonCCopy,      0, wx.ALL, 5)
        self.buttonCBoxSizer.Add(self.buttonCPaste,     0, wx.ALL, 5)

        #安装两个按键
        #self.buttonC2E = wx.Button(self, -1, "中文->英文")
        #self.Bind(wx.EVT_BUTTON, self.OnButtonC2E, self.buttonC2E)
        #self.buttonE2C = wx.Button(self, -1, "英文->中文")
        #self.Bind(wx.EVT_BUTTON, self.OnButtonE2C, self.buttonE2C)

        #安装转换按键
        self.buttonTransform = wx.Button(self, -1, "开始")
        self.Bind(wx.EVT_BUTTON, self.OnButtonTransform, self.buttonTransform)

        self.buttonTrBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        #self.buttonTrBoxSizer.Add(self.buttonC2E, 0, wx.GROW|wx.ALL, 20)
        #self.buttonTrBoxSizer.AddSpacer(80)
        #self.buttonTrBoxSizer.Add(self.buttonE2C, 0, wx.GROW|wx.ALL, 20)
        self.buttonTrBoxSizer.Add(self.buttonTransform, 0, wx.GROW|wx.ALL, 20)


        #英文StaticText控件
        self.eLabel = wx.StaticText(self, label="新文: ")
        #英文TextCtrl控件
        self.eContent = wx.TextCtrl(self, -1, size=(500, 250),
                               style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_NOHIDESEL)

        #英文文本控件操作按钮
        self.buttonESelectAll = wx.Button(self, -1, "全选")
        self.Bind(wx.EVT_BUTTON, self.OnButtonESelectAll, self.buttonESelectAll)
        self.buttonEClear = wx.Button(self, -1, "清除")
        self.Bind(wx.EVT_BUTTON, self.OnButtonEClear, self.buttonEClear)
        self.buttonECopy = wx.Button(self, -1, "复制")
        self.Bind(wx.EVT_BUTTON, self.OnButtonECopy, self.buttonECopy)
        self.buttonEPaste = wx.Button(self, -1, "粘贴")
        self.Bind(wx.EVT_BUTTON, self.OnButtonEPaste, self.buttonEPaste)

        self.buttonEBoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonEBoxSizer.Add(self.buttonESelectAll, 0, wx.ALL, 5)
        self.buttonEBoxSizer.Add(self.buttonEClear,     0, wx.ALL, 5)
        self.buttonEBoxSizer.Add(self.buttonECopy,      0, wx.ALL, 5)
        self.buttonEBoxSizer.Add(self.buttonEPaste,     0, wx.ALL, 5)

        #创建一个GridSizer用于全局布局
        self.GridSizer = wx.FlexGridSizer(rows=5, cols=3, hgap=5, vgap=5)
        '''
        self.GridSizer.AddMany([self.cLabel, self.cContent,        self.buttonCBoxSizer,
                                 (0,0),       self.buttonBoxSizer, (0,0),
                                 self.eLabel, self.eContent,       self.buttonEBoxSizer,
                                 ])
        '''

        self.GridSizer.Add((5,5), 0, 0)
        self.GridSizer.Add((0,0), 0, 0)
        self.GridSizer.Add((0,0), 0, 0)

        self.GridSizer.Add(self.cLabel, 0, 0)
        self.GridSizer.Add(self.cContent, 0, wx.EXPAND)
        self.GridSizer.Add(self.buttonCBoxSizer, 0, 0)
        
        self.GridSizer.Add((0,0), 0, 0)
        self.GridSizer.Add(self.buttonTrBoxSizer, 0, wx.EXPAND)
        self.GridSizer.Add((0,0), 0, 0)
        
        self.GridSizer.Add(self.eLabel, 0, 0)
        self.GridSizer.Add(self.eContent, 0, wx.EXPAND)
        self.GridSizer.Add(self.buttonEBoxSizer, 0, 0)

        self.GridSizer.Add((5,5), 0, 0)
        self.GridSizer.Add((0,0), 0, 0)
        self.GridSizer.Add((0,0), 0, 0)

        #调整Grid中的文本框，使之随Frame同步调整
        self.GridSizer.AddGrowableCol(1,1)
        #self.GridSizer.AddGrowableRow(1,1)


        self.SetSizerAndFit(self.GridSizer)

        #self.Fit()

    def OnButtonCSelectAll(self, evt):
        self.cContent.SelectAll()
        #self.cContent.SetSelection(-1, -1)

    def OnButtonCClear(self, evt):
        self.cContent.Clear()

    def OnButtonCCopy(self, evt):
        self.cContent.Copy()

    def OnButtonCPaste(self, evt):
        self.cContent.Paste()

    def OnButtonC2E(self, evt):
        #获取翻译结果并保存在result中
        result = self.GoTranslator.google_translate_CtoE(self.cContent.GetValue())

        #将翻译结果回写到英文框中
        self.eContent.Clear()
        self.eContent.SetValue(result)

    def OnButtonE2C(self, evt):
        #获取翻译结果并保存在result中
        result = self.GoTranslator.google_translate_EtoC(self.eContent.GetValue())

        #将翻译结果回写到中文框中
        self.cContent.Clear()
        self.cContent.SetValue(result)

    def OnButtonESelectAll(self, evt):
        self.eContent.SelectAll()

    def OnButtonEClear(self, evt):
        self.eContent.Clear()

    def OnButtonECopy(self, evt):
        self.eContent.Copy()

    def OnButtonEPaste(self, evt):
        self.eContent.Paste()

    def OnButtonTransform(self, evt):
        engResult = self.GoTranslator.google_translate_CtoE(self.cContent.GetValue())
        chnResult = self.GoTranslator.google_translate_EtoC(engResult)

        self.eContent.Clear()
        self.eContent.SetValue(chnResult)



class GoTrFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent,  title="GoTr",
                               pos=wx.DefaultPosition,
                               size = (650, 650),
                               style = wx.DEFAULT_FRAME_STYLE | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION,
                               name="MainFrame")
        self.SetIcon(wx.Icon('gotr.ico', wx.BITMAP_TYPE_ICO))

        self.panel = GoTrPanel(self)

        #self.MainSizer =  wx.BoxSizer(wx.HORIZONTAL)
        #self.MainSizer.Add(self.panel.MainSizer)
        #self.SetSizerAndFit(self.MainSizer)

        self.SetMinSize((650, 650))
        #self.SetMaxSize((600, 650))
        self.Fit()
        self.CenterOnScreen()
        self.Show()
        self.Refresh()


class GoTrApp(wx.App):
    def OnInit(self):
        self.frame = GoTrFrame(None)
        #self.panel = GoTrPanel(self.frame)

        return True



if __name__ == "__main__":
    app = GoTrApp()
    app.MainLoop()