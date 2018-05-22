#!/usr/bin/env python3

# import built-in libs
import argparse
import os
import yaml
# import local libs
import meta
import subtitles
import terminal

def debug_out(outstring):
    """print outstring if debug flag is set."""
    if args.debug:
        print('DEBUG: {}'.format(outstring))


def parse_args():
    parser = argparse.ArgumentParser(description='This script makes gifs!')
    parser.add_argument('-g', '--gifconf', default='gifs/you_can_code_a_gif_en.yaml',
                        help='Path to gif yaml to make. ex: gifs/you_can_code_a_gif_en.yaml')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable debug output')
    args = parser.parse_args()
    return args


def main(args):
    debug_out(args)
    with open(args.gifconf, "r") as f:
        config = yaml.load(f)
    debug_out(config)
    if not os.path.exists('temp'):
        os.makedirs('temp')
    #Download youtube's video via youtube-dl
    url = config['link']
    debug_out(url)
    os.system(r'youtube-dl -f mp4 -o temp/in.mp4 '+ url)
    
    invid = 'temp/in.mp4'
    
    n = 1
    cuts=[]
    debug_out(config['cuttimes'])
    for cut in config['cuttimes']:
        debug_out('start: {}'.format(cut['start']))
        debug_out('end: {}'.format(cut['end']))
        outvid = './temp/cut'+str(n)+'.avi'
        cuts.append(outvid)
        n += 1
        command = ('ffmpeg -i {0} '
                   '-ss {1} '
#                   '-filter:v "crop=1280:540:0:90" '
                   '-c:v ffv1 '
                   '-to {2} '
                   '-r 24 -y {3}'
                  ).format(invid, cut['start'], cut['end'], outvid)
        os.system(command)
    
    with open('list.txt','w') as f:
        for cut in cuts:
            print("file " + cut, file=f)
    os.system('ffmpeg -f concat -safe 0 -i list.txt -c copy -y concat_nosub.avi')
    
    #create the subtitles
    debug_out(config['subs'])

    #add the subtitles
    subtitles.subVideo(gifconf=config,inputvid='concat_nosub.avi',outputvid='final.avi')
    
    #gif THAT
    os.system('ffmpeg -y -i '+
              'final.avi -vf '+
              'fps=24,scale=1080:-1:'+
    'flags=lanczos,palettegen palette.png')
    
    os.system('ffmpeg  -i final.avi '+
              '-i palette.png -filter_complex '+
    '"fps=24,scale=1080:-1:flags=lanczos[x];[x][1:v]paletteuse" '+
    '{}.gif'.format(os.path.basename(args.gifconf).split('.')[0]))

if __name__ == "__main__":
    args = parse_args()
    main(args)
