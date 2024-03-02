# -*- coding: utf-8 -*-
"""ProyectoSemestral.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MLD8R1ZHlDWwUoL_qx3ExknuVeXPaRA2

##Librerias
"""

import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, f1_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from wordcloud import WordCloud
from nltk.tokenize import RegexpTokenizer
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.svm import SVC
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from keras.models import Sequential
from keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Dense, Dropout
import nltk

nltk.download('stopwords')
nltk.download('punkt')

"""#Proceso de entrenamiento sin Tokenizer y StopWords

## LogisticRegression

#### Carga dataframe
"""

df = pd.read_excel('oppenheimer.xlsx')

df.head()

df

df = df[['Calificación', 'Opinión']].copy()

df.head()

df['Calificación'].hist()

target_map = {'positivo': 1, 'negativo': 0}
df['target'] = df['Calificación'].map(target_map)

df.head()

"""#### División dataset"""

df_train, df_test = train_test_split(df, test_size=0.2)

df_train

df_test

"""#### Conversion de documento de texto a matriz de terminos de documentos"""

vectorizer = TfidfVectorizer(max_features=100)

X_train = vectorizer.fit_transform(df_train['Opinión'])
X_train

X_test = vectorizer.transform(df_test['Opinión'])
X_test

Y_train = df_train['target']
Y_test = df_test['target']

"""####Entrenamiento"""

model = LogisticRegression(max_iter=1000)
model.fit(X_train, Y_train)
print()
print("LOGISTIC REGRESSION")
print("Train acc:", model.score(X_train, Y_train))
print("Test acc:", model.score(X_test, Y_test))
print()
P_train = model.predict(X_train)
P_test = model.predict(X_test)

"""####Matriz de confusión"""

cm = confusion_matrix(Y_train, P_train, normalize='true')
def plot_cm(cm):
    classes = ['positivo', 'negativo']
    df_cm = pd.DataFrame(cm, index=classes, columns=classes[::-1])
    ax = sn.heatmap(df_cm, annot=True, fmt='g')
    ax.set_xlabel("Predicción")
    ax.set_ylabel("Objetivo")

plot_cm(cm)

cm = confusion_matrix(Y_test, P_test, normalize='true')
plot_cm(cm)

"""###Vocabulario"""

word_index_map = vectorizer.vocabulary_
word_index_map

model.coef_[0]

"""###Palabras positivas"""

corte = 0.5

print("Palabras más positivas:")
for word, index in word_index_map.items():
    weight = model.coef_[0][index]
    if weight > corte:
        print(word, weight)

import numpy as np
from wordcloud import WordCloud


def show_positive_wordcloud(word_index_map, model, corte=0.5, title="Positive Words"):
    positive_words = [(word, model.coef_[0][index]) for word, index in word_index_map.items() if model.coef_[0][index] > corte]

    if not positive_words:
        print("No hay palabras positivas con un peso mayor a {}".format(corte))
        return

    positive_wordcloud_data = {word: weight for word, weight in positive_words}

    wordcloud = WordCloud(
        background_color='white',
        max_words=300,
        max_font_size=40,
        scale=3,
        random_state=1
    ).generate_from_frequencies(positive_wordcloud_data)

    fig = plt.figure(1, figsize=(15, 15))
    plt.axis('off')

    if title:
        fig.suptitle(title, fontsize=20)
        fig.subplots_adjust(top=2.3)

    plt.imshow(wordcloud)
    plt.show()

show_positive_wordcloud(word_index_map, model, corte=corte, title="Positive Words Wordcloud")

"""###Palabras negativas"""

print("Palabras más negativas:")
for word, index in word_index_map.items():
    weight = model.coef_[0][index]
    if weight < -corte:
        print(word, weight)

def show_negative_wordcloud(word_index_map, model, corte=0.5, title="Negative Words"):
    negative_words = [(word, model.coef_[0][index]) for word, index in word_index_map.items() if model.coef_[0][index] < -corte]

    if not negative_words:
        print("No hay palabras negativas con un peso menor a {}".format(-corte))
        return

    negative_wordcloud_data = {word: weight for word, weight in negative_words}

    wordcloud = WordCloud(
        background_color='white',
        max_words=300,
        max_font_size=40,
        scale=3,
        random_state=1
    ).generate_from_frequencies(negative_wordcloud_data)

    fig = plt.figure(1, figsize=(15, 15))
    plt.axis('off')

    if title:
        fig.suptitle(title, fontsize=20)
        fig.subplots_adjust(top=2.3)

    plt.imshow(wordcloud)
    plt.show()

