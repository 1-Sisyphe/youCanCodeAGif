#!/usr/bin/env python3

# import built-in libs
import argparse
import os
import yaml
# import local libs
import meta
import subtitles
import terminal

def parseargs():
    parser = argparse.ArgumentParser(description='This script makes gifs!')
    parser.add_argument('-g', '--gifname', required=True,
                        help='Which gif in the config to make.')
    args = parser.parse_args()
    return args


def main():
    args = parseargs()
    if not os.path.exists('temp'):
        os.makedirs('temp')
    #Download youtube's video via youtube-dl
    url = 'https://www.youtube.com/watch?v=TS_59Y7bYoA'
    os.system(r'youtube-dl -f 136 -o temp/in.mp4 '+ url)
    
    invid = 'temp/in.mp4'
    
    #cut the scenes used in the gif
    cuttimes =[
        ("00:00:40.5","00:00:57.0"),
        ("00:01:00.7","00:01:04.5"),
        ("00:01:13.5","00:01:15.2"),
        ("00:01:20.3","00:01:31.5"),
        ("00:01:38.8","00:01:40.9"),
        ("00:01:47.2","00:01:48.3"),
        ("00:01:50.6","00:01:53.3"),
        ("00:01:55.9","00:02:00.0"),
        ("00:00:27.0","00:00:27.1")
        ]
    n = 1
    cuts=[]
    for cut in cuttimes:
        outvid = './temp/cut'+str(n)+'.avi'
        cuts.append(outvid)
        n += 1
        command = ("ffmpeg -i "+ invid
        +" -ss "+cut[0]
        +' -filter:v "crop=1280:540:0:90"'
        +" -c:v ffv1"
        +" -to "+cut[1]
        +' -r 24 -y '
        +outvid)
        os.system(command)
    
    #create the terminal scenes
    #take a snapshot used as background for the terminal
    terminal.snapshotBackground('temp/cut9.avi')
    #open this code as a string
    script_lines = [line.rstrip('\n') for line in open('main_script.py')]
    #youtube-dl terminal scene
    code_dlvideo_1 = '\n'.join(script_lines[5:10])
    code_dlvideo_2 = '\n'.join(script_lines[10:22])
    code_dlvideo_3 = '\n'.join(script_lines[22:26])
    textcuts = terminal.cutText(code_dlvideo_1,method='char',randfactors=(1,3),repeatlast=10)
    textcuts += terminal.cutText(code_dlvideo_2,starttext=code_dlvideo_1+'\n',
                                  method='line',randfactors=(1,1),slowfactor=2,repeatlast=10)
    textcuts += terminal.cutText(code_dlvideo_3,starttext=code_dlvideo_1+'\n'+code_dlvideo_2+'\n',
                                  method='char',randfactors=(1,3),repeatlast=24)
    terminal.drawFrames(seqname="dlvideo", textcuts=textcuts)
    terminal.makeVideo(seqname="dlvideo")
    
    #add subtitles scene
    code_subs = '\n'.join(script_lines[134:159])
    textcuts = terminal.cutText(code_subs,method='line',slowfactor=3,repeatlast=24,typingchar='')
    terminal.drawFrames(seqname="subs", textcuts=textcuts, fontsize=15)
    terminal.makeVideo(seqname="subs")
    
    #add concat scene
    code_concat = '\n'.join(script_lines[110:130])
    textcuts = terminal.cutText(code_concat,method='line',slowfactor=4,repeatlast=24,typingchar='')
    terminal.drawFrames(seqname="concat", textcuts=textcuts, fontsize=16)
    terminal.makeVideo(seqname="concat")
    
    #add gifthat scene
    code_gif_that = '\n'.join(script_lines[193:205])
    textcuts = terminal.cutText(code_gif_that,method='char',randfactors=(1,3),repeatlast=24)
    terminal.drawFrames(seqname="gifthat", textcuts=textcuts, fontsize=16)
    terminal.makeVideo(seqname="gifthat")
    
    #add blackscreen scene
    empty_screen = """\n\n"""
    textcuts = terminal.cutText(empty_screen,method='char',randfactors=(1,1),repeatlast=24,typingchar='')
    terminal.drawFrames(seqname="empty_screen", textcuts=textcuts, fontsize=16)
    terminal.makeVideo(seqname="empty_screen")
    
    #add "add a touch meta" scene
    code_add_meta = '\n'.join(script_lines[101:108])
    textcuts = terminal.cutText(code_add_meta,method='line',slowfactor=6,repeatlast=24,typingchar='')
    terminal.drawFrames(seqname="add_meta", textcuts=textcuts)
    terminal.makeVideo(seqname="add_meta")
    
    #add a touch of meta
    meta_code = meta.just_a_touch(subtle_level=9000)
    meta_cuts = terminal.cutText(meta_code,method='line',
            slowfactor=1,repeatlast=10,typingchar='')
    terminal.drawFrames(seqname="meta",
                    textcuts=meta_cuts,fontsize=14)
    terminal.makeVideo(seqname="meta")
    
    #concatenate the scenes
    to_concat =[
        "cut1.avi",
        "dlvideo.avi",
        "cut5.avi",
        "subs.avi",
        "cut4.avi",
        "add_meta.avi",
        "cut3.avi",
        "concat.avi",
        "cut7.avi",
        "gifthat.avi",
        "empty_screen.avi",
        "meta.avi",
        "cut8.avi"
    ]
    with open('list.txt','w') as f:
        for vid in to_concat:
            print("file 'temp/"+vid+"'",file=f)
    os.system('ffmpeg -f concat -i list.txt'+
              ' -c copy -y concat_nosub.avi')
    
    #create the subtitles
    white=(255,255,255)
    yellow=(255,233,155)
    
    #add the subtitles
    if lang=='fr':
        subtitles.subVideo(subs=subs_fr,inputvid='concat_nosub.avi',outputvid='final.avi')
    else:
        subtitles.subVideo(subs=subs_en,inputvid='concat_nosub.avi',outputvid='final.avi')
    
    #gif THAT
    os.system('ffmpeg -y -i '+
              'final.avi -vf '+
              'fps=24,scale=1080:-1:'+
    'flags=lanczos,palettegen palette.png')
    
    os.system('ffmpeg  -i final.avi '+
              '-i palette.png -filter_complex '+
    '"fps=24,scale=1080:-1:flags=lanczos[x];[x][1:v]paletteuse" '+
    
                    'you_can_code_a.gif')

if __name__ == "__main__":
    main()
