FROM ubuntu:22.04


WORKDIR /chatbot_toolkit

COPY requirements.txt .

RUN apt-get update && apt-get -y upgrade \
    && apt-get install -y python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt
    
ENTRYPOINT [ "bash" ]