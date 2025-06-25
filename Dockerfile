FROM python:3.12.11-alpine
RUN apk add --no-cache gcc musl-dev libffi-dev
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt