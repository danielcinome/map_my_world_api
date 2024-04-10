FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --upgrade -r requirements.txt
RUN cd /app && pytest app/tests -vs

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5001"]