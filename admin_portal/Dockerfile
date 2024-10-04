FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8502

COPY . .

ENTRYPOINT ["streamlit", "run", "1_🏠_Home_Page.py", "--server.port=8502", "--server.address=0.0.0.0"]