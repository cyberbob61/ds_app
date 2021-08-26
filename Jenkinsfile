pipeline {
    agent none
    stages {
        //sonar
        stage('Sonar') {
            agent { kubernetes { yamlFile 'sonaragent.yaml' } }
            steps {
                container('sonar') {
                    git url:'https://github.com/cyberbob61/ds_app.git', branch: 'main'
                    sh "sonar-scanner -Dsonar.projectKey=sonar -Dsonar.sources=. -Dsonar.host.url=http://34.116.158.178:9000 -Dsonar.login=7b369d4bd2cbf7f40193c4e73eb0a542cc89c1d7"
                }
            }
        }
        //Linter
        stage('PyLint') {
            agent { kubernetes { yamlFile 'pylint.yaml' } }
            steps {
                container('pylint') {
                    git url:'https://github.com/cyberbob61/ds_app.git', branch: 'main'
                    sh 'pip3 install -U Flask'
                    sh 'pip3 install mysql-connector-python'
                    sh 'pylint *.py --disable=W1202 --output-format=parseable --reports=no > pylint.log || echo "pylint exited with $?"'
                    recordIssues(
                        enabledForFailure: true,
                        aggregatingResults: true,
                        tool: pyLint(pattern: 'pylint.log', reportEncoding: 'UTF-8'),
                        qualityGates: [[threshold: 1, type: 'TOTAL_HIGH']]
                    )


                }
            }
                }
            }

        }
