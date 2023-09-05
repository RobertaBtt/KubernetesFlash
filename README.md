# Kubernetes Flash
Deploy fast a containerized application with simple API and deploy it with Kubernetes

We work locally with a Virtual Environment named _kubernetes_flash_env_ with Python

    cd app
    python3 -m venv kubernetes_flash_env

Activate virtual environment:

    . kubernetes_flash_env/bin/activate


Since a docker-compose is provided, you can make the container up with this command:

    docker-compose up


To see the situation of currently running docker containers:

    docker ps



Initialization with Google Cloud:

    gcloud init


Setting the project of Google Cloud:

    gcloud config set project data-wrangling-397007

Install Kubernetes command line:

    snap install kubectl --classic



Creating the Cluster

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
    
    ╔════════════════════════════════════════════════════════════╗
    ╠═ Creating update staging area                             ═╣
    ╠════════════════════════════════════════════════════════════╣
    ╠═ Installing: Google Container Registry's Docker creden... ═╣
    ╠════════════════════════════════════════════════════════════╣
    ╠═ Installing: Google Container Registry's Docker creden... ═╣
    ╠════════════════════════════════════════════════════════════╣
    ╠═ Creating backup and activating new installation          ═╣
    ╚════════════════════════════════════════════════════════════╝
    
    Performing post processing steps...done.                                                                                                                                      
    
    Update done!

To tell Google Cloud Container Registry to use this config file for credential 


    docker-credential-gcr configure-docker


Build the image of docker

    docker build -t gcr.io/data-wrangling-397007/kubernetes_flash:v1 .


Output:

    Step 1/10 : FROM python:3
     ---> 28d8ca9ad96d
    Step 2/10 : ENV PYTHONUNBUFFERED 1
     [...]
    Step 10/10 : CMD [ "python", "app.py" ]
     ---> Running in 5d053024a2f0
    Removing intermediate container 5d053024a2f0
     ---> 9d606c5761f4
    Successfully built 9d606c5761f4
    Successfully tagged gcr.io/data-wrangling-397007/kubernetes_flash:v1



To authorize the configuration of docker (configure-docker it is the plugin previosly installed)

    gcloud auth configure-docker


Activate the keys (the files json that you've downloaded):

    gcloud auth activate-service-account --key-file=../keys/data-wrangling-397007-648a818f82aa.json

Output

    Activated service account credentials for: [container-registry@data-wrangling-397007.iam.gserviceaccount.com]



Provide the authentication, after the creation of the keys:
    
    cat ../keys/data-wrangling-397007-7aa2c47805e6.json | docker login -u _json_key --password-stdin https://gcr.io


Push the container to the Registry of the containers in Google Cloud:
    
    docker push gcr.io/data-wrangling-397007/kubernetes_flash:v1


Output:

        The push refers to repository [gcr.io/data-wrangling-397007/kubernetes_flash]
        1abea940a52e: Pushed 
        619f43313141: Layer already exists 
        [...]
        v1: digest: sha256:f086939fcb size: 3050




To Deploy to Kubernetes:

    kubectl apply -f api-deployment.yaml

Output

    deployment.apps/api configured
    service/api created


A POD is a structure where the Architecture of Kubernetes is based.
Pod houses the containers.

A Kubernetes service is a set of PODs that work together inside a Kubernetes cluster.

To see the PODs in Kubernetes:
    
    kubect get pods

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
