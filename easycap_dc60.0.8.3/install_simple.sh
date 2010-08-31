#!/bin/bash
#
#
#  install_simple.sh
#
#
#  Removes the easycapdc60 driver and reinstalls it.
#  This is a stripped-down version of the installation script with all
#  inessential configuration options and tests omitted.
#
#  Tested on:   Debian Lenny,  64-bit
#               Ubuntu 10.04,  32-bit
#               OpenSUSE 11.2, 64-bit
#               Fedora 12,     32-bit
#
#-----------------------------------------------------------------------------
#
#
#        *************************************************************
#        *                                                           *
#        *     Ordinarily nothing below here needs to be changed.    *
#        *                                                           *
#        *************************************************************
#
#
#-----------------------------------------------------------------------------
DEBUG=0
#-----------------------------------------------------------------------------
#  CHECK THAT ESSENTIAL COMPONENTS ARE PRESENT
#-----------------------------------------------------------------------------
if [ "x`whoami`" != "xroot" ]; then
  echo "ERROR:  must be run as root"
  exit 1
fi
if [ "x`which gcc`" = "x" ]; then
  echo "ERROR:  cannot find gcc.  Is it installed?"
  exit 1
fi
if [ ! -x `which gcc` ]; then
  echo "ERROR:  cannot execute gcc.  Is it installed correctly?"
  exit 1
fi
if [ "x`which make`" = "x" ]; then
  echo "ERROR:  cannot find make.  Is it installed?"
  exit 1
fi
if [ ! -x `which make` ]; then
  echo "ERROR:  cannot execute make.  Is it installed correctly?"
  exit 1
fi
if [ ! -d "/usr/src" ]; then
  echo "ERROR:  cannot find directory /usr/src"
  echo "        Are the kernel headers installed?"
  exit 1
fi
DEPMODDIR=/lib/modules/`uname -r`
if [ ! -d ${DEPMODDIR} ]; then
  echo "ERROR: directory not found: ${DEPMODDIR}"
  exit 1
fi
SUBMODDIR=kernel/drivers/media/video
KERNELDIR=${DEPMODDIR}/build
if [ ! -d "${KERNELDIR}" ]; then
  echo "ERROR:  cannot find directory ${KERNELDIR}"
  echo "        Are the kernel headers installed correctly?"
  exit 1
fi
#-----------------------------------------------------------------------------

WORKDIR=`pwd`

#-----------------------------------------------------------------------------
LSMODOUT=`lsmod | grep "^easycap " - | sed -e "s, .*$,," - `
if [ "xeasycap" = "x${LSMODOUT}" ]; then rmmod easycap; fi
LSMODOUT=`lsmod | grep "^easycap " - | sed -e "s, .*$,," - `
if [ "xeasycap" = "x${LSMODOUT}" ]; then
  echo "ERROR:  easycap module cannot be removed"
  exit 1
fi
#-----------------------------------------------------------------------------
LSMODOUT=`lsmod | grep "^snd_usb_audio " - | sed -e "s, .*$,," - `
if [ "xsnd_usb_audio" = "x${LSMODOUT}" ]; then rmmod snd_usb_audio; fi
LSMODOUT=`lsmod | grep "^snd_usb_audio " - | sed -e "s, .*$,," - `
if [ "xsnd_usb_audio" = "x${LSMODOUT}" ]; then
  echo "ERROR:  snd_usb_audio module cannot be removed"
  exit 1
fi
#-----------------------------------------------------------------------------
LSMODOUT=`lsmod | grep "^stk11xx " - | sed -e "s, .*$,," - `
if [ "xstk11xx" = "x${LSMODOUT}" ]; then rmmod stk11xx; fi
LSMODOUT=`lsmod | grep "^stk11xx " - | sed -e "s, .*$,," - `
if [ "xstk11xx" = "x${LSMODOUT}" ]; then
  echo "ERROR:  stk11xx module cannot be removed"
  exit 1
fi
#-----------------------------------------------------------------------------
mkdir -p ${DEPMODDIR}/${SUBMODDIR}
if [ ! -d ${DEPMODDIR}/${SUBMODDIR} ]; then
  echo "ERROR:  directory not found: ${DEPMODDIR}/${SUBMODDIR}"
  exit 1
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
else
  echo "depmod OK"
fi
#-----------------------------------------------------------------------------
if [ ! -d ${WORKDIR} ]; then
  echo "ERROR: directory not found: ${WORKDIR}"
  exit 1
fi
cd ${WORKDIR}
if [ ".${WORKDIR}" != ".`pwd`" ]; then
  echo "ERROR:  cannot access working directory:  ${WORKDIR}"
  exit 1
fi

>/${WORKDIR}/make.out
>/${WORKDIR}/make.err

#-----------------------------------------------------------------------------
# CREATE Makefile, src/Makefile AND tools/Makefile FROM DEFAULTS
#-----------------------------------------------------------------------------
if [ ! -e ${WORKDIR}/Makefile_default ]; then
  echo "ERROR: file not found: ${WORKDIR}/Makefile_default"
  exit 1
fi
if [ -e ${WORKDIR}/Makefile ]; then rm ${WORKDIR}/Makefile; fi
if [ -e ${WORKDIR}/Makefile ]; then
  echo "ERROR: file cannot be removed: ${WORKDIR}/Makefile"
  exit 1
fi
cp -p ${WORKDIR}/Makefile_default ${WORKDIR}/Makefile

