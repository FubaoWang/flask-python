def label = "jnlp-slave"
podTemplate(label: label, cloud: 'kubernetes',
  containers: [
    containerTemplate(
        name: 'jnlp',
        image: '192.168.8.192:5000/jnlp-slave',
        alwaysPullImage: false,
    ),
    containerTemplate(name: 'docker', image: 'docker:18.06', command: 'cat', ttyEnabled: true,  privileged: true),
    containerTemplate(name: 'kubectl', image: '192.168.8.192:5000/kubectl:v1.14.1', command: 'cat', ttyEnabled: true, , privileged: true),
  ],
  nodeSelector:'ci=jenkins',
  volumes: [
    hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock'),
    hostPathVolume(mountPath: '/usr/local/jdk', hostPath: '/usr/local/jdk'),
    hostPathVolume(mountPath: '/usr/bin/docker', hostPath: '/usr/bin/docker'),
    hostPathVolume(mountPath: '/root/.m2', hostPath: '/root/.m2'),
  ],
)
{
    node(label){
		stage('Test Docker') {
		    container('docker') {
			sh 'docker version'
		    }
		}

		stage('Git Checkout'){
		git branch: '${branch}', url: 'https://github.com/FubaoWang/flask-python'
		}
		stage('Build and Push Image'){

			sh '''
			docker build -t 192.168.8.192:5000/flask-python:${Tag} .
			docker push 192.168.8.192:5000/flask-python:${Tag}
			docker rmi  192.168.8.192:5000/flask-python:${Tag}
			'''

		}

		stage('Deploy to K8s'){
			if ('true' == "${deploy}") {
				container('kubectl') {
					sh '''
					cd deploy/base
					kustomize edit set image guoxudongdocker/flask-python:${Tag}
					'''
					echo "部署到 Kubernetes"
					if ('prod' == "${ENV}") {
						sh '''
						# kustomize build deploy/overlays/prod | kubectl apply -f -
						kubectl apply -k deploy/overlays/prod
						'''
					}else {
						sh '''
						# kustomize build deploy/overlays/dev | kubectl apply -f -
						kubectl apply -k deploy/overlays/dev
						'''
					}	
				}
			}else{
				echo "跳过Deploy to K8s"
			}

		}
    }
}

