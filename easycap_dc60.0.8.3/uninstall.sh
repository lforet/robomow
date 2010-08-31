#!/bin/bash
#
#
#  uninstall.sh
#
#
#  Removes the easycap driver.
#  Tested on Debian only.
#
#
#-----------------------------------------------------------------------------
if [ "x`whoami`" != "xroot" ]; then
  echo "ERROR:  must be run as root"
  exit 1
fi

DEPMODDIR=/lib/modules/`uname -r`
SUBMODDIR=kernel/drivers/media/video

WORKDIR=`pwd`

#-----------------------------------------------------------------------------
LSMODOUT=`lsmod | grep "^easycap " - | sed -e "s, .*$,," - `
if [ "xeasycap" = "x${LSMODOUT}" ]; then rmmod easycap; fi
LSMODOUT=`lsmod | grep "^easycap " - | sed -e "s, .*$,," - `
if [ "xeasycap" = "x${LSMODOUT}" ]; then
  echo "ERROR:  easycap module cannot be removed"
fi
#-----------------------------------------------------------------------------
if [ -e ${DEPMODDIR}/${SUBMODDIR}/easycap.ko ]; then
  rm ${DEPMODDIR}/${SUBMODDIR}/easycap.ko
fi
if [ -e ${DEPMODDIR}/${SUBMODDIR}/easycap.ko ]; then
  echo "ERROR:  file cannot be deleted: ${DEPMODDIR}/${SUBMODDIR}/easycap.ko"
  exit 1
fi
#-----------------------------------------------------------------------------
depmod -a -v 1>${WORKDIR}/depmod.out 2>${WORKDIR}/depmod.err
if [ 0 -ne $? ]; then
  echo "ERROR:  step failed:  depmod"
  cat ${WORKDIR}/depmod.err
  exit 1
fi
echo "depmod OK"
#-----------------------------------------------------------------------------
if [ -e /etc/udev/rules.d/57-easycap.rules ]; then
  mv /etc/udev/rules.d/57-easycap.rules ./57-easycap.rules-REMOVED
  if [ -e ./57-easycap.rules ]; then
    diff ./57-easycap.rules-REMOVED ./57-easycap.rules >./uninstall.tmp
    if [ ! -s ./uninstall.tmp ]; then
      rm ./57-easycap.rules-REMOVED
    fi
    rm ./uninstall.tmp
  fi
fi

exit 0

