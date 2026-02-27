pipeline {
    agent any

    environment {
        IMAGE_NAME = "varuna10/varunmohanbcs34-wine-quality:latest"
        CONTAINER_NAME = "wine_api_test"
    }

    stages {

        stage('Pull Image') {
            steps {
                sh 'docker pull $IMAGE_NAME'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker rm -f $CONTAINER_NAME || true
                docker run -d -p 8000:8000 --name $CONTAINER_NAME $IMAGE_NAME
                '''
            }
        }

        stage('Wait for API') {
            steps {
                sh '''
                echo "Waiting for API..."
                for i in {1..20}
                do
                    sleep 3
                    curl -s http://localhost:8000/health && break
                done
                '''
            }
        }

        stage('Valid Request Test') {
            steps {
                sh '''
                echo "Sending VALID request"
                RESPONSE=$(curl -s -X POST http://localhost:8000/predict \
                -H "Content-Type: application/json" \
                -d @tests/valid_input.json)

                echo $RESPONSE

                echo $RESPONSE | grep wine_quality
                '''
            }
        }

        stage('Invalid Request Test') {
            steps {
                sh '''
                echo "Sending INVALID request"
                curl -s -X POST http://localhost:8000/predict \
                -H "Content-Type: application/json" \
                -d @tests/invalid_input.json
                '''
            }
        }

        stage('Stop Container') {
            steps {
                sh 'docker rm -f $CONTAINER_NAME'
            }
        }
    }
}