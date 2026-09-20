FROM python:3.10.5-slim

# Must match the owner of the bind-mounted media/static dirs on the host.
ARG APP_UID=1000
ARG APP_GID=1000

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_SETTINGS_MODULE=config.settings

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN if ! getent group "${APP_GID}" >/dev/null; then groupadd -g "${APP_GID}" app; fi \
    && if ! getent passwd "${APP_UID}" >/dev/null; then \
           useradd -u "${APP_UID}" -g "${APP_GID}" --create-home app; \
       fi \
    && mkdir -p /app/static /app/media /app/backups \
    && chmod +x /app/docker/entrypoint.sh \
    && chown -R "${APP_UID}:${APP_GID}" /app

USER ${APP_UID}:${APP_GID}

EXPOSE 8000

ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "1", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
