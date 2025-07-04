FROM python:3.13-alpine3.22

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000

CMD [ "flask", "run", "--host=0.0.0.0", "--port=3000"]