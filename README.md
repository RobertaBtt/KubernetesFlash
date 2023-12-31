# Kubernetes Flash

Deploy fast a containerized application with simple API and deploy it with Kubernetes


We work locally with a Virtual Environment named _kubernetes_flash_env_ with Python

    cd app
    python3 -m venv kubernetes_flash_env

Activate virtual environment:

    . kubernetes_flash_env/bin/activate

## Run locally

    docker-compose down && docker-compose up --build


#### Build and tag the Image

    docker build -t kubernetes_flash:v1 .


To see the docker process that are running now and in the past:

    docker ps --all


## Google Cloud Platform 

If you want to deploy this service with the Kubernetes cluseter offerend by Google, 
you have to first initialize your Google Cloud account


    gcloud init


##### Setting the project of Google Cloud:

    gcloud config set project data-wrangling-397007

##### Install Kubernetes command line:

    snap install kubectl --classic


##### Creating the Cluster

    gcloud container clusters create flashcluster --num-nodes 1 --region europe-west1


THe plugin **gke-gcloud-auth-plugin** must be installed

    gcloud components install gke-gcloud-auth-plugin


    kubectl config get-contexts

Output:

    CURRENT   NAME                                                  CLUSTER                                               AUTHINFO                                              NAMESPACE
    gke_data-wrangling-397007_europe-west1_flashcluster   gke_data-wrangling-397007_europe-west1_flashcluster   gke_data-wrangling-397007_europe-west1_flashcluster   


    gcloud container clusters get-credentials flashcluster --region europe-west1 \
        --project data-wrangling-397007

Output:

    Fetching cluster endpoint and auth data.
    kubeconfig entry generated for flashcluster.


The plugin **docker-credential-gcr** must be installed

    gcloud components install docker-credential-gcr

Output

    Your current Google Cloud CLI version is: 444.0.0
    Installing components from version: 444.0.0
    
    ┌──────────────────────────────────────────────────────────────────────────┐
    │                   These components will be installed.                    │
    ├──────────────────────────────────────────────────────┬─────────┬─────────┤
    │                         Name                         │ Version │   Size  │
    ├──────────────────────────────────────────────────────┼─────────┼─────────┤
    │ Google Container Registry's Docker credential helper │   1.5.0 │ 1.8 MiB │
    └──────────────────────────────────────────────────────┴─────────┴─────────┘
    
    For the latest full release notes, please visit:
      https://cloud.google.com/sdk/release_notes
    
    Do you want to continue (Y/n)?  Y
    [...]
    Update done!
---
To tell Google Cloud Container Registry to use this config file for credential 

    docker-credential-gcr configure-docker

### Setting Google Cloud Credentials


To authorize the configuration of docker (configure-docker it is the plugin previosly installed)

    gcloud auth configure-docker