if [ ! -e ${WORKDIR}/src/Makefile_default ]; then
  echo "ERROR: file not found: ${WORKDIR}/src/Makefile_default"
  exit 1
fi
if [ -e ${WORKDIR}/src/Makefile ]; then rm ${WORKDIR}/src/Makefile; fi
if [ -e ${WORKDIR}/src/Makefile ]; then
  echo "ERROR: file cannot be removed: ${WORKDIR}/src/Makefile"
  exit 1
fi
cp -p ${WORKDIR}/src/Makefile_default ${WORKDIR}/src/Makefile

if [ ! -e ${WORKDIR}/tools/Makefile_default ]; then
  echo "ERROR: file not found: ${WORKDIR}/tools/Makefile_default"
  exit 1
fi
if [ -e ${WORKDIR}/tools/Makefile ]; then rm ${WORKDIR}/tools/Makefile; fi
if [ -e ${WORKDIR}/tools/Makefile ]; then
  echo "ERROR: file cannot be removed: ${WORKDIR}/tools/Makefile"
  exit 1
fi
cp -p ${WORKDIR}/tools/Makefile_default ${WORKDIR}/tools/Makefile
#-----------------------------------------------------------------------------
if [ ! -e ${WORKDIR}/Makefile ]; then
  echo "ERROR: file not found: ${WORKDIR}/Makefile"
  exit 1
fi
if [ ! -e ${WORKDIR}/src/Makefile ]; then
  echo "ERROR: file not found: ${WORKDIR}/src/Makefile"
  exit 1
fi
if [ ! -e ${WORKDIR}/tools/Makefile ]; then
  echo "ERROR: file not found: ${WORKDIR}/tools/Makefile"
  exit 1
fi

make clean 1>>${WORKDIR}/make.out 2>>${WORKDIR}/make.err

if [ \( 0 -ne $? \) -o \( -s ${WORKDIR}/make.err \) ]; then
  echo "ERROR:  step failed:  make clean"
  cat ${WORKDIR}/make.err
  exit 1
else
  echo "make clean OK"
fi

if [ -e ${WORKDIR}/src/easycap.ko ]; then
  echo "ERROR:  file cannot be deleted: ${WORKDIR}/src/easycap.ko"
  exit 1
fi

make 1>>${WORKDIR}/make.out 2>>${WORKDIR}/make.err

if [ \( 0 -ne $? \) -o \( -s ${WORKDIR}/make.err \) ]; then
  echo "ERROR:  step failed:  make"
  cat ${WORKDIR}/make.err
  exit 1
else
  echo "make OK"
fi
rm ${WORKDIR}/make.out

if [ ! -e ${WORKDIR}/src/easycap.ko ]; then
  echo "ERROR:  cannot make file: ${WORKDIR}/src/easycap.ko"
  exit 1
fi
#-----------------------------------------------------------------------------
cp -p ${WORKDIR}/src/easycap.ko ${DEPMODDIR}/${SUBMODDIR}
if [ ! -e ${DEPMODDIR}/${SUBMODDIR}/easycap.ko ]; then
  echo "ERROR:  file not found: ${DEPMODDIR}/${SUBMODDIR}/easycap.ko"
  exit 1
else
  echo "copied OK"
fi
#-----------------------------------------------------------------------------
depmod -a -v 1>${WORKDIR}/depmod.out 2>${WORKDIR}/depmod.err
if [ 0 -ne $? ]; then
  echo "ERROR:  step failed:  depmod"
  cat ${WORKDIR}/depmod.err
  exit 1
else
  echo "depmod OK"
fi
rm ${WORKDIR}/depmod.out
#-----------------------------------------------------------------------------
>${WORKDIR}/modprobe.out
>${WORKDIR}/modprobe.err

if [ 0 -lt ${DEBUG} ]; then
  1>>${WORKDIR}/modprobe.out 2>>${WORKDIR}/modprobe.err \
  modprobe easycap debug="${DEBUG}"
else
  1>>${WORKDIR}/modprobe.out 2>>${WORKDIR}/modprobe.err \
  modprobe easycap
fi 
if [ 0 -ne $? ]; then
  echo "ERROR:  step failed:  modprobe"
  cat ${WORKDIR}/modprobe.err
  exit 1
fi
LSMODOUT=`lsmod | grep "^easycap " - | sed -e "s, .*$,," - `
if [ "easycap" != "${LSMODOUT}" ]; then
  echo "ERROR:  easycap module not present"
  exit 1
fi
echo "modprobe OK"
rm ${WORKDIR}/modprobe.out
if [ -e ${WORKDIR}/src/easycap.mod.c ]; then
  rm ${WORKDIR}/src/easycap.mod.c
fi
#-----------------------------------------------------------------------------
if [ -e "./57-easycap.rules" ]; then
  if [ -d "/etc/udev/rules.d" ]; then
    if [ -e "/etc/udev/rules.d/57-easycap.rules" ]; then
      echo "not overwriting /etc/udev/rules.d/57-easycap.rules"
    else
      cp -p ./57-easycap.rules /etc/udev/rules.d
      if [ -x /etc/init.d/udev ]; then /etc/init.d/udev restart; fi
    fi
  else
    echo "ERROR: directory not found: /etc/udev/rules.d"
  fi
else
  echo "ERROR: file not found: ./57-easycap.rules"
fi
exit 0

