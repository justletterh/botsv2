#!/bin/bash
SP="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SP
chmod +x up down build reboot restart push log controlup controldown controlreboot controlbuild chmod.bash&&echo "Done!!!"