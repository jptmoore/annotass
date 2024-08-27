FROM chromadb/chroma:latest

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./annotass /app

ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=10000

ENTRYPOINT ["python"]
CMD ["app.py"]
