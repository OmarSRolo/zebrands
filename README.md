# README #

Zebrands

## Instalación del sistema para desarrollo en ambiente de desarrollo ##

### 1- Instalar dependencias de desarrollo y de testing:

```bash
pip install -r ./requirements/local.txt && pip install -r ./requirements/test.txt
```

### 2- Crear bases de datos:

* Crear base de datos zibrands

### 3- Correr migraciones para ambas bases de datos:

```bash

python manage.py migrate --settings=project.settings.local
```

### 4- Crear super usuario:

```bash

python manage.py createsuperuser --settings=project.settings.local
```

### 5- Cargar los datos de pruebas:

```bash

python manage.py loaddata fixtures/load/data.json --settings=project.settings.local
```

### 6- Ejecutar todos los test del sistema:

```bash
python manage.py test --settings=project.settings.test
```

### 7- Correr el proyecto

```bash
python manage.py runserver --settings=project.settings.local
```

### 8- Generar reporte de Coverage

```bash
coverage run --source='.' manage.py test --settings=project.settings.test
```

#### 9- Generar reporte

```bash
coverage html
```

### 10- Correr Celery Worker para tareas asincrónicas

```bash
celery -A project worker -l debug
```

### 11- Correr flower para monitorizar las tareas

```bash
celery -A project flower --conf=project/settings/flower.py
```