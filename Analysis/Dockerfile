FROM python:3.9

COPY proyectosemestral.py /app/
COPY oppenheimer.xlsx /app/

WORKDIR /app

# Instala las dependencias
RUN pip install numpy pandas seaborn scikit-learn wordcloud nltk tensorflow openpyxl

CMD ["python", "proyectosemestral.py"]