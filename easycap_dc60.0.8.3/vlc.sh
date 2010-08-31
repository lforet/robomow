#!/bin/bash
#
#
#  vlc.sh
#
#
#  Usage:   ./vlc.sh PAL | NTSC
#
#
#  This script must be run by an unprivileged user.  Also, root must first
#  issue the commands
#         chmod ugo+rw /dev/easycap0
#         chmod ugo+rw /dev/easysnd1
#  after the EasyCAP is plugged in.
#  
#
#  A recent version of vlc is required.  Version 1.0.4 is known to work.
#  Version 0.8.6h as supplied wuth Debian Lenny is known not to work.
#
#-----------------------------------------------------------------------------
declare -i rc
declare -i i0

if [ "x" = "x$1" ]; then
  echo "Usage:  ./vlc.sh PAL"
  echo "or      ./vlc.sh NTSC"
  exit 1
else
  standard="$1"
fi

VLC=`which cvlc`
if [ "x" = "x${VLC}" ]; then
  echo "Cannot find vlc.  Is it installed?"
  exit 1
fi
if [ ! -x ${VLC} ]; then
  echo "Cannot execute vlc.  Is it installed?"
  exit 1
fi

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

#i0=0;
#while [ -z ${DEV_VIDEO} ]; do
#  if [ -c "/dev/video${i0}" ]; then DEV_VIDEO="/dev/video${i0}"; fi
#  if [ 8 -eq ${i0} ]; then DEV_VIDEO="NONE"; fi
#  i0=$i0+1
#done
#if [ "NONE" = "${DEV_VIDEO}" ]; then DEV_VIDEO=""; fi

if [ -z ${DEV_VIDEO} ]; then
  echo "Cannot find /dev/easycap*, /dev/video*"
  exit 1
fi

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

echo "Devices:  ${DEV_VIDEO}  ${DEV_AUDIO}"

#-----------------------------------------------------------------------------
if [ "PAL" = "${standard}" ]; then
  ${VLC} -vvv v4l2://${DEV_VIDEO}:width=720:height=576 :norm=pal :input-slave=oss://${DEV_AUDIO} --demux rawvideo 2>vlc.err
else
  ${VLC} -vvv v4l2://${DEV_VIDEO}:width=720:height=480 :norm=ntsc :input-slave=oss://${DEV_AUDIO} --demux rawvideo 2>vlc.err
fi

exit 0
