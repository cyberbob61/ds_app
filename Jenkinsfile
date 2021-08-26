pipeline {
    agent any
    stages {
        stage('Example Username/Password') {
            steps {
                sh 'echo "Service user is test"'
                sh 'curl http://ya.ru'
            }
        }
        stage('Example SSH Username with private key') {
            steps {
                sh 'echo "suppa"'
                sh 'curl http://google.com'
            }
        }
    }
}
