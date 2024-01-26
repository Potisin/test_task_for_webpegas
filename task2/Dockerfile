FROM python:3.10

RUN mkdir /test_task_for_webpegas

WORKDIR /test_task_for_webpegas

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

