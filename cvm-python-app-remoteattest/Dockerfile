# Build stage
FROM ubuntu:20.04 AS build

WORKDIR /app

COPY maa.py /app/
COPY skr.py /app/

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt upgrade -y
RUN apt-get install -y \
    build-essential \
    libssl-dev \
    libcurl4-openssl-dev \
    libjsoncpp-dev \
    libboost-all-dev \
    nlohmann-json3-dev \
    cmake \
    wget \
    git

# Install the Azure Guest Attestation package
RUN wget https://packages.microsoft.com/repos/azurecore/pool/main/a/azguestattestation1/azguestattestation1_1.0.5_amd64.deb
RUN dpkg -i azguestattestation1_1.0.5_amd64.deb

# Clone CVM Guest Attestation Repo
RUN git clone https://github.com/Azure/confidential-computing-cvm-guest-attestation.git

# Build AttestationClient app
WORKDIR /app/confidential-computing-cvm-guest-attestation/cvm-attestation-sample-app
RUN cmake . && make && cp ./AttestationClient /app

# Build AzureAttestSKR app
WORKDIR /app/confidential-computing-cvm-guest-attestation/cvm-securekey-release-app
RUN cmake . && make && cp ./AzureAttestSKR /app

WORKDIR /app
RUN rm -rf confidential-computing-cvm-guest-attestation

#Build Python Here
ADD requirements.txt .
RUN python3 -m pip install -r requirements.txt

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python3", "maa.py"]