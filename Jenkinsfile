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
        //test
        stage('Linter') {
            agent { kubernetes { yamlFile 'pylint.yaml' } }
            steps {
                container('pylint') {
                    git url:'https://github.com/cyberbob61/ds_app.git', branch: 'main'
                    //sh "pylint *.py --exit-zero"
                    //sh 'pylint *.py --output-format=parseable --reports=no module || echo "pylint exited with $?"'
                    sh 'pip3 install flask mysql'
                    sh 'pylint *.py --disable=W1202 --output-format=parseable --reports=no > pylint.log || echo "pylint exited with $?"'
                    //sh 'pylint *.py --output-format=parseable --reports=no module > pylint.log || echo "pylint exited with $?"'
                    //sh 'cat pylint.log'
                    //recordIssues enabledForFailure: true, aggregatingResults: true, tool: pyLint(pattern: 'pylint.log')
                    recordIssues(
                        enabledForFailure: true,
                        aggregatingResults: true,
                        tool: pyLint(pattern: 'pylint.log', reportEncoding: 'UTF-8'),
                        //unstableTotalAll: 100,
                        qualityGates: [[threshold: 1, type: 'TOTAL_ERROR']]
                    )


                }
            }
                }
            }

        }
