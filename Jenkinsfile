pipeline {
   agent any
   stages {
    stage('Checkout') {
      steps {
        script {
           // The below will clone your repo and will be checked out to master branch by default.
           print("cloning repo")
           git credentialsId: 'arnold.dajao@ironnetcybersecurity.com', url: 'https://github.com/arnoldmd181/piSandBox.git'
           // Do a ls -lart to view all the files are cloned. It will be clonned. This is just for you to be sure about it.
           print("ls")
//            sh "ls -lart ./*"
           sh """
                git fetch --all
            """
            //                 git config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'
           // List all branches in your repo.
           sh "git branch -a"

           // Checkout to a specific branch in your repo.
           sh "git checkout origin dc-test"
          }
       }
    }
  }
}



// def COMPONENTS = ['indexer', 'transformer', 'ingest-api']
// def ACCOUNTS = ['dev': "263734463344", 'prod': "725071466363"]
// def  FILES_LIST = sh (script: "ls   '${WORKSPACE}'", returnStdout: true).trim()

// pipeline {
// //         agent any
//     agent {
//         kubernetes {
//           defaultContainer 'python'
//           yaml '''\
//             apiVersion: v1
//             kind: Pod
//             spec:
//               containers:
//               - name: python
//                 image: python:3.6
//                 command:
//                 - cat
//                 tty: true
//                 resources:
//                   requests:
//                     memory: 1Gi
//             '''.stripIndent()
//         }
//      }
//
//     stages {
//         stage('Setup') { // Install any dependencies you need to perform testing
//           steps {
//             script {
//               sh """
//               pip3 install GitPython
//               """
//               env.GH_URL = GIT_URL.substring(0, GIT_URL.size() - 4)
//               env.COMMIT_URL = GIT_BRANCH == "dev" ? "${GH_URL}/commit/${GIT_COMMIT}" : "${GH_URL}/pull/${GIT_BRANCH.substring(3, GIT_BRANCH.size())}/commits/${GIT_COMMIT}"
// //               sh """apt-get update && apt-get install -y git"""
//               sh 'printenv'
//             }
//           }
//         }
//
//         stage("automation") {
// //           withEnv(["HOME=${env.WORKSPACE}"]) {
//             steps {
//                 echo '> Running automation ...'
// //                 sh """make -sC domain_classifier test"""
// //                 sh "./scripts/automation.sh"
//                 sh '''
//                     echo "Multiline shell steps works too"
//                     ls -lah
//                     git --version
//                     git status
//                     git fetch --all
//                     git branch
//                     git branch -r
//                     git log --oneline
//                 '''
// //                     git branch dc-test
// //                     git checkout dc-test
//                 sh "python3 ${WORKSPACE}/automation.py --workspace=${WORKSPACE} --branch=${BRANCH_NAME}"
// //                 sh "bash ${WORKSPACE}/build_scripts/test.sh domain_classifier"
//                 sh '''
//                     git status
//                     git log --oneline
//
//                     git add .
//                     git commit -m "automation added updated versions"
//                     git push --set-upstream origin dc-test2
//                 '''
//                 echo "--------Flake8 ${1}--------"
// //                 sh "pip3 install flake8"
// //                 sh "flake8 ${WORKSPACE}/domain_classifier"
//             }
//         }
//
//         stage("autopep") {
//             steps {
//                 script {
//                     echo "autopep"
//                 }
//             }
//         }
//         stage("wheel") {
//             steps {
//                 script {
//                           echo "wheel"
//                 }
//             }
//         }
//         stage("deploy") {
//             steps {
//                 script {
//                           echo "wheel"
//                 }
//             }
//         }
//     }
// }
//
