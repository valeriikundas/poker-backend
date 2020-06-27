FROM python:3.8.0-alpine
WORKDIR /backend
RUN apk add --no-cache gcc musl-dev linux-headers curl libffi-dev openssl-dev python3-dev
RUN pip install --upgrade pip
RUN pip install poetry
COPY pyproject.toml pyproject.toml
RUN poetry install
COPY . .
RUN poetry shell
CMD ["python", "app.py"]