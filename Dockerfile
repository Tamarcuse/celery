FROM python:3.9.20-slim

COPY . .
RUN pip install celery[sqs] \
  && pip install boto3 \
  && chmod +x /start.sh

CMD ["/start.sh"]