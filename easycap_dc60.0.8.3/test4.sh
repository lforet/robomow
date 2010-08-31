#!/bin/bash
#
#
#  test4.sh
#
#
#  Usage:   ./test4.sh [ 1 | 2 | 3 | ... ]
#
#  This the test suite for EasyCAPs with four video input cables labelled
#  1, 2, 3, 4 and one (possibly unlabelled) audio input cable.
#
#  EDIT THE FOLLOWING LINE TO PERFORM TESTS ON INPUT OTHER THAN INPUTS 1 AND 2.
#-----------------------------------------------------------------------------
INPUT1=1
INPUT2=2
#-----------------------------------------------------------------------------
#  These tests may not work for an unprivileged user unless root has
#  issued the commands
#         chmod ugo+rw /dev/easycap*
#         chmod ugo+rw /dev/easysnd*
#  after the EasyCAP is plugged in.  The companion script ./permit.sh can be
#  used to carry out these privilege-setting commands if preferred.
#-----------------------------------------------------------------------------
#
#  CAUTIONARY REMARK ON mencoder
#  """""""""""""""""""""""""""""
#  I have carried out a number of runs with input parameters similar to those
#  specified below but using mencoder in place of mplayer.  These runs have
#  lasted more than an hour and produced very large output files, typically
#  more than 100 GB (yes, gigabytes).  The quality of the output files has
#  been very satisfactory, but there is a problem:
#
#  On two occasions where very large output files have been produced, I have
#  subsequently experienced HARD DISK CORRUPTION.  On the first occasion the
#  corruption could be repaired by fsck with minimal inconvenience.  On the
#  second occasion all data on the hard disk was lost (no worries: everything
#  was backed up, of course).  It might just be a coincidence: the hard disk
#  problems might be unrelated to the use of mencoder, but my recommendation
#  at this time would have to be:
#              DO NOT TRY TO CREATE VERY LARGE MULTIMEDIA FILES
#                   ON A MACHINE HOLDING IRREPLACEABLE DATA.
#-----------------------------------------------------------------------------
#
#
#      test        standard       width   height  format   input    sound
#
#        1         PAL_BGHIN       640  x  480     UYVY    INPUT1   yes
#        2         PAL_BGHIN       704  x  576     UYVY    INPUT1   yes
#        3         PAL_BGHIN       720  x  576     UYVY    INPUT1   yes
#        4         PAL_BGHIN       640  x  480     UYVY    INPUT2   yes
#
#        5         NTSC_M          640  x  480     UYVY    INPUT1   yes
#        6         NTSC_443        720  x  480     UYVY    INPUT1   yes
#        7         NTSC_M          640  x  480     UYVY    INPUT2   yes
#
#        8         PAL_BGHIN       720  x  576     YUY2    INPUT1   yes
#        9         PAL_BGHIN       720  x  576     RGB24   INPUT1   yes
#       10         PAL_BGHIN       720  x  576     BGR24   INPUT1   yes
#       11         PAL_BGHIN       720  x  576     RGB32   INPUT1   yes
#       12         PAL_BGHIN       720  x  576     BGR32   INPUT1   yes
#
#       13         NTSC_443        720  x  480     YUY2    INPUT1   yes
#       14         NTSC_443        720  x  480     RGB24   INPUT1   yes
#       15         NTSC_443        720  x  480     BGR24   INPUT1   yes
#       16         NTSC_443        720  x  480     RGB32   INPUT1   yes
#       17         NTSC_443        720  x  480     BGR32   INPUT1   yes
#
#       18         PAL_BGHIN       320  x  240     UYVY    INPUT1   yes
#       19         PAL_BGHIN       360  x  288     UYVY    INPUT1   yes
#       20         PAL_BGHIN       320  x  240     UYVY    INPUT2   yes
#
#       21         NTSC_M          320  x  240     UYVY    INPUT1   yes
#       22         NTSC_443        360  x  240     UYVY    INPUT1   yes
#       23         NTSC_M          320  x  240     UYVY    INPUT2   yes
#
#       24         PAL_BGHIN       360  x  288     YUY2    INPUT1   yes
#       25         PAL_BGHIN       360  x  288     RGB24   INPUT1   yes
#       26         PAL_BGHIN       320  x  240     BGR24   INPUT1   yes
#       27         PAL_BGHIN       320  x  240     RGB32   INPUT1   yes
#       28         PAL_BGHIN       360  x  288     BGR32   INPUT1   yes
#
#       29         NTSC_443        360  x  240     YUY2    INPUT1   yes
#       30         NTSC_443        360  x  240     RGB24   INPUT1   yes
#       31         NTSC_443        320  x  240     BGR24   INPUT1   yes
#       32         NTSC_443        320  x  240     RGB32   INPUT1   yes
#       33         NTSC_443        360  x  240     BGR32   INPUT1   yes
#
#       34         PAL_BGHIN       640  x  480     UYVY    INPUT1   no
#       35         PAL_BGHIN       720  x  576     UYVY    INPUT1   no
#
#       36         NTSC_M          640  x  480     UYVY    INPUT1   no
#       37         NTSC_443        720  x  480     UYVY    INPUT1   no
#
#       65         none            none            none     none    yes
#
#
#-----------------------------------------------------------------------------
declare -i i0

