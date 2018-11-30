FROM python:3.6

ADD . /app/
WORKDIR /app/

RUN pip install -r requirements.txt

EXPOSE 8085

CMD ["python", "service.py"]