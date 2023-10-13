# Kubernetes_03.md
### 쿠버네티스 클러스터 셋업

c:\kubernetes

```bash
git clone https://github.com/techiescamp/vagrant-kubeadm-kubernetes
cd vagrant-kubeadm-kubernetes
code .
```

**설정 수정**

settings.yaml

```yaml
nodes:
  control:
    cpu: 2
    memory: 4096
  workers:
    count: 2				<<<< 1을 2로 수정
    cpu: 1
    memory: 2048
```

Vagrantfile (89~91번째 라인 주석 처리)

```bash
# Only install the dashboard after provisioning the last worker (and when enabled).
      # if i == NUM_WORKER_NODES and settings["software"]["dashboard"] and settings["software"]["dashboard"] != ""
      #   node.vm.provision "shell", path: "scripts/dashboard.sh"
      # end
```

**가상머신 생성**

```bash
vagrant up
vagrant ssh master
vagrant@master-node:~$ kubectl get node
NAME            STATUS   ROLES           AGE     VERSION
master-node     Ready    control-plane   15m     v1.27.1
worker-node01   Ready    worker          11m     v1.27.1
worker-node02   Ready    worker          7m37s   v1.27.1
```

### 레플리카셋(repllicaset)

https://kubernetes.io/ko/docs/concepts/workloads/controllers/replicaset

- 일정 개수의 파드를 `유지`하는 컨트롤러 (파드 관리를 레플리카셋이 한다.)
    - 정해진 수의 동일한 파드가 항상 실행되도록 관리
    - 노드 장애 등의 이유로 파드를 사용할 수 없다면 다른 노드에 파드를 다시 생성
    - cf. 컨테이너 관리를 pod가 해준

**시크릿 생성 및 확인**

도커 허브에서 이미지를 가져올 때 사용할 자격증명 정보를 저장할 시크릿을 생성

```bash
vagrant@master-node:~$ kubectl create secret docker-registry regcred --docker-server=https://index.docker.io/v1/ --docker-username=suahcho --docker-password='dockerhub0929!' --docker-email=sacho0929@gmail.com
secret/regcred created

vagrant@master-node:~$ kubectl get secret regcred --output=yaml
apiVersion: v1
data:
  .dockerconfigjson: eyJhdXRocyI6eyJodHRwczovL2luZGV4LmRvY2tlci5pby92MS8iOnsidXNlcm5hbWUiOiJzdWFoY2hvIiwicGFzc3dvcmQiOiJkb2NrZXJodWIwOTI5ISIsImVtYWlsIjoic2FjaG8wOTI5QGdtYWlsLmNvbSIsImF1dGgiOiJjM1ZoYUdOb2J6cGtiMk5yWlhKb2RXSXdPVEk1SVE9PSJ9fX0=
kind: Secret
metadata:
  creationTimestamp: "2023-10-06T02:55:46Z"
  name: regcred
  namespace: default
  resourceVersion: "18206"
  uid: e029eeff-e5a2-46d4-ab97-33aa91e68f2c
type: kubernetes.io/dockerconfigjson

vagrant@master-node:~$ kubectl get secret regcred --output="jsonpath={.data.\.dockerconfigjson}" | base64 --decode
{"auths":{"https://index.docker.io/v1/":{"username":"suahcho","password":"dockerhub0929!","email":"sacho0929@gmail.com","auth":"c3VhaGNobzpkb2NrZXJodWIwOTI5IQ=="}}}
```

nginx-pod-with-ubuntu.yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-nginx-pod
spec:
  containers:
  - name: my-nginx-container
    image: docker.io/nginx:latest
    ports:
    - containerPort: 80
      protocol: TCP
  - name: ubuntu-sidecar-container
    image: docker.io/alicek106/rr-test:curl
    command: ["tail"]
    args: ["-f", "/dev/null"]
  imagePullSecrets:
  - name: regcred
