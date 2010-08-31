#
# Makefile in source subdirectory
#

obj-m		+= easycap.o
easycap-objs	:= easycap_main.o easycap_low.o easycap_sound.o
easycap-objs	+= easycap_ioctl.o easycap_settings.o
easycap-objs	+= easycap_testcard.o

KERNELDIR ?= /lib/modules/2.6.32-21-generic/build
PWD       := $(shell pwd)

EXTRA_CFLAGS += -Wall -Wframe-larger-than=8192
export EXTRA_CFLAGS

all:
	$(MAKE) -C $(KERNELDIR) M=$(PWD) modules

clean:
	@rm -rf *.o *~ core .depend .*.cmd *.ko *.mod.c .tmp_versions

