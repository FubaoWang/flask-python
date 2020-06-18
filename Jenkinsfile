def label = "jnlp-slave"
node(label){
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
				kustomize edit set image 192.168.8.192:5000/flask-python:${Tag}
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


