FROM python:3.7.4-alpine3.10
LABEL authors="STCB"

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]

ENTRYPOINT ["top", "-b"]