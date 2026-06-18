#!/usr/bin/env bash

echo ">>> Обновление списков пакетов..."
apt-get update -y

echo ">>> Установка Python 3 и Pip..."
apt-get install -y python3 python3-pip python3-venv

echo ">>> Переход в папку приложения..."
cd /home/vagrant/app

echo ">>> Установка зависимостей из requirements.txt..."
if [ -f requirements.txt ]; then
    pip3 install -r requirements.txt
else
    echo "ERROR: requirements.txt not found in /home/vagrant/app"
    exit 1
fi

echo ">>> Запуск Web-сервиса (FastAPI)..."
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > /dev/null 2>&1 &

echo ">>> Сервис запущен! PID: $!"
echo ">>> Проверка статуса..."
ps aux | grep uvicorn
