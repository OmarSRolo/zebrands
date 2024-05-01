# README #

This project is a basic catalog system to manage products, built as part of a technical test for ZeBrands. Each product
has basic information such as SKU, name, price, and brand.

The system has two types of users:

Administrators who can create, update, and delete products, as well as create, update, and delete other administrators.
Anonymous users who can only retrieve product information but cannot make changes.
As a special requirement, every time an administrator makes a change to a product (for example, adjusting a price), we
notify all other administrators about the change, either by email or another mechanism.

We also track the number of times an anonymous user queries each product, so we can create some reports in the future.

The task was to build this system by implementing a REST or GraphQL API using the stack of your preference.

## Instalación del sistema para desarrollo en ambiente local ##

### 1- Clonar repositorio:

```bash
git clone https://github.com/OmarSRolo/zebrands.git 
```

### 2- Accede a la carpeta:

```bash
cd zebrands/
```

### 3- Instalar dependencias de desarrollo y de testing:

```bash
pip install -r ./requirements/local.txt && pip install -r ./requirements/test.txt
```

### 4- Crear base de datos:

* Crear base de datos zibrands

### 5- Correr migraciones:

```bash
python manage.py migrate --settings=project.settings.local
```

### 6- Crear super usuario:

```bash
python manage.py createsuperuser --settings=project.settings.local
```

### 7- Cargar datos de pruebas:

```bash
python manage.py loaddata fixtures/load/data.json --settings=project.settings.local
```

### 8- Ejecutar test del sistema:

```bash
python manage.py test --settings=project.settings.test
```

### 9- Correr el proyecto:

```bash
python manage.py runserver --settings=project.settings.local
```

### 10- Generar reporte de Coverage:

```bash
coverage run --source='.' manage.py test --settings=project.settings.test
```

#### 11- Generar reporte:

```bash
coverage html
```

### 12- Correr Celery Worker para tareas asincrónicas:

```bash
celery -A project worker -l debug
```

### 13- Correr flower para monitorizar las tareas:

```bash
celery -A project flower --conf=project/settings/flower.py
```

## Instalación con docker-compose ##

### 1- Clonar repositorio:

```bash
git clone https://github.com/OmarSRolo/zebrands.git 
```

### 2- Accede a la carpeta:

```bash
cd zebrands/
```

### 3- Ejecutar el proyecto:

```bash
docker-compose -f docker-compose-dev.yml up --build ###
```

## Usar:

Abrir navegador y entrar en la URL http://localhost:8000/api/v1/docs/

## Arquitectura:

El proyecto fue construido usando Django como framework principal. Cada uno de sus componentes puede ser escalado tanto
horizontal como vertical. Como servidor para tareas asincrónicas se usó celery con redis como broker para permitir su
escalado.

## Estructuras de carpetas:

1. **project**: Contiene los archivos de configuraciones globales de django y celery además las urls
   principales del sistema
2. **cronjobs**: Contiene las tareas de celery
3. **apps**: Contiene todas las apps del sistema.
4. **core**: Contiene los archivos bases de los servicios genéricos sin lógica de negocio
5. **infrastructure**: Contiene los servicios, factorías y entidades del dominio.

### Seguridad:

Se implementó sistema de roles y permisos a los usuarios basado en el protocolo JWT. Cada endpoint excepto los públicos
se protegieron por permisos específicos. 

## Patrones:

Como patrón principal para las operaciones de CRUD de los modelos dada las características del proyecto se usó el
TemplateMethod. Cada servicio del sistema hereda de servicio padre que contiene las operaciones básicas.

Para el sistema de notificaciones se usó un servicio de uso genérico que permite enviar a celery las tareas
correspondientes.

### Despliegue:

Contiene dos formas principales de despliegue:

1. Sistema básico basado en entornos virtuales donde principalmente puede desplegarse en VPS con todos sus componentes.
2. Sistema de despliegue basado en docker y docker compose que permite una mayor escalabilidad tanto del proyecto como
   de sus componentes. Permite despliegue en servicios como Kubernates o ECS de AWS.

Se configuró una integración contínua usando github actions para testeo y despliegue continuo.

### Testing:

Tipos de testing implementados:

1. Test de integración: Usando las herramientas de testing de Django y Django Rest Framework se validaron los servicios
   creados en cada módulo usando datos pre cargados y autogenerados.
2. Test End2End: Se modelaron usando factory-boys los diferentes modelos del negocio para generar aleatoriamente datos y
   testear los diferentes endpoints. Se parametrizaron los conjuntos de datos para probar casos extremos.