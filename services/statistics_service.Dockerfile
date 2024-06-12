FROM python:3.8-slim

WORKDIR /services/

COPY statistics_service/requirements.txt .
RUN pip install -r requirements.txt

#COPY proto/ services/proto  # TODO нуджно прото тут?
COPY kafka/ services/kafka
COPY common/ services/common
COPY statistics_service/ services/statistics_service

# TODO нужно ли?
EXPOSE 51076

ENTRYPOINT ["python", "-m", "services.statistics_service.statistics_service"]
