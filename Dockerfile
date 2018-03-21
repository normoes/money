FROM python:3.6-alpine

ENV PORT 5000

RUN mkdir /data
COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /data

VOLUME ["/data"]

EXPOSE $PORT

ENTRYPOINT ["python", "/data/server.py"]
CMD [""]
