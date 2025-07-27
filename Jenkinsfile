pipeline {
    agent any
    environment {
        GCP_PROJECT = 'video-deneme-v2'
    }

    stages {
        stage('Clone Repo') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/cakiryusuff/mlops-titanic.git']])
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Train Model') {
            steps {
                sh '''
                    . venv/bin/activate
                    python training/train.py
                '''
            }
        }

        stage('Upload to GCS') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh '''
                        . venv/bin/activate
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gsutil cp artifacts/titanic_model.pkl gs://deneme_bucket12/
                    '''
                }
            }
        }

        stage('Run Flask API in Docker') {
            steps {
                sh '''
                    docker rm -f titanic_api_container || true
                    docker build -t titanic-api .
                    docker run -d -p 5000:5000 --name titanic_api_container titanic-api
                '''
            }
        }
    }
}
