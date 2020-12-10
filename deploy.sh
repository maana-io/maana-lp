#! /usr/bin/env sh

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters. Must provide docker-registry, version-number"
    exit
fi

registry=$1
version=$2

docker build -t lp .
docker tag lp ${registry}/lp:${version}
docker push ${registry}/lp:${version}

kubectl delete service lp
kubectl delete deployment lp

cat lp_deployment.yaml | sed -e "s/{{docker-registry}}/${registry}/g" -e "s/{{version}}/${version}/g"> finalized_lp_deployment.yaml

#kubectl apply -f lp_pvc.yaml
kubectl apply -f finalized_lp_deployment.yaml
kubectl apply -f lp_service.yaml
