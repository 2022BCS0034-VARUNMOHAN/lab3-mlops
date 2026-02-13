pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "varuna10/varunmohanbcs34-wine-quality"
    }

    stages {

        stage('Clone Repository') {
            steps {
                echo "Cloning repository..."
                checkout scm
            }
        }

        stage('Create Python Environment & Install Requirements') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r api/requirements.txt
                pip install scikit-learn pandas joblib
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                . venv/bin/activate
                python scripts/train.py
                '''
            }
        }

        stage('Print Metrics + Student Info') {
            steps {
                sh '''
                echo "===== MODEL METRICS ====="
                cat Metrics/metrics.json

                echo ""
                echo "Name: VARUN MOHAN"
                echo "Roll No: 2022BCS0034"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $DOCKER_IMAGE:latest .
                '''
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh '''
                    echo $PASSWORD | docker login -u $USERNAME --password-stdin
                    docker push $DOCKER_IMAGE:latest
                    '''
                }
            }
        }
    }
}
