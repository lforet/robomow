#!/bin/bash
#
#
#  tail.sh
#
#  Usage:  ./tail.sh
#
#
#------------------------------------------------------------------------------
TAILER="./tailer"
if [ ! -x ${TAILER} ]; then
  echo "ERROR:  missing executable: ${TAILER}"
  exit 1
fi
${TAILER}
if [ 0 != $? ]; then
  echo "ERROR:  failed: ${TAILER}"
  exit 1
fi
cat /tmp/tail | sed -e "s,^.*easycap:,," >./kern.log
exec view ./kern.log
exit 0

