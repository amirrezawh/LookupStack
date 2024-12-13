kubectl apply -k postgres-operator-examples/kustomize/install/namespace

kubectl apply --server-side -k postgres-operator-examples/kustomize/install/default

kubectl apply -k postgres-operator-examples/kustomize/high-availability
