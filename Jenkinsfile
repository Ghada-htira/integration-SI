pipeline {
    agent any

    environment {
        DOCKER_HOST = "unix:///var/run/docker.sock"
        DOCKER_IMAGE = "restaurants-site"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Generate HTML') {
            steps {
                sh '''
                    echo "Running generate_html.py"
                    python3 scripts/generate_html.py
                '''
            }
        }

        stage('Build Docker image') {
            steps {
                sh '''
                    echo "Building Docker image..."
                    docker build -t restaurants-site nginx-site
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    echo "Stopping existing container..."
                    docker stop restaurants-web || true
                    docker rm restaurants-web || true

                    echo "Starting new container..."
                    docker run -d -p 8083:80 --name restaurants-web restaurants-site
                '''
            }
        }
    }

    post {
        failure {
            echo 'Deployment failed — check logs'
        }
        success {
            echo 'Deployment succeeded!'
        }
    }
}
