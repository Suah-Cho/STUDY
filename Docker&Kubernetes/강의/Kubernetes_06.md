# kubernetes_06

## 네임스페이스(namespace)

https://kubernetes.io/ko/docs/concepts/overview/working-with-objects/namespaces/

리소스를 논리적으로 구분하는 장벽

클러스터 안의 가상 클러스터 - 파드, 레플리카셋, 디플로이먼트, 서비스와 같은 쿠버네티스 리소스들이 묶여있는 하나의 가상 공간 또는 그룹

리소스를 논리적으로 구분하기 위해 제공

네임스페이스 마다 권한 설정이 가능

네임 스페이스는 개발팀이 일정 규모 이상일 때 유용

- 네임스페이스를 사용해 논리적으로 구분할 수 있는 대상
    - kubectl 명령어의 적용 범위
    - CPU 시간과 메모리 용량 등의 리소스 할당
    - 파드 네트워크 통신의 접근 제어 등

**초기 네임스페이스**

```bash
vagrant@master-node:~$ kubectl get namespace
NAME              STATUS   AGE
default           Active   6d3h
kube-node-lease   Active   6d3h
kube-public       Active   6d3h
kube-system       Active   6d3h
```

- default
    - 기본 네임스페이스
- kube-node-lease
    - 쿠버네티스 노드의 가용성을 체크하기 위한 네임스페이스
    - 하트 비트(heart beat)를 위한 leases 오브젝트가 있음
    - 하트 비트
        - health check할 때 heart beat 체크
    - 쿠버네티스 1.14버전 이상에서 사용
    
    ```bash
    vagrant@master-node:~$ kubectl get leases.coordination.k8s.io -n kube-node-lease
    NAME            HOLDER          AGE
    master-node     master-node     6d4h
    worker-node01   worker-node01   6d4h
    worker-node02   worker-node02   6d4h
    ```
    
- kube-public
    - 인증받지 않은 사용자를 포함한 모든 사용자가 읽기 권한으로 접근이 가능
    - 관례적으로 만들어져있지만 아무 리소스도 없고, 꼭 사용해야하는 것도 아니다.
    - 쿠버네티스 클러스터를 위해 예약된 공간
    
    ```bash
    vagrant@master-node:~$ kubectl get all -n kube-public
    No resources found in kube-public namespace.
    ```
    
- kube-system
    - 쿠버네티스 클러스터의 리소스가 배치되는 네임스페이스
    - 시스템이나 애드온(add on)이 사용하는 네임스페이스
    
    ```bash
    vagrant@master-node:~$ kubectl get all -n kube-system
    NAME                                           READY   STATUS    RESTARTS        AGE
    pod/calico-kube-controllers-786b679988-prp65   1/1     Running   3               6d4h
    pod/calico-node-662jz                          1/1     Running   4               6d4h
    pod/calico-node-7v5ss                          1/1     Running   3               6d4h
    pod/calico-node-qqdsc                          1/1     Running   4               6d4h
    pod/coredns-5d78c9869d-n5xgj                   1/1     Running   3               6d4h
    pod/coredns-5d78c9869d-vgr97                   1/1     Running   3               6d4h
    pod/etcd-master-node                           1/1     Running   3               6d4h
    pod/kube-apiserver-master-node                 1/1     Running   3               6d4h
    pod/kube-controller-manager-master-node        1/1     Running   5               6d4h
    pod/kube-proxy-67n8t                           1/1     Running   4               6d4h
    pod/kube-proxy-9g4j2                           1/1     Running   3               6d4h
    pod/kube-proxy-lf445                           1/1     Running   4               6d4h
    pod/kube-scheduler-master-node                 1/1     Running   5               6d4h
    pod/metrics-server-754586b847-mflrm            1/1     Running   8 (4h20m ago)   6d4h
    
    NAME                     TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)                  AGE
    service/kube-dns         ClusterIP   172.17.0.10   <none>        53/UDP,53/TCP,9153/TCP   6d4h
    service/metrics-server   ClusterIP   172.17.35.9   <none>        443/TCP                  6d4h
    
    NAME                         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
    daemonset.apps/calico-node   3         3         3       3            3           kubernetes.io/os=linux   6d4h
    daemonset.apps/kube-proxy    3         3         3       3            3           kubernetes.io/os=linux   6d4h
    
    NAME                                      READY   UP-TO-DATE   AVAILABLE   AGE
    deployment.apps/calico-kube-controllers   1/1     1            1           6d4h
    deployment.apps/coredns                   2/2     2            2           6d4h
    deployment.apps/metrics-server            1/1     1            1           6d4h
    
    NAME                                                 DESIRED   CURRENT   READY   AGE
    replicaset.apps/calico-kube-controllers-786b679988   1         1         1       6d4h
    replicaset.apps/coredns-5d78c9869d                   2         2         2       6d4h
    replicaset.apps/metrics-server-754586b847            1         1         1       6d4h
    ```
    

