#!/bin/bash
#
#
#  xawtv.sh
#
#
#  Usage:   ./xawtv.sh PAL | NTSC
#
#-----------------------------------------------------------------------------
declare -i rc
declare -i i0

if [ "x" = "x$1" ]; then
  echo "Usage:  ./xawtv.sh PAL"
  echo "or      ./xawtv.sh NTSC"
  exit 1
else
  standard="$1"
fi

XAWTV=`which xawtv`
if [ "x" = "x${XAWTV}" ]; then
  echo "Cannot find xawtv.  Is it installed?"
  exit 1
fi
if [ ! -x ${XAWTV} ]; then
  echo "Cannot execute xawtv.  Is it installed?"
  exit 1
fi
if [ "x" = "x$HOME" ]; then
  echo "ERROR:  cannot find home directory"
  exit 1
fi

if [ \( -e "$HOME/.xawtv" \) -o \( -e "$HOME/.xawtvrc" \) ]; then
  echo "Not overwriting existing file $HOME/.xawtv or $HOME/.xawtvrc"
  echo "To force a refresh, delete it/them or rename it/them."
  echo "For information on configuration syntax, run \`man xawtvrc\`"
  echo "... continuing ..."
else
  echo "No existing file $HOME/.xawtv or $HOME/.xawtvrc"
  if [ -e ./xawtvrc_${standard} ]; then
    echo "Creating it from ./xawtvrc_${standard}"
    cp -p ./xawtvrc_${standard} $HOME/.xawtv
    if [ ! -e "$HOME/.xawtv" ]; then
      echo "ERROR: failed to create $HOME/.xawtv"
      exit 1
    fi
    ln -s $HOME/.xawtv $HOME/.xawtvrc
  else
    echo "ERROR: cannot find required file ./xawtvrc_${standard}"
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

${XAWTV} -c ${DEV_VIDEO} -C ${DEV_AUDIO} 2>xawtv.err

exit 0
