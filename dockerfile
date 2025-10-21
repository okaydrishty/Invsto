FROM python:3.8-slim
RUN apt-get update && apt-get install -y \
    libatomic1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

#Generate the Prisma client
RUN prisma generate
RUN prisma migrate dev 

#Import data into the database
RUN python database.py

#FastAPI's default port.
EXPOSE 8000
ENV FASTAPI_APP=main:app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]