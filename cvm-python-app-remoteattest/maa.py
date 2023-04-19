import os
import subprocess
import base64
import uuid

TOKEN_FILE_PATH = os.environ.get("TOKEN_FILE_PATH")
CRQR_ID = os.environ.get("CRQR_ID", str(uuid.uuid4()))

if __name__ == "__main__":
    p = subprocess.Popen(
        [
            "./AttestationClient",
            "-a",
            "https://sharedeus.eus.attest.azure.net/",
            "-n",
            CRQR_ID,
            "-o",
            "TOKEN"
        ],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        close_fds=True,
    )

    jwt_from_stdout = str(p.stdout.read())
    jwt_from_stdout = jwt_from_stdout.replace("b'", "")
    jwt_from_stdout = jwt_from_stdout.replace("'", "")

    if len(jwt_from_stdout.split(".")) == 3:
        print(f"got MAA JWT token: {jwt_from_stdout}")

        if TOKEN_FILE_PATH:
            # Split the JWT token into three parts
            _, payload, _ = jwt_from_stdout.split(".")

            # Decode the Base64Url encoded strings
            # decoded_header = base64.urlsafe_b64decode(header + '===').decode('utf-8')
            decoded_payload = base64.urlsafe_b64decode(payload + "===").decode("utf-8")

            with open(TOKEN_FILE_PATH + "/maa-raw.txt", "w") as file:
                file.write(jwt_from_stdout)

            with open(TOKEN_FILE_PATH + "/maa.json", "w") as file:
                file.write(decoded_payload)
        else:
            raise FileNotFoundError("TOKEN_FILE_PATH environment variable not set.")
    else:
        raise ValueError(f"Error in fetching MAA token: {jwt_from_stdout}")
