FROM python:3.8-alpine
VOLUME /etc/zhs
COPY . /etc/zhs
WORKDIR /etc/zhs

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.14/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.14/community" >> /etc/apk/repositories
RUN apk update

# add Dependencies for building
RUN apk add libffi-dev
RUN apk add python3-dev build-base
RUN python -m pip install --upgrade pip

# install chromedriver
RUN apk update
RUN apk add chromium chromium-chromedriver

# install rest
RUN pip install -r requirements.txt

# set display port to avoid crash
# ENV DISPLAY=:99

#
ENV AM_I_IN_A_DOCKER_CONTAINER Yes

# CMD ["python", "--version"]
CMD ["sh", "./launch.sh"]

