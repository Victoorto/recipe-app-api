FROM python:3.13-slim
LABEL org.opencontainers.image.authors="santoazul.com"
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /app
WORKDIR /app

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 \
        libjpeg62-turbo \
        zlib1g && \
    apt-get install -y --no-install-recommends --no-install-suggests \
        build-essential \
        libpq-dev \
        libjpeg-dev \
        zlib1g-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    apt-get remove -y build-essential libpq-dev libjpeg-dev zlib1g-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

COPY --chown=django-user:django-user ./app /app

EXPOSE 8000

USER django-user

CMD ["run.sh"]
