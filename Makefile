CLUSTER := aurora
VERSION ?= dev

.PHONY: up down cluster images deploy status test

up: cluster images deploy ## Create the cluster, build the images and deploy the app

down: ## Delete the cluster
	kind delete cluster --name $(CLUSTER)

cluster:
	@kind get clusters | grep -qx $(CLUSTER) || kind create cluster --config infra/kind-config.yaml

images:
	docker build -t aurora-api:$(VERSION) app/api
	docker build -t aurora-worker:$(VERSION) app/worker
	kind load docker-image aurora-api:$(VERSION) aurora-worker:$(VERSION) --name $(CLUSTER)

deploy:
	kubectl apply -f deploy/manifests/
	kubectl rollout status deploy/api --timeout=120s
	kubectl rollout status deploy/worker --timeout=120s

status:
	kubectl get deploy,svc,pods -o wide -l app.kubernetes.io/part-of=aurora-orders

test:
	cd app/api && python3 -m pytest -q tests
