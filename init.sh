#!/bin/sh
SP="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SP
cd ./clones
git clone https://github.com/justletterh/pluralkit.git
echo "Done!!!"