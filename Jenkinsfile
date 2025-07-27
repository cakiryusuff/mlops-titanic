pipeline {
    agent any

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
                        gsutil cp artifacts/titanic_model.pkl gs://deneme_bucket12/
                    '''
                }
            }
        }
    }
}
