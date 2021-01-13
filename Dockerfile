FROM python:rc-slim-buster

COPY ./week_module_test.py .

RUN pip install pymysql 

ENTRYPOINT ["python3","week_module_test.py"]

