FROM python:3.7

EXPOSE 9001

COPY . /app/

RUN pip install -r /app/requirements.txt

WORKDIR /app/
ENTRYPOINT ["uvicorn", "apps:app", "--host=0.0.0.0", "--port=9001", "--reload" ]
