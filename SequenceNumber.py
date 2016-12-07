import sublime
import sublime_plugin
import sys, os

class SequenceNumberCommand(sublime_plugin.TextCommand):

  DEBUG = True

  def p(self, msg):
    if self.DEBUG:
      print(msg)

  def inputbox(self, title, msg, func_done, func_change=None, func_cancel=None):
    return self.view.window().show_input_panel(title, msg, func_done, func_change, func_cancel)

  def on_done(self, panel_string):
    self.p("on_done")

    if panel_string  == "":
      return

    self.p("restart : " +  panel_string)
    self.view.run_command(self.name(), dict(panel_string=panel_string))


  def on_change(self, panel_string):
    self.p("on_change")
    pass

  def on_cancel(self, panel_string):
    self.p("on_cancel")
    self.p(panel_string)

  def test(self, ret):
    self.p("done")

  def run_core(self, edit, panel_string):
    self.p(panel_string)

    param = self._parce(panel_string)
    if param is None:
      return

    self.insert_until_region(edit, param)


  def insert_until_region(self, edit, param):
    s = param['start']
    for region in self.view.sel():

      if region.empty():
        self.view.insert(edit, region.a, str(s))
      else:
        self.view.replace(edit, region, str(s))
      s += param['step']


  def _parce(self, str):
    # "step:1, start:0"
    ret = {}
    s = str.replace("step:","") \
           .replace("start:","") \
           .split(',')

    if len(s) == 1:
      ret['start']  = int(s[0])
    elif len(s) >= 2:
      ret['step']  = int(s[0])
      ret['start'] = int(s[1])
    return ret


  def run(self, edit, panel_string=None):

    if panel_string is None:
      # msg = "step:1, start:0"
      msg = "step:1, start:0"
      view = self.inputbox('set sequence number', msg, self.on_done, self.on_change, self.on_cancel)
    else:
      self.run_core(edit, panel_string)

