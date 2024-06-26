
FROM python:3.11

ENV PYTHONUNBUFFERED=1


WORKDIR /code

COPY requirements.txt .

RUN pip install  -r requirements.txt

EXPOSE 8000

COPY . .
# COPY . /code/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]









