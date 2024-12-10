FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]

# To run:
# docker build -t flask-app .
# docker run --network host flask-app
# this is so we can access the app on 127.0.0.1:5000