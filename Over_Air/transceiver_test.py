#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Transceiver Test
# Author: John Sylvia
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
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
from gnuradio import uhd
import time
import sip



class transceiver_test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Transceiver Test", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Transceiver Test")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "transceiver_test")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 32
        self.signal_freq = signal_freq = 1000
        self.samp_rate = samp_rate = 10e6
        self.gain = gain = 40
        self.carrier_freq = carrier_freq = 5802
        self.bpsk_object = bpsk_object = digital.constellation_bpsk().base()
        self.bpsk_object.set_npwr(1.0)

        ##################################################
        # Blocks
        ##################################################

        self._gain_range = qtgui.Range(0, 60, 0.1, 40, 200)
        self._gain_win = qtgui.RangeWidget(self._gain_range, self.set_gain, "CH Gain (dB)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._gain_win)
        self._carrier_freq_range = qtgui.Range(5725, 5875, 0.1, 5802, 200)
        self._carrier_freq_win = qtgui.RangeWidget(self._carrier_freq_range, self.set_carrier_freq, "Carrier Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._carrier_freq_win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("addr=192.168.10.2", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=[1],
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        # No synchronization enforced.

        self.uhd_usrp_source_0.set_center_freq(carrier_freq*10**6, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_gain(gain, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("addr=192.168.10.2", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=[0],
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        # No synchronization enforced.

        self.uhd_usrp_sink_0.set_center_freq(carrier_freq*10**6, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_gain(20, 0)
        self._signal_freq_range = qtgui.Range(0, 100000, 100, 1000, 200)
        self._signal_freq_win = qtgui.RangeWidget(self._signal_freq_range, self.set_signal_freq, "Signal Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._signal_freq_win)
        self.root_raised_cosine_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.root_raised_cosine(
                1,
                samp_rate,
                (samp_rate/sps),
                0.35,
                (11*sps)))
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            32768, #fftsize
            window.WIN_HAMMING, #wintype
            (carrier_freq*10**6), #fc
            samp_rate, #bw
            "Analysis", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/40)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_cc(
            digital.TED_GARDNER,
            sps,
            0.045,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_fll_band_edge_cc_0 = digital.fll_band_edge_cc(sps, 1, 1, ((2*3.141596265359)/100))
        self.digital_diff_encoder_bb_0 = digital.diff_encoder_bb(2, digital.DIFF_DIFFERENTIAL)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2, digital.DIFF_DIFFERENTIAL)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(((2*3.141596265359)/100), 2, False)
        self.digital_constellation_encoder_bc_0_1 = digital.constellation_encoder_bc(bpsk_object)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(bpsk_object)
        self.blocks_vector_source_x_0 = blocks.vector_source_b((1, 0, 0, 1, 0, 1, 0), True, 1, [])
        self.blocks_repeat_0_0 = blocks.repeat(gr.sizeof_char*1, sps)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_char*1, sps)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.analog_agc_xx_0 = analog.agc_cc((1e-4), 1.0, 1.0, 65536)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0, 0), (self.digital_fll_band_edge_cc_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.digital_constellation_encoder_bc_0_1, 0))
        self.connect((self.blocks_repeat_0_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.digital_diff_encoder_bb_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_constellation_encoder_bc_0_1, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_repeat_0_0, 0))
        self.connect((self.digital_diff_encoder_bb_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.analog_agc_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "transceiver_test")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.blocks_repeat_0.set_interpolation(self.sps)
        self.blocks_repeat_0_0.set_interpolation(self.sps)
        self.digital_symbol_sync_xx_0.set_sps(self.sps)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, (self.samp_rate/self.sps), 0.35, (11*self.sps)))

    def get_signal_freq(self):
        return self.signal_freq

    def set_signal_freq(self, signal_freq):
        self.signal_freq = signal_freq

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_sink_x_0.set_frequency_range((self.carrier_freq*10**6), self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, (self.samp_rate/self.sps), 0.35, (11*self.sps)))
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_source_0.set_gain(self.gain, 0)

    def get_carrier_freq(self):
        return self.carrier_freq

    def set_carrier_freq(self, carrier_freq):
        self.carrier_freq = carrier_freq
        self.qtgui_sink_x_0.set_frequency_range((self.carrier_freq*10**6), self.samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(self.carrier_freq*10**6, 0)
        self.uhd_usrp_source_0.set_center_freq(self.carrier_freq*10**6, 0)

    def get_bpsk_object(self):
        return self.bpsk_object

    def set_bpsk_object(self, bpsk_object):
        self.bpsk_object = bpsk_object
        self.digital_constellation_decoder_cb_0.set_constellation(self.bpsk_object)
        self.digital_constellation_encoder_bc_0_1.set_constellation(self.bpsk_object)




def main(top_block_cls=transceiver_test, options=None):

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
