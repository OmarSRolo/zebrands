FROM python:3.12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONOPTIMIZE=TRUE

COPY . .

RUN pip install --no-cache-dir --upgrade -r /requirements/local.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "--settings=project.settings.local"]
