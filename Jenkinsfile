pipeline {
    agent none
  stages {
    stage('Sonarcheck') {
      agent {
        kubernetes { yamlFile 'agent.yaml'}
             }
      steps {
        container('sonar') {
          git url:'https://github.com/cyberbob61/ds_app.git', branch: 'main'
          sh "sonar-scanner -Dsonar.projectKey=sonar -Dsonar.sources=. -Dsonar.host.url=http://34.116.158.178:9000 -Dsonar.login=7b369d4bd2cbf7f40193c4e73eb0a542cc89c1d7"
                            }
            }
                        }
        }

        }       
