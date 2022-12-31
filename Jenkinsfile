pipeline {
    agent any
    stages {
        stage('hello') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'jenkins-demo', url: 'https://github.com/mitulds/data-science-show-demo.git']])
                sh 'echo "hello world"'
            }
        }
    }
}