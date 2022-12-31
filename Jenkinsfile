pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'jenkins-demo', url: 'https://github.com/mitulds/data-science-show-demo.git']])
                sh 'echo "Checking git repo....."'
            }
        }
        stage('Install dependencies') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'jenkins-demo', url: 'https://github.com/mitulds/data-science-show-demo.git']]) 
                sh('''
                    echo "Installing dependencies....."
                
                    cd demo-session1
                    make install
                ''')
            }
        }
    }
}