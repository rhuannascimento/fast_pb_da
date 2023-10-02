FROM python:3

WORKDIR /python_etl

COPY . .

RUN pip3 install pymongo
RUN pip3 install pandas
RUN pip3 install sqlalchemy
RUN pip3 install psycopg2

CMD ["python", "./etl.py"]