FROM python:3.8

WORKDIR /db

COPY . /db

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "create_db.py"]