show_negative_wordcloud(word_index_map, model, corte=corte, title="Negative Words Wordcloud")

plt.hist(model.coef_[0], bins=30);

"""###Pruebas con otro texto"""

prueba = ["estuvo muy entretenida la película", "estuvo larga la película", "no la recomiendo"]

# Transformar la entrada con el vectorizador
x = vectorizer.transform(prueba)

# Predecir con el modelo
P = model.predict(x)

# Obtener las clases del modelo
clases = model.classes_

# Mostrar la clase predicha
for i in range (len(prueba)):
    if clases[P[i]] == 0:
        print(f"el Comentario: '{prueba[i]}' es: Negativo")
    else:
        print(f"el Comentario: '{prueba[i]}' es: Positivo")

"""## Convolutional Neural Networks (CNN)

#### Carga dataframe
"""

# Cargar datos
df = pd.read_excel('oppenheimer.xlsx')
df = df[['Calificación', 'Opinión']].copy()

# Mapeo de etiquetas
target_map = {'positivo': 1, 'negativo': 0}
df['target'] = df['Calificación'].map(target_map)

"""####División dataset"""

# Dividir datos en conjuntos de entrenamiento y prueba
df_train, df_test = train_test_split(df, test_size=0.2)

"""####Aplicar Vectorización"""

# Vectorizar texto usando one-hot encoding
vectorizer = CountVectorizer(binary=True)
X_train = vectorizer.fit_transform(df_train['Opinión']).toarray()
X_test = vectorizer.transform(df_test['Opinión']).toarray()

# Convertir etiquetas a formato numérico
le = LabelEncoder()
Y_train = le.fit_transform(df_train['target'])
Y_test = le.transform(df_test['target'])

"""####Entrenamiento"""

