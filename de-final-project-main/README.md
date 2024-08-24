# Tugas Final Project
 Project ini berisi  penelitian untuk mengambil data  tweet  review  series ‘Alice in Borderland Season 2’ secara streaming kemudian dilakukan EDA dan sentiment analisis untuk mengetahui bagaimana penilaian terhadap series tersebut, dan dilakukan modelling dengan klasifikasi.  Data  tersebut  akan  diproses menggunakan textblob,  kemudian dilanjutkan dengan mengklasifikasikan  tweet ke dalam tiga kelas, yaitu positif, negatif, dan netral. Klasifikasi ini  menggunakan  algoritma  Support  Vector Machine.  Klasifikasi  dapat  memberikan kemudahan  bagi  pengguna  untuk  melihat  opini positif,  negatif,  dan  netral.  Tingkat  akurasi  dari algoritma akan memberikan pengaruh pada  hasil klasifikasi


## Service port local
Daftar port yang digunakan pada project ini. Apabila ingin menjalankan project, pastikan port tidak digunakan
- ``5432`` postgres
- ``2181`` zookeeper
- ``9092`` broker kafka
- ``8080`` webserver

## Cara Menjalankan Project
1. Pastikan local komputer sudah terinstalasi docker dan docker-compose
2. Pastikan tidak ada port yang bertabrakkan
3. Copy file .env.example
    ```cp .env.example .env```
4. Ubah value BEARER_TOKEN   yang didapatkan dari dashboard portal twitter developer (https://developer.twitter.com/en/portal/dashboard) pada file etl.py di line [kode 47](https://github.com/davahamka/de-final-project/blob/main/dags/etl.py#L100)
4. Buka file docker-compose.yaml dan ubah image pada line [kode 47](https://github.com/davahamka/de-final-project/blob/main/docker-compose.yaml#L47) value AIRFLOW_IMAGE_NAME dari ``-final_extending_airflow:latest`` menjadi `-apache/airflow:2.5.0  `
5. Run init default docker compose (https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
6. Seteleh inisiasi selesai, jalankan perintah ```docker build . --tag final_extending_airflow:latest``` pada terminal. Hal ini dilakukan untuk membuat image baru bernama `final_extending_airflow` yang berisi airflow sekaligus library yang dibutuhkan pada project ini (mengacu pada file [ini](https://github.com/davahamka/de-final-project/blob/main/requirements.txt))
8. Ubah kembali pada file docker-compose.yaml pada line[ kode 47](https://github.com/davahamka/de-final-project/blob/main/docker-compose.yaml#L47) value AIRFLOW_IMAGE_NAME dari ```-apache/airflow:2.5.0``` menjadi ``-final_extending_airflow:latest`` 
9. Lalu jalankan lagi dengan perintah ``docker-compose up`` pada terminal


## Tools yang digunakan
- Tweepy
- Airflow
- Kafka
- TextBlob
- Scikit-Learn
- NLTK
- SQLAlchemy
- pgAdmin

## Informasi folder & file
```.
├── dags/
│   ├── __pycache__
│   ├── scripts/ (Untuk BashOperator)
│   │   └── print_date.sh
│   ├── etl.py
│   ├── final_project_dag.py
│   └── modelling.py
├── db
├── logs
├── plugins
├── screenshoot
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yaml
├── Dockerfile
└── requirements.txt
```

## Screenshoot
Screenshoot dapat dilihat [disini](https://github.com/davahamka/de-final-project/tree/main/screenshoot)