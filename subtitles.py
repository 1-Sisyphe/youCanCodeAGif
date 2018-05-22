import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import os
import shutil

if os.path.exists('temp/sub/'):
    shutil.rmtree('temp/sub/')
os.makedirs('temp/sub/')

def makePngSub(text, color, position, fontsize, filename):
    """Turn a text into a png"""
    img = Image.new('RGBA',(480, 360))
    x,y = position.split(',')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Ubuntu-B.ttf",30)
    w, h = draw.multiline_textsize(text, font=font)
    x = float(x) - w/2
    y = float(y) - h/2
    for i in range(1,6):
        draw.multiline_text((x+i,y+i), text, fill=(0,0,0), font=font, align='center')
    draw.multiline_text((x,y), text, fill=color, font=font, align='center')
    filename = 'temp/sub/{}.png'.format(filename)
    img.save(filename, 'PNG')
    return filename


def subVideo(gifconf,inputvid,outputvid):
    """Take a list a subtitles, make each png with makePngSub()
    and add the pngs to the video at the given intervals"""
    subs = gifconf['subs']
    n=1
    subfiles=[]
    for sub in subs:
        subfile = makePngSub(text=sub['text'],color=sub['color'],
                             position=sub['pos'],fontsize=sub['fontsize'],filename=str(n))
        subfiles.append(subfile)
        n+=1

    def writeFilterblocks(subs):
        """write the complex filter to chain-add all the png in one shot"""
        n = 0
        filter_blocks=[]
        for sub in subs:
            timing = sub['time']
            blocks=['']*4
            if n==0:
                blocks[0]='"[0:v]'
            else:
                blocks[0]='[tmp]'
            n+=1
            blocks[1]='['+str(n)+':v]'
            blocks[2]="overlay=enable='between(t,{})'".format(timing)
            if n!=len(subs):
                blocks[3]=' [tmp]; '
            else:
                blocks[3]='"'
            filter_blocks+=blocks
        return filter_blocks

    inputblocks = ['ffmpeg -i '+inputvid]+['-i '+subfile for subfile in subfiles]
    inputstr = ' '.join(inputblocks)
    filterstr = '-filter_complex '+''.join(writeFilterblocks(subs))
    #outputstr = '-y '+ outputvid
    outputstr = '-y -c:v ffv1 '+ outputvid
    command = inputstr+' '+filterstr+' '+outputstr
    os.system(command)
