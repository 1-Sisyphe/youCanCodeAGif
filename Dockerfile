FROM ubuntu
MAINTAINER George Lee <george@gleesoftware.com>

RUN apt-get update && apt-get install -y python3 python3-pip ffmpeg youtube-dl
RUN pip3 install youtube_dl numpy Pillow
RUN /usr/bin/python3 -c "import imp; imp.find_module('PIL'); import sys; sys.exit(0)" || exit 1

WORKDIR /usr/src/app
VOLUME ["/usr/src/app"]

CMD ["/usr/bin/python3", "main_script.py"]
