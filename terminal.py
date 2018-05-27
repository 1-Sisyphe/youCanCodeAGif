import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import random
import os
import shutil
import numpy
import exec_cmd

if os.path.exists('temp/frames/'):
    shutil.rmtree('temp/frames/')
os.makedirs('temp/frames/')

def snapshotBackground(cutscene):
    """Take a 1-frame shot from the video, used as background for the terminal"""
    command='ffmpeg -ss 00:00:00 -i {} -vf "select=eq(n\,0)" -q:v 1 -y temp/background.png'.format(cutscene)
    exec_cmd.run(command)

def find_coeffs(pa, pb):
    """used in drawTerminal to deform terminal's perspective"""
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

def drawTerminal(text, fontsize):
    """Compose an img made of a pseudo-terminal interface,
    with print outs of text and a background from the main video"""
    black = (16,16,16)
    light = (150,210,150)
    white = (190,210,230)
    x,y=(695,500)

    font_title = ImageFont.truetype("COURIER.TTF",15)
    font_text = ImageFont.truetype("COURIER.TTF",fontsize)
    img=Image.new("RGBA", (x,y),black)
    draw = ImageDraw.Draw(img)
    draw.rectangle(((4,4),(x-5,y-5)), outline = light)
    draw.rectangle(((5,5),(x-5,y-5)), outline = white)
    draw.rectangle(((9,9),(x-10,30)), outline = light)
    draw.rectangle(((10,10),(x-10,30)), outline = white)

    draw.text((11, 15),'  GIFOLATINE 3000 V1.337 - By 1-Sisyphe',light,
              font=font_title)
    draw.text((12, 16),'  GIFOLATINE 3000 V1.337 - By 1-Sisyphe',white,
              font=font_title)
    draw.text((x-50, 15),'X O',white,font=font_title)

    draw.multiline_text((10, 40),text,light,font=font_text)
    draw.multiline_text((11, 41),text,white,font=font_text)

    new_size = (800, 800)
    new_im = Image.new("RGBA", new_size)
    new_im.paste(img,(0,100))

    coeffs = find_coeffs(
        [(0, 0), (x, 0), (x, y), (0, y)],
        [(0, 0), (x, 50), (x, 450), (0, y)])

    img = new_im.transform(new_size, Image.PERSPECTIVE, coeffs,
        Image.BICUBIC)
    img = img.rotate(0.5, resample=Image.BICUBIC)
    img_finale = Image.open('temp/background.png')
    img_finale.paste(img,(340,-75),img)

    return img_finale

def cutText(text,starttext='',maxframes=None,method='char',
            randfactors=(1,1),slowfactor=1, typingchar='[]',
            repeatlast=0):
    """Take a text and cut it in a list of strings, used to animate the
    terminal frame by frame via drawFrames()"""
    cuts=[]
    n = 1
    if method == 'line':
        text = text.split('\n')
    while n < len(text):
        if method == 'line':
            cut = '\n'.join(text[:n])
        else:
            cut = text[:n]
        for r in range(1,slowfactor+1):
            cuts.append(cut)
        n += random.randint(*randfactors)
    if not maxframes:
        maxframes=len(cuts)+repeatlast
    cuts = cuts[:maxframes-repeatlast]
    for r in range(repeatlast):
        cuts.append(cuts[-1])

    cuts=[starttext+cut+typingchar for cut in cuts]
    return cuts

def drawFrames(seqname, textcuts, fontsize=16):
    """Pass each item of the textcuts list into drawTerminal() and
    save the result as a png in temp/frames, with an incremental filename
    starting by seqname."""
    for n in range(len(textcuts)):
        cut = textcuts[n]
        if cut == '': cut = ' '
        cut = cut.replace('\n',' \n ')
        img = drawTerminal(cut, fontsize)
        img.save('temp/frames/'+seqname+str(n).zfill(4)+'.png')
        n += 1

def makeVideo(seqname, framerate='24', r='24'):
    """Take all seqname png and join them in an AVI video."""
    exec_cmd.run('ffmpeg -framerate '+framerate
              +' -i temp/frames/'+seqname+'%04d.png'
              +' -c:v ffv1'
              +' -r '+r
              +' -pix_fmt yuv420p -y '
              +'temp/'+seqname+'.avi')
