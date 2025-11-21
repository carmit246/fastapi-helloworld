# fastapi-helloworld

Forked from https://github.com/enriquecatala/fastapi-helloworld repository.

This repo resresents simple CI/CD workflows using Helm and ArgoCD

## Helm chart
Resources:
1. Serviceaccount
2. Deployment
3. Service
4. HPA

** Assumption: the helloworld service is a backend microservice, and will be accessed from other services inside the K8s cluster. 
  In case it should be accessed from outside the cluster, Ingress resource should be added.

## The CI/CD workflow:

Test/Lint/Audit → Build and push image to ECR → Deploy to EKS

### CI workflow 

Triggers on PR and Merge to main branch. Will run the following:
* Lint - darker
* Audit - pip-audit (the ci currently ignores the findings to continue the process)
* Test - added simple tests. Run with pytest

### Build workflow 

Triggers on merge to main after the CI workflow competes successfully
Build the docker image
Tag the image with the current commit hash
Push to ECR

### Deploy workflow 

Triggers on merge to main after the build workflow competes successfully:

Deploy the helm chart to dev cluster, use the newly created image

Separate workflow to allow future deployment to additional envs (using github environments)

Deployment-type variable:
1. helm - ude ```helm install``` command
2. argocd - update the image tag in the values file
