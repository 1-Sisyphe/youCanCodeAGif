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
