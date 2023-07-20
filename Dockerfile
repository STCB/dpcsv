FROM python:3
LABEL authors="STCB"

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN chmod +x export-to-csv.py

CMD ["python", "export-to-csv.py"]
