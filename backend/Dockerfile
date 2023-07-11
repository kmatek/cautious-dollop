FROM python:3.11.3-alpine
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
RUN apk add --no-cache gcc musl-dev libffi-dev
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]