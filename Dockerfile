FROM python:3.9

RUN sudo apt update
RUN sudo apt install nginx

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# COPY . /app
COPY data/ data/
COPY google/ google/ 
COPY models/ models/
COPY routes/ routes/
COPY services/ services/
COPY .env .
COPY access_check.py .
COPY ai_generator.py .
COPY app.py .
COPY create_db.py .
COPY database.py .
COPY email_utils.py .
COPY meta_data.py .
COPY utils.py .
COPY validation.py .

EXPOSE 5000

CMD CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
