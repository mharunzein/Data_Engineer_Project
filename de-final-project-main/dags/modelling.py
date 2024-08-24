from sklearn.metrics import classification_report, f1_score, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve, auc, roc_auc_score
from nltk.corpus import stopwords
import pandas as pd
from textblob import TextBlob
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import nltk
from sqlalchemy import create_engine

nltk.download('stopwords')


def start_modelling():
    engine = create_engine(
        'postgresql+psycopg2://airflow:airflow@postgres:5432/airflow')
    data = pd.read_sql_table('tweets', engine)
    data.tail()

    data["sentiment"] = data['0'].apply(
        lambda tweet: TextBlob(tweet).sentiment.polarity)
    print(data)

    data["sentiment"].mask(data["sentiment"] >= 0.0, 1, inplace=True)
    data["sentiment"].mask(data["sentiment"] < 0.0, 0, inplace=True)

    print(data)

    def draw_sentiment(pos, neg):
        ig1, ax1 = plt.subplots(figsize=(4, 4))
        labels = ["Positive", "Negative"]
        sizes = [pos, neg]
        explode = (0, 0.1)
        tb_10_green = (44/255, 160/255, 44/255)
        tb_10_red = (214/255, 39/255, 40/255)
        colors = [tb_10_green, tb_10_red]
        ax1.pie(sizes, explode=explode, labels=labels,
                autopct="%1.1f%%", colors=colors, shadow=True, startangle=90)
        ax1.axis("equal")
        plt.show()

    draw_sentiment(data[data.sentiment == 1].shape[0],
                   data[data.sentiment == 0].shape[0])

    def remove_stopword(text):
        clean_text = []
        text = text.split()
        stop_words = stopwords.words('english')
        for i in text:
            if i not in stop_words:
                clean_text.append(i)
        return " ".join(clean_text)

    data["clean"] = data['0'].apply(remove_stopword)
    print(data)

    X_train, X_test, y_train, y_test = train_test_split(
        data["clean"], data["sentiment"], test_size=0.3, shuffle=True)
    tfidf_vectorizer = TfidfVectorizer(use_idf=True)
    X_train_vectors_tfidf = tfidf_vectorizer.fit_transform(X_train)
    X_test_vectors_tfidf = tfidf_vectorizer.transform(X_test)

    svm = SVC(C=1, kernel='rbf', probability=True)
    svm.fit(X_train_vectors_tfidf, y_train)

    def finalize(X, y, model):
        y_predict = model.predict(X)
        y_prob = model.predict_proba(X)[:, 1]
        fpr, tpr, thresholds = roc_curve(y, y_prob)
        roc_auc = auc(fpr, tpr)
        acc = accuracy_score(y, y_predict)
        prec = precision_score(y, y_predict)
        rec = recall_score(y, y_predict)
        f1 = f1_score(y, y_predict)
        cm = confusion_matrix(y, y_predict)
        tn, fp, fn, tp = cm.ravel()

        print('================================================\nEvaluasi Hasil Model\n================================================\n')
        print('Dengan Classification Report:\n\n',
              classification_report(y, y_predict))
        print('================================================')
        print('\nDengan Confusion Matrix:\n\n', cm)
        print('\nTrue Positif   : ', tp)
        print('True Negatif   : ', tn)
        print('False Positif  : ', fp)
        print('False Negatif  : ', fn)
        print('\n================================================')
        print('\nDengan Beberapa Metrik:')
        print('\nAUC      : ', roc_auc)
        print('Akurasi  : ', acc)
        print('Presisi  : ', prec)
        print('Recall   : ', rec)
        print('F1-score : ', f1)

    finalize(X_test_vectors_tfidf, y_test, svm)
