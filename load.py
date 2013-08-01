import os
import BaseHTTPServer as bhs

path_to_write = 'D:/Dropbox/Stephen\'s Share Folder'

class Handler(bhs.BaseHTTPRequestHandler):
  def do_GET(self):
    filename = '%s%s' % (path_to_write, self.path)
    print 'Touching file %s' % filename
    with file(filename, 'a'):
      os.utime(filename, None)
    self.send_response(200)

httpd = bhs.HTTPServer(('', 80), Handler)
httpd.serve_forever()