# Definir modelo
model = Sequential()
model.add(Dense(512, input_shape=(X_train.shape[1],), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Entrenar modelo
model.fit(X_train, Y_train, epochs=10, batch_size=32, validation_data=(X_test, Y_test))

# Evaluar modelo
y_pred = model.predict(X_test)
y_pred_binary = np.round(y_pred)
cm = confusion_matrix(Y_test, y_pred_binary)
print()
print("CNN")
print("\nReporte de Clasificación:")
print(classification_report(Y_test, y_pred_binary))

# Imprimir precisión en el conjunto de prueba
accuracy = model.evaluate(X_test, Y_test)[1]
print(f'Accuracy on test set: {accuracy}')
print("Termino de entrenamiento de CNN")
print()

"""####Matriz de confusión"""

def plot_cm(cm):
    classes = ['positivo', 'negativo']
    df_cm = pd.DataFrame(cm, index=classes, columns=classes[::-1])
    ax = sn.heatmap(df_cm, annot=True, fmt='g')
    ax.set_xlabel("Objetivo")
    ax.set_ylabel("Predicción")

# Plotear la matriz de confusión
plot_cm(cm)
plt.show()

"""####Palabras positivas"""

# Crear WordCloud para opiniones positivas
positive_reviews = df[df['target'] == 1]['Opinión'].values
positive_text = ' '.join(positive_reviews)
wordcloud_positive = WordCloud(width=800, height=400, background_color='white').generate(positive_text)

# Mostrar WordCloud para opiniones positivas
plt.figure(figsize=(6, 6))
plt.imshow(wordcloud_positive, interpolation='bilinear')
plt.title('WordCloud - Opiniones Positivas')
plt.axis('off')
plt.show()

"""####Palabras negativas"""

# Crear WordCloud para opiniones negativas
negative_reviews = df[df['target'] == 0]['Opinión'].values
negative_text = ' '.join(negative_reviews)
wordcloud_negative = WordCloud(width=800, height=400, background_color='white').generate(negative_text)

# Mostrar WordCloud para opiniones negativas
plt.figure(figsize=(6, 6))
plt.imshow(wordcloud_negative, interpolation='bilinear')
plt.title('WordCloud - Opiniones Negativas')
plt.axis('off')
plt.show()

"""##Support Vector Machine (SVM)

####Carga dataframe
"""

# Cargar datos
df = pd.read_excel('oppenheimer.xlsx')
df = df[['Calificación', 'Opinión']].copy()
df['Calificación'].hist()

# Mapeo de etiquetas
target_map = {'positivo': 1, 'negativo': 0}
df['target'] = df['Calificación'].map(target_map)

"""####División dataset"""

# Dividir datos en conjuntos de entrenamiento y prueba
df_train, df_test = train_test_split(df, test_size=0.2)

"""####Aplicar Vectorización"""

# Vectorizar texto utilizando TfidfVectorizer
vectorizer = TfidfVectorizer(max_features=100)
X_train = vectorizer.fit_transform(df_train['Opinión'])
X_test = vectorizer.transform(df_test['Opinión'])

Y_train = df_train['target']
Y_test = df_test['target']

"""####Entrenamiento"""

# Inicializar y entrenar un Support Vector Machine (SVM)
svm_model = SVC(kernel='linear', C=1.0)
svm_model.fit(X_train, Y_train)

# Hacer predicciones en el conjunto de prueba
y_pred = svm_model.predict(X_test)
print()
print("SVM")
print("\nReporte de Clasificación:")
print(classification_report(Y_test, y_pred))
print("Final entrenamiento SVM")
print()

"""####Matriz de confusión"""

# Calcular y mostrar la matriz de confusión y el informe de clasificación
cm = confusion_matrix(Y_test, y_pred)

# Visualizar la matriz de confusión
classes = ['positivo', 'negativo']
df_cm = pd.DataFrame(cm, index=classes, columns=classes[::-1])
plt.figure(figsize=(6, 4))
sn.heatmap(df_cm, annot=True, fmt='g', cmap='Blues')
plt.xlabel("Predicción")
plt.ylabel("Objetivo")
plt.title("Matriz de Confusión")
plt.show()

"""####Palabras positivas"""

# Obtener las palabras positivas según las predicciones
positive_words = df_test[df_test['target'] == 1]['Opinión']

# Concatenar las palabras positivas en un solo string
positive_text = ' '.join(positive_words)

# Crear el Word Cloud para palabras positivas
wordcloud_positive = WordCloud(width=800, height=400, background_color='white').generate(positive_text)

# Visualizar el Word Cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_positive, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud - Palabras Positivas')
plt.show()

"""####Palabras negativas"""

# Obtener las palabras negativas según las predicciones
negative_words = df_test[df_test['target'] == 0]['Opinión']

# Concatenar las palabras negativas en un solo string
negative_text = ' '.join(negative_words)

# Crear el Word Cloud para palabras negativas
wordcloud_negative = WordCloud(width=800, height=400, background_color='white').generate(negative_text)

# Visualizar el Word Cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_negative, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud - Palabras Negativas')
plt.show()

"""#Proceso de entrenamiento con Tokenizer, Stemming y StopWords

### LogisticRegression

####Carga dataframe
"""

# Carga el DataFrame desde el archivo Excel
df = pd.read_excel('oppenheimer.xlsx')

target_map = {'positivo': 1, 'negativo': 0}
df['target'] = df['Calificación'].map(target_map)

"""####Inicializar Stemming, Tokenize y StopWords"""

# Inicializa el stemmer y la lista de stopwords en español
stemmer = SnowballStemmer('spanish')
stop_words = set(stopwords.words('spanish'))

# Función para tokenizar, aplicar stemming y eliminar stopwords
def tokenize_and_stem(text):
    tokens = word_tokenize(text.lower())
    stems = [stemmer.stem(token) for token in tokens if token.isalpha() and token not in stop_words]
    return ' '.join(stems)

# Aplica la función a la columna 'Opinión' y crea una nueva columna 'op_stemmer'
df['op_stemmer'] = df['Opinión'].apply(tokenize_and_stem)

"""####División dataset"""

X_train, X_test, y_train, y_test = train_test_split(df['op_stemmer'], df['target'], test_size=0.2)

"""####Aplicación Vectorización"""

# Inicializa el vectorizador TF-IDF
vectorizer = TfidfVectorizer(max_features=100)

# Transforma los datos de entrenamiento y prueba utilizando el vectorizador
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

"""####Entrenamiento"""

# Inicializa y entrena el modelo de regresión logística
model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

# Evalúa el rendimiento del modelo en los conjuntos de entrenamiento y prueba
train_acc = model.score(X_train_tfidf, y_train)
test_acc = model.score(X_test_tfidf, y_test)
print()
print("LOGISTIC REGRESSION")
# Imprime los resultados
print("Train acc:", train_acc)
print("Test acc:", test_acc)
print("FINAL ENTRENAMIENTO LOGISTIC REGRESSION")
print()

"""####Matriz de confusión"""

cm = confusion_matrix(Y_train, P_train, normalize='true')
def plot_cm(cm):
    classes = ['positivo', 'negativo']
    df_cm = pd.DataFrame(cm, index=classes, columns=classes[::-1])
    ax = sn.heatmap(df_cm, annot=True, fmt='g')
    ax.set_xlabel("Predicción")
    ax.set_ylabel("Objetivo")

plot_cm(cm)

cm = confusion_matrix(Y_test, P_test, normalize='true')
plot_cm(cm)

"""####Palabras positivas"""

# Crear WordCloud para palabras positivas y negativas en el conjunto de entrenamiento
positive_words_train = ' '.join(X_train[y_train == 1])
negative_words_train = ' '.join(X_train[y_train == 0])

# Plotear WordCloud para palabras positivas en el conjunto de entrenamiento
plt.figure(figsize=(10, 5))
wordcloud_positive_train = WordCloud(width=800, height=400, background_color='white').generate(positive_words_train)
plt.imshow(wordcloud_positive_train, interpolation='bilinear')
plt.title('WordCloud - Palabras Positivas (Entrenamiento)')
plt.axis('off')
plt.show()

"""####Palabras negativas"""

# Plotear WordCloud para palabras negativas en el conjunto de entrenamiento
plt.figure(figsize=(10, 5))
wordcloud_negative_train = WordCloud(width=800, height=400, background_color='white').generate(negative_words_train)
plt.imshow(wordcloud_negative_train, interpolation='bilinear')
plt.title('WordCloud - Palabras Negativas (Entrenamiento)')
plt.axis('off')
plt.show()

"""### Convolutional Neural Networks (CNN)

####Carga dataframe
"""

df = pd.read_excel('oppenheimer.xlsx')

target_map = {'positivo': 1, 'negativo': 0}
df['target'] = df['Calificación'].map(target_map)

"""####Inicializar Stemming, Tokenize y StopWords"""

# Inicializa el stemmer y la lista de stopwords en español
stemmer = SnowballStemmer('spanish')
stop_words = set(stopwords.words('spanish'))

# Función para tokenizar, aplicar stemming y eliminar stopwords
def tokenize_and_stem(text):
    tokens = word_tokenize(text.lower())
    stems = [stemmer.stem(token) for token in tokens if token.isalpha() and token not in stop_words]
    return ' '.join(stems)

# Aplica la función a la columna 'Opinión' y crea una nueva columna 'op_stemmer'
df['op_stemmer'] = df['Opinión'].apply(tokenize_and_stem)

"""####Aplicar Vectorización"""

# Tokeniza las opiniones y convierte las secuencias en vectores
tokenizer = Tokenizer()
tokenizer.fit_on_texts(df['op_stemmer'])
X_seq = tokenizer.texts_to_sequences(df['op_stemmer'])

# Ajusta la longitud de las secuencias a un tamaño fijo
max_sequence_length = 100
X_pad = pad_sequences(X_seq, maxlen=max_sequence_length)

# Codifica las etiquetas en formato one-hot
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(df['target'])
y_onehot = to_categorical(y_encoded)

"""####División dataset"""

X_train_pad, X_test_pad, y_train_onehot, y_test_onehot = train_test_split(X_pad, y_onehot, test_size=0.2)

"""####Entrenamiento"""

# Define la arquitectura de la red neuronal convolucional
model = Sequential()
model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=50, input_length=max_sequence_length))
model.add(Conv1D(filters=64, kernel_size=3, activation='relu'))
model.add(GlobalMaxPooling1D())
model.add(Dense(64, activation='relu'))
model.add(Dense(2, activation='softmax'))  # 2 unidades para clasificación binaria

