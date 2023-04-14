import json
import os
import subprocess

TOKEN_FILE_PATH = os.environ.get("TOKEN_FILE_PATH")

if __name__ == "__main__":
    p = subprocess.Popen(
        ["./AttestationClient"],
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
            with open(TOKEN_FILE_PATH, 'w') as file:
                file.write(json.dumps(jwt_from_stdout))
        else:
            raise FileNotFoundError("TOKEN_FILE_PATH environment variable not set.")
        # decoded = jwt.decode(g, options={"verify_signature": False})
        # print (decoded)
    else:
        raise ValueError(f"MAA JWT was not formed properly: {jwt_from_stdout}")
