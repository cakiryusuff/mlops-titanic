pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/cakiryusuff/mlops-titanic.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Train Model') {
            steps {
                sh 'source venv/bin/activate && python train.py'
            }
        }
        stage('Upload to GCS') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh 'source venv/bin/activate && gsutil cp model.pkl gs://deneme_bucket12/'
                }
            }
        }
    }
}