Activate the keys (the files json that you've downloaded):

    gcloud auth activate-service-account --key-file=../keys/data-wrangling-397007-648a818f82aa.json

Output

    Activated service account credentials for: [container-registry@data-wrangling-397007.iam.gserviceaccount.com]



Provide the authentication, after the creation of the keys:
    
    cat ../keys/data-wrangling-397007-7aa2c47805e6.json | docker login -u _json_key --password-stdin https://gcr.io


### Build and deploy to Kubernetes

Build the image of docker

    docker build -t gcr.io/data-wrangling-397007/kubernetes_flash:v1 .


Output:

    [...]  
    Successfully tagged gcr.io/data-wrangling-397007/kubernetes_flash:v1




Push the container to the Registry of the containers in Google Cloud:
    
    docker push gcr.io/data-wrangling-397007/kubernetes_flash:v1


Output:

        The push refers to repository [gcr.io/data-wrangling-397007/kubernetes_flash]
        1abea940a52e: Pushed 
        619f43313141: Layer already exists 
        [...]
        v1: digest: sha256:f086939fcb size: 3050




##### To Deploy to Kubernetes the configuration of the pods and service:

    kubectl apply -f api-deployment.yaml

Output

    deployment.apps/api configured
    service/api created

#### Force deploy:

    kubectl delete pod <id_pod>
----

A POD is a structure where the Architecture of Kubernetes is based.
Pod houses the containers.

A Kubernetes service is a set of PODs that work together inside a Kubernetes cluster.

To see the PODs in Kubernetes:
    
    kubectl get pods

Output:
    
    NAME                   READY   STATUS        RESTARTS   AGE
    api-6f4d5d584d-j9pfn   1/1     Running       0          15s
    api-844fd4849b-hnbnj   1/1     Terminating   0          16m



To see the Services that are running in Kubernetes:

    kubectl get svc
Output:

        NAME         TYPE           CLUSTER-IP    EXTERNAL-IP      PORT(S)        AGE
        api          LoadBalancer   10.32.3.246   130.211.89.241   80:32175/TCP   88s
        kubernetes   ClusterIP      10.32.0.1     <none>           443/TCP        115m

If you can login in your Google Cloud platform:

![cluster_kubernetes.png](app%2Fdoc%2Fcluster_kubernetes.png)

And the service that we named api:

![service.png](app%2Fdoc%2Fservice.png)

So if you go in the public IP:

    http://130.211.89.241/

![app_works.png](app%2Fdoc%2Fapp_works.png)

---
##### Log work

First couple of hours : setting up the Kubernetes cluster and pod, GCP permission, 
Verifying that the service is deployed. Reverse approach end to end.
(#day 1): starting the development of the real service by starting from the test (Test Driven Development TDD)

installing the library for test:

    pip install pytest

Updating the requirements:

    pip freeze > requirements.txt

---

#day 1: 

make the assumption: Software evolves, APIs must be versioned
 Thinking about the API versioning strategy

When you build an API you try to not break the contract with the clients, 
with sudden changes that they were not prepared to deal.

So, keeping it simple: you can evolve your returing data in the API, 
as long as the clients know this.

#### Which paradigm for versioning API ?
To decide how to version is a philosofical discussion.
- Version via a request parameter
- Version number as a date
  - For example for API that changes often, like the one of Stripe, the strategy is to provide
the version in this format `YYYYMMdd` in the Header.
  
- Accept header
  - `curl -v -H 'Accept:application/vnd.example.v1+json' localhost:3000`
- in the URL: /api/v1/..

When you upgrade the software behind the API you are already breaking the contract with the client.

Better to start simple and add fields later, rather than delete fields after, breaking the clients.

Versioning the API could follow the Semantic Version paradigm.


The decision I've made for this project test is this:



If you don't specify the version, it means you are using the First version, 
or the last version ?

I choose the "**First version**" or the version that was the last or the newest
when you first contract the client, if there is authentication and clients are
paying for the API and registered users.


----

If you are not breaking things, you can just keep the current version, 
but if you are sure you are breaking staff for the clients, you should avoid this
and permit them to use the previous version until they are ready to use the latest version.

---

###### #day1

#### Test Driven Development
Writing test for two endpoints.

#### How to update a service

    kubectl set image deployment.apps/api api=gcr.io/data-wrangling-397007/kubernetes_flash:v1
    kubectl set image deployment.apps/api api=gcr.io/data-wrangling-397007/kubernetes_flash

    
Output:

    deployment.apps/api image updated
  


---

######  #day1
- Introduced the Dependency Container.
- Introduced the connection SQLiteConnection
- the POST route which needs a light DB (SQLLite) to store the list of CSV
- I want my program to be flexible enough if I want to 
change the type of database later.

Updated the POST request

Running Tests
---

######  #day2
Completed the repository for both entities csv and topic.

Completed the Tests, HTTP exception, verified end point,
move code, refactoring.

Running Tests

###### Reviewed this Readme.

