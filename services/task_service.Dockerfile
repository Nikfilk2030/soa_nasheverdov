FROM python:3.8-slim

WORKDIR /services/

COPY task_service/requirements.txt .
RUN pip install -r requirements.txt

COPY proto/ services/proto
COPY task_service/ services/task_service

EXPOSE 51075

ENTRYPOINT ["python", "-m", "services.task_service.task_service"]
