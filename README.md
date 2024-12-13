# LookupStack
Simple infrastructure for ip lookup

This stack includes:
- Terraform for provisioning infrastructure with ArvanCloud
- Ansible for automation
- Helm charts to deploy applications
- IP Lookup application written in Python using FastAPI and PostgreSQL as the database
- Prometheus and Grafana for monitoring
- Github Actions for CI/CD

## Getting started
Note: This guide assumes you are setting up a Kubernetes cluster with one master node and two worker nodes. The provided Ansible playbooks are specifically designed for this setup.

### Terraform
First, create your virtual machines (VMs) using Terraform. Navigate to the terraform directory, update the configuration files to suit your requirements, and run the following commands:
```bash
terraform init
terraform apply
```
This will provision three nodes, each with 2 vCPUs and 2 GiB of memory. If you require more resources, adjust the configuration accordingly.

### Ansible
Next, configure your nodes and prepare them for Kubernetes. Navigate to the ansible-playbooks directory and execute:
```bash
pip install -r requirements.txt  
ansible-playbook -i hosts.ini site.yaml  
```
This will:
- Install Kubernetes and its dependencies.
- Set up NFS on the master node.
- Install Node Exporter on all nodes.

### Deploy monitoring

Once Kubernetes is up and running, install Grafana, Prometheus, dashboards, and alerts for cluster and application monitoring.

Dashboards and alert configurations are located in the monitoring directory. To deploy Prometheus and Grafana, first install Helm:
```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```
Then, deploy the Grafana and Prometheus Helm charts:
```bash
helm install grafana charts/grafana --values charts/grafana/values.yaml
# Install prometheus:
helm install prometheus charts/prometheus --values charts/prometheus/values.yaml
```
Install kube-state-metrics:
```bash
helm install kube-state-metrics charts/kube-state-metrics --values charts/kube-state-metrics/values.yaml
```
To update a Helm chart after making changes, run:
```bash
helm upgrade <chart-name> <chart-directory/> --values <values-directory/values.yaml>
```

Update the Prometheus configuration (values.yaml) with the IP addresses of the Node Exporter instances. Add Grafana dashboards and alert rules as needed.


To enable storage provisioning, install the NFS provisioner:

```bash
helm install nfs-provisioner-provisioner charts/nfs-subdir-external-provisioner --values charts/nfs-subdir-external-provisioner/values.yaml
```
Update the IP address in the values file to match your NFS server.

### IP Lookup application
The IP Lookup application, built with FastAPI, retrieves the location of an IP address and stores it in PostgreSQL for future requests. Example:
```bash
curl http://0.0.0.0:8000/get-region/1.1.1.1
{"ip_address":"1.1.1.1","region":"Australia"}
```
To deploy the application:
```bash
helm install ip-lookup charts/ip-lookup --values charts/ip-lookup/values.yaml
```
Set the necessary environment variables in `values.yaml`:
```
configmap:
  DB_HOST: "postgres-postgresql-ha-pgpool.database.svc.cluster.local"
  DB_USER: "postgres"
secret:
  DATABASE_URL: ""
  DB_PASS: ""
```
Note: Secrets are left empty as they are populated through CI/CD pipelines


### PostgreSQL
This repository provides two PostgreSQL cluster options:

1- Crunchy Data PostgreSQL Operator (pgo): Ideal for high availability but requires more resources.

```
kubectl apply -k pgo/kustomize/install/namespace

kubectl apply --server-side -k pgo/kustomize/install/default

kubectl apply -k pgo/kustomize/high-availability
```

2- Bitnami PostgreSQL: Recommended for resource-constrained environments.
```
helm install postgresql-ha charts/postgresql-ha --values charts/postgresql-ha/values.yaml
```
This deploys a three-node PostgreSQL cluster with pgpool.

### CI/CD
GitHub Actions is used for CI/CD. The pipeline configuration is located in `.github/workflows/ci-cd.yaml`.

 
Set the following environment variables in your project secrets:
- DATABASE_URL: PostgreSQL connection URL
- DB_PASS: PostgreSQL database password
- DOCKER_PASSWORD: Private registry password(e.g., ArvanCloud Docker registry)
- DOCKER_USERNAME: Private registry username
- KUBECONFIG_CONTENT: Content of ~/.kube/config file

The pipeline uses the kubeconfig file to deploy the IP Lookup application with Helm.


