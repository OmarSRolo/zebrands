FROM python:3.12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONOPTIMIZE=TRUE

COPY . .

RUN pip install --no-cache-dir --upgrade -r /requirements/local.txt

EXPOSE 8000

COPY ./entrypoint.sh /entrypoint.sh

RUN sed -i 's/\r//' /entrypoint.sh

RUN chmod +x /entrypoint.sh

CMD ["python", "manage.py", "runserver", "--settings=project.settings.local"]
