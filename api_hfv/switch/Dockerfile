FROM opengn.org:32333/easypi/alpine-arm
MAINTAINER joliu<joliu@s-an.org>
WORKDIR /data
RUN apk --update add python3 py3-pip tzdata
RUN pip3 install pymysql
COPY tcpOnclient.py /data
COPY tcpOffclient.py /data
COPY tcpserver.py /data

CMD python3 /data/tcpserver.py
