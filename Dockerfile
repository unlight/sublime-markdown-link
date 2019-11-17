# FROM jess/sublime-text-3
FROM debian:bullseye-slim
RUN apt-get update && apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    locales \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
# Generate system-wide UTF-8 locale
# Sublime might nag about Ascii issue w/ Package Control otherwise
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    echo "LANG=en_US.UTF-8" > /etc/locale.conf
# Add the sublime debian repo
RUN curl -sSL https://download.sublimetext.com/sublimehq-pub.gpg | apt-key add -
RUN echo "deb https://download.sublimetext.com/ apt/stable/" > /etc/apt/sources.list.d/sublime-text.list
# Installing the libcanberra-gtk-module gets rid of a lot of annoying error messages.
RUN apt-get update && apt-get -y install \
    libcanberra-gtk-module \
    sublime-text \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
# In order to prevent writing as root:root in Sublime, we have to run the Sublime Text container
# as the user that creates the container. Normally we do this by passing $UID.
# But just passing $UID along isn't enough - Sublime has to be started by a user that exists.
# By default in the container, the only user that actually exists is root.
# Therefore we have to create a new user, and start Sublime as that user.
# This is not possible at build time, so the /run.sh script accepts an environment
# variable called $NEWUSER that creates a user and group named $USER.
# Additional note: Sublime puts a lot of stuff in ~/.config, which is mounted at runtime. Without this directory being mounted, settings/packages/etc won't persist.
RUN apt-get update && apt-get install -y apt-utils git xvfb x11-xserver-utils wget python3 python3-pip procps
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 2
RUN pip install st-package-reviewer
RUN mkdir /wd
WORKDIR /wd
COPY . .
