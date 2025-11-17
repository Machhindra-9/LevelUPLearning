@Library('shared') _
pipeline{
    agent any
    stages{
        stage('code'){
            steps{
                script{
                    call("mac")
                }
            }
        }
        stage('build'){
            steps{
                echo "build"
            }
        }
        stage('test'){
            steps{
                echo "test"
            }
        }
        stage('release'){
            steps{
                echo 'release'
            }
        }
        stage('deploy'){
            steps{
                echo 'deploy'
            }
        }
        stage('operate'){
            steps{
                echo 'operate'
            }
        }
        stage('monitor'){
            steps{
                echo 'monitor'
            }
        }
    }
}
