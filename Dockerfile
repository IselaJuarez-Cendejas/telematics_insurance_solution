version: '3.8'

services:
  backend:
    build:
      context: ./telematics_insurance_backend
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    volumes:
      - ./telematics_insurance_backend/src/database:/app/src/database
    environment:
      - FLASK_APP=main.py
      - FLASK_RUN_HOST=0.0.0.0
    depends_on:
      - frontend

  frontend:
    build:
      context: ./telematics_dashboard
      dockerfile: Dockerfile
    ports:
      - "80:80"
