FROM chromadb/chroma:latest

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./annotass /app

ENTRYPOINT ["python", "app.py"]
