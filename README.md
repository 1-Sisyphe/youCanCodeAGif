# youCanCodeAGif
Can you make an High Quality Gif (like you find on https://www.reddit.com/r/HighQualityGifs/) from A to Z only by coding?  
Yes.

Do you want to, though?  

If you have:  
- youtube-dl
- ffmpeg
- Python 3, including PIL and numpy
- Linux, because ffmpeg command lines are most likely different elsewhere

Then you can just run main_script.py, cross fingers and see what you get.
If all work fine, you are suppose to find that gif:  
Or if you changed 'lang' to 'fr' than you will find this one:  

Basically, as the gif says itself:
- the script download a video from Youtube
- cut it into interesting scenes
- create several terminal-like scenes, via terminal.py. The code you see in the terminal is the actual code from the main_script.py
- concatenates the scens from the video and from the terminal
- create the subtitles via subtitles.py and burn them into the video
- convert the video into a gif

And voilà.
But honestly, just stick to KDEnlive or your favorite video editor :)

