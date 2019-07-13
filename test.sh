#!/bin/bash
set -e
STP="$HOME/.config/sublime-text-$SUBLIME_TEXT_VERSION/Packages"

if [ ! -f /etc/init.d/xvfb ]; then
    echo installing xvfb controller
    wget -O /etc/init.d/xvfb https://gist.githubusercontent.com/randy3k/9337122/raw/xvfb
    chmod +x /etc/init.d/xvfb
fi

if [ -z $DISPLAY ]; then
    export DISPLAY=:1
fi

if [ $DISPLAY ]; then
    sh -e /etc/init.d/xvfb start
fi

if [ ! -d "$STP/$PACKAGE" ]; then
    # symlink does not play well with coverage
    echo "copy the package to sublime package directory"
    mkdir -p "$STP/$PACKAGE"
    cp -r ./ "$STP/$PACKAGE"
fi

# Disable warnings about detached HEAD
# https://stackoverflow.com/questions/36794501
git config --global advice.detachedHead false

UT_PATH="$STP/UnitTesting"
if [ ! -d "$UT_PATH" ]; then

    if [ -z $UT_URL ]; then
        UT_URL="https://github.com/randy3k/UnitTesting"
    fi

    if [ -z $UNITTESTING_TAG ]; then
        if [ $SUBLIME_TEXT_VERSION -eq 2 ]; then
            UNITTESTING_TAG="0.10.6"
        elif [ $SUBLIME_TEXT_VERSION -eq 3 ]; then
            # latest tag
            UNITTESTING_TAG=$(git ls-remote --tags "$UT_URL" |
                  sed 's|.*/\(.*\)$|\1|' | grep '^[0-9]*\.[0-9]*\.[0-9]*$' |
                  sort -t. -k1,1nr -k2,2nr -k3,3nr | head -n1)
        fi
    fi

    echo "download UnitTesting tag: $UNITTESTING_TAG"
    git clone --quiet --depth 1 --branch $UNITTESTING_TAG "$UT_URL" "$UT_PATH"
    git -C "$UT_PATH" rev-parse HEAD
    echo
fi

python "$STP/UnitTesting/sbin/run_tests.py" "$PACKAGE"

pkill "[Ss]ubl" || true
pkill 'plugin_host' || true
sleep 2
