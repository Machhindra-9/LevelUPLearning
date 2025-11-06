FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install python3-pip -y && pip3 install --no-cache-dir --break-system-packages -r requirement.txt
EXPOSE 5000
CMD ["python3","app.py"]			
