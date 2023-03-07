FROM python:latest

COPY . /www

WORKDIR /www

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT [ "python", "main.py" ]