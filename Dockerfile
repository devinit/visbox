# start with a base image
FROM django:1.10.1-python2
MAINTAINER vagrant <Alex Miller, alex.miller@devinit.org>

RUN mkdir /src
ADD ./ /src

WORKDIR /src
# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get --assume-yes install wget
RUN /src/grab_chrome.sh
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput

CMD gunicorn -w 2 -k gevent -b 0.0.0.0:80 visbox.wsgi
