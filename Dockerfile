FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONOPTIMIZE=TRUE

WORKDIR /app

COPY requirements/base.txt base.txt
COPY requirements/dev.txt dev.txt

RUN pip install --no-cache-dir --upgrade -r dev.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "--settings=project.settings.dev"]
