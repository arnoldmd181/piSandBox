#!groovy
// def ENVIRONMENTS() {
//   return GIT_BRANCH == 'master' ? ['dev'] : ['dev']
//   return GIT_BRANCH == 'master' ? ['dev'] : ['dev']
// }

def MODEL_UPDATE = ['indexer', 'transformer', 'ingest-api']
// def MODEL_UPDATE = "phishing_common,domain_classifier"

pipeline {
    environment {
        MODEL_UPDATE = "phishing_common,domain_classifier"
    }
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
        stage('Setup') { // Install any dependencies you need to perform testing
            steps {
                script {
                    sh """
                    pip3 install GitPython
                    """
                    env.GH_URL = GIT_URL.substring(0, GIT_URL.size() - 4)
                     env.COMMIT_URL = GIT_BRANCH == "dev" ? "${GH_URL}/commit/${GIT_COMMIT}" : "${GH_URL}/pull/${GIT_BRANCH.substring(3, GIT_BRANCH.size())}/commits/${GIT_COMMIT}"
                    sh 'printenv'
                }
            }

        }
	    stage('Checkout') {
	      	steps {
		        script {
		           // The below will clone your repo and will be checked out to master branch by default.
		           sh "git status"
		           print("cloning repo")
// 		           git credentialsId: 'TestGitToken1', url: 'https://github.com/arnoldmd181/piSandBox.git'
		           // Do a ls -lart to view all the files are cloned. It will be clonned. This is just for you to be sure about it.
		           print("ls")
// 		           sh """
// 		                git fetch --all
// 		            """
		            //                 git config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'
		            sh "git status"

		           // List all branches in your repo.
		           sh "git branch -a"

		           // Checkout to a specific branch in your repo.
// 		           sh "git checkout remotes/origin/dc-test"
		            sh "git status"
		        }
	      	}
	    }
	        stage("automation") {
	        steps {
	        echo 'MODEL_UPDATE: ${env.MODEL_UPDATE}'
	           echo '> Running automation ...'
	           sh '''
	                    echo "Multiline shell steps works too"
	                    git status
	                '''
	            sh "python3 ${WORKSPACE}/automation.py --workspace=${WORKSPACE} --branch=${BRANCH_NAME} --updates=\'${env.MODEL_UPDATE}\'"
	        }
	    }

    }
}