PROG=`which mplayer`
if [ "x" = "x${PROG}" ]; then
  echo "Cannot find mplayer.  Is it installed?"
  exit 1
fi
if [ ! -x ${PROG} ]; then
  echo "Cannot execute mplayer.  Is it installed?"
  exit 1
fi
#-----------------------------------------------------------------------------
if [ "x" = "x$1" ]; then
  number="1"
else
  number="$1"
fi
#-----------------------------------------------------------------------------
ls /dev/easy* /dev/video* >/dev/null 2>/dev/null
DEV_VIDEO=""
DEV_AUDIO=""
i0=0;
while [ -z ${DEV_VIDEO} ]; do
  if [ -c "/dev/easycap${i0}" ]; then DEV_VIDEO="/dev/easycap${i0}"; fi
  if [ 8 -eq ${i0} ]; then DEV_VIDEO="NONE"; fi
  i0=$i0+1
done
if [ "NONE" = "${DEV_VIDEO}" ]; then DEV_VIDEO=""; fi
#------------------------------------------------------------------------------
#  UNCOMMENT THE FOLLOWING SECTION TO ALLOW THIS SCRIPT TO LOOK FOR
#  /dev/video0 ETC. WHENEVER /dev/easycap0 ETC. CANNOT BE FOUND.
#  THIS IS USEFUL ONLY TO PEOPLE WHO ARE EXPERIMENTING AFTER BUILDING THE
#  easycap MODULE AS A CLIENT OF THE videodev MODULE (SEE ./install.sh).
#------------------------------------------------------------------------------
#  i0=0;
#  while [ -z ${DEV_VIDEO} ]; do
#    if [ -c "/dev/video${i0}" ]; then DEV_VIDEO="/dev/video${i0}"; fi
#    if [ 8 -eq ${i0} ]; then DEV_VIDEO="NONE"; fi
#    i0=$i0+1
#    done
#  if [ "NONE" = "${DEV_VIDEO}" ]; then DEV_VIDEO=""; fi
#
#  if [ -z ${DEV_VIDEO} ]; then
#    echo "Cannot find /dev/easycap*, /dev/video*"
#    exit 1
#  fi
#-----------------------------------------------------------------------------
i0=0;
while [ -z ${DEV_AUDIO} ]; do
  if [ -c "/dev/easysnd${i0}" ]; then DEV_AUDIO="/dev/easysnd${i0}"; fi
  if [ 8 -eq ${i0} ]; then DEV_AUDIO="NONE"; fi
  i0=$i0+1
done
if [ "NONE" = "${DEV_AUDIO}" ]; then DEV_AUDIO=""; fi

if [ -z ${DEV_AUDIO} ]; then
  echo "Cannot find /dev/easysnd*"
  exit 1
fi
#-----------------------------------------------------------------------------

echo "Devices are:  ${DEV_VIDEO}  ${DEV_AUDIO}"

