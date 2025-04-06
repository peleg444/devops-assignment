# בסיס: מערכת רזה של לינוקס עם פייתון 3.11
FROM python:3.11-slim

# נבצע את כל הפעולות מתוך תיקיית /app בתוך הקונטיינר
WORKDIR /app

# נעתיק את כל הקבצים שבתוך my_app לתוך הקונטיינר
COPY . /app

# נתקין את התלויות של Flask ו-MySQL Connector
RUN pip install -r requirements.txt

# נריץ את Flask
CMD ["python", "app.py"]
