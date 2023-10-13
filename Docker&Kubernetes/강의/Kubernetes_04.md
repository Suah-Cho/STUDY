# Kubernetes_04.md

### 디플로이먼트(Deployment)

- 레플리카셋, 파드의 배포를 관리
- 애플리케이션의 **배포와 업데이트**를 편하게 하기 위해서 사용
- 쿠버네티스에서 **상태가 없는 (stateless) 애플리케이션을 배포**할 때 사용하는 가장 기본적인 컨트롤러
    - 상태가 있는 애플리케이션 → 데이터베이스
- 디플로이먼트는 스케일, 롤아웃, 롤백, 자동복구 기능이 있다.
    - 스케일
        - 파드의 개수를 늘리거나 줄일 수 있다.
    - 롤아웃, 롤백
        - 서비스를 유지하면서 파드를 교체
    - 자동 복구
        - 노드 수준에서 장애가 발생했을 때 파드를 복구하는 것이 가능

**디플로이먼트 생성 및 삭제**

https://kubernetes.io/ko/docs/concepts/workloads/controllers/deployment/

1. 디플로이먼 생성

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-nginx
  template:
    metadata: 
      name: my-nginx-pod
      labels:
        app: my-nginx
    spec:
      containers:
      - name: nginx
        image: docker.io/nginx
        ports:
        - containerPort: 80
      imagePullSecrets:
      - name: regcred
```

2. 디플로이먼트, 레플리카셋, 파드 생성을 확인

```bash
vagrant@master-node:~$ kubectl apply -f deployment-nginx.yaml
deployment.apps/my-nginx-deployment created
```

```bash
vagrant@master-node:~$ kubectl get deployments,replicasets,pods
NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE
**deployment.apps/my-nginx-deployment   3/3     3            3           46s
                                     ~~~~~   ~~~~~~~~~~   ~~~~~~~~~   ~~~~
                                     |       |            |           +--  파드가 실행되고 있는 지속 시간
                                     |       |            +-- 서비스 가능한 파드의 개수 
                                     |       +-- 최신 상태로 업데이트된 파드의 개수  
                                     +-- 파드의 개수**

NAME                                             DESIRED   CURRENT   READY   AGE
replicaset.apps/my-nginx-deployment-66bcdb4565   3         3         3       46s

NAME                                       READY   STATUS    RESTARTS   AGE
pod/my-nginx-deployment-66bcdb4565-q4cvt   1/1     Running   0          46s
pod/my-nginx-deployment-66bcdb4565-rmj4h   1/1     Running   0          46s
pod/my-nginx-deployment-66bcdb4565-z2vwb   1/1     Running   0          46s
```

3. 디플로이먼트를 삭제 → 레플리카셋, 파드 또한 함께 삭제되는 것을 확인

```bash
vagrant@master-node:~$ kubectl delete deployment my-nginx-deployment
deployment.apps "my-nginx-deployment" deleted