if [ "1" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=PAL_BGHIN:width=640:height=480:outfmt=uyvy:device=${DEV_VIDEO}:input=${INPUT1}:fps=25:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

if [ "2" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=PAL_BGHIN:width=704:height=576:outfmt=uyvy:device=${DEV_VIDEO}:input=${INPUT1}:fps=25:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

if [ "3" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=PAL_BGHIN:width=720:height=576:outfmt=uyvy:device=${DEV_VIDEO}:input=${INPUT1}:fps=25:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- OTHER INPUT ----

if [ "4" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=PAL_BGHIN:width=640:height=480:outfmt=uyvy:device=${DEV_VIDEO}:input=${INPUT2}:fps=25:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#================================= NTSC ================================

if [ "5" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=NTSC_M:width=640:height=480:outfmt=uyvy:device=${DEV_VIDEO}:input=${INPUT1}:fps=30:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

if [ "6" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=NTSC_443:width=720:height=480:outfmt=uyvy:device=${DEV_VIDEO}:input=${INPUT1}:fps=30:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- OTHER INPUT ----

if [ "7" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=NTSC_M:width=640:height=480:outfmt=uyvy:device=${DEV_VIDEO}:input=${INPUT2}:fps=30:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi


#================ NON-NATIVE COLOUR FORMATS =================


#---- PAL ---- YUY2 ----

if [ "8" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=PAL_BGHIN:width=720:height=576:outfmt=yuy2:device=${DEV_VIDEO}:input=${INPUT1}:fps=25:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- PAL ---- RGB24 ----

if [ "9" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=PAL_BGHIN:width=720:height=576:outfmt=rgb24:device=${DEV_VIDEO}:input=${INPUT1}:fps=25:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- PAL ---- BGR24 ----

if [ "10" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=PAL_BGHIN:width=720:height=576:outfmt=bgr24:device=${DEV_VIDEO}:input=${INPUT1}:fps=25:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- PAL ---- RGB32 ----

if [ "11" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=PAL_BGHIN:width=720:height=576:outfmt=rgb32:device=${DEV_VIDEO}:input=${INPUT1}:fps=25:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- PAL ---- BGR32 ----

if [ "12" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=PAL_BGHIN:width=720:height=576:outfmt=bgr32:device=${DEV_VIDEO}:input=${INPUT1}:fps=25:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- NTSC ---- YUY2 ----

if [ "13" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=NTSC_443:width=720:height=480:outfmt=yuy2:device=${DEV_VIDEO}:input=${INPUT1}:fps=30:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- NTSC ---- RGB24 ----

if [ "14" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=NTSC_443:width=720:height=480:outfmt=rgb24:device=${DEV_VIDEO}:input=${INPUT1}:fps=30:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- NTSC ---- RGB32 ----

if [ "15" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=NTSC_443:width=720:height=480:outfmt=rgb32:device=${DEV_VIDEO}:input=${INPUT1}:fps=30:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- NTSC ---- BGR24 ----

if [ "16" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=NTSC_443:width=720:height=480:outfmt=bgr24:device=${DEV_VIDEO}:input=${INPUT1}:fps=30:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- NTSC ---- BGR32 ----

if [ "17" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=NTSC_443:width=720:height=480:outfmt=bgr32:device=${DEV_VIDEO}:input=${INPUT1}:fps=30:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#=========================== PAL LOW RESOLUTION ========================

if [ "18" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=PAL_BGHIN:width=320:height=240:outfmt=uyvy:device=${DEV_VIDEO}:input=${INPUT1}:fps=25:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

if [ "19" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=PAL_BGHIN:width=360:height=288:outfmt=uyvy:device=${DEV_VIDEO}:input=${INPUT1}:fps=25:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- OTHER INPUT ----

if [ "20" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=PAL_BGHIN:width=320:height=240:outfmt=uyvy:device=${DEV_VIDEO}:input=${INPUT2}:fps=25:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#========================== NTSC LOW RESOLUTION ========================

if [ "21" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=NTSC_M:width=320:height=240:outfmt=uyvy:device=${DEV_VIDEO}:input=${INPUT1}:fps=30:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

if [ "22" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=NTSC_443:width=360:height=240:outfmt=uyvy:device=${DEV_VIDEO}:input=${INPUT1}:fps=30:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- OTHER INPUT ----

if [ "23" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=NTSC_M:width=320:height=240:outfmt=uyvy:device=${DEV_VIDEO}:input=${INPUT2}:fps=30:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi


#================ NON-NATIVE COLOUR FORMATS LOW RESOLUTION =================


#---- PAL ---- YUY2 ----

if [ "24" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=PAL_BGHIN:width=360:height=288:outfmt=yuy2:device=${DEV_VIDEO}:input=${INPUT1}:fps=25:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- PAL ---- RGB24 ----

if [ "25" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=PAL_BGHIN:width=360:height=288:outfmt=rgb24:device=${DEV_VIDEO}:input=${INPUT1}:fps=25:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- PAL ---- BGR24 ----

if [ "26" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=PAL_BGHIN:width=320:height=240:outfmt=bgr24:device=${DEV_VIDEO}:input=${INPUT1}:fps=25:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- PAL ---- RGB32 ----

if [ "27" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=PAL_BGHIN:width=320:height=240:outfmt=rgb32:device=${DEV_VIDEO}:input=${INPUT1}:fps=25:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- PAL ---- BGR32 ----

if [ "28" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=PAL_BGHIN:width=360:height=288:outfmt=bgr32:device=${DEV_VIDEO}:input=${INPUT1}:fps=25:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- NTSC ---- YUY2 ----

if [ "29" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=NTSC_443:width=360:height=240:outfmt=yuy2:device=${DEV_VIDEO}:input=${INPUT1}:fps=30:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- NTSC ---- RGB24 ----

if [ "30" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=NTSC_443:width=360:height=240:outfmt=rgb24:device=${DEV_VIDEO}:input=${INPUT1}:fps=30:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- NTSC ---- RGB32 ----

if [ "31" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=NTSC_443:width=320:height=240:outfmt=rgb32:device=${DEV_VIDEO}:input=${INPUT1}:fps=30:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- NTSC ---- BGR24 ----

if [ "32" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=NTSC_443:width=320:height=240:outfmt=bgr24:device=${DEV_VIDEO}:input=${INPUT1}:fps=30:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#---- NTSC ---- BGR32 ----

if [ "33" = "${number}" ]; then
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=NTSC_443:width=360:height=240:outfmt=bgr32:device=${DEV_VIDEO}:input=${INPUT1}:fps=30:adevice=${DEV_AUDIO}:forceaudio:immediatemode=0 -hardframedrop -vo xv -ao oss -msglevel all=9
fi

#=============== NO SOUND ===============

if [ "34" = "${number}" ]; then
echo "This test intentionally has no sound output"
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=PAL_BGHIN:width=640:height=480:outfmt=uyvy:device=${DEV_VIDEO}:input=${INPUT1}:fps=25 -hardframedrop -vo xv -msglevel all=9
fi

if [ "35" = "${number}" ]; then
echo "This test intentionally has no sound output"
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=PAL_BGHIN:width=720:height=576:outfmt=uyvy:device=${DEV_VIDEO}:input=${INPUT1}:fps=25 -hardframedrop -vo xv -msglevel all=9
fi

if [ "36" = "${number}" ]; then
echo "This test intentionally has no sound output"
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=NTSC_M:width=640:height=480:outfmt=uyvy:device=${DEV_VIDEO}:input=${INPUT1}:fps=30 -hardframedrop -vo xv -msglevel all=9
fi

if [ "37" = "${number}" ]; then
echo "This test intentionally has no sound output"
1>test.log 2>&1 \
${PROG} tv:// -tv driver=v4l2:norm=NTSC_443:width=720:height=480:outfmt=uyvy:device=${DEV_VIDEO}:input=${INPUT1}:fps=30 -hardframedrop -vo xv -msglevel all=9
fi

#=============== SOUND ONLY (needs sox and its oss library) ===============

if [ "65" = "${number}" ]; then
if [ "x" = "x`which sox`" ]; then
  echo "Cannot find sox.  Is it installed?"
  exit 1
fi
if [ ! -x `which sox` ]; then
  echo "Cannot execute sox.  Is it installed?"
  exit 1
fi

echo "This test intentionally has no video output"
sox -V3 -c 2 -r 32000 -t raw -s2 ${DEV_AUDIO} -c 2 -r 32000 -s2 -t ossdsp /dev/dsp
fi

exit 0

