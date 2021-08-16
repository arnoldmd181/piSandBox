// def COMPONENTS = ['indexer', 'transformer', 'ingest-api']
// def ACCOUNTS = ['dev': "263734463344", 'prod': "725071466363"]
// def  FILES_LIST = sh (script: "ls   '${WORKSPACE}'", returnStdout: true).trim()

pipeline {
//         agent any
    agent {
        kubernetes {
          defaultContainer 'python'
          yaml '''\
            apiVersion: v1
            kind: Pod
            spec:
              containers:
              - name: python
                image: python:3.6
                command:
                - cat
                tty: true
                resources:
                  requests:
                    memory: 1Gi
            '''.stripIndent()
        }
     }
    stages {
        stage("test") {
//           withEnv(["HOME=${env.WORKSPACE}"]) {
            steps {
                echo '> Running make test ...'
//                 sh """make -sC domain_classifier test"""
//                 sh "./scripts/automation.sh"
                sh '''
                    echo "Multiline shell steps works too"
                    ls -lah
                '''
                sh "python3 ${WORKSPACE}/scripts/automation.py"
//                 sh "bash ${WORKSPACE}/build_scripts/test.sh domain_classifier"
                echo "--------Flake8 ${1}--------"
//                 sh "pip3 install flake8"
//                 sh "flake8 ${WORKSPACE}/domain_classifier"
            }
//            }
        }
        stage("autopep") {
            steps {
                script {
                    echo "autopep"
                }
            }
        }
        stage("wheel") {
            steps {
                script {
                          echo "wheel"
                }
            }
        }
        stage("deploy") {
            steps {
                script {
                          echo "wheel"
                }
            }
        }
    }
}