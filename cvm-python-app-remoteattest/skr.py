import subprocess
import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import uuid

MAA_URL = os.environ.get("MAA_URL", "https://sharedeus.eus.attest.azure.net")
HOST_NAME = "0.0.0.0"
PORT = 8081


class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        payload = json.loads(body.decode("utf-8"))

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        # access payload parameters
        secret = payload.get('s', None)
        kek_key_url = payload.get('k', None)
        nonce = payload.get('n', str(uuid.uuid4()))

        if self.path == '/wrap':
            # wrap a key
            p = subprocess.Popen(
                [
                    "./AzureAttestSKR",
                    "-a",
                    MAA_URL,
                    "-n",
                    nonce,
                    "-k",
                    kek_key_url,
                    "-c",
                    "sp",
                    "-s",
                    secret,
                    "-w"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                close_fds=True,
            )
            wrapped_key = str(p.stdout.read())
            wrapped_key = wrapped_key.replace("b'", "")
            wrapped_key = wrapped_key.replace("\\n", "")

            self.wfile.write(
                json.dumps({"wrapped_key": wrapped_key}).encode("utf-8")
            )
        elif self.path == '/unwrap':
            # unwrap a key
            p = subprocess.Popen(
                [
                    "./AzureAttestSKR",
                    "-a",
                    MAA_URL,
                    "-n",
                    nonce,
                    "-k",
                    kek_key_url,
                    "-c",
                    "sp",
                    "-s",
                    secret,
                    "-u"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                close_fds=True,
            )
            unwrapped_key = str(p.stdout.read())
            unwrapped_key = unwrapped_key.replace("b'", "")
            unwrapped_key = unwrapped_key.replace("\\n", "")

            self.wfile.write(
                json.dumps({"unwrapped_key": unwrapped_key}).encode("utf-8")
            )
        else:
            raise NotImplementedError(f'{self.path} url is not implemented')


if __name__ == "__main__":
    webServer = HTTPServer((HOST_NAME, PORT), MyServer)
    print("Server started http://%s:%s" % (HOST_NAME, PORT))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
