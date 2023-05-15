FROM python:3.10

WORKDIR /

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt
RUN mkdir /hr-app

COPY ./hr-app /hr-app
WORKDIR /hr-app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
