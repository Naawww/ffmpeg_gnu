import ffmpeg
import re


def drop_extension(file_path):
    return re.findall('.+(?=.)', file_path)[0]


def convert_mp4_to_mp3(video_file_path):
    """Really simple ffmpeg command. It gets the audio out of the video"""
    audio_file_path = re.findall('.+(?=.mp4)',video_file_path)[0] + ".mp3"
    ffmpeg.input(video_file_path).output(audio_file_path).run()
    return


def get_frame_mp4(video_file_path, frame_num):
    """Very simple ffmpeg command. It pulls the specified frame from the video and gives it to you as a jpg"""
    frame_file_path = re.findall('.+(?=.mp4)', video_file_path)[0] + ".jpg"
    (ffmpeg.input(video_file_path)
        .filter('select', 'gte(n,{})'.format(frame_num))
        .output(frame_file_path, vframes=1, format='image2', vcodec='mjpeg')).run()
    return


def get_palette(video_file_path, start=0, duration=2.5,):
    in_file = ffmpeg.input(video_file_path, ss=start, t=duration)
    palette = in_file.filter("palettegen")
    ffmpeg.overwrite_output(palette.output('palette.png')).run()
    return


def make_gif_from_video(video_file_path, start=0, duration=2.5, gif_name=None):
    gif_name = gif_name or drop_extension(video_file_path)
    gif_file_path = gif_name + ".gif"

    # get the file, and make the palette
    in_file = ffmpeg.input(video_file_path, ss=start, t=duration)
    palette = in_file.filter("palettegen")

    # scale and lower framerate:
    smaller = in_file.filter('scale', 480, -1).filter('fps', 12)
    # apply the palette to the video clip, and make into a gif
    output_stream = ffmpeg.filter([smaller, palette], "paletteuse").output(gif_file_path)
    ffmpeg.overwrite_output(output_stream).run()
    return


if __name__ == '__main__':
    make_gif_from_video("alex_singing.mp4")