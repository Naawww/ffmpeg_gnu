import sys
GNU_RADIO_PATH = 'C:/Program Files/GNURadio-3.7'
sys.path.append(str(GNU_RADIO_PATH))
sys.path.append(str(GNU_RADIO_PATH + '/lib'))
sys.path.append(str(GNU_RADIO_PATH + '/lib' + '/site-packages'))
sys.path.append(str(GNU_RADIO_PATH + '/gr-python27'))
sys.path.append(str(GNU_RADIO_PATH + '/gr-python27' + '/lib'))
sys.path.append(str(GNU_RADIO_PATH + '/gr-python27' + '/lib' + '/site-packages'))
sys.path.append(str(GNU_RADIO_PATH + '/gr-python27' + '/lib' + '/site-packages' + '/wx-3.0-msw'))

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Udp Rx
# Generated: Tue Jul 10 15:44:26 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx
import subprocess


def save_subprocess_pid(pid):
    """Saves the pid of the current subprocess so it can be accessed in later program runs"""
    file_name = "subprocess_pid_{0}.txt".format(pid)
    with open(file_name, 'w') as x_file:
        x_file.write(str(pid))


def check_exists_subprocess_pid_file():
    """This returns the pids of previous subprocesses which were run from this program"""
    import glob
    import re
    pid_files =  glob.glob("subprocess_pid_*.txt")
    pids = [int(re.findall("\d.+(?=.txt)", path)[0]) for path in pid_files]
    return pids


def kill_zombie_processes():
    """This finds subprocess_pid_###.txt files from old runs of this program, and kills the associated
    subprocesses."""
    import os
    import signal
    # first check if the subprocess already exists
    existing_pids = check_exists_subprocess_pid_file()
    for pid in existing_pids:
        try:
            os.kill(pid, signal.SIGTERM)
        except:
            print("Couldnt find subprocess pid {0}...".format(pid))
        os.remove("subprocess_pid_{0}.txt".format(pid))


def run_subprocess(cmd):
    """
    First this kills any hanging zombie processes, then it runs the specified command in the shell. It also saves the
    pid of the subprocess so it can be killed if necessary later.
    :param cmd:
    :return:
    """
    kill_zombie_processes()
    p = subprocess.Popen(cmd)
    save_subprocess_pid(p.pid)


def run_ffmpeg_cmd(ffmpeg_cmd):
    run_subprocess('ffmpeg.exe {0}'.format(ffmpeg_cmd))


class FfmpegHeirBlock(gr.hier_block2):

    def __init__(self, ffmpeg_code='-i test.mp3 -f wave upd://127.0.0.1::1234',
                        samp_rate=32e3,
                        ip_address='127.0.0.1',
                        port=1234,
                        payload_size=1472):
        gr.hier_block2.__init__(
            self, "Heir Block",
            gr.io_signature(0, 0, 0),
            gr.io_signature(1, 1, gr.sizeof_short),
        )

        ##################################################
        # Parameters
        ##################################################
        self.ffmpeg_code = ffmpeg_code
        self.samp_rate = samp_rate
        self.ip_address = ip_address
        self.port = port
        self.payload_size = payload_size

        ##################################################
        # Blocks
        ##################################################
        run_ffmpeg_cmd(self.ffmpeg_code)
        self.blocks_udp_source_0 = blocks.udp_source(gr.sizeof_short*1, ip_address, port, payload_size, True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_udp_source_0, 0), (self, 0))


class udp_rx(grc_wxgui.top_block_gui):
    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Aareff LBC Player")
        _icon_path = "C:\Program Files\GNURadio-3.7\share\icons\hicolor\scalable/apps\gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 44100

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_c(
        	self.GetWin(),
        	title='Aareff Oscilliscope',
        	sample_rate=samp_rate,
        	v_scale=0.2,
        	v_offset=0,
        	t_scale=5e-3,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label='Counts',
        )
        self.Add(self.wxgui_scopesink2_0.win)
        self.blocks_ffmpeg_source_0 = FfmpegHeirBlock('-re -i http://media-sov.musicradio.com/LBCUK? -f wav udp://127.0.0.1:1234')
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((0.000025, ))
        self.blocks_interleaved_short_to_complex_0 = blocks.interleaved_short_to_complex(False, False)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.audio_sink_0 = audio.sink(samp_rate, '', True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_ffmpeg_source_0, 0), (self.blocks_interleaved_short_to_complex_0, 0))
        self.connect((self.blocks_interleaved_short_to_complex_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.wxgui_scopesink2_0, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.audio_sink_0, 1))
        self.connect((self.blocks_complex_to_float_0, 0), (self.audio_sink_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate)


def main(top_block_cls=udp_rx, options=None):
    tb = top_block_cls()
    tb.Start(True)

    tb.Wait()

if __name__ == '__main__':
    main()
