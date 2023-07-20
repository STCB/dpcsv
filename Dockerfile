FROM python:3
LABEL authors="STCB"

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "export-to-csv.py"]

ENTRYPOINT ["top", "-b"]
