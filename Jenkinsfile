pipeline {
  agent {
    kubernetes {
      yamlFile 'agent.yaml'
    }
  }
  stages {
    stage('Docker Build') {
      steps {
	    container('sonar') {
	      git url:'https://github.com/cyberbob61/ds_app.git', branch: 'main'
          sh "sonar-scanner   -Dsonar.projectKey=sonarcicd   -Dsonar.sources=."
	    }
      }
    }
  }
}
