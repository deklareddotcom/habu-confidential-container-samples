import subprocess
import os

MAA_URL = os.environ.get("MAA_URL", "https://sharedeus.eus.attest.azure.net/")
DEK_SECRET = os.environ.get("DEK_SECRET")
KEK_AKV_URL = os.environ.get(
    "KEK_AKV_URL", "https://aksteevaultdev7289fd6d.vault.azure.net/keys/test-sid/3d3ae438f67843b4a1ea81df179894d7")

if __name__ == "__main__":
    # wrap a key
    p = subprocess.Popen(
        [
            "./AzureAttestSKR",
            "-a",
            MAA_URL,
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

    if DEK_SECRET != unwrapped_key:
        raise ValueError(
            f"Failed to (un)wrap a symmetric key using secure key release. key={DEK_SECRET}, unwrapped_key={unwrapped_key}")

    print(f"found dek {unwrapped_key}")
