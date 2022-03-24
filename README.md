# Python Flask App with Helm Package deployment

## Run the below command to create a fresh docker image:

```
 docker build -t flask-blacklist-svc:v1 package

```


## Before Deploying the helm charts the prerequisite is to create a namespace :


```
kubectl create ns microservices

```


## Once namespace is created, execute the below command to create a new helm release, make sure, the present directory is the one where Chart.yaml and values.yaml is saved

```
 helm install  flask-blacklist . -n microservices
```
 

## To test the functionality of the app, we can simply do a port forwarding to map the container ports to local machines.

```
 kubectl port-forward flask-blacklist-deployment-54hbr   5004:5004 

```
 
 
-- http://127.0.0.1:5004/?n=88 

-- http://127.0.0.1/blacklisted
