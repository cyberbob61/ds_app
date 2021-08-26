pipeline {
    agent none
    stages {
        //sonar
        stage('Sonarcheck') {
            agent { kubernetes { yamlFile 'sonaragent.yaml' } }
            steps {
                container('sonar') {
                    git url:'https://github.com/cyberbob61/ds_app.git', branch: 'main'
                    sh "sonar-scanner -Dsonar.projectKey=sonar -Dsonar.sources=. -Dsonar.host.url=http://34.116.158.178:9000 -Dsonar.login=7b369d4bd2cbf7f40193c4e73eb0a542cc89c1d7"
                }
            }
        }
        //test
        stage('Linter') {
            agent { kubernetes { yamlFile 'pylint.yaml' } }
            steps {
                container('pylint') {
                    git url:'https://github.com/cyberbob61/ds_app.git', branch: 'main'
                    //sh "pylint *.py"
                    sh 'python3 -m pylint --output-format=parseable --fail-under=<threshold value> module --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" | tee pylint.log || echo "pylint exited with $?"'
                    echo "linting Success, Generating Report"
                    recordIssues enabledForFailure: true, aggregatingResults: true, tool: pyLint(pattern: 'pylint.log')
                }
            }
        }
    }
}
