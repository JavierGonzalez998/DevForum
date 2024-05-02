FROM ubuntu:latest

#Setting Environment
ENV PIP_BREAK_SYSTEM_PACKAGES 1
RUN apt-get update && apt-get install -y -q --no-install-recommends \
        apt-transport-https \
        build-essential \
        ca-certificates \
        curl \
        git \
        libssl-dev \
        wget \
    && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "--login", "-c"]
RUN touch ~/.bashrc && chmod +x ~/.bashrc
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
RUN . ~/.nvm/nvm.sh && source ~/.bashrc && nvm install 20.11.1

RUN apt-get update -y
RUN apt-get upgrade
RUN yes yes |apt-get install unzip

#Installing Python
RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip \
    python3.12-venv

#Setting Build Project    
WORKDIR /app
COPY . .

RUN python3 -m venv /app/.venv_docker
RUN . /app/.venv_docker/bin/activate

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN reflex db init
RUN reflex db makemigrations
RUN reflex db migrate 

CMD reflex run --env prod --no-zip
