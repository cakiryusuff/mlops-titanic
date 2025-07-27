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

        stage('Install GCP CLI') {
            steps {
                sh '''
                    if ! command -v gcloud > /dev/null; then
                        echo ">>> Installing Google Cloud SDK"
                        sudo apt update
                        sudo apt install -y apt-transport-https ca-certificates gnupg curl

                        echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | \
                          sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

                        curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
                          sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

                        sudo apt update
                        sudo apt install -y google-cloud-sdk
                    else
                        echo ">>> gcloud already installed"
                    fi
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
