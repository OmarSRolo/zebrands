FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONOPTIMIZE=TRUE

WORKDIR /app

COPY requirements/local.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements/local.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "--settings=project.settings.local"]
