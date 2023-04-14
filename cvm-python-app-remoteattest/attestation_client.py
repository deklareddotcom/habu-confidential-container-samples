import os
import subprocess
import base64

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
    #jwt_from_stdout = jwt_from_stdout.replace('"', "")

    if len(jwt_from_stdout.split(".")) == 3:
        print(f"got MAA JWT token: {jwt_from_stdout}")

        if TOKEN_FILE_PATH:
            # Split the JWT token into three parts
            header, payload, signature = jwt_from_stdout.split('.')

            # Decode the Base64Url encoded strings
            decoded_header = base64.urlsafe_b64decode(header + '===').decode('utf-8')
            decoded_payload = base64.urlsafe_b64decode(payload + '===').decode('utf-8')
            decoded_signature = base64.urlsafe_b64decode(signature + '===').decode('utf-8')

            with open(TOKEN_FILE_PATH+"/maa-raw", 'w') as file:
                file.write(jwt_from_stdout)

            with open(TOKEN_FILE_PATH+"/maa-json", 'w') as file:
                file.write(f'Header:\n{decoded_header}\n')
                file.write(f'Payload:\n{decoded_payload}\n')
                file.write(f'Signature:\n{decoded_signature}\n')
        else:
            raise FileNotFoundError("TOKEN_FILE_PATH environment variable not set.")
        # decoded = jwt.decode(g, options={"verify_signature": False})
        # print (decoded)
    else:
        raise ValueError(f"MAA JWT was not formed properly: {jwt_from_stdout}")
