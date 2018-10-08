FROM python

MAINTAINER grezbo <grezboo@gmail.com>


ENV EMAIL_ADDR ''
ENV EMAIL_PASSWD ''
ENV TO_EMAIL_ADDR ''
ENV SMTP_SERVER ''
ENV INTERVAL ''

COPY main.py /main.py
RUN chmod +x /main.py

ENTRYPOINT ["./main.py"]