# Compila el modelo
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy']) ## se agrega Precision() y Recall()?

# Entrena el modelo
model.fit(X_train_pad, y_train_onehot, epochs=10, batch_size=32, validation_split=0.2)
print()
print("CNN")
# Evalúa el modelo en el conjunto de prueba
accuracy = model.evaluate(X_test_pad, y_test_onehot)[1]
print(f'Accuracy on test set: {accuracy}')
print("Final entrenamiento CNN")
print()

"""####Matriz de confusión"""

# Visualizar la matriz de confusión
classes = ['negativo', 'positivo']
df_cm = pd.DataFrame(cm, index=classes, columns=classes[::-1])
plt.figure(figsize=(6, 4))
sn.heatmap(df_cm, annot=True, fmt='g', cmap='Blues')
plt.xlabel("Predicción")
plt.ylabel("Objetivo")
plt.title("Matriz de Confusión")
plt.show()

"""####Palabras positivas"""

# Crear WordCloud para palabras positivas y negativas
positive_words_test = ' '.join(X_test[y_test == 1])
negative_words_test = ' '.join(X_test[y_test == 0])

# Plotear WordCloud para palabras positivas en el conjunto de prueba
plt.figure(figsize=(10, 5))
wordcloud_positive_test = WordCloud(width=800, height=400, background_color='white').generate(positive_words_test)
plt.imshow(wordcloud_positive_test, interpolation='bilinear')
plt.title('WordCloud - Palabras Positivas (Prueba)')
plt.axis('off')
plt.show()

