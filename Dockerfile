FROM jess/sublime-text-3
RUN apt-get update && apt-get install -y apt-utils git xvfb wget python3 procps
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN mkdir /wd
WORKDIR /wd
COPY . .
