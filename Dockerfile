FROM python:3.10-alpine

RUN apk --no-cache --update-cache add gcc gfortran python3 python3-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./annotass /app

ENTRYPOINT ["python", "app.py"]