"""####Palabras negativas"""

# Plotear WordCloud para palabras negativas en el conjunto de prueba
plt.figure(figsize=(10, 5))
wordcloud_negative_test = WordCloud(width=800, height=400, background_color='white').generate(negative_words_test)
plt.imshow(wordcloud_negative_test, interpolation='bilinear')
plt.title('WordCloud - Palabras Negativas (Prueba)')
plt.axis('off')
plt.show()

"""###Support Vector Machine (SVM)

####Carga dataframe
"""

# Cargar datos
df = pd.read_excel('oppenheimer.xlsx')
df = df[['Calificación', 'Opinión']].copy()
df['Calificación'].hist()

# Mapeo de etiquetas
target_map = {'positivo': 1, 'negativo': 0}
df['target'] = df['Calificación'].map(target_map)

"""####División dataset"""

# Dividir datos en conjuntos de entrenamiento y prueba
df_train, df_test = train_test_split(df, test_size=0.2)

"""#### Inicializar Stemming, Tokenize y StopWords"""

# Inicializa el stemmer y la lista de stopwords en español
stemmer = SnowballStemmer('spanish')
stop_words = set(stopwords.words('spanish'))

# Función para tokenizar, aplicar stemming y eliminar stopwords
def tokenize_and_stem(text):
    tokens = word_tokenize(text.lower())
    stems = [stemmer.stem(token) for token in tokens if token.isalpha() and token not in stop_words]
    return ' '.join(stems)

# Aplica la función a la columna 'Opinión' y crea una nueva columna 'op_stemmer'
df_train['op_stemmer'] = df_train['Opinión'].apply(tokenize_and_stem)
df_test['op_stemmer'] = df_test['Opinión'].apply(tokenize_and_stem)

"""####Aplicar Vectorización"""

# Vectorizar texto utilizando TfidfVectorizer
vectorizer = TfidfVectorizer(max_features=100)
X_train = vectorizer.fit_transform(df_train['op_stemmer'])
X_test = vectorizer.transform(df_test['op_stemmer'])

Y_train = df_train['target']
Y_test = df_test['target']

"""####Entrenamiento"""

# Inicializar y entrenar un Support Vector Machine (SVM)
svm_model = SVC(kernel='linear', C=1.0)
svm_model.fit(X_train, Y_train)

