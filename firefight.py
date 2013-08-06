import BaseHTTPServer as bhs
import optparse
import os
import random
import subprocess
import sys
import time

parser = optparse.OptionParser()
parser.add_option('-v', '--volume', dest='volume', default=1,
                  help='Set volume')
(options, args) = parser.parse_args(sys.argv)
print 'Volume = %s' % str(options.volume)

# Stephen's Mac
path_to_audio = '/Users/Stephen/Hideo/'
audio_command = ('afplay',)
filenames = {'/rifle': 'Rifle Shot.wav',
             '/pistol': 'Pistol Shot.wav'}
ricochet_name = 'Rico & Whiz By Single 0%d.wav'
cat_noise = 'angry4.wav'
angry_shot = 10
shots_fired = 0

# My desktop
# path_to_audio = 'D:/hideo-dev/fx'
# audio_command = ('d:/hideo-dev/fx/swavplayer.exe',)
# filenames = {'/pistol': 'barreta_m9-Dion_Stapper-1010051237.wav',
             # '/rifle': 'Shotgun_Blast-Jim_Rogers-1914772763.wav'}


class Handler(bhs.BaseHTTPRequestHandler):
  def Play(self, filename, sleep):
    time.sleep(sleep)
    command = audio_command + (filename, '-v', str(options.volume))
    subprocess.Popen(command)

  def RandomRicochet(self):
    return ricochet_name % random.randrange(1, 5)

  def AngerCat(self, sleep=0.2):
    self.Play(cat_noise, sleep)

  def Ricochet(self, sleep=0.8):
    self.Play(self.RandomRicochet(), sleep)

  def do_GET(self):
    if self.path not in filenames:
      self.send_response(500, message='wtfmate?\n\n')
      return
    audio_file = '%s/%s' % (path_to_audio, filenames[self.path])
    print 'Playing sound %s' % audio_file
    command_tuple = audio_command + (audio_file,)
    subprocess.Popen(command_tuple)
    global shots_fired
    shots_fired += 1
    if shots_fired == 1:
      self.Ricochet()
      self.AngerCat()  
      self.send_response(200, message='pwnage\n\n')
      return
    if 'pistol' in self.path:
      if random.random() < 0.5:
        self.Ricochet()  
    self.send_response(200, message='pwnage\n\n')


httpd = bhs.HTTPServer(('', 80), Handler)
httpd.serve_forever()
