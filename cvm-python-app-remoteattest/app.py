import subprocess
import json

# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = "0.0.0.0"
PORT = 8081


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        p = subprocess.Popen(
            ["./AttestationClient"],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            close_fds=True,
        )

        g = str(p.stdout.read())
        g = g.replace("b'", "")
        g = g.replace("'", "")
        res = g.split(".")
        l = len(res)

        if l == 3:
            # now we have a fully formed JWT perform the decode and split
            print("JWT Token length Found ", l)
            # decoded = jwt.decode(g, options={"verify_signature": False})
            # print (decoded)
            self.wfile.write(json.dumps(g).encode("utf-8"))
        else:
            self.wfile.write(
                json.dumps({"error": "JWT was not formed properly %s"}, g).encode(
                    "utf-8"
                )
            )


if __name__ == "__main__":
    webServer = HTTPServer((HOST_NAME, PORT), MyServer)
    print("Server started http://%s:%s" % (HOST_NAME, PORT))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
