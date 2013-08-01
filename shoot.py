import os, time
from watchdog import observers
from watchdog import events
import subprocess

# path_to_watch = '/Users/Stephen/Hideo'
path_to_watch = 'D:/Dropbox/Stephen\'s Share Folder'
rifle_file = '%s/Rifle Shot.wav' % path_to_watch
pistol_file = '%s/Pistol Shot.wav' % path_to_watch
MOD_TIME = 0
SOUND_FUNC = 1


def PlaySound(file):
  # return subprocess.Popen(['afplay', file])
  print 'Play sound %s' % file


def PlayRifle():
  PlaySound(rifle_file)


def PlayPistol():
  PlaySound(pistol_file)


# 0 means this file already existed, -1 will mean it did not exist
# Otherwise it's set to the last modified time of the file
files = {'rifle1': PlayRifle,
         'rifle2': PlayRifle,
         'pistol': PlayPistol}


class ModHandler(events.FileSystemEventHandler):
  def on_modified(self, event):
    files[event.src_path.split(os.sep)[-1]]()


if __name__ == '__main__':
  handlers = []
  observer = observers.Observer()
  observer.schedule(ModHandler(), path_to_watch)
  observer.start()
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    observer.stop()
  observer.join()

# while 1:
#  time.sleep(0.01)
#  for file in files:
#    try:
#      stat = os.stat('%s/%s' % (path_to_watch, file))
#    except OSError:
#      files[file][MOD_TIME] = -1
#      continue # No file is ok, we will wait for it
#    last_modified = files[file][MOD_TIME]
#    files[file][MOD_TIME] = stat.st_mtime
#    if last_modified != files[file][MOD_TIME]:
#      if last_modified != 0:  # It's -1 if the file is new, otherwise last modified time
#        files[file][SOUND_FUNC]()
