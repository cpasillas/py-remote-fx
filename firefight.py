import BaseHTTPServer as bhs
import optparse
import random
import subprocess
import sys
import time
import ConfigParser

parser = optparse.OptionParser()
parser.add_option('-v', '--volume', dest='volume', default=1,
                  help='Set volume')
parser.add_option('-c', '--config', dest='config', default='ff.cfg',
                  help='Relative path to a config file')
(options, args) = parser.parse_args(sys.argv)

print 'Volume = %s' % str(options.volume)

config = ConfigParser.RawConfigParser()

try:
  with open(options.config): pass
  print 'Using config file: %s' % options.config
  config.read(options.config)
except IOError:
  print 'ERROR: Could not find config file: %s' % options.config

audio_path = config.get('ff','audio_path')
audio_command = (config.get('ff','audio_command'),)
guns = {'rifle': config.get('guns','rifle'),
        'pistol': config.get('guns','pistol')}
ricochet_name = config.get('misc','ricochet_name')
cat_noise = config.get('misc','cat_noise')
shots_fired = 0


class Handler(bhs.BaseHTTPRequestHandler):


  def Play(self, filename, sleep):
    time.sleep(sleep)
    file_path = '%s/%s' % (audio_path, filename)

    try:
      with open(file_path): pass
      self.PlaySound(file_path)
    except IOError:
      print 'ERROR: Could not find sound file: %s' % file_path


  def PlaySound(self, file_path):
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


  ##
  # Send an HTTP GET request like "http://localhost/pistol", where "pistol"
  # is one of `gun_type`.
  def do_GET(self):
    global shots_fired
    gun_type = self.path[1:7]
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

# Start the server!  Ctrl+C to exit.
try:
  httpd.serve_forever()
except KeyboardInterrupt:
  print '\n\nTotal shots fired: %s\n' % shots_fired
