FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

#FastAPI's default port.
EXPOSE 8000
ENV FASTAPI_APP=app.main:app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
