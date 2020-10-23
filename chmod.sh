#!/bin/bash
SP="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SP
rm -f containerless/sync clones/sync bots/sync
echo -e "#!/bin/bash\ncd ..\npython3 sync"|tee containerless/sync clones/sync bots/sync>/dev/null
chmod +x sync clean chmod.sh build up down reboot log containerless/log containerless/sync clones/sync bots/sync containerless/up containerless/down containerless/build bots/build bots/log bots/up bots/down clones/up clones/log clones/down clones/build
echo "Done!!!"