FROM python:3.8-slim

WORKDIR /services/

COPY authentication_service/requirements.txt .
RUN pip install -r requirements.txt

COPY proto/ services/proto
COPY authentication_service/ services/authentication_service

EXPOSE 5000

ENV FLASK_APP=services.authentication_service.app.py

CMD ["flask", "run", "--host=0.0.0.0"]
