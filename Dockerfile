FROM python:3.14
WORKDIR /api
COPY . /api
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]