vagrant@master-node:~$ kubectl get deployments,replicasets,pods
No resources found in default namespace.
```

**디플로이먼트를 사용하는 이유**

1. **스케일**
    - 레플리카의 값을 변경해서 파드의 개수를 조절 → 처리 능력을 높이고 낮추는 기능
    - 파드이 개수를 늘리는 중에 쿠버네티스 클러스터의 자원(CPU, 메모리, …)이 부족해지면 노드를 추가하여 자원이 생길 때까지 파드 생성을 보류
    1. 레플리카 값을 3으로 설정해서 디플로이먼트를 생성
    
    web-deploy-replicas-3.yaml
    
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: web-deply
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: web
      template:
        metadata: 
          labels:
            app: web
        spec:
          containers:
          - name: nginx
            image: docker.io/nginx
            ports:
            - containerPort: 80
          imagePullSecrets:
          - name: regcred
    ```
    
    ```yaml
    vagrant@master-node:~$ kubectl apply -f web-deploy-replicas-3.yaml
    deployment.apps/web-deply created
    
    vagrant@master-node:~$ kubectl get deploy,rs,po -o wide
    NAME                        READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES            SELECTOR
    deployment.apps/web-deply   3/3     3            3           49s   nginx        docker.io/nginx   app=web
    
    NAME                                   DESIRED   CURRENT   READY   AGE   CONTAINERS   IMAGES            SELECTOR
    replicaset.apps/web-deply-6dc9946879   3         3         3       49s   nginx        docker.io/nginx   app=web,pod-template-hash=6dc9946879
    
    NAME                             READY   STATUS    RESTARTS   AGE   IP              NODE            NOMINATED NODE   READINESS GATES
    pod/web-deply-6dc9946879-65st9   1/1     Running   0          49s   172.16.158.16   worker-node02   <none>           <none>
    pod/web-deply-6dc9946879-8z2k6   1/1     Running   0          49s   172.16.158.15   worker-node02   <none>           <none>
    pod/web-deply-6dc9946879-pqdms   1/1     Running   0          49s   172.16.87.203   worker-node01   <none>           <none>
    ```
    
    2. 레플리카 값을 5로 변경해서 적용
    
    ```bash
    vagrant@master-node:~$ cp web-deploy-replicas-3.yaml web-deploy-replicas-5.yaml
    ```
    
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: web-deply
    spec:
      replicas: 5
      selector:
        matchLabels:
          app: web
      template:
        metadata: 
          labels:
            app: web
        spec:
          containers:
          - name: nginx
            image: docker.io/nginx
            ports:
            - containerPort: 80
          imagePullSecrets:
          - name: regcred
    ```
    
    ```bash
    vagrant@master-node:~$ kubectl apply -f web-deploy-replicas-5.yaml
    deployment.apps/web-deply configured
    
    vagrant@master-node:~$ kubectl get deploy,rs,po -o wide
    NAME                        READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES            SELECTOR
    deployment.apps/web-deply   5/5     5            5           3m12s   nginx        docker.io/nginx   app=web
    
    NAME                                   DESIRED   CURRENT   READY   AGE     CONTAINERS   IMAGES            SELECTOR
    replicaset.apps/web-deply-6dc9946879   5         5         5       3m12s   nginx        docker.io/nginx   app=web,pod-template-hash=6dc9946879
    
    NAME                             READY   STATUS    RESTARTS   AGE     IP              NODE            NOMINATED NODE   READINESS GATES
    pod/web-deply-6dc9946879-65st9   1/1     Running   0          3m12s   172.16.158.16   worker-node02   <none>           <none>
    **pod/web-deply-6dc9946879-7ff9b   1/1     Running   0          33s     172.16.87.204   worker-node01   <none>           <none>
    pod/web-deply-6dc9946879-8gd52   1/1     Running   0          33s     172.16.158.17   worker-node02   <none>           <none>**
    pod/web-deply-6dc9946879-8z2k6   1/1     Running   0          3m12s   172.16.158.15   worker-node02   <none>           <none>
    pod/web-deply-6dc9946879-pqdms   1/1     Running   0          3m12s   172.16.87.203   worker-node01   <none>           <none>
    ```
    
    3. kubectl scale 명령으로 레플리카 값을 변경
    
    ```bash
    vagrant@master-node:~$ kubectl scale deployments web-deply --replicas=10
    deployment.apps/web-deply scaled
    
    vagrant@master-node:~$ kubectl scale deployments web-deply --replicas=10
    deployment.apps/web-deply scaled
    vagrant@master-node:~$ kubectl get deploy,rs,po -o wide
    
    NAME                        READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES            SELECTOR
    deployment.apps/web-deply   10/10   10           10          5m24s   nginx        docker.io/nginx   app=web
    
    NAME                                   DESIRED   CURRENT   READY   AGE     CONTAINERS   IMAGES            SELECTOR
    replicaset.apps/web-deply-6dc9946879   10        10        10      5m24s   nginx        docker.io/nginx   app=web,pod-template-hash=6dc9946879
    
    NAME                             READY   STATUS    RESTARTS   AGE     IP              NODE            NOMINATED NODE   READINESS GATES
    pod/web-deply-6dc9946879-65st9   1/1     Running   0          5m24s   172.16.158.16   worker-node02   <none>           <none>
    pod/web-deply-6dc9946879-7ff9b   1/1     Running   0          2m45s   172.16.87.204   worker-node01   <none>           <none>
    pod/web-deply-6dc9946879-8gd52   1/1     Running   0          2m45s   172.16.158.17   worker-node02   <none>           <none>
    pod/web-deply-6dc9946879-8z2k6   1/1     Running   0          5m24s   172.16.158.15   worker-node02   <none>           <none>
    **pod/web-deply-6dc9946879-fvd82   1/1     Running   0          13s     172.16.87.206   worker-node01   <none>           <none>
    pod/web-deply-6dc9946879-jsst8   1/1     Running   0          13s     172.16.87.205   worker-node01   <none>           <none>**
    pod/web-deply-6dc9946879-pqdms   1/1     Running   0          5m24s   172.16.87.203   worker-node01   <none>           <none>
    **pod/web-deply-6dc9946879-vgww4   1/1     Running   0          13s     172.16.87.207   worker-node01   <none>           <none>
    pod/web-deply-6dc9946879-vw9v2   1/1     Running   0          13s     172.16.158.18   worker-node02   <none>           <none>
    pod/web-deply-6dc9946879-xg87j   1/1     Running   0          13s     172.16.158.19   worker-node02   <none>           <none>**
    ```
    
2. **디플로이먼트를 사용하는 이유 2) 롤아웃, 롤백**
- 애플리케이션을 업데이터할 때 레플리카셋의 변경 사항을 저장하는 `리비전(revision)을 남겨서 롤백을 가능`하게 해주고, 무중단 서비스를 위해 `파드의 롤링 업데이터 전략을 지정`할 수 있다.
    1. —record옵션을 추가해 디플로이먼트를 생성
    
    ```bash
    vagrant@master-node:~$ kubectl apply -f deployment-nginx.yaml --record
    Flag --record has been deprecated, --record will be removed in the future
    deployment.apps/my-nginx-deployment created
    
    vagrant@master-node:~$ kubectl get deploy,rs,po -o wide
    NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES            SELECTOR
    deployment.apps/my-nginx-deployment   3/3     3            3           32s   nginx        docker.io/nginx   app=my-nginx
    
    NAME                                             DESIRED   CURRENT   READY   AGE   CONTAINERS   IMAGES            SELECTOR
    replicaset.apps/my-nginx-deployment-66bcdb4565   3         3         3       32s   nginx        docker.io/nginx   app=my-nginx,pod-template-hash=66bcdb4565
    
    NAME                                       READY   STATUS    RESTARTS   AGE   IP              NODE            NOMINATED NODE   READINESS GATES
    pod/my-nginx-deployment-66bcdb4565-jlk26   1/1     Running   0          32s   172.16.87.208   worker-node01   <none>           <none>
    pod/my-nginx-deployment-66bcdb4565-kqgvs   1/1     Running   0          32s   172.16.158.20   worker-node02   <none>           <none>
    pod/my-nginx-deployment-66bcdb4565-sjpc7   1/1     Running   0          32s   172.16.158.21   worker-node02   <none>           <none>
    ```
    
    2. **kubectl set image 명령으로 파드의 이미지를 변경**
    
    ```bash
    vagrant@master-node:~$ kubectl set image deployments my-nginx-deployment nginx=nginx:1.11 --record
    Flag --record has been deprecated, --record will be removed in the future
    deployment.apps/my-nginx-deployment image updated
    
    vagrant@master-node:~$ kubectl get deploy,rs,po -o wide
    NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES       SELECTOR
    deployment.apps/my-nginx-deployment   3/3     3            3           3m19s   nginx        nginx:1.11   app=my-nginx
    
    NAME                                             DESIRED   CURRENT   READY   AGE     CONTAINERS   IMAGES            SELECTOR
    replicaset.apps/my-nginx-deployment-57488f8967   3         3         3       77s     nginx        nginx:1.11        app=my-nginx,pod-template-hash=57488f8967
    replicaset.apps/my-nginx-deployment-66bcdb4565   0         0         0       3m19s   nginx        docker.io/nginx   app=my-nginx,pod-template-hash=66bcdb4565
    
    NAME                                       READY   STATUS    RESTARTS   AGE   IP              NODE            NOMINATED NODE   READINESS GATES
    pod/my-nginx-deployment-57488f8967-46b6v   1/1     Running   0          13s   172.16.158.23   worker-node02   <none>           <none>
    pod/my-nginx-deployment-57488f8967-gkkhd   1/1     Running   0          47s   172.16.158.22   worker-node02   <none>           <none>
    pod/my-nginx-deployment-57488f8967-kjqsf   1/1     Running   0          76s   172.16.87.209   worker-node01   <none>           <none>
    ```
    
  3. 리비전 정보 확인
  
  —recode=true옵션으로 디플로이먼트를 변경하려면 변경 사항을 기록하여 해당 버전의 레플리카셋을 보존할 수 있음
  
  ```bash
  vagrant@master-node:~$ kubectl rollout history deployment my-nginx-deployment
  deployment.apps/my-nginx-deployment
  REVISION  CHANGE-CAUSE
  1         kubectl apply --filename=deployment-nginx.yaml --record=true
  2         kubectl set image deployments my-nginx-deployment nginx=nginx:1.11 --record=true
  ```

  4. 이전 버전의 레플리카셋으로 롤백
  
  ```bash
  vagrant@master-node:~$ kubectl rollout undo deployment my-nginx-deployment --to-revision=1
  deployment.apps/my-nginx-deployment rolled back
  
  vagrant@master-node:~$ kubectl get rs,pod
  NAME                                             DESIRED   CURRENT   READY   AGE
  **replicaset.apps/my-nginx-deployment-57488f8967   0         0         0       3d17h  // 두번재 생성한 레플리카셋
  replicaset.apps/my-nginx-deployment-66bcdb4565   3         3         3       3d17h  // 처음 생성한 레플리카셋 <- --to-revision=1로 처음 만든 레플리카셋 사용한다해서 바뀌고 있는 것을 확인할 수 있음**
  
  NAME                                       READY   STATUS    RESTARTS   AGE
  pod/my-nginx-deployment-66bcdb4565-fsbd7   1/1     Running   0          38s
  pod/my-nginx-deployment-66bcdb4565-q7ktw   1/1     Running   0          30s
  pod/my-nginx-deployment-66bcdb4565-wxz4v   1/1     Running   0          34s
  
  vagrant@master-node:~$ kubectl rollout history deployment my-nginx-deployment
  deployment.apps/my-nginx-deployment
  REVISION  CHANGE-CAUSE
  2         kubectl set image deployments my-nginx-deployment nginx=nginx:1.11 --record=true
  3         kubectl apply --filename=deployment-nginx.yaml --record=true **// --to-revision으로 버전을 바꾸면 그 버전으로 바뀌는 것이 아니라 해당 버전을 복사해서 새로운 버전을 만든다.**
  ```

  5. 디플로이먼트 상세 정보 출력
  
  ```bash
  vagrant@master-node:~$ kubectl describe deployment my-nginx-deployment
  Name:                   my-nginx-deployment
  Namespace:              default
  CreationTimestamp:      Fri, 06 Oct 2023 06:43:45 +0000
  Labels:                 <none>
  **Annotations:            deployment.kubernetes.io/revision: 3**
                          kubernetes.io/change-cause: kubectl apply --filename=deployment-nginx.yaml --record=true
  Selector:               app=my-nginx
  Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
  StrategyType:           RollingUpdate
  MinReadySeconds:        0
  RollingUpdateStrategy:  25% max unavailable, 25% max surge
  Pod Template:
    Labels:  app=my-nginx
    Containers:
     nginx:
      Image:        docker.io/nginx
      Port:         80/TCP
      Host Port:    0/TCP
      Environment:  <none>
      Mounts:       <none>
    Volumes:        <none>
  Conditions:
    Type           Status  Reason
    ----           ------  ------
    Available      True    MinimumReplicasAvailable
    Progressing    True    NewReplicaSetAvailable
  OldReplicaSets:  my-nginx-deployment-57488f8967 (0/0 replicas created)
  **NewReplicaSet:   my-nginx-deployment-66bcdb4565 (3/3 replicas created)
  Events:**
    Type    Reason             Age    From                   Message
    ----    ------             ----   ----                   -------
    Normal  ScalingReplicaSet  3d17h  deployment-controller  Scaled up replica set my-nginx-deployment-66bcdb4565 to 3
    Normal  ScalingReplicaSet  3d17h  deployment-controller  Scaled up replica set my-nginx-deployment-57488f8967 to 1
    Normal  ScalingReplicaSet  3d17h  deployment-controller  Scaled down replica set my-nginx-deployment-66bcdb4565 to 2 from 3
    Normal  ScalingReplicaSet  3d17h  deployment-controller  Scaled up replica set my-nginx-deployment-57488f8967 to 2 from 1
    Normal  ScalingReplicaSet  3d17h  deployment-controller  Scaled down replica set my-nginx-deployment-66bcdb4565 to 1 from 2
    Normal  ScalingReplicaSet  3d17h  deployment-controller  Scaled up replica set my-nginx-deployment-57488f8967 to 3 from 2
    Normal  ScalingReplicaSet  3d17h  deployment-controller  Scaled down replica set my-nginx-deployment-66bcdb4565 to 0 from 1
    Normal  ScalingReplicaSet  6m16s  deployment-controller  Scaled up replica set my-nginx-deployment-66bcdb4565 to 1 from 0
    Normal  ScalingReplicaSet  6m12s  deployment-controller  Scaled down replica set my-nginx-deployment-57488f8967 to 2 from 3
    Normal  ScalingReplicaSet  6m12s  deployment-controller  Scaled up replica set my-nginx-deployment-66bcdb4565 to 2 from 1
    Normal  ScalingReplicaSet  6m8s   deployment-controller  Scaled down replica set my-nginx-deployment-57488f8967 to 1 from 2
    Normal  ScalingReplicaSet  6m8s   deployment-controller  Scaled up replica set my-nginx-deployment-66bcdb4565 to 3 from 2
    Normal  ScalingReplicaSet  6m4s   deployment-controller  Scaled down replica set my-nginx-deployment-57488f8967 to 0 from 1
  ```

  6. 스케일 변경 및 롤백
  
  ```bash
  vagrant@master-node:~$ kubectl scale --replicas=10 deployment my-nginx-deployment --record=tr
  ue
  Flag --record has been deprecated, --record will be removed in the future
  deployment.apps/my-nginx-deployment scaled
  
  vagrant@master-node:~$ kubectl get all
  NAME                                       READY   STATUS              RESTARTS   AGE
  pod/my-nginx-deployment-66bcdb4565-5phrk   1/1     Running             0          12s
  pod/my-nginx-deployment-66bcdb4565-8vkfs   1/1     Running             0          12s
  pod/my-nginx-deployment-66bcdb4565-fsbd7   1/1     Running             0          7m51s
  pod/my-nginx-deployment-66bcdb4565-gpgdk   1/1     Running             0          12s
  pod/my-nginx-deployment-66bcdb4565-lwjmn   1/1     Running             0          12s
  pod/my-nginx-deployment-66bcdb4565-q7ktw   1/1     Running             0          7m43s
  pod/my-nginx-deployment-66bcdb4565-q9fz4   1/1     Running             0          12s
  pod/my-nginx-deployment-66bcdb4565-sk9hx   1/1     Running             0          12s
  pod/my-nginx-deployment-66bcdb4565-tzrjf   1/1     Running             0          12s
  pod/my-nginx-deployment-66bcdb4565-wxz4v   1/1     Running             0          7m47s
  
  NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
  service/kubernetes   ClusterIP   172.17.0.1   <none>        443/TCP   4d
  
  NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE
  deployment.apps/my-nginx-deployment   **10/10**    10           10           3d17h
  
  NAME                                             DESIRED   CURRENT   READY   AGE
  replicaset.apps/my-nginx-deployment-57488f8967   0         0         0       3d17h
  replicaset.apps/my-nginx-deployment-66bcdb4565   **10        10        10**       3d17h   **// 스케일을 변경해도 레플리카셋은 그대로 유지**
  ```

  7. 모든 리소스 삭제(다음 실습을 위해)
  
  ```bash
  vagrant@master-node:~$ kubectl delete deployment,replicaset,pod --all
  deployment.apps "my-nginx-deployment" deleted
  replicaset.apps "my-nginx-deployment-57488f8967" deleted
  pod "my-nginx-deployment-66bcdb4565-5phrk" deleted
  pod "my-nginx-deployment-66bcdb4565-8vkfs" deleted
  pod "my-nginx-deployment-66bcdb4565-fsbd7" deleted
  pod "my-nginx-deployment-66bcdb4565-gpgdk" deleted
  pod "my-nginx-deployment-66bcdb4565-lwjmn" deleted
  pod "my-nginx-deployment-66bcdb4565-q7ktw" deleted
  pod "my-nginx-deployment-66bcdb4565-q9fz4" deleted
  pod "my-nginx-deployment-66bcdb4565-sk9hx" deleted
  pod "my-nginx-deployment-66bcdb4565-tzrjf" deleted
  pod "my-nginx-deployment-66bcdb4565-wxz4v" deleted
  ```

**디플로이먼트를 사용하는 이유3) 자동 복구**

- 파드 내 컨테이너가 종료되는 경우, 파드가 컨테이너 수준의 장애에 대해 자동 복구를 시도하고, 디플로이먼트는 파드 단위로 복구를 시도

  1. 30초 단위로 재기동하는 파드를 정의
  
  restart-pod.yaml
  
  ```yaml
  apiVersion: v1
  kin: Pod
  metadata:
    name: test1
  spec:
    containers:
    - name: busybox
      image: docker.io/busybox:1
      command: ["sh", "-c", "sleep 30; exit 0"]
    restartPolicy: Always
    imagePullSecrets:
    - name: regcred
  ```

  2. 동일 사양의 파드를 4개 기동하는 디플로이먼트를 정의
  
  restart-deployment.yaml
  
  ```yaml
  apiVersion: apps/v1
  kin: Deployment
  metadata:
    name: test2
  spec:
    replicas: 4
    selector:
      matchLabels:
        app: test2
    template:
      metadata:
        lables:
          app: test2
      spec:
        containers:
        - name: busybox
          image: docker.io/busybox:1
          command: ["sh", "-c", "sleep 30; exit 0"]
        imagePullSecrets:
        - name: regcred
  ```

  3. 파드와 디플로이먼트를 각각 배포
  
  ```bash
  vagrant@master-node:~$ kubectl apply -f restart-pod.yaml
  pod/test1 created
  
  vagrant@master-node:~$ kubectl apply -f restart-deployment.yaml
  deployment.apps/test2 created
  ```
  4. 노드 및 파드 동작을 확인
  ```bash
  vagrant@master-node:~$ kubectl get node,pod -o wide
  NAME                 STATUS   ROLES           AGE    VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
  node/master-node     Ready    control-plane   4d1h   v1.27.1   10.0.0.10     <none>        Ubuntu 22.04.3 LTS   5.15.0-83-generic   cri-o://1.27.1
  node/worker-node01   Ready    worker          4d1h   v1.27.1   10.0.0.11     <none>        Ubuntu 22.04.3 LTS   5.15.0-83-generic   cri-o://1.27.1
  node/worker-node02   Ready    worker          4d     v1.27.1   10.0.0.12     <none>        Ubuntu 22.04.3 LTS   5.15.0-83-generic   cri-o://1.27.1
  
  NAME                        READY   STATUS    RESTARTS      AGE     IP              NODE            NOMINATED NODE   READINESS GATES
  **pod/test1                   1/1     Running   3 (41s ago)   2m32s   172.16.158.31   worker-node02   <none>           <none>**
  pod/test2-958d4f5c4-4qdqh   1/1     Running   1 (3s ago)    43s     172.16.87.217   worker-node01   <none>           <none>
  pod/test2-958d4f5c4-bk8tn   1/1     Running   1 (5s ago)    43s     172.16.87.216   worker-node01   <none>           <none>
  pod/test2-958d4f5c4-c2k8h   1/1     Running   1 (11s ago)   43s     172.16.158.32   worker-node02   <none>           <none>
  pod/test2-958d4f5c4-rhf7n   1/1     Running   1 (10s ago)   43s     172.16.158.33   worker-node02   <none>           <none>
  ```

  5. 단독으로 기동한 test1 파드가 배포된 노드를 정지 (Running 상태에서)
  
  ```bash
  C:\Users\User>cd /
  
  C:\>cd kubernetes
  
  C:\kubernetes>cd vagrant-kubeadm-kubernetes
  
  C:\kubernetes\vagrant-kubeadm-kubernetes>vagrant halt node02
  ==> node02: Attempting graceful shutdown of VM...
  
  C:\kubernetes\vagrant-kubeadm-kubernetes>
  ```
  6. 노드 및 파드 동작을 확인
  ```bash
  vagrant@master-node:~$ kubectl get node
  NAME            STATUS     ROLES           AGE    VERSION
  master-node     Ready      control-plane   4d1h   v1.27.1
  worker-node01   Ready      worker          4d1h   v1.27.1
  worker-node02   **NotReady**   worker          4d1h   v1.27.1
  
  vagrant@master-node:~$ kubectl get pod -o wide
  NAME                    READY   STATUS             RESTARTS        AGE     IP              NODE            NOMINATED NODE   READINESS GATES
  test1                   0/1     Completed          5 (3m14s ago)   7m25s   172.16.158.31   worker-node02   <none>           <none>
  test2-958d4f5c4-4qdqh   0/1     CrashLoopBackOff   4 (80s ago)     5m36s   172.16.87.217   worker-node01   <none>           <none>
  test2-958d4f5c4-bk8tn   1/1     Running            5 (86s ago)     5m36s   172.16.87.216   worker-node01   <none>           <none>
  test2-958d4f5c4-c2k8h   0/1     CrashLoopBackOff   4 (87s ago)     5m36s   172.16.158.32   worker-node02   <none>           <none>
  test2-958d4f5c4-rhf7n   0/1     CrashLoopBackOff   4 (98s ago)     5m36s   172.16.158.33   worker-node02   <none>           <none>
  ```
  
  - 노드 종료 후 6분 정도 경과하면 디플로이먼트로 배포한 test2는 활성화 노드에 대체 파드를 생성하는 반면, 단독으로 기동한 test1은 원래 노드에 위치하는 것을 확인할 수 있음
  - 변경사항 확인 ⇒ kubectl get pod -o wide --watch

  ```bash
  vagrant@master-node:~$ kubectl get pod -o wide
  NAME                    READY   STATUS             RESTARTS        AGE   IP              NODE            NOMINATED NODE   READINESS GATES
  test1                   0/1     Terminating        5 (22m ago)     26m   172.16.158.31   worker-node02   <none>           <none>
  test2-958d4f5c4-4qdqh   0/1     CrashLoopBackOff   8 (3m36s ago)   24m   172.16.87.217   worker-node01   <none>           <none>
  test2-958d4f5c4-6f5sg   1/1     Running            7 (5m14s ago)   14m   172.16.87.218   worker-node01   <none>           <none>
  test2-958d4f5c4-bk8tn   0/1     CrashLoopBackOff   8 (3m46s ago)   24m   172.16.87.216   worker-node01   <none>           <none>
  test2-958d4f5c4-c2k8h   0/1     Terminating        4 (20m ago)     24m   172.16.158.32   worker-node02   <none>           <none>
  test2-958d4f5c4-rhf7n   0/1     Terminating        4 (20m ago)     24m   172.16.158.33   worker-node02   <none>           <none>
  test2-958d4f5c4-t7bsx   1/1     Running            7 (5m27s ago)   14m   172.16.87.219   worker-node01   <none>           <none>
  ```

  7. 노드 재가동 후 노드 및 파드 동작 확인
  
  ```bash
  C:\kubernetes\vagrant-kubeadm-kubernetes>vagrant up node02
  ```
  
  ⇒ 중지되었던 노드가 복원되면, Terminating 상태였던 파드가 모두 제거되는 것을 확인 ⇒ 노드와의 통신이 회복되어 상태가 불분명했던 파드의 상태가 확인되어 삭제되는 것으로 단독으로 기동한 파드는 완전히 소멸됨
  
  일시적인 장애로 자동 복구가 발동되었을 때 더 불안한 상태로 빠지는 것을 막기 위해서 디플로이먼트는 천천히 복구를 할 수 있도록 만들어져 있다.
  
  ```bash
  vagrant@master-node:~$ kubectl get node -o wide
  NAME            STATUS   ROLES           AGE    VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
  master-node     Ready    control-plane   4d1h   v1.27.1   10.0.0.10     <none>        Ubuntu 22.04.3 LTS   5.15.0-83-generic   cri-o://1.27.1
  worker-node01   Ready    worker          4d1h   v1.27.1   10.0.0.11     <none>        Ubuntu 22.04.3 LTS   5.15.0-83-generic   cri-o://1.27.1
  worker-node02   Ready    worker          4d1h   v1.27.1   10.0.0.12     <none>        Ubuntu 22.04.3 LTS   5.15.0-83-generic   cri-o://1.27.1
  
  vagrant@master-node:~$ kubectl get pod -o wide
  NAME                    READY   STATUS             RESTARTS         AGE   IP              NODE            NOMINATED NODE   READINESS GATES
  test2-958d4f5c4-4qdqh   0/1     Completed          10 (5m40s ago)   32m   172.16.87.217   worker-node01   <none>           <none>
  test2-958d4f5c4-6f5sg   0/1     CrashLoopBackOff   8 (97s ago)      22m   172.16.87.218   worker-node01   <none>           <none>
  test2-958d4f5c4-bk8tn   0/1     CrashLoopBackOff   10 (16s ago)     32m   172.16.87.216   worker-node01   <none>           <none>
  test2-958d4f5c4-t7bsx   0/1     CrashLoopBackOff   8 (114s ago)     22m   172.16.87.219   worker-node01   <none>           <none>
  ```

  8. 모든 리소스 삭제
  
  ```bash
  kubectl delete deployment,replicaset,pod --all --force
  
  vagrant@master-node:~$ kubectl get all
  NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
  service/kubernetes   ClusterIP   172.17.0.1   <none>        443/TCP   4d1h
  ```

## 디플로이먼트 배포 전략
<details>
  <summary> [참고자료](https://dev.classmethod.jp/articles/ci-cd-deployment-strategies-kr/) </summary>
  <div markdown="1">
    
  **인플레이스 배포(In-place Deployment)**
  - 버전 차이가 나면 안되는 서비스 -> 금융권
    
  **롤링 배포(Rolling Update Deployment)**
  
  - 하나씩 버전 update를 하는 것
  - 접속한 사용자에 따라서 어떤 사용자는 이전 버전을, 어떤 사용자는 새로운 버전을 사용할 수 있다.
  
  ![image](https://github.com/Suah-Cho/STUDY/assets/102336763/8fb7261e-1b69-44d1-abe6-1165dd8fc919)

  **블루/그린 배포(Blue/Green Deployment)**
  
  - 현재 blue서비스만 사용하고 있을 때 blue에 버전1, green에 버전2가 돌고 있으면 로드 밸런서를 이용하여 green 서비스로 바꿀 수 있다.
  - 서비스 중단 없이 빠르게 새 시스템으로 옮길 수 있다.
  - 똑같은 서비스를 두개 가지고 있어야하기 때문에, 리소스를 많이 잡아먹는 단점이 있다.
  
  **카나리(Canary Delpoyment)**
  
  - 전체 시스템의 일부를 새로운 시스템으로 보내본 후, 별다른 문제가 없으면 request를 점점 늘려가 결과적으로 예전 시스템을 버리고 새로운 시스템으로 옮기는 것
  </div>
</details>
    
### Recreate(재생성)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample-deployment-recreate
spec:
  strategy:
    type: Recreate
  replicas: 3
  selector:
    matchLabels:
      app: sample-app
  template:
    metadata:
      labels:
        app: sample-app
    spec:
      containers:
      - name: nginx-container
        image: docker.io/nginx:1.16
      imagePullSecrets:
      - name: regcred
```

