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
    volumeMounts:
    - name: openfaas-basic-auth
      mountPath: /etc/secrets/openfaas-basic-auth
      readOnly: true
    - name: openfaas-endpoint
      mountPath: /etc/openfaas-endpoint
      readOnly: true
  volumes:
  - name: openfaas-basic-auth
    secret:
      secretName: openfaas-basic-auth
  - name: openfaas-endpoint
    configMap:
      name: jenkins-openfaas-endpoint
"""
    }
  }
  
  environment {
    AWS_REGION = "us-east-1"
    DOCKER_REPO = "829968223664.dkr.ecr.us-east-1.amazonaws.com/"
  }

  stages {
    stage('Setup') {
      steps {
        container('build') {
          sh """
            apt update
            DEBIAN_FRONTEND=noninteractive apt install -y docker.io awscli curl
            curl -sLS cli.openfaas.com | sh
            aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $DOCKER_REPO
            cat /etc/secrets/openfaas-basic-auth/basic-auth-password | faas-cli login -g `cat /etc/openfaas-endpoint/openfaas_endpoint` -u `cat /etc/secrets/openfaas-basic-auth/basic-auth-user` --password-stdin
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
              faas-cli deploy -f \${f}.yml
              cd \$OLDPWD
          done
          """
        }
      }
    }
  }
}
