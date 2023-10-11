## LoadBalancer 타입의 서비스

일반적으로 온프레미스 환경에서는 NodePort 타입의 서비스를 사용하고, 퍼블릭 클라우드 환경에서는 LoadBalancer 타입의 서비스를 사용해서 애플리케이션을 외부에 노출

- 로드밸런서
    - 서버에 가해지는 부하를 분산해 주는 장치 또는 기술의 통칭
    - **L4 로드밸런서**
        - 네트워크 계층 또는 트랜스포트 계층의 정보를 기반으로 부하 분산
        - IP주소 또는 PORT 주소를 이용
        - 쿠버네티스에서 말하는 일반적인 로드밸런서는 L4로드밸런서의 기능을 수행
    - **L7 로드밸런서**
        - 애플리케이션 계층의 정보를 기반으로 부하 분산
        - URL, HTTP 헤더, Cookie 등과 같은 사용자 요청 정보를 이용
        - 쿠버네티스에서 L7 로드밸런서 기능을 인그레스(Ingress)를 사용해 구현

![image](https://github.com/Suah-Cho/STUDY/assets/102336763/404738e8-8ffb-4599-af34-57005d9e293d)


### **TO DO** **클라우드 플랫폼에서 LoadBalancer타입의 서비스를 연동**

### **온프레미스 환경에서 LoadBalancer타입의 서비스를 연동**

온프레미스 환경 : 클러스터 내부에 로드밸런서 서비스를 받아 주는 구성이 필요 ⇒ MetalLB 가 담당

**1. MetalLB**

- 쿠버네티스 클러스터 내에서 로드 밸런싱을 제공하기 위한 오픈 소스 프로젝트
- 클라우드 공급자에서 실행되지 않는 클러스터에서 LoadBalancer 유형의 쿠버네티스 서비스 생성이 가능

**2. 로드밸런서가 없는 환경에서 LoadBalancer(쿠버네티스의 서비스 중 하나) 타입의 서비스를 노출**

```bash
vagrant@master-node:~$ kubectl create deployment my-nginx --image=docker.io/nginx
deployment.apps/my-nginx created

vagrant@master-node:~$ kubectl get pod
NAME                       READY   STATUS    RESTARTS   AGE
my-nginx-9bcccb77c-6489k   1/1     Running   0          10s

vagrant@master-node:~$ kubectl expose deployment my-nginx --port 80 --type LoadBalancer
service/my-nginx exposed

vagrant@master-node:~$ kubectl get service
NAME         TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes   ClusterIP      172.17.0.1      <none>        443/TCP        5d
my-nginx     LoadBalancer   172.17.58.154   **<pending>**     80:30422/TCP   12s
                                            **~~~~~~~~~
                                            로드밸런서가 존재하지 않기 때문에 Pending 상태가 지속**
```

**3. Service, Deployment 삭제**

```bash
vagrant@master-node:~$ kubectl delete deployment my-nginx
deployment.apps "my-nginx" deleted
vagrant@master-node:~$ kubectl delete service my-nginx
service "my-nginx" deleted
vagrant@master-node:~$ kubectl get all
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   172.17.0.1   <none>        443/TCP   5d
```

**[MetalLB 설치](https://metallb.universe.tf/installation/)**

**4. strictARP mode 활성화**

```bash
vagrant@master-node:~$ kubectl get configmap kube-proxy -n kube-system -o yaml | \
sed -e "s/strictARP: false/strictARP: true/" | \
kubectl apply -f - -n kube-system
Warning: resource configmaps/kube-proxy is missing the kubectl.kubernetes.io/last-applied-configuration annotation which is required by kubectl apply. kubectl apply should only be used on resources created declaratively by either kubectl create --save-config or kubectl apply. The missing annotation will be patched automatically.
configmap/kube-proxy configured
```

**5. MetalLB 설치**

```bash
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.11/config/manifests/metallb-native.yaml

vagrant@master-node:~$ kubectl get all -n metallb-system
NAME                              READY   STATUS              RESTARTS   AGE
pod/controller-64f57db87d-lv5rl   0/1     Running             0          25s
pod/speaker-64lcd                 0/1     ContainerCreating   0          25s
pod/speaker-89sp9                 0/1     ContainerCreating   0          25s
pod/speaker-9b56x                 0/1     ContainerCreating   0          25s

NAME                      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
service/webhook-service   ClusterIP   172.17.36.240   <none>        443/TCP   25s

NAME                     DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
daemonset.apps/speaker   3         3         0       3            0           kubernetes.io/os=linux   25s

NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/controller   0/1     1            0           25s

NAME                                    DESIRED   CURRENT   READY   AGE
replicaset.apps/controller-64f57db87d   1         1         0       25s

```

**6. LoadBalancer 서비스에 할당할 IP대역을 정의 ⇒ VirtualBox Host-Only 네트워크 관리자의 설정을 확인**

![image](https://github.com/Suah-Cho/STUDY/assets/102336763/5d042d51-6862-49c6-bc5d-04f776a9e5da)


routing-config.yaml

```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: first-pool
  namespace: metallb-system
spec:
  addresses:
  - 10.0.0.30-10.0.0.254
```

```bash
vagrant@master-node:~$ kubectl get IPAddressPool -n metallb-system
NAME         AUTO ASSIGN   AVOID BUGGY IPS   ADDRESSES
first-pool   true          false             ["10.0.0.30-10.0.0.254"]

vagrant@master-node:~$ kubectl get IPAddressPool -n metallb-system
NAME         AUTO ASSIGN   AVOID BUGGY IPS   ADDRESSES
first-pool   true          false             ["10.0.0.30-10.0.0.254"]
```

**7. 디플로이먼트와 서비스를 생성 후 EXTERNAL-IP가 할당되는 것을 호가인**

```bash
vagrant@master-node:~$ kubectl create deployment my-nginx --image=docker.io/nginx
deployment.apps/my-nginx created
vagrant@master-node:~$ kubectl get deployment,pod
NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/my-nginx   1/1     1            1           9s

NAME                           READY   STATUS    RESTARTS   AGE
pod/my-nginx-9bcccb77c-k8pwd   1/1     Running   0          9s
vagrant@master-node:~$ kubectl expose deployment my-nginx --port 80 --type LoadBalancer
service/my-nginx exposed
vagrant@master-node:~$ kubectl get service
NAME         TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
kubernetes   ClusterIP      172.17.0.1     <none>        443/TCP        5d1h
my-nginx     LoadBalancer   172.17.2.207   10.0.0.30     80:31204/TCP   5s
```

**8. EXTERNAL-IP로 접속**

```bash
vagrant@master-node:~$ wget -q -O - http://10.0.0.30
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
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

**9. 노드 IP와 포트(공개 포트)로 접근**

```bash
vagrant@master-node:~$ wget -q -O - http://10.0.0.10:31204
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
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

**10. 디플로이먼트를 추가 생성 및노출**

```bash
vagrant@master-node:~$ kubectl apply -f hostname-deployment.yaml
deployment.apps/hostname-deployment created

vagrant@master-node:~$ kubectl get deployment
NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
hostname-deployment   3/3     3            3           15s
my-nginx              1/1     1            1           34m

vagrant@master-node:~$ kubectl expose deployment hostname-deployment --port 80 --type LoadBalancer
service/hostname-deployment exposed
```

**11. 서비스 확인**

```bash
vagrant@master-node:~$ kubectl get service
NAME                  TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
**hostname-deployment   LoadBalancer   172.17.35.246   10.0.0.31     80:31945/TCP   43s**
kubernetes            ClusterIP      172.17.0.1      <none>        443/TCP        5d1h
my-nginx              LoadBalancer   172.17.2.207    10.0.0.30     80:31204/TCP   35m

vagrant@master-node:~$ wget -q -O - http://10.0.0.31:80 | grep Hello
        <p>Hello,  hostname-deployment-85cbb79457-**8ttxf**</p>     </blockquote>
vagrant@master-node:~$ wget -q -O - http://10.0.0.31:80 | grep Hello
        <p>Hello,  hostname-deployment-85cbb79457-**57nrk**</p>     </blockquote>
vagrant@master-node:~$ wget -q -O - http://10.0.0.31:80 | grep Hello
        <p>Hello,  hostname-deployment-85cbb79457-**6gq6r**</p>     </blockquote>
```

**12. 리소스 정리**

```bash
vagrant@master-node:~$ kubectl delete service my-nginx
service "my-nginx" deleted
vagrant@master-node:~$ kubectl delete service hostname-deployment
service "hostname-deployment" deleted
vagrant@master-node:~$ kubectl delete deployment my-nginx
deployment.apps "my-nginx" deleted
vagrant@master-node:~$ kubectl delete deployment hostname-deployment
deployment.apps "hostname-deployment" deleted
vagrant@master-node:~$ kubectl delete namespace metallb-system
namespace "metallb-system" deleted

vagrant@master-node:~$ kubectl get all
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   172.17.0.1   <none>        443/TCP   5d1h
vagrant@master-node:~$ kubectl get namespace
NAME              STATUS   AGE
default           Active   5d1h
kube-node-lease   Active   5d1h
kube-public       Active   5d1h
kube-system       Active   5d1h
```