![image](https://github.com/Suah-Cho/STUDY/assets/102336763/4e65950f-1d1d-4488-b25c-d16836a611b3)


```bash
vagrant@master-node:~$ kubectl apply -f sample-deployment-recreate.yaml
deployment.apps/sample-deployment-recreate created

vagrant@master-node:~$ kubectl get replicaset,pod
NAME                                                   DESIRED   CURRENT   READY   AGE
replicaset.apps/sample-deployment-recreate-9ff76c956   3         3         3       35s

NAME                                             READY   STATUS    RESTARTS   AGE
pod/sample-deployment-recreate-9ff76c956-625v4   1/1     Running   0          35s
pod/sample-deployment-recreate-9ff76c956-gzms6   1/1     Running   0          35s
pod/sample-deployment-recreate-9ff76c956-xvxh6   1/1     Running   0          35s

vagrant@master-node:~$ kubectl get replicaset --watch
NAME                                   DESIRED   CURRENT   READY   AGE
sample-deployment-recreate-9ff76c956   3         3         3       89s

// 다른 cmd창에서
vagrant@master-node:~$ kubectl set image deployment sample-deployment-recreate nginx-container=nginx:1.17
deployment.apps/sample-deployment-recreate image updated

vagrant@master-node:~$ kubectl get replicaset --watch
NAME                                   DESIRED   CURRENT   READY   AGE
sample-deployment-recreate-9ff76c956   3         3         3       89s
sample-deployment-recreate-9ff76c956   0         3         3       3m6s
sample-deployment-recreate-9ff76c956   0         3         3       3m6s
sample-deployment-recreate-9ff76c956   0         0         0       3m6s  **// 첫번째 RS종료**
sample-deployment-recreate-77dc8d9fb   3         0         0       0s    **// 새로운 RS생성**
sample-deployment-recreate-77dc8d9fb   3         0         0       0s
sample-deployment-recreate-77dc8d9fb   3         3         0       1s    **// 첫번재 RS종료 시점부터 이 때까지 일시적으로 서비스가 중지된다.**
sample-deployment-recreate-77dc8d9fb   3         3         1       20s
sample-deployment-recreate-77dc8d9fb   3         3         2       21s
sample-deployment-recreate-77dc8d9fb   3         3         3       23s   **// 새로운 RS을 서비스**
```

### RollingUpdate

sample-deployment-rollingupdate.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample-deployment-rollingupdate
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0  **//업데이트 중 동시에 정지 가능한 최대 파드 수**
      maxSurge: 1        **//업데이트 중 동시에 생성할 수 있는 최대 파드 수**
  replicas: 3              maxUnavailable과 maxSurge를 모두 0으로 설정할 수는 없
  selector:
    matchLabels:
      app: sample-app
  template:
    metadata:
      labels:
        app: sample-app
    spec:
      containers:
      - name: nginx-container
        image: docker.io/nginx:1.16
      imagePullSecrets:
      - name: regcred
```

```bash
vagrant@master-node:~$ kubectl apply -f sample-deployment-rollingupdate.yaml
deployment.apps/sample-deployment-rollingupdate created

vagrant@master-node:~$ kubectl get rs,pod
NAME                                                        DESIRED   CURRENT   READY   AGE
replicaset.apps/sample-deployment-rollingupdate-9ff76c956   3         3         3       27s

NAME                                                  READY   STATUS    RESTARTS   AGE
pod/sample-deployment-rollingupdate-9ff76c956-9cxpm   1/1     Running   0          27s
pod/sample-deployment-rollingupdate-9ff76c956-b44r8   1/1     Running   0          27s
pod/sample-deployment-rollingupdate-9ff76c956-cf5q7   1/1     Running   0          27s

vagrant@master-node:~$ kubectl get replicaset --watch
NAME                                        DESIRED   CURRENT   READY   AGE
sample-deployment-rollingupdate-9ff76c956   3         3         3       44s

// 다른 cmd창에서
vagrant@master-node:~$ kubectl set image deployment sample-deployment-rollingupdate nginx-container=nginx:1.17
deployment.apps/sample-deployment-rollingupdate image updated

vagrant@master-node:~$ kubectl get replicaset --watch
NAME                                        DESIRED   CURRENT   READY   AGE
sample-deployment-rollingupdate-9ff76c956   3         3         3       44s
sample-deployment-rollingupdate-77dc8d9fb   1         0         0       0s
sample-deployment-rollingupdate-77dc8d9fb   1         0         0       0s
sample-deployment-rollingupdate-77dc8d9fb   1         1         0       0s
sample-deployment-rollingupdate-77dc8d9fb   1         1         1       2s
sample-deployment-rollingupdate-9ff76c956   2         3         3       89s
sample-deployment-rollingupdate-77dc8d9fb   2         1         1       2s
sample-deployment-rollingupdate-9ff76c956   2         3         3       89s
sample-deployment-rollingupdate-77dc8d9fb   2         1         1       2s
sample-deployment-rollingupdate-9ff76c956   2         2         2       89s
sample-deployment-rollingupdate-77dc8d9fb   2         2         1       2s
sample-deployment-rollingupdate-77dc8d9fb   2         2         2       3s
sample-deployment-rollingupdate-9ff76c956   1         2         2       90s
sample-deployment-rollingupdate-77dc8d9fb   3         2         2       4s
sample-deployment-rollingupdate-9ff76c956   1         2         2       91s
sample-deployment-rollingupdate-77dc8d9fb   3         2         2       4s
sample-deployment-rollingupdate-9ff76c956   1         1         1       91s
sample-deployment-rollingupdate-77dc8d9fb   3         3         2       4s
sample-deployment-rollingupdate-77dc8d9fb   3         3         3       5s
sample-deployment-rollingupdate-9ff76c956   0         1         1       92s
sample-deployment-rollingupdate-9ff76c956   0         1         1       92s
sample-deployment-rollingupdate-9ff76c956   0         0         0       92s
```

- **LAB maxUnavailable=1, maxSurge=0**
    
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: sample-deployment-rollingupdate
    spec:
      strategy:
        type: RollingUpdate
        rollingUpdate:
          maxUnavailable: 1
          maxSurge: 0
      replicas: 3
      selector:
        matchLabels:
          app: sample-app
      template:
        metadata:
          labels:
            app: sample-app
        spec:
          containers:
          - name: nginx-container
            image: docker.io/nginx:1.16
          imagePullSecrets:
          - name: regcred
    ```
    
    ```bash
    vagrant@master-node:~$ kubectl apply -f sample-deployment-rollingupdate.yaml
    deployment.apps/sample-deployment-rollingupdate created
    
    //다른 cmd창에서
    vagrant@master-node:~$ kubectl set image deployment sample-deployment-rollingupdate nginx-container=nginx:1.17
    deployment.apps/sample-deployment-rollingupdate image updated
    
    vagrant@master-node:~$ kubectl get replicaset --watch
    NAME                                        DESIRED   CURRENT   READY   AGE
    sample-deployment-rollingupdate-9ff76c956   3         3         3       11s
    sample-deployment-rollingupdate-77dc8d9fb   0         0         0       0s
    sample-deployment-rollingupdate-77dc8d9fb   0         0         0       0s
    sample-deployment-rollingupdate-9ff76c956   2         3         3       17s
    sample-deployment-rollingupdate-77dc8d9fb   1         0         0       0s
    sample-deployment-rollingupdate-9ff76c956   2         3         3       17s
    sample-deployment-rollingupdate-77dc8d9fb   1         0         0       0s
    sample-deployment-rollingupdate-9ff76c956   2         2         2       17s
    sample-deployment-rollingupdate-77dc8d9fb   1         1         0       0s
    sample-deployment-rollingupdate-77dc8d9fb   1         1         1       2s
    sample-deployment-rollingupdate-9ff76c956   1         2         2       19s
    sample-deployment-rollingupdate-9ff76c956   1         2         2       19s
    sample-deployment-rollingupdate-77dc8d9fb   2         1         1       2s
    sample-deployment-rollingupdate-77dc8d9fb   2         1         1       2s
    sample-deployment-rollingupdate-9ff76c956   1         1         1       19s
    sample-deployment-rollingupdate-77dc8d9fb   2         2         1       2s
    sample-deployment-rollingupdate-77dc8d9fb   2         2         2       4s
    sample-deployment-rollingupdate-9ff76c956   0         1         1       21s
    sample-deployment-rollingupdate-77dc8d9fb   3         2         2       4s
    sample-deployment-rollingupdate-9ff76c956   0         1         1       21s
    sample-deployment-rollingupdate-9ff76c956   0         0         0       21s
    sample-deployment-rollingupdate-77dc8d9fb   3         2         2       4s
    sample-deployment-rollingupdate-77dc8d9fb   3         3         2       4s
    sample-deployment-rollingupdate-77dc8d9fb   3         3         3       6s
    ```
    
    ![image](https://github.com/Suah-Cho/STUDY/assets/102336763/00cd6cc3-e3ea-4ff2-ab22-cb6d1f638544)

    ### Blue/Green 업데이트 실습
    
    **디플로이먼트 전략에서 제공하는 것이 아니고 service를 이용해서 구현**
    
    **1. BLUE 디플로이먼트를 생성**
    
    sample-deployment.yaml
    
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: sample-deployment-blue
    spec:
      selector:
        matchLabels:
          app: blue-green-deployment
          version: v1.16
      replicas: 3
      template:
        metadata:
          labels:
            app: blue-green-deployment
            version: v1.16
        spec:
          containers:
          - name: mywebserver
            image: docker.io/alicek106/rr-test:echo-hostname
          imagePullSecrets:
          - name: regcred
    ```
    
    ```bash
    vagrant@master-node:~$ kubectl apply -f sample-deployment.yaml
    deployment.apps/sample-deployment-blue created
    vagrant@master-node:~$ kubectl get pod --show-labels
    NAME                                      READY   STATUS    RESTARTS   AGE   LABELS
    sample-deployment-blue-58bc49f974-dv2s7   1/1     Running   0          17s   app=blue-green-deployment,pod-template-hash=58bc49f974,version=v1.16
    sample-deployment-blue-58bc49f974-x9tbv   1/1     Running   0          17s   app=blue-green-deployment,pod-template-hash=58bc49f974,version=v1.16
    sample-deployment-blue-58bc49f974-zst78   1/1     Running   0          17s   app=blue-green-deployment,pod-template-hash=58bc49f974,version=v1.16
    ```
    
    **2. 서비스 생성**
    
    sample-service-nodeport.yaml
    
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: blue-green-service
    spec:
      type: NodePort
      ports:
      - name: http
        port: 8080
        targetPort: 80
      selector:
        app: blue-green-deployment
        version: v1.16
    ```
    
    ```bash
    vagrant@master-node:~$ kubectl apply -f sample-service-nodeport.yaml
    service/blue-green-service created
    vagrant@master-node:~$ kubectl get service
    NAME                 TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)          AGE
    blue-green-service   NodePort    172.17.3.75   <none>        8080:30168/TCP   6s
    kubernetes           ClusterIP   172.17.0.1    <none>        443/TCP          6d1h
    ```
    
    **노드 포트로 서비스 동작을 확인**
    
    마스터 노드에서 접근
    
    ```bash
    vagrant@master-node:~$ wget -q -O - http://10.0.0.10:30168 | grep Hello
            <p>Hello,  sample-deployment-blue-58bc49f974-x9tbv</p>  </blockquote>
    vagrant@master-node:~$ wget -q -O - http://10.0.0.10:30168 | grep Hello
            <p>Hello,  sample-deployment-blue-58bc49f974-zst78</p>  </blockquote>
    vagrant@master-node:~$ wget -q -O - http://10.0.0.10:30168 | grep Hello
            <p>Hello,  sample-deployment-blue-58bc49f974-dv2s7</p>  </blockquote>
    ```
    
    클러스터 외부(내 pc)에서 접근
    
    ![image](https://github.com/Suah-Cho/STUDY/assets/102336763/d3052625-e47e-4687-b15d-ed5a99e79841)

    
    ![image](https://github.com/Suah-Cho/STUDY/assets/102336763/80b7237b-a834-48be-93fa-b89df5a30a1b)

    
    cf) CLUSTER-IP와 PORT로 접근
    
    ```bash
    vagrant@master-node:~$ wget -q -O - http://172.17.3.75:8080 | grep Hello
            <p>Hello,  sample-deployment-blue-58bc49f974-zst78</p>  </blockquote>
    ```
    
    **4. GREEN 디플로이먼트를 생성**
    
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: sample-deployment-green
    spec:
      selector:
        matchLabels:
          app: blue-green-deployment
          version: v1.17
      replicas: 3
      template:
        metadata:
          labels:
            app: blue-green-deployment
            version: v1.17
        spec:
          containers:
          - name: mywebserver
            image: docker.io/alicek106/rr-test:echo-hostname
          imagePullSecrets:
          - name: regcred
    ```
    
    ```bash
    vagrant@master-node:~$ kubectl apply -f sample-deployment-green.yaml
    deployment.apps/sample-deployment-green created
    
    vagrant@master-node:~$ kubectl get pod
    NAME                                       READY   STATUS    RESTARTS   AGE
    sample-deployment-blue-58bc49f974-dv2s7    1/1     Running   0          13m
    sample-deployment-blue-58bc49f974-x9tbv    1/1     Running   0          13m
    sample-deployment-blue-58bc49f974-zst78    1/1     Running   0          13m
    sample-deployment-green-5c7657d76f-g8w5w   1/1     Running   0          5s
    sample-deployment-green-5c7657d76f-lbvwm   1/1     Running   0          5s
    sample-deployment-green-5c7657d76f-trj9d   1/1     Running   0          5s
    
    vagrant@master-node:~$ kubectl get pod -o wide
    NAME                                       READY   STATUS    RESTARTS   AGE   IP              NODE            NOMINATED NODE   READINESS GATES
    sample-deployment-blue-58bc49f974-dv2s7    1/1     Running   0          15m   172.16.87.216   worker-node01   <none>           <none>
    sample-deployment-blue-58bc49f974-x9tbv    1/1     Running   0          15m   172.16.87.217   worker-node01   <none>           <none>
    sample-deployment-blue-58bc49f974-zst78    1/1     Running   0          15m   172.16.158.49   worker-node02   <none>           <none>
    sample-deployment-green-5c7657d76f-g8w5w   1/1     Running   0          96s   172.16.87.218   worker-node01   <none>           <none>
    sample-deployment-green-5c7657d76f-lbvwm   1/1     Running   0          96s   172.16.158.53   worker-node02   <none>           <none>
    sample-deployment-green-5c7657d76f-trj9d   1/1     Running   0          96s   172.16.158.52   worker-node02   <none>           <none>
    ```
    
    두 가지 버전의 애플리케이션이 함께 실행되고 있으며, BLUE버전은 NodePort 서비스를 통해서 외부에 노출되어 있고, GREEN버전은 내부에서만 접근이 가능
    
    **5. BLUE버전에서 GREEN버전으로 서비스 대상을 변경**
    
    sample-service-nodeport.yaml 수정
    
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: blue-green-service
    spec:
      type: NodePort
      ports:
      - name: http
        port: 8080
        targetPort: 80
      selector:
        app: blue-green-deployment
        version: v1.17
    ```
    
    ```bash
    vagrant@master-node:~$ kubectl apply -f sample-service-nodeport.yaml
    service/blue-green-service configured
    ```
    
    ```yaml
    vagrant@master-node:~$ kubectl get service
    NAME                 TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)          AGE
    blue-green-service   NodePort    172.17.3.75   <none>        8080:**30168**/TCP   16m  // 서비스의 공개 포트가 그대로 유지
    kubernetes           ClusterIP   172.17.0.1    <none>        443/TCP          6d1h
    ```
    
    **노드 IP와 PORT로 서비스를 확인 ⇒ GREEN 버전의 애플리케이션이 응답하는 것을 확인**
    
    ```bash
    vagrant@master-node:~$ wget -q -O - http://10.0.0.10:30168 | grep Hello
            <p>Hello,  sample-deployment-green-5c7657d76f-g8w5w</p> </blockquote>
    ```
    
    ![image](https://github.com/Suah-Cho/STUDY/assets/102336763/8dfdbd01-32ad-4e5f-a9f4-5b89f43feee3)

    
    ⇒ 클라이언트는 똑같은 방식으로 접근했는데, 백에서 돌고있는 파드가 변경되어 다른 파드가 노출된다.
    
    ## Canary 업데이트
    
    BLUE/GREEN 업데이트처럼 디플로이먼트 전략에서 제공하는 것이 아니라 Ingress를 이용해 구현
    
    **1. MetalLB 설치**
    
    ```bash
    vagrant@master-node:~$ kubectl get configmap kube-proxy -n kube-system -o yaml | \
    >     sed -e "s/strictARP: false/strictARP: true/" | \
    >     kubectl apply -f - -n kube-system
    configmap/kube-proxy configured
    
    kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.11/config/manifests/metallb-native.yaml
    
    vagrant@master-node:~$ kubectl apply -f routing-config.yaml -n metallb-system
    ipaddresspool.metallb.io/first-pool created
    l2advertisement.metallb.io/example created
    ```
    
    **2. nginx ingress controller 설치**
    
    ```bash
    vagrant@master-node:~$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/baremetal/deploy.yaml
    
    vagrant@master-node:~$ kubectl get all -n ingress-nginx
    NAME                                            READY   STATUS      RESTARTS   AGE
    pod/ingress-nginx-admission-create-knnh4        0/1     Completed   0          18h
    pod/ingress-nginx-admission-patch-88p84         0/1     Completed   0          18h
    pod/ingress-nginx-controller-79bc9f5df8-rbc84   1/1     Running     1          18h
    
    NAME                                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
    service/ingress-nginx-controller             **NodePort**    172.17.39.79    <none>        **80:30253/TCP,443:32407/TCP**   18h
    service/ingress-nginx-controller-admission   ClusterIP   172.17.48.148   <none>        443/TCP                      18h
    
    NAME                                       READY   UP-TO-DATE   AVAILABLE   AGE
    deployment.apps/ingress-nginx-controller   1/1     1            1           18h
    
    NAME                                                  DESIRED   CURRENT   READY   AGE
    replicaset.apps/ingress-nginx-controller-79bc9f5df8   1         1         1       18h
    
    NAME                                       COMPLETIONS   DURATION   AGE
    job.batch/ingress-nginx-admission-create   1/1           15s        18h
    job.batch/ingress-nginx-admission-patch    1/1           23s        18h
    
    vagrant@master-node:~$ kubectl edit service ingress-nginx-controller -n ingress-nginx
    type : NodePort  -> LoadBalancer
    service/ingress-nginx-controller edited
    
    vagrant@master-node:~$ kubectl get service -n ingress-nginx
    NAME                                 TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
    ingress-nginx-controller             **LoadBalancer**   172.17.39.79    10.0.0.30     80:30253/TCP,443:32407/TCP   18h
    ingress-nginx-controller-admission   ClusterIP      172.17.48.148   <none>        443/TCP                      18h
    ```
    
    **3. 웹 서비스를 제공하는 디플로이먼트, 서비스, 인그레스를 생성**
    
    production-deployment.yaml
    
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: production-deployment
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: nginx
      template:
        metadata:
          labels:
            app: nginx
        spec:
          containers:
          - name: nginx
            image: docker.io/nginx:1.14.2
            ports:
            - containerPort: 80
          imagePullSecrets:
          - name: regcred
    ```
    
    production-service.yaml
    
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: production-service
    spec:
      type: ClusterIP
      selector:
        app: nginx
      ports:
        - protocol: TCP
          port: 80
          targetPort: 80
    ```
    
    production-ingress.yaml
    
    ```yaml
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: production-ingress
    spec:
      ingressClassName: nginx
      rules:
      - host: www.canary.com
        http:
          paths:
          - pathType: Prefix
            path: /
            backend:
              service:
                name: production-service
                port:
                  number: 80
    ```
    
    ```bash
    vagrant@master-node:~$ kubectl apply -f production-deployment.yaml
    deployment.apps/production-deployment created
    vagrant@master-node:~$ kubectl apply -f production-service.yaml
    service/production-service created
    vagrant@master-node:~$ kubectl apply -f production-ingress.yaml
    ingress.networking.k8s.io/production-ingress created
    ```
    
    ```bash
    vagrant@master-node:~$ kubectl get pod
    NAME                                     READY   STATUS    RESTARTS   AGE
    production-deployment-768d775c57-7xghk   1/1     Running   0          61s
    production-deployment-768d775c57-vnmdr   1/1     Running   0          61s
    production-deployment-768d775c57-vxxqg   1/1     Running   0          61s
    
    vagrant@master-node:~$ kubectl get service
    NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
    kubernetes           ClusterIP   172.17.0.1      <none>        443/TCP        6d2h
    production-service   NodePort    172.17.20.176   <none>        80:31792/TCP   57s
    
    vagrant@master-node:~$ kubectl get ingress
    NAME                 CLASS   HOSTS            ADDRESS     PORTS   AGE
    production-ingress   nginx   www.canary.com   10.0.0.12   80      97s
    ```
    
    **4. 인그레스로 접속(요청을 전달)**
    
    ```bash
    vagrant@master-node:~$ kubectl get service -n ingress-nginx
    NAME                                 TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
    ingress-nginx-controller             LoadBalancer   172.17.39.79    10.0.0.30     80:30253/TCP,443:32407/TCP   19h
    ingress-nginx-controller-admission   ClusterIP      172.17.48.148   <none>        443/TCP                      19h
    ```
    
    ```bash
    sudo vi /etc/hosts
    10.0.0.30 www.canary.com
    
    vagrant@master-node:~$ wget -q -O - http://www.canary.com
    <!DOCTYPE html>
    <html>
    <head>
    <title>Welcome to nginx!</title>
    <style>
        body {
            width: 35em;
            margin: 0 auto;
            font-family: Tahoma, Verdana, Arial, sans-serif;
        }
    </style>
    </head>
    <body>
    <h1>Welcome to nginx!</h1>
    <p>If you see this page, the nginx web server is successfully installed and
    working. Further configuration is required.</p>
    
    <p>For online documentation and support please refer to
    <a href="http://nginx.org/">nginx.org</a>.<br/>
    Commercial support is available at
    <a href="http://nginx.com/">nginx.com</a>.</p>
    
    <p><em>Thank you for using nginx.</em></p>
    </body>
    </html>
    ```
    
    내 PC의 C:\Windows\System32\drivers\etc\hosts 파일에 10.0.0.30 www.canary.com 내용을 추가해서 테스트도 가능
    
    (메모장을 관리자 권한으로 실행해서 수정 후 저장)
    
    ![image](https://github.com/Suah-Cho/STUDY/assets/102336763/5bc3f700-02dd-4f88-a0ca-2a5ec94a1b88)

    
    **5. 새로운 버전의 디플로이먼트, 서비스를 생성**
    
    canary-deployment.yaml
    
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: canary-deployment
    spec:
      replicas: 1				
      selector:
        matchLabels:
          app: nginx-canary
      template:
        metadata:
          labels:
            app: nginx-canary
        spec:
          containers:
          - name: nginx-canary
            image: docker.io/alicek106/rr-test:echo-hostname
            ports:
            - containerPort: 80
          imagePullSecrets:
          - name: regcred
    ```
    
    canary-service.yaml
    
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: canary-service
    spec:
      tpye: ClusterIP
      selector:
        app: nginx-canary
      ports:
        - protocol: TCP
          port: 80
          targetPort: 80
    ```
    
    ```bash
    vagrant@master-node:~$ kubectl apply -f canary-deployment.yaml
    deployment.apps/canary-deployment created
    vagrant@master-node:~$ kubectl apply -f canary-service.yaml
    service/canary-service created
    vagrant@master-node:~$ kubectl get all
    NAME                                         READY   STATUS    RESTARTS   AGE
    pod/canary-deployment-76fb4d56cd-zk6kb       1/1     Running   0          19s
    pod/production-deployment-768d775c57-7xghk   1/1     Running   0          43m
    pod/production-deployment-768d775c57-vnmdr   1/1     Running   0          43m
    pod/production-deployment-768d775c57-vxxqg   1/1     Running   0          43m
    
    NAME                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
    service/canary-service       ClusterIP   172.17.42.132   <none>        80/TCP    12s
    service/kubernetes           ClusterIP   172.17.0.1      <none>        443/TCP   6d3h
    service/production-service   ClusterIP   172.17.20.176   <none>        80/TCP    43m
    
    NAME                                    READY   UP-TO-DATE   AVAILABLE   AGE
    deployment.apps/canary-deployment       1/1     1            1           19s
    deployment.apps/production-deployment   3/3     3            3           43m
    
    NAME                                               DESIRED   CURRENT   READY   AGE
    replicaset.apps/canary-deployment-76fb4d56cd       1         1         1       19s
    replicaset.apps/production-deployment-768d775c57   3         3         3       43m
    ```
    
    production-deployment를 통해서 생성된 파드는 ingress를 통해서 외부에 노출되어 있으나, canary-deployment를 통해서 생성된 파드는 외부에서 접근할 수 없는 상태
    
    **6. 인그레스 추가**
    
    canary-ingress.yaml
    
    ```yaml
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: canary-ingress
      annotations:
        nginx.ingress.kubernetes.io/canary: "true"  << nginx의 canary를 사용하겠다.
        nginx.ingress.kubernetes.io/canary-weight: "20"  << 아래 spec에 만족하는 서비스 쪽으로 이동하겠다.
    spec:
      ingressClassName: nginx
      rules:
      - host: www.canary.com
        http:
          paths:
          - pathType: Prefix
            path: /
            backend:
              service:
                name: canary-service
                port:
                  number: 80
    ```
    
    ```bash
    vagrant@master-node:~$ kubectl apply -f canary-ingress.yaml
    ingress.networking.k8s.io/canary-ingress created
    
    vagrant@master-node:~$ kubectl get ingress
    NAME                 CLASS   HOSTS            ADDRESS     PORTS   AGE
    canary-ingress       nginx   www.canary.com   10.0.0.12   80      18s
    production-ingress   nginx   www.canary.com   10.0.0.12   80      49m
    
    vagrant@master-node:~$ kubectl get service -n ingress-nginx
    NAME                                 TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
    ingress-nginx-controller             LoadBalancer   172.17.39.79    10.0.0.30     80:30253/TCP,443:32407/TCP   19h
    ingress-nginx-controller-admission   ClusterIP      172.17.48.148   <none>        443/TCP                      19h
    ```
    
    **7. [http://www.canary.com](http://www.canary.com요청을)으로 요청을 전달했을 때 요청이 분배되어 처리되는 것을 확인**
    
    ![image](https://github.com/Suah-Cho/STUDY/assets/102336763/b24754ff-3d3e-4377-92ae-6239d6e2c3b3)

    
    ![image](https://github.com/Suah-Cho/STUDY/assets/102336763/33cfb65b-4e0a-462d-86f2-1e5909a0b04a)

    
    **8. canary-ingress.yaml파일에 canary-weight를 변경**
    
    20 → 80으로 변경
    
    ```bash
    vagrant@master-node:~$ kubectl apply -f canary-ingress.yaml
    ingress.networking.k8s.io/canary-ingress configured
    ```
    
    ![image](https://github.com/Suah-Cho/STUDY/assets/102336763/44c4ea7e-28bd-429e-b358-96dc95453d84)

    
    ![image](https://github.com/Suah-Cho/STUDY/assets/102336763/a7eb6e76-d27c-4c28-bb27-e4f9156e2bc0)

    
    **⇒ 신규 버전이 더 많이 응답하는 것을 볼 수 있다.**

### 데몬셋(DaemonSet)

- `각 노드에 파드를 하나씩 배치`하는 리소스
    - 레플리카 수를 지정할 수 없고 하나의 노드에 두 개의 파드를 배치할 수 없다.
    - 단, 내가 배치하고 싶지 않은 노드가 있는 경우 nodeSelector 또는 노드 안티어피니티를 사용해서 예외처리할 수 있다.
    - 노드를 늘렸을 때 DaemonSet의 파드도 자동으로 늘어난 노드에서 기동이 된다.
    - 호스트 단위로 로그를 수집하는 경우, 리소스 사용 현황 및 노드 상태를 모니터링하는 경우 사용
  1. 데몬셋 정의
  
  sample-daemonset.yaml
  
  ```yaml
  apiVersion: apps/v1
  kind: DaemonSet
  metadata:
    name: sample-daemonset
  spec:
    selector:
      matchLabels:
        app: sample-app
    template:
      metadata:
        labels:
          app: sample-app
      spec:
        containers:
        - name: nginx-container
          image: docker.io/nginx:1.16
        imagePullSecrets:
        - name: regcred
  ```

  2. node01을 중지
  
  ```bash
  vagrant halt node01
  
  vagrant@master-node:~$ kubectl get node
  NAME            STATUS     ROLES           AGE    VERSION
  master-node     Ready      control-plane   4d3h   v1.27.1
  worker-node01   NotReady   worker          4d3h   v1.27.1
  worker-node02   Ready      worker          4d3h   v1.27.1
  ```

  3. 데몬셋 생성
  
  ```bash
  vagrant@master-node:~$ kubectl apply -f sample-daemonset.yaml
  daemonset.apps/sample-daemonset created
  
  vagrant@master-node:~$ kubectl get daemonset,pod -o wide
  NAME                              DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE   CONTAINERS        IMAGES                 SELECTOR
  daemonset.apps/sample-daemonset   1         1         1       1            1           <none>          23s   nginx-container   docker.io/nginx:1.16   app=sample-app
  
  NAME                         READY   STATUS    RESTARTS   AGE   IP              NODE            NOMINATED NODE   READINESS GATES
  pod/sample-daemonset-zj6j4   1/1     Running   0          23s   172.16.158.48   **worker-node02**   <none>           <none>
  ```

  4. node01을 기동
  
  ```bash
  vagrant up node01
  ```

  5. 데몬셋 확인
  
  ```bash
  vagrant@master-node:~$ kubectl get daemonset,pod -o wide
  NAME                              **DESIRED**   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE     CONTAINERS        IMAGES                 SELECTOR
  daemonset.apps/sample-daemonset   **2**         2         2       2            2           <none>          3m39s   nginx-container   docker.io/nginx:1.16   app=sample-app
  
  NAME                         READY   STATUS    RESTARTS   AGE     IP              NODE            NOMINATED NODE   READINESS GATES
  pod/sample-daemonset-84xgf   1/1     Running   0          49s     172.16.87.227   **worker-node01**   <none>           <none>
  pod/sample-daemonset-zj6j4   1/1     Running   0          3m39s   172.16.158.48   worker-node02   <none>           <none>
  ```

**데몬셋 업데이터 전략**

OnDelete

- 파드가 다시 생성될 때 새로 정의한 파드를 생성
- 데몬셋 매니페스트가 변경되어도 기존 파드를 업데이트하지 않고, 파드가 다시 생성될 때 새롭게 정의한 파드를 생성

sample-daemonset-ondelete.yaml

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: sample-daemonset-ondelete
spec:
  updateStrategy:
   type: OnDelete
  selector:
    matchLabels:
      app: sample-app
  template:
    metadata:
      labels:
        app: sample-app
    spec:
      containers:
      - name: nginx-container
        image: docker.io/nginx:1.16
      imagePullSecrets:
      - name: regcred
```

```bash
// 데몬셋 생성
vagrant@master-node:~$ kubectl apply -f sample-daemonset-ondelete.yaml
daemonset.apps/sample-daemonset-ondelete created

// 데몬셋과 파드를 확인
vagrant@master-node:~$ kubectl get daemonset
NAME                        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
sample-daemonset-ondelete   2         2         2       2            2           <none>          64s

vagrant@master-node:~$ kubectl get pod -o wide
NAME                              READY   STATUS    RESTARTS   AGE   IP              NODE            NOMINATED NODE   READINESS GATES
sample-daemonset-ondelete-df99n   1/1     Running   0          52s   172.16.87.228   **worker-node01**   <none>           <none>
sample-daemonset-ondelete-lm4hn   1/1     Running   0          52s   172.16.158.49   **worker-node02**   <none>           <none>

// 데몬셋의 이미지를 변경
vagrant@master-node:~$ kubectl set image daemonset sample-daemonset-ondelete nginx-container=nginx:1.17
daemonset.apps/sample-daemonset-ondelete image updated

// 파드를 조회 => 파드가 변경되지 않고 유지되는 것을 확인
vagrant@master-node:~$ kubectl get pod -o wide
NAME                              READY   STATUS    RESTARTS   AGE     IP              NODE            NOMINATED NODE   READINESS GATES
sample-daemonset-ondelete-df99n   1/1     Running   0          2m45s   172.16.87.228   **worker-node01**   <none>           <none>
sample-daemonset-ondelete-lm4hn   1/1     Running   0          2m45s   172.16.158.49   worker-node02   <none>           <none>

// 파드를 삭제
vagrant@master-node:~$ kubectl delete pod sample-daemonset-ondelete-df99n
pod "sample-daemonset-ondelete-df99n" deleted

// 파드를 조회 => 새로운 파드가 삭제된 파드와 동일한 노드에 생성된 것을 확인
vagrant@master-node:~$ kubectl get pod -o wide
NAME                              READY   STATUS    RESTARTS   AGE    IP              NODE            NOMINATED NODE   READINESS GATES
**sample-daemonset-ondelete-fgbmx**   1/1     Running   0          3s     172.16.87.229   **worker-node01**   <none>           <none>
sample-daemonset-ondelete-lm4hn   1/1     Running   0          5m6s   172.16.158.49   worker-node02   <none>           <none>

// 새로 생성된 파드를 상세 조회
vagrant@master-node:~$ kubectl describe pod sample-daemonset-ondelete-fgbmx
Name:             sample-daemonset-ondelete-fgbmx
Namespace:        default
Priority:         0
Service Account:  default
Node:             worker-node01/10.0.0.11
Start Time:       Tue, 10 Oct 2023 03:21:01 +0000
Labels:           app=sample-app
                  controller-revision-hash=77dc8d9fb
                  pod-template-generation=2
Annotations:      cni.projectcalico.org/containerID: c7bcdc8d5ea23e3e4a28bbcf5c5a253b3836eb5fef5addaac6471242902b9c35
                  cni.projectcalico.org/podIP: 172.16.87.229/32
                  cni.projectcalico.org/podIPs: 172.16.87.229/32
Status:           Running
IP:               172.16.87.229
IPs:
  IP:           172.16.87.229
Controlled By:  DaemonSet/sample-daemonset-ondelete
Containers:
  nginx-container:
    Container ID:   cri-o://4c0e20014e959b5d0909a22e5d4d03319a102a8eed5827d87583fd4295d02a11
    **Image:          nginx:1.17**
    Image ID:       docker.io/library/nginx@sha256:6fff55753e3b34e36e24e37039ee9eae1fe38a6420d8ae16ef37c92d1eb26699
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Tue, 10 Oct 2023 03:21:03 +0000
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-t4wbl (ro)
Conditions:
  Type              Status
  Initialized       True
  Ready             True
  ContainersReady   True
  PodScheduled      True
Volumes:
  kube-api-access-t4wbl:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/disk-pressure:NoSchedule op=Exists
                             node.kubernetes.io/memory-pressure:NoSchedule op=Exists
                             node.kubernetes.io/not-ready:NoExecute op=Exists
                             node.kubernetes.io/pid-pressure:NoSchedule op=Exists
                             node.kubernetes.io/unreachable:NoExecute op=Exists
                             node.kubernetes.io/unschedulable:NoSchedule op=Exists
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  77s   default-scheduler  Successfully assigned default/sample-daemonset-ondelete-fgbmx to worker-node01
  Normal  Pulled     76s   kubelet            Container image "nginx:1.17" already present on machine
  Normal  Created    76s   kubelet            Created container nginx-container
  Normal  Started    75s   kubelet            Started container nginx-container

// 기존에 실행되고 있던 파드를 상세 조회
vagrant@master-node:~$ kubectl describe pod sample-daemonset-ondelete-lm4hn
Name:             sample-daemonset-ondelete-lm4hn
Namespace:        default
Priority:         0
Service Account:  default
Node:             worker-node02/10.0.0.12
Start Time:       Tue, 10 Oct 2023 03:15:59 +0000
Labels:           app=sample-app
                  controller-revision-hash=9ff76c956
                  pod-template-generation=1
Annotations:      cni.projectcalico.org/containerID: 821e7f1ac0cdc3feb4db1c91879f3b263401f8ddd5ca8c5093d49ccf2e2dc0cd
                  cni.projectcalico.org/podIP: 172.16.158.49/32
                  cni.projectcalico.org/podIPs: 172.16.158.49/32
Status:           Running
IP:               172.16.158.49
IPs:
  IP:           172.16.158.49
Controlled By:  DaemonSet/sample-daemonset-ondelete
Containers:
  nginx-container:
    Container ID:   cri-o://70f4f0dc577685fb989f170e62ecb6bf699e9e4ddcab1d31956960567da0cf20
    **Image:          docker.io/nginx:1.16**
    Image ID:       docker.io/library/nginx@sha256:2963fc49cc50883ba9af25f977a9997ff9af06b45c12d968b7985dc1e9254e4b
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Tue, 10 Oct 2023 03:16:00 +0000
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-lb5zz (ro)
Conditions:
  Type              Status
  Initialized       True
  Ready             True
  ContainersReady   True
  PodScheduled      True
Volumes:
  kube-api-access-lb5zz:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/disk-pressure:NoSchedule op=Exists
                             node.kubernetes.io/memory-pressure:NoSchedule op=Exists
                             node.kubernetes.io/not-ready:NoExecute op=Exists
                             node.kubernetes.io/pid-pressure:NoSchedule op=Exists
                             node.kubernetes.io/unreachable:NoExecute op=Exists
                             node.kubernetes.io/unschedulable:NoSchedule op=Exists
Events:
  Type    Reason     Age    From               Message
  ----    ------     ----   ----               -------
  Normal  Scheduled  7m40s  default-scheduler  Successfully assigned default/sample-daemonset-ondelete-lm4hn to worker-node02
  Normal  Pulled     7m38s  kubelet            Container image "docker.io/nginx:1.16" already present on machine
  Normal  Created    7m38s  kubelet            Created container nginx-container
  Normal  Started    7m38s  kubelet            Started container nginx-container
```

**RollingUpdate**

- - 즉시 파드를 업데이트 할 때 사용 ( 기본값 )
- - maxSurge(동시에 생성할 수 있는 최대 파드 수)를 설정할 수 없으며, maxUnavailable(동시에 정지 가능한 최대 파드 수)만 설정할 수 있다.
- - maxUnavailable의 기본값은 1이며, 0으로 지정할 수 없다.

  sample-daemonset-rollingupdate.yaml
  ```yaml
  apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: sample-daemonset-rollingupdate
spec:
  updateStrategy:
    type: RollingUpdate			<<<<
    rollingUpdate:				<<<<
      maxUnavailable: 1
  selector:
    matchLabels:
      app: sample-app
  template:
    metadata:
      labels:
        app: sample-app
    spec:
      containers:
      - name: nginx-container
        image: docker.io/nginx:1.16
      imagePullSecrets:
      - name: regcred
```
```bash
// 데몬셋 생성
vagrant@master-node:~$ kubectl apply -f sample-daemonset-rollingupdate.yaml
daemonset.apps/sample-daemonset-rollingupdate created

// 데몬셋과 파드 조회
vagrant@master-node:~$ kubectl get daemonset
NAME                             DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
sample-daemonset-rollingupdate   2         2         2       2            2           <none>          23s

vagrant@master-node:~$ kubectl get pod -o wide
NAME                                   READY   STATUS    RESTARTS   AGE   IP              NODE            NOMINATED NODE   READINESS GATES
sample-daemonset-rollingupdate-stkfn   1/1     Running   0          31s   172.16.158.5    worker-node02   <none>           <none>
sample-daemonset-rollingupdate-t9pls   1/1     Running   0          31s   172.16.87.232   worker-node01   <none>           <none>

// 파드 상태를 모니터링
vagrant@master-node:~$ kubectl get pod -o wide --watch
NAME                                   READY   STATUS    RESTARTS   AGE   IP              NODE            NOMINATED NODE   READINESS GATES
sample-daemonset-rollingupdate-stkfn   1/1     Running   0          74s   172.16.158.5    worker-node02   <none>           <none>
sample-daemonset-rollingupdate-t9pls   1/1     Running   0          74s   172.16.87.232   worker-node01   <none>           <none>

// (별도 창에서) 데몬셋 이미지를 변경
vagrant@master-node:~$ kubectl set image daemonset sample-daemonset-rollingupdate nginx-container=nginx:1.17

//파드 상태 변화를 확인
NAME                                  READY  STATUS             RESTARTS AGE   IP             NODE           NOMINATED NODE  READINESS GATES
sample-daemonset-rollingupdate-stkfn  1/1    Running            0        74s   172.16.158.5   worker-node02  <none>          <none>
sample-daemonset-rollingupdate-t9pls  1/1    Running            0        74s   172.16.87.232  worker-node01  <none>          <none>
sample-daemonset-rollingupdate-t9pls  1/1    Terminating        0        2m9s  172.16.87.232  worker-node01  <none>          <none>	⇐ node01에 기존 파드를 종료
sample-daemonset-rollingupdate-t9pls  0/1    Terminating        0        3m    <none>         worker-node01  <none>          <none>
sample-daemonset-rollingupdate-gklb7  0/1    Pending            0        0s    <none>         <none>         <none>          <none>	⇐ node01에 새로운 파드를 실행
sample-daemonset-rollingupdate-gklb7  0/1    Pending            0        0s    <none>         worker-node01  <none>          <none>	
sample-daemonset-rollingupdate-gklb7  0/1    ContainerCreating  0        0s    <none>         worker-node01  <none>          <none>
sample-daemonset-rollingupdate-gklb7  1/1    Running            0        2s    172.16.87.233  worker-node01  <none>          <none>	⇐ node01에 새로운 파드를 실행 완료
sample-daemonset-rollingupdate-stkfn  1/1    Terminating        0        3m2s  172.16.158.5   worker-node02  <none>          <none>	⇐ node02에 기존 파드를 종료
sample-daemonset-rollingupdate-stkfn  0/1    Terminating        0        3m3s  <none>         worker-node02  <none>          <none>
sample-daemonset-rollingupdate-8t22j  0/1    Pending            0        0s    <none>         <none>         <none>          <none>	⇐ node02에 새로운 파드를 실행
sample-daemonset-rollingupdate-8t22j  0/1    ContainerCreating  0        1s    <none>         worker-node02  <none>          <none>
sample-daemonset-rollingupdate-8t22j  1/1    Running            0        2s    172.16.158.6   worker-node02  <none>          <none>	⇐ node02에 새로운 파드를 실행 완료

```

### 서비스(Service)

파드를 연결하고 외부에 노출

**서비스 기능**

- 여러 개의 파드에 쉽게 접근할 수 있도록 고유한 도메인 이름을 부여
- 여러 개의 파드에 접근할 때, 요청을 분산하는 로드 밸런서 기능을 수행
- 클라우드 플랫폼의 로드 밸런서, 클러서 노드의 포트 등을 통해 파드를 외부에 노출

**서비스 타입**

| ClusterIP | - 디폴트
- 클러스터 내부에서 파드들에 접근할 때 사용
- 외부로 파드를 노출하지 않기 때문에 클러스터 내부에서만 사용되는 파드에 적합 |
| --- | --- |
| NodePort | - 파드에 접근할 수 있는 포트를 클러스터의 모든 노드에 동일하게 개방
- 외부에서 파드에 접근할 수 있는 서비스 타입
- 접근할 수 있는 포트는 랜덤으로 정해지지만, 특정 포트로 접근하도록 설정할 수 있다. |
| LoadBalancer | - 클라우드 플랫폼에서 제공하는 로드밸런서를 동적으로 프로비저닝해 파드에 연결
- NodePort타입과 마찬가지로 외부에서 파드에 접근할 수 있는 서비스 타입
- 일반적으로  AWS, GCP 등과 같은 클라우드 플랫폼 환경에서 사용 |
| ExternalName | - 외부 서비스를 쿠버네티스 내부에서 호출하고자 할 때 사용
- 클러스터 내의 파드에서 외부 IP주소에 서비스의 이름으로 접근할 수 있다. |

**서비스를 생성하는 방법**

- 매니페스트(YAML)을 이용해서 생성
- kubectl expose 명령을 사용해서 생성

**디플로이먼트로 파드를 생성하고, 생성한 파드로 요청을 전달**

  1. 디플로먼트 생성
  
  hostname-deployment.yaml
  
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: hostname-deployment
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: webserver
    template:
      metadata:
        labels: 
          app: webserver
        name: mywebserver
      spec:
        containers:
        - name: mywebserver-container
          image: docker.io/alicek106/rr-test:echo-hostname
          ports:
          - containerPort: 80
        imagePullSecrets:
        - name: regcred
  ```
  
  ```bash
  vagrant@master-node:~$ kubectl apply -f hostname-deployment.yaml
  deployment.apps/hostname-deployment created
  
  **// 파드에서 제공하는 웹 서비스를 이용하기 위해 파드의 NAME과 IP를 확인**
  vagrant@master-node:~$ kubectl get pod -o wide
  NAME                                   READY   STATUS    RESTARTS   AGE   IP              NODE            NOMINATED NODE   READINESS GATES
  hostname-deployment-85cbb79457-68x95   1/1     Running   0          38s   172.16.87.230   worker-node01   <none>           <none>
  hostname-deployment-85cbb79457-z2v6r   1/1     Running   0          38s   172.16.158.51   worker-node02   <none>           <none>
  hostname-deployment-85cbb79457-zkslc   1/1     Running   0          38s   172.16.158.50   worker-node02   <none>           <none>
  ```

  2. 임시 파드를 실행해서 디플로이한 파드의 IP주소로 요청을 전달
  
  ```bash
  vagrant@master-node:~$ kubectl run -it --rm debug --image=docker.io/busybox --restart=Never sh
  If you don't see a command prompt, try pressing enter.
  / # wget -q -O - http://172.16.87.230 | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-68x95</p>     </blockquote>
  / #
  ```

**파드 IP 주소를 기반으로 애플리케이션 파드에 접근했을 때 문제점**

1. 파드가 수시로 삭제, 생성되는 과정에서 애플리케이션 파드의 IP주소가 변경될 수 있다.

⇒ 클라이언트 파드가 변경된 애플리케이션 파드의 IP주소를 알 수 없다. → 이름을 기반으로 애플리케이션 파드에 접근할 수 있는 방안이 필요

2. 클라이언트 파드는 자신이 알고 있는 애플리케이션 파드의 IP로만 접근 가능

⇒ 부하가 특정 파드로 집중될 수 있다. → 로드밸런싱 기능이 필요

**ClusterIP 타입의 서비스**

![image](https://github.com/Suah-Cho/STUDY/assets/102336763/44c0e910-8936-4136-b2c9-e72e383dc931)

  1. 서비스 생성
  
  hostname-service-clusterip.yaml
  
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: hostname-service-clusterip
  spec:
    type: ClusterIP   **// 서비스 타입(기본값이 ClusterIP)**
    selector:         **// 어떤 라벨의 파드에 접근할 수 있게 만들 것인지 결정**
      app: webserver **// 파드의 라벨**
    ports:
    - name: web-port
      port: 8080      **// 서비스의 IP에 접근할 때 사용할 포트**
      targetPort: 80  **// selector 항목에서 정의한 라벨에 의해 접근 대상이 된 파드 내부에서 사용하는 포트**
  ```

  2. 서비스 생성 및 확인
  
  ```bash
  vagrant@master-node:~$ kubectl apply -f hostname-service-clusterip.yaml
  service/hostname-service-clusterip created
  
  vagrant@master-node:~$ kubectl get service
  NAME                         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
  **hostname-service-clusterip   ClusterIP   172.17.17.62   <none>        8080/TCP   20s  // clusterip가 172.17.17.62이고 포트 번호가 8080인 서비스**
  kubernetes                   ClusterIP   172.17.0.1     <none>        443/TCP    4d6h
  ~~~~~~~~~~~
  -> 쿠버네티스 API에 접근하기 위한 서비스
  ```
  
  CLUSTER-IP
  
  ⇒ 쿠버네티스 클러스터에서만 사용할 수 잇는 내부 IP로, 이 IP를 통해 서비스에 연결된 파드로 접근이 가능

  3. 임시 파드 생성 후 서비스의 CLUSTER-IP와 PORT로 요청을 전송
  
  ```bash
  vagrant@master-node:~$ kubectl run -it --rm debug --image=docker.io/busybox --restart=Never s
  h
  If you don't see a command prompt, try pressing enter.
  / #
  / #
  / # ip a
  1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue qlen 1000
      link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
      inet 127.0.0.1/8 scope host lo
         valid_lft forever preferred_lft forever
      inet6 ::1/128 scope host
         valid_lft forever preferred_lft forever
  2: tunl0@NONE: <NOARP> mtu 1480 qdisc noop qlen 1000
      link/ipip 0.0.0.0 brd 0.0.0.0
  4: eth0@if25: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1480 qdisc noqueue qlen 1000
      link/ether 1e:2c:c4:e4:bc:6f brd ff:ff:ff:ff:ff:ff
      inet **172.16.158.52**/32 scope global eth0
         valid_lft forever preferred_lft forever
      inet6 fe80::1c2c:c4ff:fee4:bc6f/64 scope link
         valid_lft forever preferred_lft forever
  / # wget -q -O - http://172.17.17.62:8080 | grep Hello
          <p>Hello,  **hostname-deployment-85cbb79457-z2v6r**</p>     </blockquote>
  / # wget -q -O - http://172.17.17.62:8080 | grep Hello
          <p>Hello,  **hostname-deployment-85cbb79457-z2v6r**</p>     </blockquote>
  / # wget -q -O - http://172.17.17.62:8080 | grep Hello
          <p>Hello,  **hostname-deployment-85cbb79457-z2v6r**</p>     </blockquote>
  / # wget -q -O - http://172.17.17.62:8080 | grep Hello
          <p>Hello,  **hostname-deployment-85cbb79457-68x95**</p>     </blockquote>
  / # wget -q -O - http://172.17.17.62:8080 | grep Hello
          <p>Hello,  **hostname-deployment-85cbb79457-zkslc**</p>     </blockquote>
  / # wget -q -O - http://172.17.17.62:8080 | grep Hello
          <p>Hello,  **hostname-deployment-85cbb79457-zkslc**</p>     </blockquote>
  / # wget -q -O - http://172.17.17.62:8080 | grep Hello
          <p>Hello,  **hostname-deployment-85cbb79457-68x95**</p>     </blockquote>
  
  **// => 서비스의 CLUSTER-IP와 PORT로 접근
  // => 서비스에 연결된 파드로 로드밸런싱되는 것을 확인**
  ```

  4. 서비스의 NAME과 PORT로 요청을 전달
  
  쿠버네티스는 애플리케이션이 서비스나 파드를 쉽게 찾을 수 있도록 내부 DNS를 구동
  
  ```bash
  / # wget -q -O - http://hostname-service-clusterip:8080 | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-z2v6r</p>     </blockquote>
  / # wget -q -O - http://hostname-service-clusterip:8080 | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-68x95</p>     </blockquote>
  / # wget -q -O - http://hostname-service-clusterip:8080 | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-z2v6r</p>     </blockquote>
  / # wget -q -O - http://hostname-service-clusterip:8080 | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-zkslc</p>     </blockquote>
  / # wget -q -O - http://hostname-service-clusterip:8080 | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-68x95</p>     </blockquote>
  / # wget -q -O - http://hostname-service-clusterip:8080 | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-zkslc</p>     </blockquote>
  
  **// => 서비스의 NAME과 PORT로 접근**
  ```

  5. (다른 터미널에서) 파드 하나를 삭제
  
  ```bash
  vagrant@master-node:~$ kubectl get pod
  NAME                                   READY   STATUS    RESTARTS   AGE
  debug                                  1/1     Running   0          8m49s
  **hostname-deployment-85cbb79457-68x95**   1/1     Running   0          64m
  hostname-deployment-85cbb79457-z2v6r   1/1     Running   0          64m
  hostname-deployment-85cbb79457-zkslc   1/1     Running   0          64m
  
  vagrant@master-node:~$ kubectl delete pod hostname-deployment-85cbb79457-68x95
  pod "hostname-deployment-85cbb79457-68x95" deleted
  
  vagrant@master-node:~$ kubectl get pod
  NAME                                   READY   STATUS    RESTARTS   AGE
  debug                                  1/1     Running   0          9m51s
  **hostname-deployment-85cbb79457-66j59   1/1     Running   0          39s**
  hostname-deployment-85cbb79457-z2v6r   1/1     Running   0          65m
  hostname-deployment-85cbb79457-zkslc   1/1     Running   0          65m
  ```

  6. (원래 터미널에서) 서비스로 접근했을 때 새로 생성된 파드로 요청이 전달되는 것을 확인
  
  ```bash
  / # wget -q -O - http://hostname-service-clusterip:8080 | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-z2v6r</p>     </blockquote>
  / # wget -q -O - http://hostname-service-clusterip:8080 | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-**66j59**</p>     </blockquote>  **************************************************************************<= 새로운 파드로 요청이 전달**************************************************************************
  / # wget -q -O - http://hostname-service-clusterip:8080 | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-zkslc</p>     </blockquote>
  ```

  7. 대화형 파드에서 hostname-service-clusterip 서비스로 반복해서 요청을 전달하는 스크립트를 실행 → 반환되는 호스트명이 라운드로빈 방식으로 출력되는 것을 확인
  
  ```bash
  / # while true; do wget -q -O - http://hostname-service-clusterip:8080 | grep Hello | grep He
  llo; sleep 1; done
          <p>Hello,  hostname-deployment-85cbb79457-z2v6r</p>     </blockquote>
          <p>Hello,  hostname-deployment-85cbb79457-66j59</p>     </blockquote>
          <p>Hello,  hostname-deployment-85cbb79457-zkslc</p>     </blockquote>
          <p>Hello,  hostname-deployment-85cbb79457-z2v6r</p>     </blockquote>
          <p>Hello,  hostname-deployment-85cbb79457-z2v6r</p>     </blockquote>
          <p>Hello,  hostname-deployment-85cbb79457-z2v6r</p>     </blockquote>
          <p>Hello,  hostname-deployment-85cbb79457-66j59</p>     </blockquote>
          <p>Hello,  hostname-deployment-85cbb79457-zkslc</p>     </blockquote>
          <p>Hello,  hostname-deployment-85cbb79457-66j59</p>     </blockquote>
  ```

  8. 서비스 생성 후 실행되는 파드에는 서비스와 관련한 환경변수가 설정되어 있다.
  
  ```bash
  / # env | grep HOSTNAME_SERVICE_CLUSTERIP
  HOSTNAME_SERVICE_CLUSTERIP_PORT_8080_TCP_ADDR=172.17.17.62
  HOSTNAME_SERVICE_CLUSTERIP_SERVICE_HOST=172.17.17.62
  HOSTNAME_SERVICE_CLUSTERIP_PORT_8080_TCP_PORT=8080
  HOSTNAME_SERVICE_CLUSTERIP_SERVICE_PORT_WEB_PORT=8080
  HOSTNAME_SERVICE_CLUSTERIP_PORT_8080_TCP_PROTO=tcp
  HOSTNAME_SERVICE_CLUSTERIP_SERVICE_PORT=8080
  HOSTNAME_SERVICE_CLUSTERIP_PORT=tcp://172.17.17.62:8080
  HOSTNAME_SERVICE_CLUSTERIP_PORT_8080_TCP=tcp://172.17.17.62:8080
  ```

**세션 어피니티(sessionAffinity) ⇒ 클라이언트 IP별로 전송 파드를 고정**

  1. hostname-service-clusterip.yaml 수정
  
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: hostname-service-clusterip
  spec:
    type: ClusterIP
    selector:
      app: webserver
    ports:
    - name: web-port
      port: 8080
      targetPort: 80
    sessionAffinity: ClientIP **// 클라이언트 IP주소에 따라 요청을 처리할 파드가 결정**
  ```
  
  2. 서비스 배포
  
  ```bash
  vagrant@master-node:~$ kubectl apply -f hostname-service-clusterip.yaml
  service/hostname-service-clusterip **configured**
  
  vagrant@master-node:~$ kubectl get pod,service -o wide
  NAME                                       READY   STATUS    RESTARTS   AGE   IP              NODE            NOMINATED NODE   READINESS GATES
  pod/hostname-deployment-85cbb79457-66j59   1/1     Running   0          15m   172.16.87.232   worker-node01   <none>           <none>
  pod/hostname-deployment-85cbb79457-z2v6r   1/1     Running   0          81m   172.16.158.51   worker-node02   <none>           <none>
  pod/hostname-deployment-85cbb79457-zkslc   1/1     Running   0          81m   172.16.158.50   worker-node02   <none>           <none>
  
  NAME                                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE    SELECTOR
  service/hostname-service-clusterip   ClusterIP   172.17.17.62   <none>        8080/TCP   29m    app=webserver
  service/kubernetes                   ClusterIP   172.17.0.1     <none>        443/TCP    4d7h   <none>
  ```

  3. 대화형 파드에서 hostname-service-clusterip 서비스로 반복해서 요청을 전달
  
  ```bash
  vagrant@master-node:~$ kubectl run -it --rm debug --image=docker.io/busybox --restart=Never sh
  If you don't see a command prompt, try pressing enter.
  / #
  / #
  / # ip a
  1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue qlen 1000
      link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
      inet 127.0.0.1/8 scope host lo
         valid_lft forever preferred_lft forever
      inet6 ::1/128 scope host
         valid_lft forever preferred_lft forever
  2: tunl0@NONE: <NOARP> mtu 1480 qdisc noop qlen 1000
      link/ipip 0.0.0.0 brd 0.0.0.0
  4: eth0@if26: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1480 qdisc noqueue qlen 1000
      link/ether 06:65:ca:b7:b4:ad brd ff:ff:ff:ff:ff:ff
      inet **172.16.158.53**/32 scope global eth0
         valid_lft forever preferred_lft forever
      inet6 fe80::465:caff:feb7:b4ad/64 scope link
         valid_lft forever preferred_lft forever
  
  / # while true; do wget -q -O - http://hostname-service-clusterip:8080 | grep Hello; sleep 1;
   done
          <p>Hello,  hostname-deployment-85cbb79457-66j59</p>     </blockquote>
          <p>Hello,  hostname-deployment-85cbb79457-66j59</p>     </blockquote>
          <p>Hello,  hostname-deployment-85cbb79457-66j59</p>     </blockquote>
          <p>Hello,  hostname-deployment-85cbb79457-66j59</p>     </blockquote>
          <p>Hello,  hostname-deployment-85cbb79457-66j59</p>     </blockquote>
  **// 동일한 파드가 응답하는 것을 확인**
  ```

  4. (다른 터미널에서)  3번과정을 동일하게 진행
  
  ```bash
  vagrant@master-node:~$ kubectl run -it --rm debug2 --image=docker.io/busybox --restart=Never sh
  If you don't see a command prompt, try pressing enter.
  / #
  / # ip a
  1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue qlen 1000
      link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
      inet 127.0.0.1/8 scope host lo
         valid_lft forever preferred_lft forever
      inet6 ::1/128 scope host
         valid_lft forever preferred_lft forever
  2: tunl0@NONE: <NOARP> mtu 1480 qdisc noop qlen 1000
      link/ipip 0.0.0.0 brd 0.0.0.0
  4: eth0@if13: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1480 qdisc noqueue qlen 1000
      link/ether c6:d8:19:d6:0f:cf brd ff:ff:ff:ff:ff:ff
      inet 172.16.87.233/32 scope global eth0
         valid_lft forever preferred_lft forever
      inet6 fe80::c4d8:19ff:fed6:fcf/64 scope link
         valid_lft forever preferred_lft forever
  
  / # while true; do wget -q -O - http://hostname-service-clusterip:8080 | grep Hello; sleep 1; done
          <p>Hello,  hostname-deployment-85cbb79457-zkslc</p>     </blockquote>
          <p>Hello,  hostname-deployment-85cbb79457-zkslc</p>     </blockquote>
          <p>Hello,  hostname-deployment-85cbb79457-zkslc</p>     </blockquote>
          <p>Hello,  hostname-deployment-85cbb79457-zkslc</p>     </blockquote>
          <p>Hello,  hostname-deployment-85cbb79457-zkslc</p>     </blockquote>
  ```

**노드 포트(NodePort) 타입의 서비스**

모든 노드의 특정 포트를 개방해 서비스에 접근하는 방식

노드의 IP주소에 공개 포트를 오픈 → 클러스터 외부에서 클러스터 내부의 파드로 요청을 전달하는 것이 가능

- 공개 포트
    - 30,000 ~ 32,767 범위

![image](https://github.com/Suah-Cho/STUDY/assets/102336763/af242fa0-3b39-461a-9fef-ef51470072ef)

  1. 디플로이먼트 생성
  
  ```bash
  vagrant@master-node:~$ kubectl apply -f hostname-deployment.yaml
  deployment.apps/hostname-deployment created
  
  vagrant@master-node:~$ kubectl apply -f hostname-deployment.yaml
  deployment.apps/hostname-deployment created
  
  vagrant@master-node:~$ kubectl get pod -o wide
  NAME                                   READY   STATUS    RESTARTS   AGE   IP              NODE            NOMINATED NODE   READINESS GATES
  hostname-deployment-85cbb79457-4547z   1/1     Running   0          54s   172.16.158.55   worker-node02   <none>           <none>
  hostname-deployment-85cbb79457-qltpp   1/1     Running   0          54s   172.16.87.234   worker-node01   <none>           <none>
  hostname-deployment-85cbb79457-z945j   1/1     Running   0          54s   172.16.158.54   worker-node02   <none>           <none>
  ```

  2. 서비스 정의
  
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: hostname-service-nodeport
  spec:
    type: NodePort
    ports:
    - name: web-port
      port: 8080
      targetPort: 80
    selector:
      app: webserver
  ```

  3. 서비스 생성 및 확인
  
  ```bash
  vagrant@master-node:~$ kubectl apply -f hostname-service-nodeport.yaml
  service/hostname-service-nodeport created
  
  vagrant@master-node:~$ kubectl get service
  NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
  **hostname-service-nodeport   NodePort    172.17.59.148   <none>        8080:30525/TCP   20s
                                                                             ~~~~~~
                                                                           공개 포트 : 모든 노드에서 동일하게 접근할 수 있는 포트**
  kubernetes                  ClusterIP   172.17.0.1      <none>        443/TCP          4d7h
  
  ```

  4. 클러스터 내에서 모든 노드의 INTERNAL-IP 또는 EXTERNAL-IP와 노드 공개 포트로 접근이 가능
  
  ```bash
  vagrant@master-node:~$ kubectl get node -o wide
  NAME            STATUS   ROLES           AGE    VERSION   **INTERNAL-IP   EXTERNAL-IP**   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
  master-node     Ready    control-plane   4d7h   v1.27.1   10.0.0.10     <none>        Ubuntu 22.04.3 LTS   5.15.0-83-generic   cri-o://1.27.1
  worker-node01   Ready    worker          4d7h   v1.27.1   10.0.0.11     <none>        Ubuntu 22.04.3 LTS   5.15.0-83-generic   cri-o://1.27.1
  worker-node02   Ready    worker          4d7h   v1.27.1   10.0.0.12     <none>        Ubuntu 22.04.3 LTS   5.15.0-83-generic   cri-o://1.27.1
  
  vagrant@master-node:~$ kubectl get pod -o wide
  NAME                                   READY   STATUS    RESTARTS   AGE   IP              NODE            NOMINATED NODE   READINESS GATES
  hostname-deployment-85cbb79457-**4547z**   1/1     Running   0          10m   172.16.158.55   worker-node02   <none>           <none>
  hostname-deployment-85cbb79457-**qltpp**   1/1     Running   0          10m   172.16.87.234   worker-node01   <none>           <none>
  hostname-deployment-85cbb79457-**z945j**   1/1     Running   0          10m   172.16.158.54   worker-node02   <none>           <none>
  
  // master노드의 공개 포트로 요청을 전달
  vagrant@master-node:~$ wget -q -O - http://10.0.0.10:**30525** | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-**4547z**</p>     </blockquote>
  vagrant@master-node:~$ wget -q -O - http://10.0.0.10:**30525** | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-**z945j**</p>     </blockquote>
  vagrant@master-node:~$ wget -q -O - http://10.0.0.10:**30525** | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-**qltpp**</p>     </blockquote>
  
  // node01노드의 공개 포트로 요청을 전달
  vagrant@master-node:~$ wget -q -O - http://10.0.0.11:30525 | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-**z945j**</p>     </blockquote>
  vagrant@master-node:~$ wget -q -O - http://10.0.0.11:30525 | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-**qltpp**</p>     </blockquote>
  vagrant@master-node:~$ wget -q -O - http://10.0.0.11:30525 | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-**4547z**</p>     </blockquote>
  
  // 서비스 이름으로 접근은 불가
  vagrant@master-node:~$ wget -O - http://hostname-service-nodeport:30525 | grep Hello
  --2023-10-10 07:40:39--  http://hostname-service-nodeport:30525/
  Resolving hostname-service-nodeport (hostname-service-nodeport)... failed: Temporary failure in name resolution.
  wget: unable to resolve host address ‘hostname-service-nodeport’
  ```

  5. 클러스터 내에서 서비스의 서비스 이름 또는 CLUSTER-IP와 ClusterIP 서비스 포트를 이용한 접근도 가능
  
  NodePort 타입의 서비스가 ClusterIP타입의 서비스 기능을 포함하고 있으므로 클러스터에서 서비스의 내부 IP와 DNS이름을 이용한 접근이 가능
  
  ```bash
  vagrant@master-node:~$ kubectl get service
  NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
  hostname-service-nodeport   NodePort    172.17.59.148   <none>        8080:30525/TCP   14m
  kubernetes                  ClusterIP   172.17.0.1      <none>        443/TCP          4d8h
  
  vagrant@master-node:~$ wget -q -O - http://172.17.59.148:8080 | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-4547z</p>     </blockquote>
  vagrant@master-node:~$ wget -q -O - http://172.17.59.148:8080 | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-z945j</p>     </blockquote>
  vagrant@master-node:~$ wget -q -O - http://172.17.59.148:8080 | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-qltpp</p>     </blockquote>
  
  vagrant@master-node:~$ kubectl run -it --rm debug --image=docker.io/busybox /bin/sh
  If you don't see a command prompt, try pressing enter.
  / # wget -q -O - http://172.17.59.148:8080 | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-qltpp</p>     </blockquote>
  / # wget -q -O - http://172.17.59.148:8080 | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-z945j</p>     </blockquote>
  / # wget -q -O - http://172.17.59.148:8080 | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-4547z</p>     </blockquote>
  / # wget -q -O - http://**hostname-service-nodeport**:8080 | grep Hello
          <p>Hello,  hostname-deployment-85cbb79457-4547z</p>     </blockquote>
  ```

  6. 호스트 PC의 웹 브라우저를 이용한 접근도 가능
  
  ![image](https://github.com/Suah-Cho/STUDY/assets/102336763/9c84a40c-a244-44bb-9936-9399b717b158)

  ![image](https://github.com/Suah-Cho/STUDY/assets/102336763/1c0cdf83-7ed9-4083-b596-ffdd4c6c6f8f)

  ![image](https://github.com/Suah-Cho/STUDY/assets/102336763/733c15a6-42f4-471d-a307-73ef2de498f7)

7. 리소스 정리
```bash
vagrant@master-node:~$ kubectl delete -f hostname-service-nodeport.yaml
service "hostname-service-nodeport" deleted
vagrant@master-node:~$ kubectl delete -f hostname-deployment.yaml
deployment.apps "hostname-deployment" deleted

vagrant@master-node:~$ kubectl get all
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   172.17.0.1   <none>        443/TCP   4d8h
```
