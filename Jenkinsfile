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
                sh('''
                    echo "Installing dependencies....."
                
                    cd demo-session1
                    pip install --upgrade pip
                    pip install -r requirements.txt
                ''')
            }
        }
        stage('Build'){
            steps {
                sh('''
                    echo "Building....."
                
                python src/tools/upload_data_V2.py -db True
                ''')
            }
        }
        }
    }
}