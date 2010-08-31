#!/bin/bash
#
#
#  tvtime4.sh
#
#
#  Usage:   ./tvtime4.sh PAL | NTSC
#
#
#  This will work for an unprivileged user only if root has
#  issued the commands
#         chmod ugo+rw /dev/easycap0
#         chmod ugo+rw /dev/easysnd1
#  after the EasyCAP is plugged in.
#
#
#  PLEASE NOTE:  tvtime requires about 5 seconds to start up, and during
#                this period messages will appear in the terminal window
#                which can be ignored.  Don't give up too soon!
#
#                If there is no sound, close tvtime and try again.
#
#  If the script fails for any reason it might leave tvtime or sox running,
#  in which case it will be necessary to remove these processes manually.
#  Use ps -A to find the process number n, then kill -9 n.
#
#-----------------------------------------------------------------------------
declare -i rc
declare -i i0

if [ "x" = "x$1" ]; then
  echo "Usage:  ./tvtime4.sh PAL"
  echo "or      ./tvtime4.sh NTSC"
  exit 1
else
  standard="$1"
fi

TVTIME=`which tvtime`
if [ "x" = "x${TVTIME}" ]; then
  echo "Cannot find tvtime.  Is it installed?"
  exit 1
fi
if [ ! -x ${TVTIME} ]; then
  echo "Cannot execute tvtime.  Is it installed?"
  exit 1
fi

SOX=`which sox`
if [ "x" = "x${SOX}" ]; then
  echo "Cannot find sox.  Is it installed?"
  exit 1
fi
if [ ! -x ${SOX} ]; then
  echo "Cannot execute sox.  Is it installed?"
  exit 1
fi

if [ "x" = "x$HOME" ]; then
  echo "ERROR:  cannot find home directory"
  exit 1
fi

if [ -e "$HOME/.tvtime/tvtime.xml" ]; then
  echo "Not overwriting existing file $HOME/.tvtime/tvtime.xml"
  echo "To force a refresh, delete it or rename it"
  echo "... continuing"
else
  echo "No existing file $HOME/.tvtime/tvtime.xml"
  if [ -e ./tvtime_${standard}.xml ]; then
    echo "Creating it from ./tvtime_${standard}.xml"
    mkdir -p $HOME/.tvtime
    cp -p ./tvtime_${standard}.xml $HOME/.tvtime/tvtime.xml
    if [ ! -e "$HOME/.tvtime/tvtime.xml" ]; then
      echo "ERROR: failed to create $HOME/.tvtime/tvtime.xml"
      exit 1
    fi
  else
    echo "ERROR: cannot find required file ./tvtime_${standard}.xml"
    exit 1
  fi
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
  
(${TVTIME} -d ${DEV_VIDEO} -i 0 -n "${standard}" 1>/dev/null 2>/dev/null) &
rc=1
while [ 0 -ne ${rc} ];
do
  sleep 0.5
  tvtime-command run_command "(sox -c 2 -r 32000 -t raw -s2 ${DEV_AUDIO} -c 2 -r 32000 -s2 -t ossdsp /dev/dsp 1>/dev/null 2>/dev/null)" 1>/dev/null
  rc=$?
done

process=`ps -A | grep sox - | tail -n 1 | sed "s,^ *,#,;s, .*$,,;s,#*,," `
if [ "x" != "x${process}" ]; then
  kill -9 ${process}
fi
exit 0
