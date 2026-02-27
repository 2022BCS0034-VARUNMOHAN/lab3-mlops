pipeline {
    agent any

    environment {
        IMAGE = "varuna10/varunmohanbcs34-wine-quality:latest"
        CONTAINER = "wine-test-container"
        PORT = "8000"
    }

    stages {

        stage('Pull Docker Image') {
            steps {
                sh 'docker pull $IMAGE'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker rm -f $CONTAINER || true
                docker run -d -p 8000:8000 --name $CONTAINER $IMAGE
                '''
            }
        }

        stage('Wait for API Readiness') {
            steps {
                sh '''
                echo "Waiting for API..."
                for i in {1..30}
                do
                    if curl -s http://localhost:8000/health > /dev/null
                    then
                        echo "API is ready!"
                        exit 0
                    fi
                    sleep 2
                done
                echo "API failed to start"
                exit 1
                '''
            }
        }

        stage('Send Valid Request') {
            steps {
                sh '''
                echo "Sending valid input..."
                RESPONSE=$(curl -s -X POST http://localhost:8000/predict \
                -H "Content-Type: application/json" \
                -d @tests/valid_input.json)

                echo "API Response:"
                echo $RESPONSE

                echo $RESPONSE | grep wine_quality
                '''
            }
        }

        stage('Send Invalid Request') {
            steps {
                sh '''
                echo "Sending invalid input..."
                STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
                -X POST http://localhost:8000/predict \
                -H "Content-Type: application/json" \
                -d @tests/invalid_input.json)

                echo "HTTP Status: $STATUS"

                if [ "$STATUS" -eq 200 ]; then
                    echo "ERROR: Invalid input accepted!"
                    exit 1
                fi
                '''
            }
        }

        stage('Stop Container') {
            steps {
                sh 'docker rm -f $CONTAINER || true'
            }
        }
    }
}