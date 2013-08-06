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

audio_path = '/Users/Stephen/Hideo/'
audio_command = ('afplay',)
guns = {'rifle': 'Rifle Shot.wav',
        'pistol': 'Pistol Shot.wav'}
ricochet_name = 'Rico & Whiz By Single 0%d.wav'
cat_noise = 'angry4.wav'
shots_fired = 0


class Handler(bhs.BaseHTTPRequestHandler):
  def Play(self, filename, sleep):
    time.sleep(sleep)
    file_path = '%s/%s' % (audio_path, filename)
    print 'Playing sound %s' % file_path 
    command = audio_command + (file_path, '-v', str(options.volume))
    subprocess.Popen(command)

  def RandomRicochet(self):
    return ricochet_name % random.randrange(1, 5)

  def AngerCat(self, sleep=0.2):
    self.Play(cat_noise, sleep)

  def Ricochet(self, sleep=0.8):
    self.Play(self.RandomRicochet(), sleep)

  def Shoot(self, type):
    if type not in guns:
      return False
    self.Play(guns[type], 0)
    return True

  def do_GET(self):
    global shots_fired
    gun_type = self.path[1:0]
    shot_fired = self.Shoot(gun_type)
    if not shot_fired:
      self.send_response(500, message='wtfmate?\n\n')
      return
    shots_fired += 1
    if shots_fired == 1:
      self.Ricochet()
      self.AngerCat()  
    elif 'pistol' in self.path:
      if random.random() < 0.5:
        self.Ricochet()  
    self.send_response(200, message='pwnage\n\n')


httpd = bhs.HTTPServer(('', 80), Handler)
httpd.serve_forever()
