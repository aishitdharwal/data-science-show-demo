pipeline {
    agent any
    stages {
        stage('Checkout Github code') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'jenkins-demo', url: 'https://github.com/mitulds/data-science-show-demo.git']])
            }
        }

        stage('Install dependencies'){
            steps {
                git branch: 'main', credentialsId: '4e81c4a3-a713-4e86-b78c-5493dccdc580', url: 'https://github.com/mitulds/data-science-show-demo.git'
                sh('''
                    echo "Installing dependencies....."
                    cd demo-session1
                    pip3 install --upgrade pip
                    pip3 install -r requirements.txt
                ''')
            }
        }

        stage('Build 01') {
            steps {
                sh('''
                    echo "build 01....."
                    cd demo-session1
                    python3 src/tools/upload_data_V2.py -db True -db_name 'groceries'
                    python3 src/tools/upload_data_V2.py -db_name 'groceries' -t 'csv-to-database'
                ''')
            }
        }

        stage('Build 02') {
            steps {
                sh('''
                    echo "build 02....."
                    cd demo-session1
                    python3 src/tools/upload_data_V2.py -db True -db_name 'groceries_cleaned'
                    python3 src/tools/upload_data_V2.py -db_name 'groceries_cleaned' -t 'cleaned_csv-to-database'
                ''')
            }
        }

    }
}