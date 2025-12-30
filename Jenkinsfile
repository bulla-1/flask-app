pipeline {
    agent any
    
    environment {
        APP_NAME = 'flask-app'
        DOCKER_IMAGE = "flask-app:${BUILD_NUMBER}"
        CONTAINER_NAME = 'flask-app-container'
        APP_PORT = '5000'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 Pulling code from GitHub...'
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo '🐍 Setting up Python virtual environment...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Lint') {
            steps {
                echo '🔍 Running code linting with flake8...'
                sh '''
                    . venv/bin/activate
                    flake8 app.py --max-line-length=120 --ignore=E501,W503 || true
                '''
            }
        }
        
        stage('Test') {
            steps {
                echo '🧪 Running unit tests...'
                sh '''
                    . venv/bin/activate
                    pytest tests/ -v --tb=short
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh "docker build -t ${DOCKER_IMAGE} ."
                sh "docker tag ${DOCKER_IMAGE} ${APP_NAME}:latest"
            }
        }
        
        stage('Deploy') {
            steps {
                echo '🚀 Deploying application...'
                sh '''
                    # Stop and remove existing container if running
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    
                    # Run new container
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p ${APP_PORT}:5000 \
                        --restart unless-stopped \
                        ${DOCKER_IMAGE}
                    
                    # Wait for container to be healthy
                    sleep 5
                    
                    # Verify deployment
                    docker ps | grep ${CONTAINER_NAME}
                '''
            }
        }
        
        stage('Health Check') {
            steps {
                echo '❤️ Verifying deployment health...'
                sh '''
                    # Wait for app to start
                    sleep 3
                    
                    # Check if the app responds
                    curl -f http://localhost:${APP_PORT}/health || exit 1
                    
                    echo "✅ Application is healthy and running!"
                '''
            }
        }
    }
    
    post {
        success {
            echo '''
            ✅ ================================
            ✅ Pipeline completed successfully!
            ✅ Application is now running at:
            ✅ http://localhost:5000
            ✅ ================================
            '''
        }
        failure {
            echo '''
            ❌ ================================
            ❌ Pipeline failed!
            ❌ Check the logs for details.
            ❌ ================================
            '''
            // Cleanup on failure
            sh '''
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true
            '''
        }
        always {
            echo '🧹 Cleaning up workspace...'
            cleanWs()
        }
    }
}