# Hacer predicciones en el conjunto de prueba
y_pred = svm_model.predict(X_test)
print()
print("SVM")
# Calcular y mostrar el accuracy
accuracy = svm_model.score(X_test, Y_test)
print(f'Accuracy on test set: {accuracy}')
print("Final entrenamiento SVM")
print()

"""####Matriz de confusión"""

# Calcular y mostrar la matriz de confusión y el informe de clasificación
cm = confusion_matrix(Y_test, y_pred)

# Visualizar la matriz de confusión
classes = ['positivo', 'negativo']
df_cm = pd.DataFrame(cm, index=classes, columns=classes[::-1])
plt.figure(figsize=(6, 4))
sn.heatmap(df_cm, annot=True, fmt='g', cmap='Blues')
plt.xlabel("Predicción")
plt.ylabel("Objetivo")
plt.title("Matriz de Confusión")
plt.show()

"""####Palabras positivas"""

# Crear WordCloud para palabras positivas y negativas
positive_words = ' '.join(df_train[df_train['target'] == 1]['op_stemmer'])
negative_words = ' '.join(df_train[df_train['target'] == 0]['op_stemmer'])

wordcloud_positive = WordCloud(width=800, height=400, background_color='white').generate(positive_words)
wordcloud_negative = WordCloud(width=800, height=400, background_color='white').generate(negative_words)

# Plotear WordCloud para palabras positivas
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_positive, interpolation='bilinear')
plt.title('WordCloud - Palabras Positivas')
plt.axis('off')
plt.show()

"""####Palabras negativas"""

# Plotear WordCloud para palabras negativas
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_negative, interpolation='bilinear')
plt.title('WordCloud - Palabras Negativas')
plt.axis('off')
plt.show()

"""#Proceso de entrenamiento con Tokenizer y Stemming

### LogisticRegression

####Carga dataframe
"""

# Carga el DataFrame desde el archivo Excel
df = pd.read_excel('oppenheimer.xlsx')

target_map = {'positivo': 1, 'negativo': 0}
df['target'] = df['Calificación'].map(target_map)

"""####Inicializar Stemming y Tokenize"""

# Inicializa el stemmer y la lista de stopwords en español
stemmer = SnowballStemmer('spanish')
stop_words = set(stopwords.words('spanish'))

# Función para tokenizar, aplicar stemming y eliminar stopwords
def tokenize_and_stem(text):
    tokens = word_tokenize(text.lower())
    stems = [stemmer.stem(token) for token in tokens if token.isalpha() and token not in stop_words]
    return ' '.join(stems)

# Aplica la función a la columna 'Opinión' y crea una nueva columna 'op_stemmer'
df['op_stemmer'] = df['Opinión'].apply(tokenize_and_stem)

"""####División dataset"""

X_train, X_test, y_train, y_test = train_test_split(df['op_stemmer'], df['target'], test_size=0.2)

"""####Aplicar Vectorización"""

# Inicializa el vectorizador TF-IDF
vectorizer = TfidfVectorizer(max_features=100)

# Transforma los datos de entrenamiento y prueba utilizando el vectorizador
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

"""####Entrenamiento"""

# Inicializa y entrena el modelo de regresión logística
model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

# Evalúa el rendimiento del modelo en los conjuntos de entrenamiento y prueba
train_acc = model.score(X_train_tfidf, y_train)
test_acc = model.score(X_test_tfidf, y_test)
print()
print("LOGISTIC REGRESSION")
# Imprime los resultados
print("Train acc:", train_acc)
print("Test acc:", test_acc)
print("Final entrenamiento LOGISTIC REGRESSION")
print()

"""####Matriz de confusión"""

def plot_cm(cm):
    classes = ['positivo', 'negativo']
    df_cm = pd.DataFrame(cm, index=classes, columns=classes[::-1])
    ax = sn.heatmap(df_cm, annot=True, fmt='g')
    ax.set_xlabel("Predicción")
    ax.set_ylabel("Objetivo")
    plt.show()
    cm = confusion_matrix(y_train, model.predict(X_train_tfidf), normalize='true')
plot_cm(cm)

"""####Palabras positivas"""

