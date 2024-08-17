import codecs
import http.client
import http.server
import importlib
import importlib.abc
import importlib.util
import sys
import threading
import urllib.request


class ServerHandler(http.server.BaseHTTPRequestHandler):
    files = {
        'remote.py': b'def test():\n    print("Hello")'
    }

    def do_GET(self):
        filename = self.path[1:]
        content = self.files.get(filename)
        if content is None:
            self.send_error(404)
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(content)

    def do_HEAD(self):
        filename = self.path[1:]
        if filename in self.files:
            self.send_response(200)
            self.end_headers()
        else:
            self.send_error(404)


server = http.server.HTTPServer(('', 8080), ServerHandler)
thr = threading.Thread(target=server.serve_forever)
thr.start()


class NetworkLoader(importlib.abc.SourceLoader):
    def __init__(self, baseurl):
        self.baseurl = baseurl

    def get_url(self, fullname):
        return f'{self.baseurl}/{fullname}.py'

    def get_data(self, url):
        with urllib.request.urlopen(url) as f:
            return f.read()

    def get_filename(self, name):
        return f'{self.get_url(name)}'

    def exists(self, name):
        req = urllib.request.Request(self.get_url(name), method='HEAD')
        try:
            with urllib.request.urlopen(req) as f:
                pass
        except:
            return False
        return f.status == 200


class NetworkFinder(importlib.abc.MetaPathFinder):
    def __init__(self, baseurl):
        self.loader = NetworkLoader(baseurl)

    def find_spec(self, fullname, path, target=None):
        if self.loader.exists(fullname):
            return importlib.util.spec_from_loader(fullname, self.loader)


sys.meta_path.append(NetworkFinder('http://localhost:8080'))

import remote
remote.test()

server.shutdown()
thr.join()