```

```bash
kubectl apply -f nginx-pod-with-ubuntu.yaml
pod/my-nginx-pod created
vagrant@master-node:~$ kubectl get pod
NAME           READY   STATUS    RESTARTS   AGE
my-nginx-pod   2/2     Running   0          8s
vagrant@master-node:~$ kubectl get pod -o wide
NAME           READY   STATUS    RESTARTS   AGE   IP             NODE            NOMINATED NODE   READINESS GATES
my-nginx-pod   2/2     Running   0          29s   172.16.158.2   worker-node02   <none>           <none>
vagrant@master-node:~$ kubectl apply -f nginx-pod-with-ubuntu.yaml
pod/my-nginx-pod unchanged
```

**레플리카셋 생성 및 확인**

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: replicaset-nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-nginx-pods-label
  template:
    metadata:
      name: my-nginx-pod
      labels:
        app: my-nginx-pods-label
    spec:
      containers:
      - name: my-nginx-container
        image: docker.io/nginx:latest
        ports:
        - containerPort: 80
          protocol: TCP
      imagePullSecrets:
      - name: regcred
```

```bash
vagrant@master-node:~$ kubectl apply -f replicaset-nginx.yaml
replicaset.apps/replicaset-nginx **created**
vagrant@master-node:~$ kubectl get pod -o wide
NAME                     READY   STATUS    RESTARTS   AGE     IP              NODE            NOMINATED NODE   READINESS GATES
my-nginx-pod             2/2     Running   0          5m57s   172.16.158.2    worker-node02   <none>           <none>
replicaset-nginx-jnfxg   1/1     Running   0          40s     172.16.158.3    worker-node02   <none>           <none>
replicaset-nginx-lcxbh   1/1     Running   0          40s     172.16.87.193   worker-node01   <none>           <none>
replicaset-nginx-mnkr5   1/1     Running   0          40s     172.16.87.194   worker-node01   <none>           <none>

vagrant@master-node:~$ kubectl get rs -o wide
NAME               DESIRED   CURRENT   READY   AGE   CONTAINERS           IMAGES                   SELECTOR
replicaset-nginx   3         3         3       66s   my-nginx-container   docker.io/nginx:latest   app=my-nginx-pods-label
```

**파드의 개수를 늘려서 실행**

```bash
vagrant@master-node:~$ cp replicaset-nginx.yaml replicaset-nginx-4pods.yaml
```

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: replicaset-nginx
spec:
  replicas: **4**
  selector:
    matchLabels:
      app: my-nginx-pods-label
  template:
    metadata:
      name: my-nginx-pod
      labels:
        app: my-nginx-pods-label
    spec:
      containers:
      - name: my-nginx-container
        image: docker.io/nginx:latest
        ports:
        - containerPort: 80
          protocol: TCP
      imagePullSecrets:
      - name: regcred
```

```bash
vagrant@master-node:~$ kubectl apply -f replicaset-nginx-4pods.yaml
replicaset.apps/replicaset-nginx **configured**
vagrant@master-node:~$ kubectl get pod -o wide
NAME                     READY   STATUS    RESTARTS   AGE     IP              NODE            NOMINATED NODE   READINESS GATES
replicaset-nginx-h95cz   1/1     Running   0          22s     172.16.158.4    worker-node02   <none>           <none>
replicaset-nginx-jnfxg   1/1     Running   0          4m31s   172.16.158.3    worker-node02   <none>           <none>
replicaset-nginx-lcxbh   1/1     Running   0          4m31s   172.16.87.193   worker-node01   <none>           <none>
replicaset-nginx-mnkr5   1/1     Running   0          4m31s   172.16.87.194   worker-node01   <none>           <none>