# Crear WordCloud para palabras positivas y negativas
positive_words = ' '.join(X_train[y_train == 1])
negative_words = ' '.join(X_train[y_train == 0])

# Plotear WordCloud para palabras positivas
plt.figure(figsize=(10, 5))
wordcloud_positive = WordCloud(width=800, height=400, background_color='white').generate(positive_words)
plt.imshow(wordcloud_positive, interpolation='bilinear')
plt.title('WordCloud - Palabras Positivas')
plt.axis('off')
plt.show()

"""####Palabras negativas"""

# Plotear WordCloud para palabras negativas
plt.figure(figsize=(10, 5))
wordcloud_negative = WordCloud(width=800, height=400, background_color='white').generate(negative_words)
plt.imshow(wordcloud_negative, interpolation='bilinear')
plt.title('WordCloud - Palabras Negativas')
plt.axis('off')
plt.show()



"""### Convolutional Neural Networks (CNN)

####Carga dataframe
"""

# Carga el DataFrame desde el archivo Excel
df = pd.read_excel('oppenheimer.xlsx')

target_map = {'positivo': 1, 'negativo': 0}
df['target'] = df['Calificación'].map(target_map)

"""####Inicializar Stemming, Tokenize y vectorización"""

# Inicializa el stemmer y la lista de stopwords en español
stemmer = SnowballStemmer('spanish')
stop_words = set(stopwords.words('spanish'))

# Función para tokenizar, aplicar stemming y eliminar stopwords
def tokenize_and_stem(text):
    tokens = word_tokenize(text.lower())
    stems = [stemmer.stem(token) for token in tokens if token.isalpha() and token not in stop_words]
    return ' '.join(stems)

# Aplica la función a la columna 'Opinión' y crea una nueva columna 'op_stemmer'
df['op_stemmer'] = df['Opinión'].apply(tokenize_and_stem)

# Tokeniza las opiniones y convierte las secuencias en vectores
tokenizer = Tokenizer()
tokenizer.fit_on_texts(df['op_stemmer'])
X_seq = tokenizer.texts_to_sequences(df['op_stemmer'])

# Ajusta la longitud de las secuencias a un tamaño fijo
max_sequence_length = 100
X_pad = pad_sequences(X_seq, maxlen=max_sequence_length)

# Codifica las etiquetas en formato one-hot
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(df['target'])
y_onehot = to_categorical(y_encoded)

"""####División dataset"""

X_train_pad, X_test_pad, y_train_onehot, y_test_onehot = train_test_split(X_pad, y_onehot, test_size=0.2)

"""####Entrenamiento"""

# Define la arquitectura de la red neuronal convolucional
model = Sequential()
model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=50, input_length=max_sequence_length))
model.add(Conv1D(filters=64, kernel_size=3, activation='relu'))
model.add(GlobalMaxPooling1D())
model.add(Dense(64, activation='relu'))
model.add(Dense(2, activation='softmax'))  # 2 unidades para clasificación binaria

# Compila el modelo
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entrena el modelo
model.fit(X_train_pad, y_train_onehot, epochs=10, batch_size=32, validation_split=0.2)
print()
print("CNN")
# Evalúa el modelo en el conjunto de prueba
accuracy = model.evaluate(X_test_pad, y_test_onehot)[1]
print(f'Accuracy on test set: {accuracy}')
print("Fin entrenamiento CNN")
print()

"""####Matriz de confusión"""

# Visualizar la matriz de confusión
classes = ['negativo', 'positivo']
df_cm = pd.DataFrame(cm, index=classes, columns=classes[::-1])
plt.figure(figsize=(6, 4))
sn.heatmap(df_cm, annot=True, fmt='g', cmap='Blues')
plt.xlabel("Predicción")
plt.ylabel("Objetivo")
plt.title("Matriz de Confusión")
plt.show()

"""####Palabras positivas"""

# Crear WordCloud para palabras positivas y negativas
positive_words = ' '.join(df[df['target'] == 1]['op_stemmer'])
negative_words = ' '.join(df[df['target'] == 0]['op_stemmer'])

