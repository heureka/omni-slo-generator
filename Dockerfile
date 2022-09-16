FROM python:3.10-slim

RUN apt-get update && apt-get install -y curl

RUN addgroup --gid 1000 omnigen  \
    && adduser --disabled-password -gecos '' --uid 1000 --gid 1000 omnigen

USER omnigen
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY . /app
WORKDIR /app

RUN /home/omnigen/.local/bin/poetry install -n

ENTRYPOINT ["/home/omnigen/.local/bin/poetry", "run"]
CMD ["python", "omni_slo_generator/main.py"]
