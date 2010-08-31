#!/bin/bash
#
#
#  install.sh
#
#
#  Usage:  ./install.sh
#          ./install.sh kernel_directory
#
#  With no command-line argument the build is against the running kernel.
#  In this case the easycap module is removed and reinstalled.  This is
#  the usual choice.
#
#  The optional argument kernel_directory is the name of a top kernel
#  directory (which contains the MAINTAINERS file).  With this argument
#  the easycap module is rebuilt, but obviously not installed.  This
#  choice is for testing and maintenance only.
#
#
#  This script has been tested on:   Debian Lenny,  64-bit
#                                    Ubuntu 10.04,  32-bit
#                                    OpenSUSE 11.2, 64-bit
#
#-----------------------------------------------------------------------------
#  DEBUG=n    the easycap module is configured at diagnostic level n (0 to 9)
#  CLIENT=0   the easycap module is independent of the videodev module
#  CLIENT=1   the easycap module registers as a client of the videodev module
#  WFRAME=0   heeds the warning: the frame size ... is larger than 1024 bytes
#  WFRAME=1   overcomes this warning
#-----------------------------------------------------------------------------
DEBUG=0
CLIENT=0
WFRAME=1
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
KERNELDIR=""
if [ "x" != "x$1" ]; then KERNELDIR="$1"; fi
#-----------------------------------------------------------------------------
#  CHECK ESSENTIAL COMPONENTS PRESENT
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

#KERNELDIR=/home/rmthomas/KERNEL/linux-new
if [ -z "${KERNELDIR}" ]; then KERNELDIR="${DEPMODDIR}/build"; fi

if [ -z "${KERNELDIR}" ]; then
  echo "ERROR:  Kernel build directory is not set"
  exit 1
fi
if [ ! -d "${KERNELDIR}" ]; then
  echo "ERROR:  cannot find directory ${KERNELDIR}"
  echo "        Are the kernel headers installed correctly?"
  exit 1
fi
echo "kernel directory is ${KERNELDIR}"
#-----------------------------------------------------------------------------
#  CREATE TEMPORARY SUBDIRECTORY FOR CONFIGURATION TESTS
#-----------------------------------------------------------------------------
TAGFILE="./tmpsrc/this_directory_may_be_removed_by_easycap_installer"
if [ -d ./tmpsrc ]; then
  if [ -e "${TAGFILE}" ]; then
    rm -fR ./tmpsrc
  else
    echo "ERROR: directory ./tmpsrc unexpectedly exists."
    echo "       Please remove it after saving any valuable contents."
    exit 1
  fi
fi
mkdir ./tmpsrc
>${TAGFILE}
#-----------------------------------------------------------------------------
#  RECENT VERSIONS OF gcc ACCEPT THE FLAG -Wframe-larger-than=n
#  BUT THIS FLAG IS UNKNOWN TO EARLIER VERSIONS AND GENERATES AN ERROR.
#  SO TRY IT AND SEE.
#-----------------------------------------------------------------------------
if [ 1 -eq ${WFRAME} ]; then
  echo "int main(void) {return 0;}" >./tmpsrc/tmp.c
  sleep 1; touch ./tmpsrc/tmp.c; sleep 1
  1>./tmpsrc/tmp.out 2>./gcc.err \
  gcc -o ./tmpsrc/exe -Wframe-larger-than=8192 ./tmpsrc/tmp.c
  if [ -s "./gcc.err" ]; then
    echo "flag -Wframe-larger-than not needed for this compiler"
    WFRAME=0
  fi
  rm gcc.err
fi
#-----------------------------------------------------------------------------
#  IF the easycap MODULE IS BEING BUILT AS A CLIENT OF THE videodev MODULE
#  FURTHER CONFIGURATION IS NECESSARY.  FIRST CREATE A COUPLE OF MAKEFILES ...
#-----------------------------------------------------------------------------
if [ 1 -eq ${CLIENT} ]; then
  cat >"./tmpMakefile" <<AAAAAAAA
#
# Temporary top-level makefile.  May be deleted.
#
ALL:	build
build:
	@cd tmpsrc; make
AAAAAAAA

  cat >"./tmpsrc/Makefile" <<BBBBBBBB
#
# Temporary tmpsrc/Makefile.  May be deleted.
#

obj-m     += tmp.o

KERNELDIR ?= ${KERNELDIR}
PWD       := \$(shell pwd)

EXTRA_CFLAGS += -Wall

all:
	\$(MAKE) -C \$(KERNELDIR) M=\$(PWD) modules

