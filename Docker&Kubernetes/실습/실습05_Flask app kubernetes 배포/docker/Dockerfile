FROM python
WORKDIR /app
COPY app.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD [ "python", "/app/app.py" ]
