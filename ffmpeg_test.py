from __future__ import unicode_literals
import argparse
import ffmpeg
import sys


parser = argparse.ArgumentParser(
    description='Read individual video frame into memory as jpeg and write to stdout')
parser.add_argument('in_filename', help='Input filename')
parser.add_argument('frame_num', help='Frame number')




def read_frame_as_jpeg(in_filename, frame_num):
    out, err = (
        ffmpeg
        .input(in_filename)
        .filter('select', 'gte(n,{})'.format(frame_num))
        .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
        .run(capture_stdout=True)
    )
    return out

if __name__ == '__main__':
    probe = ffmpeg.probe('alex_singing.mp4')
    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    width = int(video_info['width'])
    height = int(video_info['height'])
    num_frames = int(video_info['nb_frames'])
    print(video_info)


    # #args = parser.parse_args()
    # out = read_frame_as_jpeg("alex_singing.mp4", 4)#args.in_filename, args.frame_num)
    # sys.stdout.buffer.write(out)
    # import os

