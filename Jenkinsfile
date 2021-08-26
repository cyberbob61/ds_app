pipeline {
    agent none
    stages {
        stage('Sonarcheck') {
            steps {
                container('sonar') {
                    agent { kubernetes { yamlFile 'agent.yaml' } }
                    git url:'https://github.com/cyberbob61/ds_app.git', branch: 'main'
                }
                sh 'echo "Service user is test"'
                sh 'curl http://ya.ru'
            }
        }
        //stage('Example SSH Username with private key') {
        //    steps {
        //        sh 'echo "suppa"'
        //        sh 'curl http://google.com'
        //    }
        //}
    }
}
