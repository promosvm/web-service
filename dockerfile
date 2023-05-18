FROM python:3.6-slim  

COPY . /root 

WORKDIR /root

RUN pip install flask gunicorn numpy joblib scipy scikit-learn flask_wtf pandas 