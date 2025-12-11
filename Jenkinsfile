pipeline {
  agent any
  environment {
    IMAGE = "restaurants-site:ci"
    PORT = "8083"
  }
  stages {
    stage('Checkout') {
      steps {
        checkout([$class: 'GitSCM',
          branches: [[name: '*/develop']],
          userRemoteConfigs: [[url: 'https://github.com/Ghada-htira/projet-integration.git', credentialsId: 'github-token']]
        ])
      }
    }

    stage('Generate HTML') {
      steps {
        echo "Running generate_html.py"
        sh 'python3 scripts/generate_html.py || python scripts/generate_html.py'
        sh 'ls -la nginx-site/site || true'
      }
    }

    stage('Build Docker image') {
      steps {
        echo "Building Docker image ${IMAGE}"
        sh "docker build -t ${IMAGE} nginx-site/"
      }
    }

    stage('Deploy') {
      steps {
        echo "Stopping and removing old container (if any)"
        sh "docker rm -f auto-web || true"
        echo "Starting new container on port ${PORT}"
        sh "docker run -d --name auto-web --network bis_network -p ${PORT}:80 ${IMAGE}"
        sh "docker ps --filter name=auto-web --format 'table {{.Names}}\\t{{.Image}}\\t{{.Ports}}'"
      }
    }
  }
  post {
    success {
      echo "Deployment succeeded"
    }
    failure {
      echo "Deployment failed — check logs"
    }
  }
}
