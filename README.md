# Facerec Redis

This project is created using Python and Django together with resource of the https://github.com/ageitgey/face_recognition to doing the face recognition of the faces and storage faces images in datatraining and using Redis database to storage array how to bytes to that o face recognition happen more faster.


# Run with virtualenv

Create in a specific folder the file docker-compose.yml and copy and paste the code below:
```
version: '3.8'
services:
    redis_training:
        container_name: redis_training
        image: redis:6.2-alpine
        ports:
            - '6379:6379'
        command: redis-server --save 20 1 --loglevel warning --requirepass ##your_password##
        volumes:
            - cache:/data
volumes:
    cache:
        driver: local
```

- Run Redis database
```
$ docker compose up -d
```

### Configure virtualenv

Beside the file docker-compose.yml create the environment venv with the commands below:

```python
python -m pip install --user virtualenv

virtualenv venv

source venv/bin/activate

```

### Install requirements

Inside the root project install requirements of the project.

```
$ pip install -r requirements.txt
```

### Environment Variables
The file .env must be configured of agreement with your environment.

```
DJANGO_DEBUG=######
DJANGO_SECRET_KEY=######
DJANGO_ALLOWED_HOSTS=######,######
REDIS_HOST=######
REDIS_PORT=######
REDIS_PASSWORD=######
```

### Running project

```
$ python manage runserver

Starting development server at http://127.0.0.1:8000/

```

# Running with Docker

In the root project execute the command below:
```
$ docker compose up -d
```

## License

[MIT]([https://choosealicense.com/licenses/mit/](https://github.com/celioantony/facerec_redis/blob/main/LICENSE)https://github.com/celioantony/facerec_redis/blob/main/LICENSE)