vagrant@master-node:~$ kubectl get pod
NAME                     READY   STATUS    RESTARTS   AGE
**replicaset-nginx-h95cz   1/1     Running   0          83s  // 하나가 추가된 것**
replicaset-nginx-jnfxg   1/1     Running   0          5m32s
replicaset-nginx-lcxbh   1/1     Running   0          5m32s
replicaset-nginx-mnkr5   1/1     Running   0          5m32s
```

**scale 명령으로 replicas수정**

```bash
vagrant@master-node:~$ kubectl scale replicaset replicaset-nginx --replicas=5
replicaset.apps/replicaset-nginx scaled
vagrant@master-node:~$ kubectl get pod
NAME                     READY   STATUS    RESTARTS   AGE
**replicaset-nginx-44znd   1/1     Running   0          4s**
replicaset-nginx-h95cz   1/1     Running   0          2m40s
replicaset-nginx-jnfxg   1/1     Running   0          6m49s
replicaset-nginx-lcxbh   1/1     Running   0          6m49s
replicaset-nginx-mnkr5   1/1     Running   0          6m49s
```

**파드를 삭제하면 파드 내 컨테이너도 함께 삭제된다.**

```bash
vagrant ssh master
```

nginx-pod-with-ubuntu.yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-nginx-pod
spec:
  containers:
  - name: my-nginx-container
    image: nginx
    ports:
    - containerPort: 80
      protocol: TCP
  - name: ubuntu-sidecar-container
    image: alicek106/rr-test:curl
    command: ["tail"]
    args: ["-f", "/dev/null"]
```

```bash
vagrant@master-node:~$ kubectl apply -f nginx-pod-with-ubuntu.yaml
pod/my-nginx-pod created
vagrant@master-node:~$ kubectl get pods
NAME           READY   STATUS    RESTARTS   AGE
my-nginx-pod   2/2     Running   0          53s
```

**edit 명령으로 속성을 수정**

```bash
vagrant@master-node:~$ kubectl edit replicaset replicaset-nginx

# Please edit the object below. Lines beginning with a '#' will be ignored,
# and an empty file will abort the edit. If an error occurs while saving this file will be
# reopened with the relevant failures.
#
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"apps/v1","kind":"ReplicaSet","metadata":{"annotations":{},"name":"replicaset-nginx","namespace":"default"},"spec":{"replicas":4,"selector":{"matchLabels":{"app":"my-nginx-pods-label"}},"template":{"metadata":{"labels":{"app":"my-nginx-pods-label"},"name":"my-nginx-pod"},"spec":{"containers":[{"image":"docker.io/nginx:latest","name":"my-nginx-container","ports":[{"containerPort":80,"protocol":"TCP"}]}],"imagePullSecrets":[{"name":"regcred"}]}}}}
creationTimestamp: "2023-10-06T03:16:49Z"
  generation: 4
  name: replicaset-nginx
  namespace: default
  resourceVersion: "21024"
  uid: 35848c55-65f2-4df8-ad5c-89010da5338b
spec:
  replicas: **6**
  selector:
    matchLabels:
      app: my-nginx-pods-label
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: my-nginx-pods-label
      name: my-nginx-pod
    spec:
      containers:
      - image: docker.io/nginx:latest
        imagePullPolicy: Always
        name: my-nginx-container
        ports:
        - containerPort: 80
          protocol: TCP
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
      dnsPolicy: ClusterFirst
      imagePullSecrets:
      - name: regcred
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
status:
  availableReplicas: 6
  fullyLabeledReplicas: 6
  observedGeneration: 4
  readyReplicas: 6
  replicas: 6

replicaset.apps/replicaset-nginx edited

vagrant@master-node:~$ kubectl get pods
NAME                     READY   STATUS    RESTARTS   AGE
replicaset-nginx-44znd   1/1     Running   0          5m1s
replicaset-nginx-h95cz   1/1     Running   0          7m37s
replicaset-nginx-jnfxg   1/1     Running   0          11m
replicaset-nginx-lcxbh   1/1     Running   0          11m
replicaset-nginx-mnkr5   1/1     Running   0          11m
replicaset-nginx-nvbf8   1/1     Running   0          2m47s  **// 하나의 파드 추가**
```

**레플리카셋 삭제 → 레플리카셋에 의해 생성된 파드도 함께 삭제된다.**

