# Pythonizame Blog

Powered by Django and PostGreSQL

# Pre Requisitos

### PostGreSQL en MAC:

```bash
$[kiubtech] export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/<version>/bin
```

donde <version> es la versión instalada de PostGreSQL. Ejemplo, para el caso de PostGreSQL v 9.5 sería
```bash
$[kiubtech] export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.5/bin
```


# Instalación

## Paso 1. Clonar repositorio. 

```bash
$[kiubtech] git clone https://github.com/kiubtech/pythonizame.git
```

## Paso 2. Instalar requerimientos

```bash
$[kiubtech] cd pythonizame/requirements
$[kiubtech] pip install -r local.txt
```

## Paso 3. Crear archivo settings.json

Al descargar el proyecto podrás observar que existe un archivo llamado "settings.example.json". Es necesario crear una copia de este archivo y nombrarlo "settings.json"

```bash
$[kiubtech] cp settings.example.json settings.json
```

### Paso 3.1 Credenciales de base de datos

Es necesario configurar las credenciales de la base de datos de la siguiente manera: 

```json
"DB": {
    "ENGINE": "django.db.backends.postgresql_psycopg2",
    "HOST": "localhost",
    "NAME": "your-database",
    "USER": "your-username",
    "PASSWORD": "your-password",
    "PORT": 5432
  },
```
### Paso 3.2 Amazon S3

Si tienen una cuenta de Amazon y requieren que los archivos media funcionen con un bucket de Amazon S3, será necesario llenar la siguiente configuración.

```json
"AMAZON": {
    "AWS_ACCESS_KEY_ID": "******",
    "AWS_SECRET_ACCESS_KEY": "******",
    "S3": {
      "USE_S3": true,
      "AWS_STORAGE_BUCKET_NAME": "yourbucket",
      "AWS_S3_CUSTOM_DOMAIN": "yourbucket.s3.amazonaws.com",
      "MEDIAFILES_LOCATION": "media"
    }
  },
```

### Paso 3.3 Configuración de la URL de la web. 

Es necesario configurar "URL_SERVER" y agregarlo en la sección "ALLOWED_HOSTS" tal como lo podemos ver a continuación:

Tomando como ejemplo el dominio www.pythoniza.me


```json
"SECURITY": {
    "LOGIN_REDIRECT_URL": "/management/dashboard/",
    "ALLOWED_HOSTS": [
      "pythoniza.me",
      "www.pythoniza.me"
    ]
  },
"URL_SERVER": "https://www.pythoniza.me",
```

MEDIAFILES_LOCATION es la configuración para poder definir una carpeta específica para los archivos media de los usuarios. 



# Licenciamiento.

MIT License

    Copyright (c) 2018 Kiub Technologies
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.


# Live demo

Puedes conocer el proyecto en acción accediendo a nuestro blog [Pythonízame](https://www.pythoniza.me)

# Créditos

Core Team:

- [Alex Dzul](https://github.com/alexdzul)
- [Gaspar Dzul](https://github.com/gaspardzul)
- [Daniel Wong](https://github.com/dwong27)
- [Carlos Uicab](https://github.com/CarlosUicab)


Make with love by [@kiubtech](https://twitter.com/kiubtech) and [@pythonizame](https://twitter.com/pythonizame).
