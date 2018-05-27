from typing import List, Any


lang='en'

import logging
import os
import exec_cmd

func_completed = []  # type: List[str]
logger = logging.getLogger(__file__)
invid = 'temp/in.mp4'

def load_completed():
    global func_completed
    logger.info("Loading completed functions")
    if os.path.exists('temp/completed_funcs.txt'):
        func_completed = [line.rstrip() for line in open('temp/completed_funcs.txt')]
    logger.info("Found completed funcs: " + func_completed.__str__())

def mark_completed(func):
    global func_completed
    func_completed.append(func.__name__)
    with open('temp/completed_funcs.txt','w') as file:
        for func_name in func_completed:
           print(func_name, file=file)

def execute(func):
    global func_completed
    if not any(func.__name__ in s for s in func_completed):
        func()
        mark_completed(func)

def setup_logging():
    logging.basicConfig(format='[%(name)s] %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    logger.info("Started logging")

def setup_directories():
    logger.info('Creating directories')
    if not os.path.exists('temp'):
        os.makedirs('temp')

    import shutil
    for s in ['COURIER.TTF', 'main_script.py']:
        shutil.copy2(s, 'temp/' + s)

    if not os.path.exists('out'):
        os.makedirs('out')

def download_youtube():
    logger.info('Download youtube video via youtube-dl')
    url = 'https://www.youtube.com/watch?v=TS_59Y7bYoA'

    exec_cmd.run(r'youtube-dl -f 136 -o '+invid+' '+ url)

def cut_scenes():
    global invid
    logger.info('cut the scenes used in the gif')
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
        outvid = 'temp/cut'+str(n)+'.avi'
        cuts.append(outvid)
        n += 1
        command = ("ffmpeg -i "+ invid
        +" -ss "+cut[0]
        +' -filter:v "crop=1280:540:0:90"'
        +" -c:v ffv1"
        +" -to "+cut[1]
        +' -r 24 -y '
        +outvid)
        exec_cmd.run(command)

def create_custom_scenes():
    logger.info('create the terminal scenes')
    import terminal
    logger.info('take a snapshot used as background for the terminal')
    terminal.snapshotBackground('temp/cut9.avi')
    logger.info('open this code as a string')
    import codecs
    script_lines = [line.rstrip('\n') for line in codecs.open('temp/main_script.py', 'r', 'utf-8')]
    logger.info('youtube-dl terminal scene')
    code_dlvideo_1 = '\n'.join(script_lines[50:54])
    code_dlvideo_2 = '\n'.join(script_lines[58:69])
    code_dlvideo_3 = '\n'.join(script_lines[70:73])
    textcuts = terminal.cutText(code_dlvideo_1,method='char',randfactors=(1,3),repeatlast=10)
    textcuts += terminal.cutText(code_dlvideo_2,starttext=code_dlvideo_1+'\n',
                                  method='line',randfactors=(1,1),slowfactor=2,repeatlast=10)
    textcuts += terminal.cutText(code_dlvideo_3,starttext=code_dlvideo_1+'\n'+code_dlvideo_2+'\n',
                                  method='char',randfactors=(1,3),repeatlast=24)
    terminal.drawFrames(seqname="dlvideo", textcuts=textcuts)
    terminal.makeVideo(seqname="dlvideo")

    logger.info('add subtitles scene')
    if lang=='fr':
        code_subs = '\n'.join(script_lines[213:237])
    else:
        code_subs = '\n'.join(script_lines[187:212])
    textcuts = terminal.cutText(code_subs,method='line',slowfactor=3,repeatlast=24,typingchar='')
    terminal.drawFrames(seqname="subs", textcuts=textcuts, fontsize=15)
    terminal.makeVideo(seqname="subs")

    logger.info('add concat scene')
    code_concat = '\n'.join(script_lines[160:180])
    textcuts = terminal.cutText(code_concat,method='line',slowfactor=4,repeatlast=24,typingchar='')
    terminal.drawFrames(seqname="concat", textcuts=textcuts, fontsize=16)
    terminal.makeVideo(seqname="concat")

    logger.info('add gifthat scene')
    code_gif_that = '\n'.join(script_lines[246:256])
    textcuts = terminal.cutText(code_gif_that,method='char',randfactors=(1,3),repeatlast=24)
    terminal.drawFrames(seqname="gifthat", textcuts=textcuts, fontsize=16)
    terminal.makeVideo(seqname="gifthat")

    logger.info('add blackscreen scene')
    empty_screen = """\n\n"""
    textcuts = terminal.cutText(empty_screen,method='char',randfactors=(1,1),repeatlast=24,typingchar='')
    terminal.drawFrames(seqname="empty_screen", textcuts=textcuts, fontsize=16)
    terminal.makeVideo(seqname="empty_screen")

    logger.info('add "add a touch meta" scene')
    if lang=='fr':
        code_add_meta = '\n'.join(script_lines[144:149])
    else:
        code_add_meta = '\n'.join(script_lines[151:156])
    textcuts = terminal.cutText(code_add_meta,method='line',slowfactor=6,repeatlast=24,typingchar='')
    terminal.drawFrames(seqname="add_meta", textcuts=textcuts)
    terminal.makeVideo(seqname="add_meta")

    logger.info('add a touch of meta')
    import meta
    if lang=='fr':
        meta_code = meta.juste_un_doigt(oss=117)
        meta_cuts = terminal.cutText(meta_code,method='line',
                slowfactor=1,repeatlast=10,typingchar='')
        terminal.drawFrames(seqname="meta",
                        textcuts=meta_cuts,fontsize=5)
        terminal.makeVideo(seqname="meta")
    else:
        meta_code = meta.just_a_touch(subtle_level=9000)
        meta_cuts = terminal.cutText(meta_code,method='line',
                slowfactor=1,repeatlast=10,typingchar='')
        terminal.drawFrames(seqname="meta",
                        textcuts=meta_cuts,fontsize=14)
        terminal.makeVideo(seqname="meta")


def concat_scenes():
    logger.info('concatenate the scenes')
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
    with open('temp/list.txt','w') as f:
        for vid in to_concat:
            print("file '"+vid+"'",file=f)
    exec_cmd.run('ffmpeg -f concat -i temp/list.txt'+
              ' -c copy -y temp/concat_nosub.avi')

def create_subtiles():
    logger.info('create the subtitles')
    import subtitles
    white=(255,255,255)
    yellow=(255,233,155)
    subs_en =[
        ["You can't just code a gif...",yellow,(830,420),'1,2.5'],
        ["Of course I can.",white,(800,420),'3,4'],
        ["I'm going to code",white,(800,420),'4.1,7'],
        ["this entire gif.",white,(800,480),'5.2,7'],
        ["And I'll give you the\n source in the comments.",
         white,(800,450),'7.1,10'],
        ['"You can\'t code a gif..."',white,(820,420),'11.8,13'],
        ["It's nothing more than",white,(800,420),'14,16'],
        ["a huge waste of time!",white,(800,480),'15,16'],
        ["First: I download our video\nfrom Youtube.",
         white,(640,450),'17,19.5'],
        ["Then I separate each scene...",
         white,(640,480),'20,23'],
        ["Now I add our dialogs...",white,(640,480),'24,25.4'],
        ["Let me see...",yellow,(640,480),'30.5,32.5'],
        ["Can you add a bit of META?",yellow,(640,480),'32.9,34.5'],
        ["I will put just a touch...",white,(640,420),'35,40'],
        ["Very subtle, no one will see it.",white,(640,480),'37,40'],
        ["Now I concatenate the scenes....",white,(640,480),'45.6,47.6'],
        ["And to finish...",white,(640,420),'49.6,52'],
        ["GIF THAT!",white,(640,480),'50.2,52'],
        ["I AM",white,(640,400),'62.8,64.6'],
        ["INVINCIBLE!!!",white,(640,460),'63.3,64.6']

    ]
    subs_fr =[
        ["On ne peut pas\ncoder un gif...",yellow,(840,420),'1,2.5'],
        ["Bien sûr qu'on peut.",white,(800,420),'3,4'],
        ["Je vais te coder",white,(800,420),'4.1,7'],
        ["ce gif de A à Z.",white,(800,480),'5.2,7'],
        ["Et je te mets le code\n dans les commentaires.",
         white,(800,450),'7.1,10'],
        ['"On ne peut pas\ncoder un gif..."',white,(840,420),'11.8,13'],
        ["C'est rien de plus",white,(800,420),'14,16'],
        ["qu'une énorme perte de temps !",white,(800,480),'15,16'],
        ["Premièrement: je télécharge la\n vidéo depuis Youtube.",
         white,(640,450),'17,19.5'],
        ["Ensuite je découpe les scènes...",
         white,(640,480),'20,23'],
        ["J'ajoute nos dialogues...",white,(640,480),'23.5,25.4'],
        ["Attend voir...",yellow,(640,480),'30.3,32'],
        ["Tu peux ajouter un peu de META ?",yellow,(640,480),'32.5,34.5'],
        ["OK mais juste une pincée...",white,(640,420),'35,40'],
        ["Très subtil, personne ne le verra.",white,(640,480),'37,40'],
        ["Je colle les scènes bout à bout...",white,(640,480),'45,47'],
        ["Et pour finir...",white,(640,420),'49.1,51.6'],
        ["GIF MOI ÇA !",white,(640,480),'50,51.6'],
        ["JE SUIS",white,(640,400),'62.8,64.6'],
        ["INVINCIBLE !!!",white,(640,460),'63.3,64.6']
    ]

    #add the subtitles
    if lang=='fr':
        subtitles.subVideo(subs=subs_fr,inputvid='temp/concat_nosub.avi',outputvid='temp/final.avi')
    else:
        subtitles.subVideo(subs=subs_en,inputvid='temp/concat_nosub.avi',outputvid='temp/final.avi')

def generate_gif():
    logger.info('gif THAT')
    exec_cmd.run('ffmpeg -y -i '+
              'temp/final.avi -vf '+
              'fps=24,scale=1080:-1:'+
    'flags=lanczos,palettegen temp/palette.png')

    exec_cmd.run('ffmpeg  -i temp/final.avi '+
              '-i temp/palette.png -filter_complex '+
    '"fps=24,scale=1080:-1:flags=lanczos[x];[x][1:v]paletteuse" '+

                    'out/you_can_code_a.gif')

def main():
    setup_logging()
    load_completed()
    setup_directories()
    execute(download_youtube)
    execute(cut_scenes)
    execute(create_custom_scenes)
    execute(concat_scenes)
    execute(create_subtiles)
    execute(generate_gif)


if __name__ == "__main__":
    main()