1. 레플리카셋 이름을 이용해서 삭제
    
    ```bash
    vagrant@master-node:~$ kubectl delete rs replicaset-nginx
    replicaset.apps "replicaset-nginx" deleted
    
    vagrant@master-node:~$ kubectl get rs,pod
    No resources found in default namespace.
    ```
    
2. YAML 파일을 이용하여 삭제
    
    ```bash
    vagrant@master-node:~$ kubectl get pods,rs
    NAME                         READY   STATUS              RESTARTS   AGE
    pod/replicaset-nginx-294pp   1/1     Running             0          8s
    pod/replicaset-nginx-5cbnn   1/1     Running             0          8s
    pod/replicaset-nginx-dgkk9   1/1     Running             0          8s
    pod/replicaset-nginx-xcvfv   0/1     ContainerCreating   0          8s
    
    NAME                               DESIRED   CURRENT   READY   AGE
    replicaset.apps/replicaset-nginx   4         4         3       8s
    
    vagrant@master-node:~$ kubectl delete -f replicaset-nginx-4pods.yaml
    replicaset.apps "replicaset-nginx" deleted
    
    vagrant@master-node:~$ kubectl get pods,rs
    No resources found in default namespace.
    ```
    
3. 파드는 유지하고 레플리카셋만 삭제
    
    ```bash
    vagrant@master-node:~$ kubectl delete -f replicaset-nginx-4pods.yaml **--cascade=orphan**
    replicaset.apps "replicaset-nginx" deleted
    
    vagrant@master-node:~$ kubectl get pods,rs
    NAME                         READY   STATUS    RESTARTS   AGE
    pod/replicaset-nginx-9dmjr   1/1     Running   0          71s
    pod/replicaset-nginx-h6j2q   1/1     Running   0          71s
    pod/replicaset-nginx-n44r6   1/1     Running   0          71s
    pod/replicaset-nginx-s7zrp   1/1     Running   0          71s
    ```
    
    **레플리카셋의 동작 원리**
    
    - 라벨 셀렉터(Label Selector)를 이용해서 유지할 파드를 정의
    - 레플리카셋은 spec.selector.matchLabels에 정의된 라벨을 통해 생성해야하는 파드를 찾음
        
        → app: my-nginx-pods-label
        
    - 라벨을 가지는 파드의 개수가 replicas 항목에 정의된 숫자보다 적으면 파드를 정의하는 파드 템플릿(template)항목의 내용으로 패드를 생성
    
    1. 레플리카셋 생성전에 app:my-nginx-pods-label 라벨을 가지는 파드를 먼저 생성
        
        ```yaml
        apiVersion: v1
        kind: Pod
        metadata:
          name: my-nginx-pod
          labels:
            app: my-nginx-pods-label
        spec:
          containers:
          - name: my-nginx-container
            image: docker.io/nginx:latest
            ports:
            - containerPort: 80
              protocol: TCP
          imagePullSecrets:
          - name: regcred
        ```
        
        ```bash
        vagrant@master-node:~$ kubectl apply -f nginx-pod-without-rs.yaml
        pod/my-nginx-pod created
        
        vagrant@master-node:~$ kubectl get pod --show-labels
        NAME           READY   STATUS    RESTARTS   AGE   LABELS
        my-nginx-pod   1/1     Running   0          36s   app=my-nginx-pods-label
        ```
        
    2. app:my-nginx-pods-label라벨을 가지는 파드 3개를 생성하는 레플리카셋을 생성
        
        ```yaml
        apiVersion: apps/v1
        kind: ReplicaSet
        metadata:
          name: replicaset-nginx
        spec:
          replicas: 3
          selector:
            matchLabels:
              app: my-nginx-pods-label
          template:
            metadata:
              name: my-nginx-pod
              labels:
                app: my-nginx-pods-label
            spec:
              containers:
              - name: my-nginx-container
                image: docker.io/nginx:latest
                ports:
                - containerPort: 80
                  protocol: TCP
              imagePullSecrets:
              - name: regcred
        ```
        
        ```bash
        vagrant@master-node:~$ kubectl apply -f replicaset-nginx.yaml
        replicaset.apps/replicaset-nginx created
        
        vagrant@master-node:~$ kubectl get pod --show-labels
        NAME                     READY   STATUS    RESTARTS   AGE    LABELS
        my-nginx-pod             1/1     Running   0          2m9s   app=my-nginx-pods-label
        replicaset-nginx-d9rdb   1/1     Running   0          32s    app=my-nginx-pods-label  **//두개의 파드만 새로 생성**
        replicaset-nginx-trbp6   1/1     Running   0          32s    app=my-nginx-pods-label
        
        **// 라벨이 동일하면 총 pod개수에 맞춰서 만들어진다.**
        
        vagrant@master-node:~$ kubectl delete pod my-nginx-pod
        pod "my-nginx-pod" deleted
        vagrant@master-node:~$ kubectl get pod --show-labels
        NAME                     READY   STATUS    RESTARTS   AGE     LABELS
        replicaset-nginx-d9rdb   1/1     Running   0          2m22s   app=my-nginx-pods-label 
        replicaset-nginx-trbp6   1/1     Running   0          2m22s   app=my-nginx-pods-label
        **replicaset-nginx-xqfqk   1/1     Running   0          10s     app=my-nginx-pods-label // 레플맄카셋이 새로운 파드를 생성**
        ```
        
    
    1. 레플리카셋이 생성한 파드의 라벨을 변경
        
        ```bash
        replicaset-nginx-d9rdb 변경
        
        vagrant@master-node:~$ kubectl edit pod replicaset-nginx-d9rdb
        
        		# labels:
                # app: my-nginx-pods-label
        **주석처리**
        
        pod/replicaset-nginx-d9rdb **edited**
        
        vagrant@master-node:~$ kubectl get pod --show-labels
        NAME                     READY   STATUS    RESTARTS   AGE     LABELS
        replicaset-nginx-d9rdb   1/1     Running   0          5m29s   **<none>**
        replicaset-nginx-trbp6   1/1     Running   0          5m29s   app=my-nginx-pods-label
        replicaset-nginx-xqfqk   1/1     Running   0          3m17s   app=my-nginx-pods-label
        **replicaset-nginx-znhdc   1/1     Running   0          6s      app=my-nginx-pods-label //레플리카셋에 의해 새로운 pod 생성된다.**
        ```
        
    
    1. 레플리카셋을 삭제 → 라벨이 일치하지 않는 파드는 삭제되지 않음 (레플리카의 관리 대상이 아님)
        
        ```bash
        vagrant@master-node:~$ kubectl get rs -o wide
        NAME               DESIRED   CURRENT   READY   AGE    CONTAINERS           IMAGES                   SELECTOR
        replicaset-nginx   3         3         3       9m7s   my-nginx-container   docker.io/nginx:latest   app=my-nginx-pods-label
        
        vagrant@master-node:~$ kubectl delete replicaset replicaset-nginx
        replicaset.apps "replicaset-nginx" **deleted**
        
        vagrant@master-node:~$ kubectl get rs -o wide
        No resources found in default namespace.
        
        vagrant@master-node:~$ kubectl get pod --show-labels
        NAME                     READY   STATUS    RESTARTS   AGE     LABELS
        replicaset-nginx-d9rdb   1/1     Running   0          9m48s   <none>
        **// 라벨이 삭제된 파드는 레플리카셋에 의해 삭제되지 않는다.**
        ```
        
    2. 라벨이 삭제된 파드는 직접 삭제
        
        ```bash
        vagrant@master-node:~$ kubectl delete pod replicaset-nginx-d9rdb
        pod "replicaset-nginx-d9rdb" deleted
        
        vagrant@master-node:~$ kubectl get pod --show-labels
        No resources found in default namespace.
        ```
        
