#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.5.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import iio
from gnuradio import zeromq



from gnuradio import qtgui


def set_usb_contexts(usb1, usb3):
    global usb_bottom_diff_1, usb_top_sum_3
    usb_bottom_diff_1 = usb1
    usb_top_sum_3 = usb3

class reciever(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "reciever")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.usb_top_sum_3 = usb_top_sum_3
        self.usb_bottom_diff_1 = usb_bottom_diff_1
        self.samp_rate = samp_rate = 5000000

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_push_sink_0_0_0 = zeromq.push_sink(gr.sizeof_float, 1, 'tcp://*:5557', 100, False, (-1))
        self.zeromq_push_sink_0_0 = zeromq.push_sink(gr.sizeof_float, 1, 'tcp://*:5556', 100, False, (-1))
        self.zeromq_push_sink_0 = zeromq.push_sink(gr.sizeof_float, 1, 'tcp://*:5555', 100, False, (-1))
        self.iio_pluto_source_0_0 = iio.fmcomms2_source_fc32(usb_top_sum_3 if usb_top_sum_3 else iio.get_pluto_uri(), [True, True], 32768)
        self.iio_pluto_source_0_0.set_len_tag_key('packet_len')
        self.iio_pluto_source_0_0.set_frequency(2399000000)
        self.iio_pluto_source_0_0.set_samplerate(samp_rate)
        self.iio_pluto_source_0_0.set_gain_mode(0, 'slow_attack')
        self.iio_pluto_source_0_0.set_gain(0, 64)
        self.iio_pluto_source_0_0.set_quadrature(True)
        self.iio_pluto_source_0_0.set_rfdc(True)
        self.iio_pluto_source_0_0.set_bbdc(True)
        self.iio_pluto_source_0_0.set_filter_params('Auto', '', 0, 0)
        self.iio_pluto_source_0 = iio.fmcomms2_source_fc32(usb_bottom_diff_1 if usb_bottom_diff_1 else iio.get_pluto_uri(), [True, True], 32768)
        self.iio_pluto_source_0.set_len_tag_key('packet_len')
        self.iio_pluto_source_0.set_frequency(2399000000)
        self.iio_pluto_source_0.set_samplerate(samp_rate)
        self.iio_pluto_source_0.set_gain_mode(0, 'slow_attack')
        self.iio_pluto_source_0.set_gain(0, 64)
        self.iio_pluto_source_0.set_quadrature(True)
        self.iio_pluto_source_0.set_rfdc(True)
        self.iio_pluto_source_0.set_bbdc(True)
        self.iio_pluto_source_0.set_filter_params('Auto', '', 0, 0)
        self.blocks_sub_xx_1 = blocks.sub_ff(1)
        self.blocks_sub_xx_0 = blocks.sub_cc(1)
        self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_arg_0_0 = blocks.complex_to_arg(1)
        self.blocks_complex_to_arg_0 = blocks.complex_to_arg(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.band_pass_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                0.5e6,
                1.5e6,
                5000,
                window.WIN_HAMMING,
                6.76))
        self.band_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                0.5e6,
                1.5e6,
                5000,
                window.WIN_HAMMING,
                6.76))


        ##################################################
        # Connections
        ##################################################
        self.connect((self.band_pass_filter_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.band_pass_filter_0_0, 0), (self.blocks_complex_to_mag_squared_0_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_complex_to_arg_0, 0))
        self.connect((self.blocks_complex_to_arg_0, 0), (self.blocks_sub_xx_1, 0))
        self.connect((self.blocks_complex_to_arg_0_0, 0), (self.blocks_sub_xx_1, 1))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.zeromq_push_sink_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.zeromq_push_sink_0_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_complex_to_arg_0_0, 0))
        self.connect((self.blocks_sub_xx_1, 0), (self.zeromq_push_sink_0_0_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.iio_pluto_source_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.iio_pluto_source_0_0, 0), (self.band_pass_filter_0_0, 0))
        self.connect((self.iio_pluto_source_0_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.iio_pluto_source_0_0, 0), (self.blocks_sub_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "reciever")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_usb_top_sum_3(self):
        return self.usb_top_sum_3

    def set_usb_top_sum_3(self, usb_top_sum_3):
        self.usb_top_sum_3 = usb_top_sum_3

    def get_usb_bottom_diff_1(self):
        return self.usb_bottom_diff_1

    def set_usb_bottom_diff_1(self, usb_bottom_diff_1):
        self.usb_bottom_diff_1 = usb_bottom_diff_1

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, 0.5e6, 1.5e6, 5000, window.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, self.samp_rate, 0.5e6, 1.5e6, 5000, window.WIN_HAMMING, 6.76))
        self.iio_pluto_source_0.set_samplerate(self.samp_rate)
        self.iio_pluto_source_0_0.set_samplerate(self.samp_rate)




def main(top_block_cls=reciever, options=None):
    
    # ADDED THE FOLLOWING IF BLOCK
    if len(sys.argv) > 2:
        usb1_arg = sys.argv[1]
        usb3_arg = sys.argv[2]
        set_usb_contexts(usb1_arg, usb3_arg)
    else:
        print("Usage: python3 reciever.py <usb_1> <usb_3>")
        sys.exit(1)

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
