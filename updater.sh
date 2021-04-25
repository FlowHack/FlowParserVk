#!/bin/bash

echo "Обновление python3 до актуальной версии"
sleep 2
sudo apt reinstall python3 -y

echo "Установка python3-venv"
sleep 2
sudo apt install python3-venv -y

echo "Установка python3-pip"
sleep 2
sudo apt install python3-pip -y

echo "Создание виртуального окружения"
sleep 2
python3 -m venv venv
source "$PWD/venv/bin/activate"

echo "Установка зависимостей"
sleep 2
pip3 install wheel
pip3 install requirements.txt

echo "Запуск программы"
python3 linux.py
