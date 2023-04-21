import subprocess
import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import uuid

MAA_URL = os.environ.get("MAA_URL", "https://sharedeus.eus.attest.azure.net")
HOST_NAME = "0.0.0.0"
PORT = 8081


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        # access query parameters
        secret = query_params.get('secret', [None])[0]
        kek_key_url = query_params.get('kek_key_url', [None])[0]
        nonce = query_params.get('nonce', [str(uuid.uuid4())])[0]

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
                    "-s",
                    secret,
                    "-w"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                close_fds=True,
            )
            wrapped_key = str(p.stdout.read())
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
                    "-s",
                    secret,
                    "-u"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                close_fds=True,
            )
            unwrapped_key = str(p.stdout.read())

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
