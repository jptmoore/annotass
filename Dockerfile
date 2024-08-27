FROM chromadb/chroma:latest

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./annotass /app

EXPOSE 10000

ENV PORT=10000

ENTRYPOINT ["python", "app.py"]
