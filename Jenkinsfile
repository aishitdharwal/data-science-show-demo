pipeline {
    agent none
    stages {
        stage('Python'){
            agent {
                docker {
                    image 'python:2-alpine'
                }
            }
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'jenkins-demo', url: 'https://github.com/mitulds/data-science-show-demo.git']]) 
                sh('''
                    echo "Installing dependencies....."
                
                    cd demo-session1
                    pip install --upgrade pip
                    pip install -r requirements.txt
                ''')
            }
        }

        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'jenkins-demo', url: 'https://github.com/mitulds/data-science-show-demo.git']])
                sh 'echo "Checking git repo....."'
            }
        }

        stage('Build') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'jenkins-demo', url: 'https://github.com/mitulds/data-science-show-demo.git']]) 
                sh('''
                    echo "build....."

                    cd demo-session1
                    python3 src/tools/upload_data_V2.py -db True
                ''')
            }
        }

    }
}