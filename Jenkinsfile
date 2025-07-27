pipeline {
    agent any

    environment {
        GCP_PROJECT = 'video-deneme-v2'
    }

    stages {
        stage('Clone Repo') {
            steps {
                echo 'Cloning repository...'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/cakiryusuff/mlops-titanic.git']])
            }
        }
        stage('Install Dependencies') {
            steps {
                echo 'installing dependencies...'
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
                echo 'Training model...'
                sh '''
                    . venv/bin/activate
                    python training/train.py
                '''
            }
        }
        stage('Upload to GCS') {
            steps {
                echo 'Uploading to GCS...'
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh '''
                        . venv/bin/activate
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gsutil cp artifacts/titanic_model.pkl gs://video-jenkins-bucket/
                    '''
                }
            }
        }
        stage('Run Flask API in Docker') {
            steps {
                echo 'Running Flask API in Docker...'
                sh '''
                    docker rm -f titanic_api_container || true
                    docker build -t titanic-api .
                    docker run -d -p 5000:5000 --name titanic_api_container titanic-api
                '''
            }
        }
    }
}
