# discretizando-el-tiempo-continuo

Para poder levantar el proyecto usted debe ejecutar:

```
docker compose up -d --build
docker compose exec api python manage.py migrate
docker compose exec api python poblar_personajes.py
```

- `migrate` crea las tablas en la base de datos.
- `poblar_personajes.py` carga los personajes jugables (incluidos los perros, cuyas imágenes están en `static/`).

Luego verifique la url: localhost:8000/api/seleccion-personaje

Si hay un error de conexion con la base de datos, cambiar 'db' por localhost o docker.internal.host o llame al profesor