### 네임스페이스의 리소스를 조회

**default 네임스페이스에 생성된 파드 확인**

```bash
vagrant@master-node:~$ kubectl get pod --namespace default
No resources found in default namespace. 
vagrant@master-node:~$ kubectl get pod
No resources found in default namespace.
vagrant@master-node:~$ kubectl config get-contexts
CURRENT   NAME                          CLUSTER      AUTHINFO           NAMESPACE
*         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin 
```

### **네임스페이스 생성**

- **YAML 파일을 이용**

production-namespace.yaml

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
```

```bash
vagrant@master-node:~$ kubectl apply -f production-namespace.yaml
namespace/production created

vagrant@master-node:~$ kubectl get namespace
NAME              STATUS   AGE
default           Active   6d5h
kube-node-lease   Active   6d5h
kube-public       Active   6d5h
kube-system       Active   6d5h
production        Active   14s
```

- **create 구문을 이용**

```bash
vagrant@master-node:~$ kubectl create namespace mynamespace
namespace/mynamespace created

vagrant@master-node:~$ kubectl get namespace
NAME              STATUS   AGE
default           Active   6d5h
kube-node-lease   Active   6d5h
kube-public       Active   6d5h
kube-system       Active   6d5h
mynamespace       Active   76s
production        Active   2m45s
```

TO DO. **네임슴페이스를 만들면 서비스 어카운트 default와 그에 대응하는 시크릿이 만들어지는 것을 확인**

**매니페스트에서 리소스를 생성할 네임스페이스를 생성하는 방법**

hostname-deploy-svc-ns.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hostname-deploy-ns
  namespace: production	
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webserver
  template:
    metadata:
      name: my-webserver
      labels:
        app: webserver
    spec:
      containers:
      - name: my-webserver
        image: docker.io/alicek106/rr-test:echo-hostname
        ports:  
        - containerPort: 80

---
apiVersion: v1
kind: Service
metadata:
  name: hostname-svc-clusterip-ns
  namespace: production
spec:
  type: ClusterIP
  ports:
  - name: web-port
    port: 8080
    targetPort: 80
  selector:
    app: webserver
```

```bash
vagrant@master-node:~$ kubectl apply -f hostname-deploy-syc-deploy-svc-ns.yaml
deployment.apps/hostname-deploy-ns created
service/hostname-svc-clusterip-ns created

vagrant@master-node:~$ kubectl get all -n production
NAME                                     READY   STATUS    RESTARTS   AGE
pod/hostname-deploy-ns-746f55c57-2bbnf   1/1     Running   0          85s
pod/hostname-deploy-ns-746f55c57-724t8   1/1     Running   0          85s
pod/hostname-deploy-ns-746f55c57-pvskf   1/1     Running   0          85s

NAME                                TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
service/hostname-svc-clusterip-ns   ClusterIP   172.17.25.68   <none>        8080/TCP   118s

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/hostname-deploy-ns   3/3     3            3           85s

NAME                                           DESIRED   CURRENT   READY   AGE
replicaset.apps/hostname-deploy-ns-746f55c57   3         3         3       85s
```

**네임스페이스 사용 예**

ㅎ하나의 쿠버네티스 클러스터에 다양한 환경(개발, 테스트, 운영 환경 등)을 구현하고자 할 때

→ 하나의 네임스페이스 내에서는 오브젝트의 이름이 중복되는 것을 허용하지 않은

