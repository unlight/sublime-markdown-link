#!/bin/bash

echo PACKAGE = $PACKAGE

set -e

sudo sh -e /etc/init.d/xvfb start
/docker.sh bootstrap
sudo ln -s "$HOME/sublime_text_3/sublime_text" /usr/bin/subl
/docker.sh install_package_control
/docker.sh run_tests --coverage
