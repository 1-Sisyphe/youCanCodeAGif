# youCanCodeAGif
Could you make a High Quality Gif (like what you find on https://www.reddit.com/r/HighQualityGifs) from A to Z only by coding?  
Yes.

Do you want to, though?  

If yes, then make sure that you have:  
- youtube-dl
- ffmpeg
- Python 3, including PIL and numpy
- Linux, because ffmpeg command lines are most likely different on other OS

Then you can just run main_script.py, cross fingers and see what you get.  

If all work fine, you are suppose to find that gif: https://imgur.com/3tFIv4d.gifv  
Or if you changed 'lang' to 'fr' in main_script.py, you will find this one: https://i.imgur.com/Gg7Cz3B.gifv  

Basically, as the gif says:
- the script download a video from Youtube
- cut it into interesting scenes
- create several terminal-like scenes, via terminal.py. The code you see in the terminal is the actual code from the main_script.py
- concatenates the scenes from the video and from the terminal
- create the subtitles via subtitles.py and burn them into the video
- convert the video into a gif

And voilà.  
But honestly, you might prefer to just stick to KDEnlive or your favorite video editor :)

## Dockerized

You can leverage Docker containers to code up a GIF. The only requirement you need is [Docker](https://docs.docker.com/install/).

### Run the docker image with this repository

To run the Docker container in an environment specific to this repository:

```
# clone this repo
$ git clone https://github.com/1-Sisyphe/youCanCodeAGif

# make sure the repo is your current working directory
$ cd youCanCodeAGif

# docker run the docker image (it mounts the cwd to "/usr/src/app")
$ docker run --rm -ti -v `pwd`:/usr/src/app slikshooz/youcancodeagif:latest "python main_script.py"
```

### Create dockerimage

For those of you who would rather build it themselves, here is a way to use the same Dockerfile

```
# Build the image locally
$ docker build -t youcancodeagif .
```