![image](https://github.com/Suah-Cho/STUDY/assets/102336763/aacb8c38-1095-496e-b97f-1746021f6fdd)

**네임스페이스의 서비스에 접근하기**

클러스터 내부에서는 서비스 이름을 이용해서 파드에 접근하는 것이 가능

⇒ 같은 네임 스페이스 서비스에 접근할 때는 서비스 이름만으로 접근이 가능

***같은 네임스페이스 내의 서비스에 접근할 때는 서비스 이름만으로 접근이 가능***

production네임스페이스에 테스트용 임시 파드를 생성해서 production네임스페이스의 서비스에 접근

```bash
vagrant@master-node:~$ kubectl run -it --rm debug --image=docker.io/busybox --restart=Never **-n production** /bin/sh
If you don't see a command prompt, try pressing enter.
/ #
/ #
/ # wget -q -O - hostname-svc-clusterip-ns:8080
<!DOCTYPE html>
<meta charset="utf-8" />
<link rel="stylesheet" type="text/css" href="./css/layout.css" />
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">

<div class="form-layout">
        <blockquote>
        <p>Hello,  hostname-deploy-ns-746f55c57-724t8</p>       </blockquote>
</div>
```

***다른 네임스페이스에 존재하는 서비스에는 서비스 이름만으로는 접근이 불가***

default 네임 스페이스에 생성된 테스트용 임시 파드는 production네임스페이스의 서비스에 접근할 수 없음

```bash
vagrant@master-node:~$ kubectl run -it --rm debug --image=docker.io/busybox --restart=Never /bin/sh
If you don't see a command prompt, try pressing enter.
/ # wget -q -O - hostname-svc-clusterip-ns:8080 
wget: bad address 'hostname-svc-clusterip-ns:8080'
```

다른 네임스페이스에 존재하는 서비스는 <서비스>.<네임스페이스 이름>.svc 처럼 서비스 이름 뒤에 네임스페이스 이름을 붙여서 접근해야한다.

```bash
/ # wget -q -O - hostname-svc-clusterip-ns.production.svc:8080
<!DOCTYPE html>
<meta charset="utf-8" />
<link rel="stylesheet" type="text/css" href="./css/layout.css" />
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">

<div class="form-layout">
        <blockquote>
        <p>Hello,  hostname-deploy-ns-746f55c57-pvskf</p>       </blockquote>
</div>
```

***네임스페이스 삭제***

네임스페이스를 삭제하면 네임스페이스에 존재하는 모든 리소스가 함께 삭제된다.

```bash
kubectl delete namespace production
namespace "production" deleted

vagrant@master-node:~$ kubectl get ns
NAME              STATUS   AGE
default           Active   6d6h
kube-node-lease   Active   6d6h
kube-public       Active   6d6h
kube-system       Active   6d6h
mynamespace       Active   32m
```

**네임스페이스에 속하는 오브젝트**

```bash
vagrant@master-node:~$ kubectl api-resources --namespaced=true
NAME                        SHORTNAMES   APIVERSION                     NAMESPACED   KIND
bindings                                 v1                             true         Binding
configmaps                  cm           v1                             true         ConfigMap
endpoints                   ep           v1                             true         Endpoints
events                      ev           v1                             true         Event
limitranges                 limits       v1                             true         LimitRange
persistentvolumeclaims      pvc          v1                             true         PersistentVolumeClaim
pods                        po           v1                             true         Pod
podtemplates                             v1                             true         PodTemplate
replicationcontrollers      rc           v1                             true         ReplicationController
resourcequotas              quota        v1                             true         ResourceQuota
secrets                                  v1                             true         Secret
serviceaccounts             sa           v1                             true         ServiceAccount
services                    svc          v1                             true         Service
controllerrevisions                      apps/v1                        true         ControllerRevision
daemonsets                  ds           apps/v1                        true         DaemonSet
deployments                 deploy       apps/v1                        true         Deployment
replicasets                 rs           apps/v1                        true         ReplicaSet
statefulsets                sts          apps/v1                        true         StatefulSet
localsubjectaccessreviews                authorization.k8s.io/v1        true         LocalSubjectAccessReview
horizontalpodautoscalers    hpa          autoscaling/v2                 true         HorizontalPodAutoscaler
cronjobs                    cj           batch/v1                       true         CronJob
jobs                                     batch/v1                       true         Job
leases                                   coordination.k8s.io/v1         true         Lease
networkpolicies                          crd.projectcalico.org/v1       true         NetworkPolicy
networksets                              crd.projectcalico.org/v1       true         NetworkSet
endpointslices                           discovery.k8s.io/v1            true         EndpointSlice
events                      ev           events.k8s.io/v1               true         Event
addresspools                             metallb.io/v1beta1             true         AddressPool
bfdprofiles                              metallb.io/v1beta1             true         BFDProfile
bgpadvertisements                        metallb.io/v1beta1             true         BGPAdvertisement
bgppeers                                 metallb.io/v1beta2             true         BGPPeer
communities                              metallb.io/v1beta1             true         Community
ipaddresspools                           metallb.io/v1beta1             true         IPAddressPool
l2advertisements                         metallb.io/v1beta1             true         L2Advertisement
pods                                     metrics.k8s.io/v1beta1         true         PodMetrics
ingresses                   ing          networking.k8s.io/v1           true         Ingress
networkpolicies             netpol       networking.k8s.io/v1           true         NetworkPolicy
poddisruptionbudgets        pdb          policy/v1                      true         PodDisruptionBudget
rolebindings                             rbac.authorization.k8s.io/v1   true         RoleBinding
roles                                    rbac.authorization.k8s.io/v1   true         Role
csistoragecapacities                     storage.k8s.io/v1              true         CSIStorageCapacity
```

**네임스페이스에 속하지 않는 오브젝트**

```bash
vagrant@master-node:~$ kubectl api-resources --namespaced=false
NAME                              SHORTNAMES   APIVERSION                             NAMESPACED   KIND
componentstatuses                 cs           v1                                     false        ComponentStatus
namespaces                        ns           v1                                     false        Namespace
nodes                             no           v1                                     false        Node
persistentvolumes                 pv           v1                                     false        PersistentVolume
mutatingwebhookconfigurations                  admissionregistration.k8s.io/v1        false        MutatingWebhookConfiguration
validatingwebhookconfigurations                admissionregistration.k8s.io/v1        false        ValidatingWebhookConfiguration
customresourcedefinitions         crd,crds     apiextensions.k8s.io/v1                false        CustomResourceDefinition
apiservices                                    apiregistration.k8s.io/v1              false        APIService
tokenreviews                                   authentication.k8s.io/v1               false        TokenReview
selfsubjectaccessreviews                       authorization.k8s.io/v1                false        SelfSubjectAccessReview
selfsubjectrulesreviews                        authorization.k8s.io/v1                false        SelfSubjectRulesReview
subjectaccessreviews                           authorization.k8s.io/v1                false        SubjectAccessReview
certificatesigningrequests        csr          certificates.k8s.io/v1                 false        CertificateSigningRequest
bgpconfigurations                              crd.projectcalico.org/v1               false        BGPConfiguration
bgpfilters                                     crd.projectcalico.org/v1               false        BGPFilter
bgppeers                                       crd.projectcalico.org/v1               false        BGPPeer
blockaffinities                                crd.projectcalico.org/v1               false        BlockAffinity
caliconodestatuses                             crd.projectcalico.org/v1               false        CalicoNodeStatus
clusterinformations                            crd.projectcalico.org/v1               false        ClusterInformation
felixconfigurations                            crd.projectcalico.org/v1               false        FelixConfiguration
globalnetworkpolicies                          crd.projectcalico.org/v1               false        GlobalNetworkPolicy
globalnetworksets                              crd.projectcalico.org/v1               false        GlobalNetworkSet
hostendpoints                                  crd.projectcalico.org/v1               false        HostEndpoint
ipamblocks                                     crd.projectcalico.org/v1               false        IPAMBlock
ipamconfigs                                    crd.projectcalico.org/v1               false        IPAMConfig
ipamhandles                                    crd.projectcalico.org/v1               false        IPAMHandle
ippools                                        crd.projectcalico.org/v1               false        IPPool
ipreservations                                 crd.projectcalico.org/v1               false        IPReservation
kubecontrollersconfigurations                  crd.projectcalico.org/v1               false        KubeControllersConfiguration
flowschemas                                    flowcontrol.apiserver.k8s.io/v1beta3   false        FlowSchema
prioritylevelconfigurations                    flowcontrol.apiserver.k8s.io/v1beta3   false        PriorityLevelConfiguration
nodes                                          metrics.k8s.io/v1beta1                 false        NodeMetrics
ingressclasses                                 networking.k8s.io/v1                   false        IngressClass
runtimeclasses                                 node.k8s.io/v1                         false        RuntimeClass
clusterrolebindings                            rbac.authorization.k8s.io/v1           false        ClusterRoleBinding
clusterroles                                   rbac.authorization.k8s.io/v1           false        ClusterRole
priorityclasses                   pc           scheduling.k8s.io/v1                   false        PriorityClass
csidrivers                                     storage.k8s.io/v1                      false        CSIDriver
csinodes                                       storage.k8s.io/v1                      false        CSINode
storageclasses                    sc           storage.k8s.io/v1                      false        StorageClass
volumeattachments                              storage.k8s.io/v1                      false        VolumeAttachment
```

**kubectl 커맨드의 기본네임스페이스 설정**

***test-env네임스페이스를 생성***

```bash
vagrant@master-node:~$ kubectl create namespace test-env
namespace/test-env created

vagrant@master-node:~$ kubectl get ns
NAME              STATUS   AGE
default           Active   6d6h
kube-node-lease   Active   6d6h
kube-public       Active   6d6h
kube-system       Active   6d6h
mynamespace       Active   57m
test-env          Active   16s
```

***현재 설정된 네임스페이스의 모든 리소스를 조회 ⇒ 네임스페이스를 명시하지 않으면 default네임스페이스에서 조회***

```bash
vagrant@master-node:~$ kubectl get all
NAME                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
service/kubernetes           ClusterIP   172.17.0.1      <none>        443/TCP   3h9m
```

***현재 설정된 컨텍스트를 확인하고 기본으로 사용될 네임스페이스를  test-env 변경***

컨텍스트 ⇒ 클러스터(kubectl이 사용할 쿠버네티스 API서버의 접속 정보 목록)와 사용자 항목(쿠버네티스의 API서버에 접속하기 위한 사용자 인증 정보 목록)을 조합한 값 목록

```bash
vagrant@master-node:~$ kubectl config get-contexts
CURRENT   NAME                          CLUSTER      AUTHINFO           NAMESPACE
*         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin
vagrant@master-node:~$ kubectl config set-context --current --namespace=test-env
Context "kubernetes-admin@kubernetes" modified.
vagrant@master-node:~$ kubectl config get-contexts
CURRENT   NAME                          CLUSTER      AUTHINFO           NAMESPACE
*         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin   **test-env**
```

***현재 설정된 네임스페이스의 모든 리소스를 조회***

```bash
vagrant@master-node:~$ kubectl get all
No resources found in test-env namespace.
```

***현재 컨텍스트에서 기본으로 사용될 네임스페이스를 default로 변경하고 test-env네임스페이스를 삭제***

```bash
vagrant@master-node:~$ kubectl config set-context --current --namespace=default
Context "kubernetes-admin@kubernetes" modified.

vagrant@master-node:~$ kubectl delete namespace test-env
namespace "test-env" deleted

vagrant@master-node:~$ kubectl get ns
NAME              STATUS   AGE
default           Active   6d6h
kube-node-lease   Active   6d6h
kube-public       Active   6d6h
kube-system       Active   6d6h
mynamespace       Active   71m
```

## 컨피그맵(configmap), 시크릿(secret) : 설정값을 파드에 전달

애플리케이션의 설정 정보나 패스워드나 같은 인증 정보는 컨테이너에 담지 말고 분리해서 네임스페이스에 저장하고 컨테이너가 읽도록 하면, 테스트 환경, 프로덕션 환경 별로 빌드할 필요가 없다.

**네임 스페이스에 저장한 설정 정보를 “컨피그맵”이라고 하고, 인증 정보와 같이 보안이 필요한 정보를 “시크릿”이라고 한다.**

컨테이너에서는 컨피그맵 또는 시크릿을 `파일 시스템으로 마운트`해서 읽거나 `환경 변수로 참조`할 수 있다.

![image](https://github.com/Suah-Cho/STUDY/assets/102336763/47f54087-791c-435c-935b-8b8ac118ad0c)

### **컨피그맵**

일반적인 설정 정보를 담아 저장할 수 있는 쿠버네티스 오브젝트

네임스페이스에 속하기 때문에 네임스페이스별로 컨피그맵이 존재한다.

**컨피그맵 생성**

YAML 파일을 사용해 생성할 수 있으나, kubectl create configmap 명령어로 쉽게 생성

```bash
vagrant@master-node:~$ kubectl create configmap log-level-configmap --from-literal LOG_LEVEL=DEBUG
configmap/log-level-configmap created

vagrant@master-node:~$ kubectl create configmap config-k8s --from-literal k8s=kubernetes --from-literal container=docker
configmap/config-k8s created                   ~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                             컨피그맵의 이름  컨피그맵에 저장될 값의 키 = 값 형식으로 정의
```

**컨피그맵 확인**

```bash
vagrant@master-node:~$ kubectl get configmap  =>kubectl get cm
NAME                  DATA   AGE
config-k8s            2      3m7s
kube-root-ca.crt      1      6d7h
log-level-configmap   1      4m26s

vagrant@master-node:~$ kubectl describe configmap log-level-configmap
Name:         log-level-configmap
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
**LOG_LEVEL:       <= 키**
----
**DEBUG            <= 값**

BinaryData
====

Events:  <none>

vagrant@master-node:~$ kubectl get configmap log-level-configmap -o yaml
apiVersion: v1
data:
  **LOG_LEVEL: DEBUG      <= 키:값**
kind: ConfigMap
metadata:
  creationTimestamp: "2023-10-12T06:53:40Z"
  name: log-level-configmap
  namespace: default
  resourceVersion: "179280"
  uid: 38638f02-e581-4793-8829-7b72673a99a7
```

### **파드에서 컨피그맵을 사용하는 방법** **1. 컨피그맵의 값을 파드의 환경변수로 사용**

**컨피그맵에 정의된 모든 키-값 쌍을 파드의 환경 변수로 설정**

cm-to-env-all.yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: cm-to-env-all
spec:
  containers:
  - name: my-container
    image: docker.io/busybox
    args: ['tail', '-f', '/dev/null']
    envFrom:                      ## 컨피그맵에 정의된 모든 키-값 쌍을 가져와서 환경변수로 설정
    - configMapRef:
        name: log-level-configmap ## LOG_LEVEL=DEBUG
    - configMapRef:
        name: config-k8s          ## k8s=kubernetes, container=docker
```

```yaml
vagrant@master-node:~$ kubectl apply -f cm-to-env-all.yaml
pod/cm-to-env-all created

vagrant@master-node:~$ kubectl get pod
NAME            READY   STATUS    RESTARTS   AGE
cm-to-env-all   1/1     Running   0          4m50s

vagrant@master-node:~$ kubectl exec cm-to-env-all -- env
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
TERM=xterm
HOSTNAME=cm-to-env-all
**LOG_LEVEL=DEBUG
container=docker
k8s=kubernetes**
KUBERNETES_SERVICE_HOST=172.17.0.1
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_PORT_443_TCP_ADDR=172.17.0.1
PRODUCTION_SERVICE_PORT=tcp://172.17.20.176:80
PRODUCTION_SERVICE_PORT_80_TCP_ADDR=172.17.20.176
PRODUCTION_SERVICE_PORT_80_TCP=tcp://172.17.20.176:80
PRODUCTION_SERVICE_PORT_80_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP_PROTO=tcp
PRODUCTION_SERVICE_SERVICE_HOST=172.17.20.176
PRODUCTION_SERVICE_SERVICE_PORT=80
KUBERNETES_PORT=tcp://172.17.0.1:443
KUBERNETES_PORT_443_TCP=tcp://172.17.0.1:443
PRODUCTION_SERVICE_PORT_80_TCP_PORT=80
KUBERNETES_SERVICE_PORT=443
HOME=/root

vagrant@master-node:~$ kubectl delete -f cm-to-env-all.yaml
pod "cm-to-env-all" deleted
```

**컨피그맵에 존재하는 키-값 쌍 중 원하는 데이터만 파드의 환경 변수로 설정**

cm-to-env-selective.yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: cm-to-env-selective
spec:
  containers:
  - name: my-container
    image: docker.io/busybox
    args: ['tail', '-f', '/dev/null']
    env:
    - name: NEW_LOG_LEVEL             ## 새롭게 설정할 환경변수의 이름
      valueFrom:
        configMapKeyRef:
          name: log-level-configmap   ## 참조할 컨피그맵의 이름
          key: LOG_LEVEL              ## 가져올 데이터의 키
    - name: NEW_CONTAINER            
      valueFrom:
        configMapKeyRef:
          name: config-k8s
          key: container
```

```bash
vagrant@master-node:~$ kubectl apply -f cm-to-env-selective.yaml
pod/cm-to-env-selective created

vagrant@master-node:~$ kubectl get pod
NAME                  READY   STATUS    RESTARTS   AGE
cm-to-env-selective   1/1     Running   0          6s

vagrant@master-node:~$ kubectl exec cm-to-env-selective -- env
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
TERM=xterm
HOSTNAME=cm-to-env-selective
NEW_LOG_LEVEL=DEBUG
NEW_CONTAINER=docker
PRODUCTION_SERVICE_SERVICE_PORT=80
KUBERNETES_SERVICE_HOST=172.17.0.1
PRODUCTION_SERVICE_PORT_80_TCP_PORT=80
PRODUCTION_SERVICE_PORT_80_TCP_ADDR=172.17.20.176
KUBERNETES_SERVICE_PORT=443
KUBERNETES_PORT_443_TCP_PROTO=tcp
PRODUCTION_SERVICE_PORT=tcp://172.17.20.176:80
PRODUCTION_SERVICE_PORT_80_TCP=tcp://172.17.20.176:80
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_PORT=tcp://172.17.0.1:443
KUBERNETES_PORT_443_TCP=tcp://172.17.0.1:443
KUBERNETES_PORT_443_TCP_ADDR=172.17.0.1
PRODUCTION_SERVICE_SERVICE_HOST=172.17.20.176
PRODUCTION_SERVICE_PORT_80_TCP_PROTO=tcp
HOME=/root

vagrant@master-node:~$ kubectl delete -f cm-to-env-selective.yaml
pod "cm-to-env-selective" deleted
```

### 파드에서 컨피그맵을 사용하는 방법 2. 컨피그맵의 값을 파드 내부의 파일로 마운트해서 사용

**컨피그맵의 모든 키-값 데이터를 파드에 마운트**

cm-to-volume-all.yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: cm-to-volume-all
spec:
  containers:
  - name: my-container
    image: docker.io/busybox
    args: ['tail', '-f', '/dev/null']
    volumeMounts:
    - name: configmap-volume
      mountPath: /etc/config
  volumes:
  - name: configmap-volume
    configMap:
      name: config-k8s
```

```bash
vagrant@master-node:~$ kubectl apply -f cm-to-volume-all.yaml
pod/cm-to-volume-all created

vagrant@master-node:~$ kubectl get pod
NAME               READY   STATUS    RESTARTS   AGE
cm-to-volume-all   1/1     Running   0          8s

vagrant@master-node:~$ kubectl exec cm-to-volume-all -- ls /etc/config
container  
k8s     //컨피그맵의 키 이름과 동일한 파일이 생성된 것을 확인

vagrant@master-node:~$ kubectl exec cm-to-volume-all -- cat /etc/config/container
docker    //container 키에 해당하는 데이터가 파일에 저장된 것을 확인

kubectl exec cm-to-volume-all -- cat /etc/config/k8s
kubernetes    //k8s 키에 해당하는 데이터가 파일에 저장된 것을 확인
```

⇒ 컨피그맵의 키는 파일의 이름으로, 같은 파일의 내용으로 들어가는 것을 확인

**컨피그맵에 존재하는 키-값 쌍 중 원하는 데이터만 파드에 마운트**

cm-to-volume-selective.yaml