BBBBBBBB
#-----------------------------------------------------------------------------
#  ... THEN PERFORM TEST COMPILATIONS AS FOLLOWS
#-----------------------------------------------------------------------------
#  COMPILATION AGAINST VERY RECENT KERNELS REQUIRES INCLUSION OF
#  <v4l2-device.h> AS WELL AS <v4l2-dev.h>.
#-----------------------------------------------------------------------------
  echo "#include <media/v4l2-dev.h>" >>./tmpsrc/tmp.c
  echo "#include <media/v4l2-device.h>" >>./tmpsrc/tmp.c
  echo "int main(void) {return 0;}" >>./tmpsrc/tmp.c
  sleep 1; touch ./tmpMakefile ./tmpsrc/Makefile ./tmpsrc/tmp.c; sleep 1
  make -f tmpMakefile 1>./tmpsrc/tmp.out 2>./make.err
  if [ \( 0 -ne $? \) -o \( -s "./make.err" \) ]; then
    echo "<media/v4l2-device.h> will not be included"
    EASYCAP_NEEDS_V4L2_DEVICE_H=""
  else
    echo "<media/v4l2-device.h> will be included"
    EASYCAP_NEEDS_V4L2_DEVICE_H="yes"
  fi
  rm -fR make.err
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  CHECK THAT video_register_device() IS DEFINED
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  rm ./tmpsrc/tmp.c
  echo "#include <media/v4l2-dev.h>" >./tmpsrc/tmp.c
  if [ ! -z "${EASYCAP_NEEDS_V4L2_DEVICE_H}" ]; then
    echo "#include <media/v4l2-device.h>" >>./tmpsrc/tmp.c
  fi
  echo "int main(void) {struct video_device *pv;" >>./tmpsrc/tmp.c
  echo "int r,t,n;" >>./tmpsrc/tmp.c
  echo "pv=NULL;t=0;n=0;" >>./tmpsrc/tmp.c
  echo "r=video_register_device(pv,t,n);return(0);}" >>./tmpsrc/tmp.c
  sleep 1; touch ./tmpMakefile ./tmpsrc/Makefile ./tmpsrc/tmp.c; sleep 1
  make -f tmpMakefile 1>./tmpsrc/tmp.out 2>./make.err
  if [ \( 0 -ne $? \) -o \( -s "./make.err" \) ]; then
    echo "ERROR: video_register_device() cannot be used"
    cat ./tmpsrc/tmp.c
    cat ./make.err
    rm ./make.err
    rm -fR ./tmpMakefile ./tmpsrc
    exit 1
  fi
  rm make.err
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  IT IS NECESSARY TO ASCERTAIN THE V4L2 TYPE OF video_device.fops, BECAUSE
#  THIS CHANGED IN DECEMBER 2008.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  rm ./tmpsrc/tmp.c
  echo "#include <media/v4l2-dev.h>" >./tmpsrc/tmp.c
  if [ ! -z "${EASYCAP_NEEDS_V4L2_DEVICE_H}" ]; then
    echo "#include <media/v4l2-device.h>" >>./tmpsrc/tmp.c
  fi
  echo "int main(void) {struct video_device v;" >>./tmpsrc/tmp.c
  echo "struct v4l2_file_operations f;" >>./tmpsrc/tmp.c
  echo "v.fops = &f;return(0);}" >>./tmpsrc/tmp.c
  sleep 1; touch ./tmpMakefile ./tmpsrc/Makefile ./tmpsrc/tmp.c; sleep 1
  make -f tmpMakefile 1>./tmpsrc/tmp.out 2>./make.err
  if [ \( 0 -ne $? \) -o \( -s "./make.err" \) ]; then
    echo "struct v4l2_file_operations will not be used"
    rm ./make.err

    rm ./tmpsrc/tmp.c
    echo "#include <media/v4l2-dev.h>" >./tmpsrc/tmp.c
    if [ ! -z "${EASYCAP_NEEDS_V4L2_DEVICE_H}" ]; then
      echo "#include <media/v4l2-device.h>" >>./tmpsrc/tmp.c
    fi
    echo "int main(void) {struct video_device v;" >>./tmpsrc/tmp.c
    echo "struct file_operations f;" >>./tmpsrc/tmp.c
    echo "v.fops = &f;return(0);}" >>./tmpsrc/tmp.c
    sleep 1; touch ./tmpMakefile ./tmpsrc/Makefile ./tmpsrc/tmp.c; sleep 1
    make -f tmpMakefile 1>./tmpsrc/tmp.out 2>./make.err
    if [ -s "./make.err" ]; then
      echo "struct file_operations not appropriate either"
      cat ./make.err
      rm ./make.err
      rm -fR ./tmpMakefile ./tmpsrc
      exit 1
    else
      echo "struct file_operations OK"
      EASYCAP_NEEDS_V4L2_FOPS=""
    fi
  else
    echo "struct v4l2_file_operations OK"
    EASYCAP_NEEDS_V4L2_FOPS="yes"
  fi
  rm ./make.err
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
else
  EASYCAP_NEEDS_V4L2_DEVICE_H=""
  EASYCAP_NEEDS_V4L2_FOPS=""
