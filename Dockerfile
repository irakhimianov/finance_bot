FROM python:3.10
RUN mkdir -p /usr/src/finance_bot
WORKDIR /usr/src/finance_bot
COPY . /usr/src/finance_bot

ENV TELEGRAM_API_TOKEN=""
ENV ADMIN=""
ENV ADMINS=""
ENV GEO_TOKEN=""
ENV WEATHER_TOKEN=""
ENV EXCHANGERATE_TOKEN=""

RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]