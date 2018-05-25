FROM jrottenberg/ffmpeg:3.4-scratch as ffmpeg
FROM python:3-alpine

COPY --from=ffmpeg /bin/ffmpeg /usr/local/bin/ffmpeg

# install the pip libraries required
## todo: optimize this
RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
  && apk --no-cache --update-cache add gcc gfortran jpeg-dev python python-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev \
  && pip install youtube_dl numpy Pillow

# completely optional
WORKDIR /usr/src/app

# /bin/sh so we can execute whatever command we tell it to
ENTRYPOINT ["/bin/sh", "-c"]
