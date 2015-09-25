import SimpleHTTPServer, SocketServer
import urlparse
import sys

PORT = 8080

tv = None
try:
    import cec
    cec.init()
    tv = cec.Device(0)
    print("CEC exist")
except ImportError:
    print("CEC not exist - you must install it!")

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):

       # Parse query data & params to find out what was passed
       parsedParams = urlparse.urlparse(self.path)
       queryParsed = urlparse.parse_qs(parsedParams.query)

       # request is either for a file to be served up or our test
       if parsedParams.path == "/powerOn":
          self.power(True)
       elif parsedParams.path == "/PowerOff":
           self.power(False)
       else:
          # Default to serve up a local file 
          self.not_found(parsedParams.path)

    def power(self, state):
        if tv:
            try:
                if state:
                    tv.power_on()
                else:
                    tv.standby();
            except:
                self.error("Unexpected error")

        else:
            self.error("Error: CEC not exist")

    def send_ok(self, message):
       self.send_response(200)
       self.send_header('Content-Type', 'text/html')
       self.end_headers()

       self.wfile.write(message)
       self.wfile.close()

    def error(self, message):
       self.send_response(400)
       self.send_header('Content-Type', 'text/html')
       self.end_headers()

       self.wfile.write(message)
       self.wfile.close()

    def not_found(self, path):

       self.send_response(404)
       self.send_header('Content-Type', 'text/html')
       self.end_headers()

       self.wfile.write("Function '%s' not found" % path)
       self.wfile.close()

Handler = MyHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()