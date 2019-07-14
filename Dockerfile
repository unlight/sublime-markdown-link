FROM jess/sublime-text-3
RUN apt-get update && apt-get install -y apt-utils git xvfb wget python3 python3-pip procps
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 2
RUN pip install st-package-reviewer
RUN mkdir /wd
WORKDIR /wd
COPY . .
