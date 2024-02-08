FROM python:3.11.7-alpine3.19

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY app /code/app

COPY main.py config.py /code/

EXPOSE 5000

ENV FLASK_APP=main.py

# CMD ["flask", "run", "--host=0.0.0.0" ]

CMD ["python", "main.py", "--host=0.0.0.0"]