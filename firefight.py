import BaseHTTPServer as bhs
import os
import subprocess

# Stephen's Mac
# path_to_audio = '/Users/Stephen/Hideo/'
# audio_command = ('afplay',)
# filenames = {'pistol': '',
#              'rifle': ''}

# My desktop
path_to_audio = 'D:/hideo-dev/fx'
audio_command = ('d:/hideo-dev/fx/swavplayer.exe',)
filenames = {'/pistol': 'barreta_m9-Dion_Stapper-1010051237.wav',
             '/rifle': 'Shotgun_Blast-Jim_Rogers-1914772763.wav'}


class Handler(bhs.BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path not in filenames:
      self.send_response(500, message='wtfmate?')
      return
    audio_file = '%s/%s' % (path_to_audio, filenames[self.path])
    print 'Playing sound %s' % audio_file
    command_tuple = audio_command + (audio_file,)
    print command_tuple
    subprocess.Popen(command_tuple)
    self.send_response(200, message='pwnage')


httpd = bhs.HTTPServer(('', 80), Handler)
httpd.serve_forever()
