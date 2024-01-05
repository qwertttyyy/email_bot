FROM python:3.11-slim

WORKDIR /app/src

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV TZ=Europe/Moscow

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir
RUN apt update && apt install nano

COPY . .

CMD ["python", "bot/run_bot.py"]