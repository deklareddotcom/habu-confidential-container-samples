import subprocess
import os
import time
import uuid

MAA_URL = os.environ.get("MAA_URL", "https://sharedeus.eus.attest.azure.net/")
DEK_SECRET = os.environ.get("DEK_SECRET")
KEK_AKV_URL = os.environ.get("KEK_AKV_URL")
NONCE = os.environ.get("NONCE", str(uuid.uuid4()))

if __name__ == "__main__":
    # wrap a key
    p = subprocess.Popen(
        [
            "./AzureAttestSKR",
            "-a",
            MAA_URL,
            "-n",
            NONCE,
            "-k",
            KEK_AKV_URL,
            "-s",
            DEK_SECRET,
            "-w"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        close_fds=True,
    )
    wrapped_key = str(p.stdout.read())

    # unwrap a key
    p = subprocess.Popen(
        [
            "./AzureAttestSKR",
            "-a",
            MAA_URL,
            "-n",
            NONCE,
            "-k",
            KEK_AKV_URL,
            "-s",
            wrapped_key,
            "-u"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        close_fds=True,
    )
    unwrapped_key = str(p.stdout.read())

    time.sleep(3600)

    if DEK_SECRET != unwrapped_key:
        raise ValueError(
            f"Failed to (un)wrap a symmetric key using secure key release. key={DEK_SECRET}, wrapped_key={wrapped_key}, unwrapped_key={unwrapped_key}")

    print(f"found dek {unwrapped_key}")
