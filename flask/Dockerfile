FROM ubuntu:18.04

RUN apt update
RUN apt-get -y install ffmpeg
RUN apt -y install python3.8
RUN apt-get -y install python3-pip
RUN python3 -m pip install -U youtube_dl
RUN python3 -m pip install -U discord.py[voice]
RUN python3 -m pip install -U python-dotenv

WORKDIR /bot

COPY . .

CMD ["python3", "bot.py"]
