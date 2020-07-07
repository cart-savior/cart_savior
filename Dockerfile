FROM python:3.8.3-slim

ADD flask/requirements.txt ./
RUN pip install -r requirements.txt

ADD flask/ ./
CMD python application.py