fi
rm -fR ./tmpMakefile ./tmpsrc
#-----------------------------------------------------------------------------

WORKDIR=`pwd`

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
# CREATE Makefile, src/Makefile AND tools/Makefile FOR BUILD AS NECESSARY
#-----------------------------------------------------------------------------
if [ -e "./Makefile" ]; then
  echo "not overwriting top level Makefile"
else
  echo "-> regenerating top level Makefile"
  cat >"./Makefile" <<CCCCCCCC
#
# Makefile at top level
#

ALL:	build

build:
	@echo "Building"
	@cd src; make
	@cd tools; make

clean:
	@echo "Cleaning"
	@cd src; make clean
	@cd tools; make clean

CCCCCCCC
  chmod ugo+rw ./Makefile
fi
FLAGS="-Wall"
if [ 0 -ne ${WFRAME} ]; then FLAGS="${FLAGS} -Wframe-larger-than=8192"; fi
if [ 0 -lt ${DEBUG} ]; then FLAGS="${FLAGS} -DEASYCAP_DEBUG=${DEBUG}"; fi
if [ 1 -eq ${CLIENT} ]; then
  FLAGS="${FLAGS} -DEASYCAP_IS_VIDEODEV_CLIENT"
  if [ ! -z ${EASYCAP_NEEDS_V4L2_FOPS} ]; then
    FLAGS="${FLAGS} -DEASYCAP_NEEDS_V4L2_FOPS"
  fi
  if [ ! -z ${EASYCAP_NEEDS_V4L2_DEVICE_H} ]; then
    FLAGS="${FLAGS} -DEASYCAP_NEEDS_V4L2_DEVICE_H"
  fi
fi

TMPFNM=`mktemp`
cat >"${TMPFNM}" <<DDDDDDDD
#
# Makefile in source subdirectory
#

obj-m		+= easycap.o
easycap-objs	:= easycap_main.o easycap_low.o easycap_sound.o
easycap-objs	+= easycap_ioctl.o easycap_settings.o
easycap-objs	+= easycap_testcard.o

KERNELDIR ?= ${KERNELDIR}
PWD       := \$(shell pwd)

EXTRA_CFLAGS += ${FLAGS}
export EXTRA_CFLAGS

all:
	\$(MAKE) -C \$(KERNELDIR) M=\$(PWD) modules

clean:
	@rm -rf *.o *~ core .depend .*.cmd *.ko *.mod.c .tmp_versions

DDDDDDDD
if [ -e "./src/Makefile" ]; then
  diff ${TMPFNM} ./src/Makefile >./install.tmp
  if [ -s ./install.tmp ]; then
    SUFFIX="_`date +%s`"
    echo "-> saving former src/Makefile as src/Makefile${SUFFIX}"
    mv ./src/Makefile ./src/Makefile${SUFFIX}
    echo "-> regenerating src/Makefile"
    mv ${TMPFNM} ./src/Makefile
  else
    echo "not overwriting src/Makefile"
    rm ${TMPFNM}
  fi
  rm ./install.tmp
else
  echo "---> generating src/Makefile"
  mv ${TMPFNM} ./src/Makefile
fi
chmod ugo+rw ./src/Makefile

if [ -e "./tools/Makefile" ]; then
  echo "not overwriting tools/Makefile"
else
  echo "---> generating tools/Makefile"
  cat >"./tools/Makefile" <<EEEEEEEE
#
# Makefile in tools subdirectory
#

THISDIR = \`pwd\`

all:	tailer

tailer:	tailer.c
	@\${CC} -o tailer tailer.c
	@mv tailer ..

clean:
	@rm -f *.o tailer ../tailer

EEEEEEEE
  chmod ugo+rw ./tools/Makefile
fi
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
#  IF BUILDING AGAINST A NON-RUNNING KERNEL, DO NOT INSTALL IT
#-----------------------------------------------------------------------------
if [ "${KERNELDIR}" != "${DEPMODDIR}/build" ]; then exit 0; fi
#=============================================================================
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
#-------------------------------------EOF-------------------------------------
