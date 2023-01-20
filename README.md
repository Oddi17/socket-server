# socket-server
Суть работы состоит в том, чтобы обеспечить управление некоторым
устройством по сети (например, через Интернет) с помощью современного стека технологий
и средств проектирования и разработки ПО.
Задание: спроектировать и разработать две программы для для ОС Linux на языке
программирования Python:
1. Сервис, отслеживающий изменения в состоянии «умного» устройства, имитируемого
локальным файлом, согласно варианту лабораторной работы, и
получающий/передающий запросы и ответы по сетевому протоколу управления,
заданному вариантом лабораторной работы.
2. Клиентскую программу для управления устройством через сервис (и проверки работы
сервиса).
Сервис должен быть выполнен в виде консольного приложения, которое можно
запустить либо интерактивно в терминале, либо с помощью подсистемы инициализации и
управления службами systemd. Функциональность сервиса можно условно поделить на две
части: имитация взаимодействия (опроса или получения уведомлений) с устройством и
взаимодействие с клиентами по сети.

# Запуск

-Check for the existence of the cond.txt in your directory.This file should be named cond.txt and contain the parameters of your device

-Set the address and port in command line when running the scripts server.py and client.py when you starting (first address then port, for example - #0.0.0.0 7082) or just default values will be used - "0.0.0.0":12345

-Start file server.py #python3 server.py

-Start file client.py #python3 client.py

-After launch follow the commands in your console

-Also you can use CTRL+C for terminates the currently-running program



