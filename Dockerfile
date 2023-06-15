FROM python:3.10-slim-buster

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir pip --upgrade
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
