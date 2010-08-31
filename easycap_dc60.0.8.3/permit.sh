#!/bin/bash
#
#  permit.sh
#
#
#if [ -c /dev/video0 ]; then chmod ugo+rw /dev/video* ; fi
if [ -c /dev/easycap0 ]; then chmod ugo+rw /dev/easycap* ; fi
if [ -c /dev/easysnd0 ]; then chmod ugo+rw /dev/easysnd* ; fi
if [ -c /dev/easysnd1 ]; then chmod ugo+rw /dev/easysnd* ; fi
if [ -c /dev/dsp ]; then chmod ugo+rw /dev/dsp ; fi

