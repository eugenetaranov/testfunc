pipeline {
  agent {
    kubernetes {
      yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    some-label: test
spec:
  serviceAccountName: jenkins-agent
  containers:
  - name: build
    image: ubuntu
    tty: true
    securityContext: 
      privileged: true 
    command:
    - cat
    env:
    - name: OPENFAAS_USER
      valueFrom:
        secretKeyRef:
          name: openfaas-basic-auth
          key: basic-auth-user
    - name: OPENFAAS_PASSWORD
      valueFrom:
        secretKeyRef:
          name: openfaas-basic-auth
          key: basic-auth-password
"""
    }
  }
  
  environment {
    AWS_REGION = "us-east-1"
    DOCKER_REPO = "829968223664.dkr.ecr.us-east-1.amazonaws.com/"
    OPENFAAS_URL = "http://openfaas.testdomain.com"
    DEBIAN_FRONTEND = "noninteractive"
  }

  stages {
    stage('Setup') {
      steps {
        container('build') {
          sh """
            apt update
            apt install -y docker.io awscli curl amazon-ecr-credential-helper
            curl -sLS cli.openfaas.com | sh
            aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $DOCKER_REPO
            dockerd &
          """
        }
      }
    }
    stage('Build') {
      steps {
        container('build') {
          sh """cd openfaas/
          for f in `ls functions`
          do
              cd functions/\${f}
              test -f install_templates.sh && sh -x install_templates.sh
              faas-cli build -f \${f}.yml
              cd \$OLDPWD
          done
          docker images
          """
        }
      }
    }
    stage('Deploy') {
      steps {
        container('build') {
          sh """cd openfaas/
          for f in `ls functions`
          do
              cd functions/\${f}
              faas-cli push -f \${f}.yml
              cd \$OLDPWD
          done
          """
        }
      }
    }
  }
}
