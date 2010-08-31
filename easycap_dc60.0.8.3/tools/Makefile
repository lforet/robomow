#
# Makefile in tools subdirectory
#

THISDIR = `pwd`

all:	tailer

tailer:	tailer.c
	@${CC} -o tailer tailer.c
	@mv tailer ..

clean:
	@rm -f *.o tailer ../tailer

