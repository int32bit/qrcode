FROM python:2
MAINTAINER int32bit krystism@gmail.com

RUN set -ex \
        && apt-get -y update  \
        && apt-get install -y --no-install-recommends python-qrtools \
        && sed -i '181s/tostring/tobytes/' /usr/lib/python2.7/dist-packages/qrtools.py \
        && rm -rf /var/lib/apt/lists/*

ADD . /opt/qrcode
RUN pip install -r /opt/qrcode/requirements.txt
WORKDIR /root
ENTRYPOINT ["/opt/qrcode/endpoint.sh"]
CMD ["--help"]
