Запускалось на версии Python3.6

Клонирование репозитория:

1. git clone https://github.com/Jokend23/Computer-Vision.git

Перед запуском надо создать виртуальное окружение:
(если ОС Win, смотрим в гугл как сделать вир. окруж под Win)

1. sudo apt-get install virtualenv 
2. cd Computer-vision/
3. virtualenv -p python3.6 venv
4. source venv/bin/activate

Установка dlib:
(!для Windows!)
1. https://coderoad.ru/41912372/%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-dlib-%D0%BD%D0%B0-Windows-10 - первый ответ на вопрос

Установка dlib:
(!для linux!)
1. sudo apt-get install -y python3-setuptools build-essential cmake
2. git clone https://github.com/davisking/dlib.git
3. cd dlib
4. mkdir build
5. cd build
6. cmake ..
7. cmake --build .
8. cd ..
9. python3 setup.py install
(Дожидаемся окончания загрузки)

Установка модулей:

1. sudo apt-get install -y python3-setuptools build-essential cmake
2. pip install -r req.txt

Запуск заданий:

1. python main.py
2. python main_2.py
3. python main_out.py
4. python main_4.out.py
5. python detector.py
6. python detector_run.py
7. python road_markings.py