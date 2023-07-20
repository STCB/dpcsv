FROM python:3
LABEL authors="STCB"

COPY ./export-to-csv.py /app/app.py
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]

ENTRYPOINT ["top", "-b"]