# Plotear WordCloud para palabras positivas
plt.figure(figsize=(10, 5))
wordcloud_positive = WordCloud(width=800, height=400, background_color='white').generate(positive_words)
plt.imshow(wordcloud_positive, interpolation='bilinear')
plt.title('WordCloud - Palabras Positivas')
plt.axis('off')
plt.show()

"""####Palabras negativas"""

# Plotear WordCloud para palabras negativas
plt.figure(figsize=(10, 5))
wordcloud_negative = WordCloud(width=800, height=400, background_color='white').generate(negative_words)
plt.imshow(wordcloud_negative, interpolation='bilinear')
plt.title('WordCloud - Palabras Negativas')
plt.axis('off')
plt.show()

"""###Support Vector Machine (SVM)

####Carga dataframe
"""

# Cargar datos
df = pd.read_excel('oppenheimer.xlsx')
df = df[['Calificación', 'Opinión']].copy()
df['Calificación'].hist()

# Mapeo de etiquetas
target_map = {'positivo': 1, 'negativo': 0}
df['target'] = df['Calificación'].map(target_map)

"""####División dataset"""

# Dividir datos en conjuntos de entrenamiento y prueba
df_train, df_test = train_test_split(df, test_size=0.2)

"""####Inicializar Stemming y Tokenize"""

# Inicializa el stemmer y la lista de stopwords en español
stemmer = SnowballStemmer('spanish')
stop_words = set(stopwords.words('spanish'))

# Función para tokenizar, aplicar stemming y eliminar stopwords
def tokenize_and_stem(text):
    tokens = word_tokenize(text.lower())
    stems = [stemmer.stem(token) for token in tokens if token.isalpha() and token not in stop_words]
    return ' '.join(stems)

# Aplica la función a la columna 'Opinión' y crea una nueva columna 'op_stemmer'
df_train['op_stemmer'] = df_train['Opinión'].apply(tokenize_and_stem)
df_test['op_stemmer'] = df_test['Opinión'].apply(tokenize_and_stem)

"""####Aplicar Vectorización"""

# Vectorizar texto utilizando TfidfVectorizer
vectorizer = TfidfVectorizer(max_features=100)
X_train = vectorizer.fit_transform(df_train['op_stemmer'])
X_test = vectorizer.transform(df_test['op_stemmer'])

Y_train = df_train['target']
Y_test = df_test['target']

"""####Entrenamiento"""

# Inicializar y entrenar un Support Vector Machine (SVM)
svm_model = SVC(kernel='linear', C=1.0)
svm_model.fit(X_train, Y_train)

# Hacer predicciones en el conjunto de prueba
y_pred = svm_model.predict(X_test)
print()
print("SVM")
# Calcular y mostrar el accuracy en el conjunto de entrenamiento
train_accuracy = svm_model.score(X_train, Y_train)
print(f'Accuracy on training set: {train_accuracy}')
print("Fin entrenamiento SVM")
print()
# Hacer predicciones en el conjunto de prueba
y_pred = svm_model.predict(X_test)

"""####Matriz de confusión"""

# Visualizar la matriz de confusión
classes = ['positivo', 'negativo']
df_cm = pd.DataFrame(cm, index=classes, columns=classes[::-1])
plt.figure(figsize=(6, 4))
sn.heatmap(df_cm, annot=True, fmt='g', cmap='Blues')
plt.xlabel("Predicción")
plt.ylabel("Objetivo")
plt.title("Matriz de Confusión")
plt.show()

"""####Palabras positivas"""

# Crear WordCloud para palabras positivas y negativas
positive_words = ' '.join(df_test[df_test['target'] == 1]['op_stemmer'])
negative_words = ' '.join(df_test[df_test['target'] == 0]['op_stemmer'])

wordcloud_positive = WordCloud(width=800, height=400, background_color='white').generate(positive_words)
wordcloud_negative = WordCloud(width=800, height=400, background_color='white').generate(negative_words)

# Plotear WordCloud para palabras positivas
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_positive, interpolation='bilinear')
plt.title('WordCloud - Palabras Positivas')
plt.axis('off')
plt.show()

"""####Palabras negativas"""

# Plotear WordCloud para palabras negativas
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_negative, interpolation='bilinear')
plt.title('WordCloud - Palabras Negativas')
plt.axis('off')
plt.show()
