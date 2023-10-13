<details>
<summary>용어</suammry>
<div markdown="1">

- docker
    - 컨테이너 생성 실행 관리 도구
    - 제약 사항
        - 하나의 단일 노드(하나의 서버)에서만 컨테이너를 생성 실행 관리 한다.
    - compose
        - 한 개 이상의 컨테이너를 관리할 때 사용

</div>
</details>
    

### 파일로부터 컨피그맵 생성

nginx의 설정 파일인 nginx.conf 또는 MySQL의 설정 파일인 mysql/conf의 내용을 통째로 컨피그맵에 저장한 뒤 이를 볼륨 파일 또는 파드 내부에 제공할 수 있도록 컨피그맵을 파일로부터 생성하는 기능을 제공

**파일 내용 전체를 컨피그맵의 값으로 설정**

```bash
vagrant@master-node:~$ echo Hello, k8s! >> index.html

vagrant@master-node:~$ cat index.html
Hello, k8s!

vagrant@master-node:~$ kubectl create configmap cm-from-file-without-key --from-file index.html
configmap/cm-from-file-without-key created   // 컨피그맵의 키를 지정하지 않고 컨피그맵을 생성

vagrant@master-node:~$ kubectl describe configmap cm-from-file-without-key
Name:         cm-from-file-without-key
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
**index.html:   // 파일 이름 = key**
----
**Hello, k8s!   // 파일 내용 = value**

BinaryData
====

Events:  <none>

vagrant@master-node:~$ kubectl create configmap cm-from-file-with-key --from-file INDEXFILE=i
ndex.html
configmap/cm-from-file-with-key created

vagrant@master-node:~$ kubectl describe configmap cm-from-file-with-key
Name:         cm-from-file-with-key
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
INDEXFILE:   **//지정된 값이 key로 저장**
----
Hello, k8s!  **//파일 내용을 값으로 설정**

BinaryData
====

Events:  <none>
```

**여러 개의 키-값 형식의 내용으로 구성된 설정 파일을 컨피그맵으로 설정**

multiple-key-value.ini

```yaml
driver-class-name=com.mysql.cj.jdbc.Driver
jdbc-url=jdbc:mysql://localhost:3306/springbootdb
username=root
password=p@ssw0rd
```

```bash
vagrant@master-node:~$ kubectl create configmap cm-from-ini-file --from-env-file multiple-key-value.ini
configmap/cm-from-ini-file created

vagrant@master-node:~$ kubectl describe configmap cm-from-ini-file
Name:         cm-from-ini-file
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
**driver-class-name:  // 설정 파일의 키에 해당하는 값**
----
**com.mysql.cj.jdbc.Driver   // 설정 파일의 값에 해당하는 값**
**jdbc-url:**
----
**jdbc:mysql://localhost:3306/springbootdb
password:**
----
**p@ssw0rd
username:**
----
**root**

BinaryData
====

Events:  <none>
```

**모든 컨피그맵 삭제**

```bash
vagrant@master-node:~$ kubectl delete configmap cm-from-file-with-key
configmap "cm-from-file-with-key" deleted
vagrant@master-node:~$ kubectl delete configmap cm-from-file-without-key
configmap "cm-from-file-without-key" deleted
vagrant@master-node:~$ kubectl delete configmap cm-from-ini-file
configmap "cm-from-ini-file" deleted
vagrant@master-node:~$ kubectl delete configmap config-k8s
configmap "config-k8s" deleted
vagrant@master-node:~$ kubectl delete configmap log-level-configmap
configmap "log-level-configmap" deleted
vagrant@master-node:~$ kubectl get configmap
NAME               DATA   AGE
kube-root-ca.crt   1      7d1h
```

### **YAML파일로 컨피그맵 정의**

kubectl create 명령에서  —dry-run옵션과 -o yaml 옵션을 사용해서 컨피그맵을 생성하지 않고 컨피그맵 설정을 yaml파일로 export할 수 있으며, 해당 파일을 이용해서 컨피그맵을 생성할 수 있다.

**컨피그맵을 생성하지 않고 YAML 파일 형식으로 출력**

```bash
vagrant@master-node:~$ kubectl create configmap cm-by-dry-run --from-literal mykey=myvalue --dry-run=client -o yaml
apiVersion: v1
data:
  mykey: myvalue
kind: ConfigMap
metadata:
  creationTimestamp: null
  name: cm-by-dry-run
```

**출력을 리다이렉트해서 YAML파일을 생성**

```bash
vagrant@master-node:~$ kubectl create configmap cm-by-dry-run --from-literal mykey=myvalue --dry-run=client -o yaml > my-configmap.yaml
vagrant@master-node:~$ cat my-configmap.yaml
apiVersion: v1
data:
  mykey: myvalue
kind: ConfigMap
metadata:
  creationTimestamp: null
  name: cm-by-dry-run
```

**YAML 파일을 이용해서 컨피그맵을 생성**

```bash
vagrant@master-node:~$ kubectl apply -f my-configmap.yaml
configmap/cm-by-dry-run created
vagrant@master-node:~$ kubectl describe configmap cm-by-dry-run
Name:         cm-by-dry-run
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
mykey:
----
myvalue

BinaryData
====

Events:  <none>
```

**YAML 형식을 출력을 kubectl apply -f 명령어의 입력으로 전달해서 생성하는 방법도 존재**

```bash
vagrant@master-node:~$ kubectl create configmap cm-by-dry-run2 --from-literal mykey=myvalue --dry-run=client -o yaml | kubectl apply -f -
configmap/cm-by-dry-run2 created
vagrant@master-node:~$ kubectl describe configmap cm-by-dry-run2
Name:         cm-by-dry-run2
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
mykey:
----
myvalue

BinaryData
====

Events:  <none>
```

## 시크릿(Secret)

민감한 정보를 저장하기 위한 용도로 사용

네임스페이스에 종속되는 쿠버네티스 오브젝트

**시크릿 생성 방법**

—form-literal옵션을 이용

```bash
vagrant@master-node:~$ kubectl create secret generic my-password --from-literal password=p@ss
w0rd
secret/my-password created
vagrant@master-node:~$ kubectl get secret
NAME          TYPE                             DATA   AGE
my-password   Opaque                           1      8s
regcred       kubernetes.io/dockerconfigjson   1      6d22h
```

- Opaque
    - 시크릿 종류를 명시하지 않을 경우 자동으로 설정되는 타입
    - 사용자가 정의하는 데이터를 저장하는 일반 목적의 시크릿
    - kubectl create secret 명령어로 시크릿을 생성할 때는 generic으로 명시

**—from-file 옵션을 이용**

```bash
vagrant@master-node:~$ echo mypassword > pw1 && echo yourpassword > pw2
vagrant@master-node:~$ ls pw*
pw1  pw2
vagrant@master-node:~$ kubectl create secret generic our-password --from-file pw1 --from-file pw2
secret/our-password created
```

**시크릿 내용 확인**

```bash
vagrant@master-node:~$ kubectl get secret
NAME           TYPE                             DATA   AGE
my-password    Opaque                           1      5m50s
our-password   Opaque                           2      25s
regcred        kubernetes.io/dockerconfigjson   1      6d22h
vagrant@master-node:~$ kubectl describe secret our-password
Name:         our-password
Namespace:    default
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
**pw1:  11 bytes     // 파일 이름이 키로 사용되고 있고, 시크릿 키: 값의 크기(byte)형식으로 출력되는 것을 확인
pw2:  13 bytes**
```

```bash
vagrant@master-node:~$ kubectl get secret our-password -o yaml
apiVersion: v1
data:
  **pw1: bXlwYXNzd29yZAo=        // 시크릿의 값이 BASE64로 인코딩되어 있는 것을 확인
  pw2: eW91cnBhc3N3b3JkCg==**
kind: Secret
metadata:
  creationTimestamp: "2023-10-13T01:50:05Z"
  name: our-password
  namespace: default
  resourceVersion: "199646"
  uid: e5e0cebf-0cd6-4fed-a91a-85c21ca9b691
type: Opaque

vagrant@master-node:~$ echo bXlwYXNzd29yZAo= | base64 -d
mypassword
vagrant@master-node:~$ echo eW91cnBhc3N3b3JkCg= | base64 -d
yourpassword
```

### **파드에서 시크릿을 사용하는 방법 1. 시크릿의 값을 파드의 환경변수로 사용**

**시크릿에 저장된 모든 키-값 쌍을 파드의 환경 변수로 설정**

secret-env-from-all.yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-env-from-all
spec:
  contianers:
  - name: my-container
    image: docker.io/busybox
    args: ['tail', '-f', '/dev/null']
    envFrom:
    - secretRef:
        name: my-password
```

```bash
vagrant@master-node:~$ kubectl apply -f secret-env-from-all.yaml
pod/secret-env-from-all created

vagrant@master-node:~$ kubectl get pod
NAME                     READY   STATUS    RESTARTS   AGE
secret-env-from-all      1/1     Running   0          8s

vagrant@master-node:~$ kubectl exec secret-env-from-all -- env
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
TERM=xterm
HOSTNAME=secret-env-from-all
**password=p@ssw0rd**
PRODUCTION_SERVICE_PORT_80_TCP=tcp://172.17.20.176:80
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP_ADDR=172.17.0.1
PRODUCTION_SERVICE_PORT_80_TCP_ADDR=172.17.20.176
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT=tcp://172.17.0.1:443
PRODUCTION_SERVICE_SERVICE_HOST=172.17.20.176
PRODUCTION_SERVICE_SERVICE_PORT=80
PRODUCTION_SERVICE_PORT=tcp://172.17.20.176:80
KUBERNETES_SERVICE_HOST=172.17.0.1
KUBERNETES_PORT_443_TCP=tcp://172.17.0.1:443
PRODUCTION_SERVICE_PORT_80_TCP_PROTO=tcp
PRODUCTION_SERVICE_PORT_80_TCP_PORT=80
KUBERNETES_SERVICE_PORT=443
KUBERNETES_PORT_443_TCP_PORT=443
HOME=/root
```

**시크릿에 저장된 키-값 쌍 중 원하는 데이터만 파드의 환경 변수로 설정**

secret-env-from-selective.yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-env-from-selective
spec:
  containers:
  - name: my-container
    image: docker.io/busybox
    args: ['tail', '-f', '/dev/null']
    env:
    - name: YOUR_PASSWORD
      valueFrom:
        secretKeyRef:
          name: our-password
          key: pw2
```

```bash
vagrant@master-node:~$ kubectl apply -f secret-env-from-selective.yaml
pod/secret-env-from-selective created

vagrant@master-node:~$ kubectl get pod
NAME                        READY   STATUS              RESTARTS   AGE
secret-env-from-selective   1/1     Running             0          4s

vagrant@master-node:~$ kubectl exec secret-env-from-selective -- env
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
TERM=xterm
HOSTNAME=secret-env-from-selective
**YOUR_PASSWORD=yourpassword**

PRODUCTION_SERVICE_PORT_80_TCP_ADDR=172.17.20.176
PRODUCTION_SERVICE_SERVICE_HOST=172.17.20.176
PRODUCTION_SERVICE_SERVICE_PORT=80
PRODUCTION_SERVICE_PORT_80_TCP=tcp://172.17.20.176:80
PRODUCTION_SERVICE_PORT_80_TCP_PORT=80
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP_ADDR=172.17.0.1
KUBERNETES_SERVICE_HOST=172.17.0.1
KUBERNETES_PORT=tcp://172.17.0.1:443
PRODUCTION_SERVICE_PORT=tcp://172.17.20.176:80
PRODUCTION_SERVICE_PORT_80_TCP_PROTO=tcp
KUBERNETES_SERVICE_PORT=443
KUBERNETES_PORT_443_TCP=tcp://172.17.0.1:443
HOME=/root
```

### **파드에서 시크릿을 사용하는 방법 2. 시크릿의 값을 파드 내부의 파일로 마운트해서 사용**

**시크릿의 모든 키-값 데이터를 파드에 마운트**

secret-volume-from-all.yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-volume-from-all
spec:
  containers:
  - name: my-container
    image: docker.io/busybox
    args: ['tail', '-f', '/dev/null']
    volumeMounts:                ## 생성한 볼륨을 컨테이너에 마운트(맵핑)
    - name: secret-volume        ## 마운트할 볼륨 이름
      mountPath: /etc/secret     ## 컨테이너의 디렉터리
  volumes:
  - name: secret-volume
    secret:
      secretName: our-password   ## 볼륨에 맵핑될 시크릿의 이름
```

```bash
vagrant@master-node:~$ kubectl apply -f secret-volume-from-all.yaml
pod/secret-volume-from-all created

vagrant@master-node:~$ kubectl get pod
NAME                     READY   STATUS    RESTARTS   AGE
cm-to-volume-selective   1/1     Running   1          18h
secret-volume-from-all   1/1     Running   0          5s

vagrant@master-node:~$ kubectl exec secret-volume-from-all -- ls /etc/secret 
pw1
pw2

vagrant@master-node:~$ kubectl exec secret-volume-from-all -- cat /etc/secret/pw1
mypassword
vagrant@master-node:~$ kubectl exec secret-volume-from-all -- cat /etc/secret/pw2
yourpassword
```

**시크릿에 존재하는 키-값 중 원하는 데이터만 파드에 마운트**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-volume-from-selective
spec:
  containers:
  - name: my-container
    image: docker.io/busybox
    args: ['tail', '-f', '/dev/null']
    volumeMounts:                ## 생성한 볼륨을 컨테이너에 마운트(맵핑)
    - name: secret-volume        ## 마운트할 볼륨 이름
      mountPath: /etc/secret     ## 컨테이너의 디렉터리
  volumes:
  - name: secret-volume
    secret:
      secretName: our-password   ## 볼륨에 맵핑될 시크릿의 이름
      items:
      - key: pw1
        path: password1
```

```bash
vagrant@master-node:~$ kbuectl apply -f secret-volume-from-selective.yaml
-bash: kbuectl: command not found
vagrant@master-node:~$ kubectl apply -f secret-volume-from-selective.yaml
pod/secret-volume-from-selective created
vagrant@master-node:~$ kubectl get pod
NAME                           READY   STATUS    RESTARTS   AGE
cm-to-volume-selective         1/1     Running   1          18h
secret-volume-from-selective   1/1     Running   0          5s
vagrant@master-node:~$ kubectl exec secret-volume-from-selective -- ls /etc/secret
password1
vagrant@master-node:~$ kubectl exec secret-volume-from-selective -- cat /etc/secret/password1
mypassword
```

### 시크릿 타입

https://kubernetes.io/ko/docs/concepts/configuration/secret/#secret-types

| 빌트인 타입 | 사용처 |
| --- | --- |
| Opaque | 임의의 사용자 정의 데이터 |
| kubernetes.io/service-account-token | 서비스 어카운트 토큰 |
| kubernetes.io/dockercfg | 직렬화 된(serialized) ~/.dockercfg 파일 |
| kubernetes.io/dockerconfigjson | 직렬화 된 ~/.docker/config.json 파일 |
| kubernetes.io/basic-auth | 기본 인증을 위한 자격 증명(credential) |
| kubernetes.io/ssh-auth | SSH를 위한 자격 증명 |
| kubernetes.io/tls | TLS 클라이언트나 서버를 위한 데이터 |
| bootstrap.kubernetes.io/token | 부트스트랩 토큰 데이터 |

## 잡과 크론잡(Job, CronJob)

### 잡(Job)

일회성 또는 배치 작업을 실행하기 위한 객체

주로 한 번 실행하고 완료해야 하는 작업을 정의하는데 사용

파드의 모든 컨테이너가 정상적으로 종료할 때까지 재실행

특정 개수 만큼의 파드를 정상적으로 실행 종료되는 것을 보장

### 잡 컨트롤러의 특징

- 지정한 실행 횟수와 병행 개수에 따라 한 개 이상의 파드를 실행
- 잡은 파드 내에 있는 모든 컨테이너가 정상 종료한 경우에 파드를 정상 종료한 것으로 취급
- 잡에 기술한 파드의 실행 회수를 전부 정상 종료하면, 잡은 종료
- 노드 장애 등에 의해 잡의 파드가 제거된 경우, 다른 노드에 파드를 재실행

![Alt text](image-4.png)

### 잡 활용 예

**1) 동시 실행과 순차 실행**

![Alt text](image-3.png)

**2) 파드를 실행할 노드를 선택**

![Alt text](image-2.png)

**3) 온라인 배치 처리 요청**

![Alt text](image-1.png)

**4) 정기 실행 배치 처리**

크론잡은 설정한 시간에 정기적으로 잡을 실행 ⇒ 데이터의 백업이나 매시간 마다 실행되는 배치 처리 등을 실행

### 잡 병렬성 관리

잡 하나가 동시에 실행할 파드를 지정

.spec.parallelism 필드에 설정

기본값은 1이고, 0으로 설정하면 잡을 정지

**잡을 이용해서 정상적으로 종료되는 파드를 실행**

job-normal-end.yaml

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: job-normal-end
spec:
  template:
    spec:
      containers:
      - name: busybox
        image: docker.io/busybox
        command: ["sh", "-c", "sllep 5; exit0"]
      imagePullSecrets:
      - name: regcred
      restartPolicy: Never
  completions: 6
```

```bash
vagrant@master-node:~$ kubectl apply -f job-normal-end.yaml
job.batch/job-normal-job created
vagrant@master-node:~$ kubectl get job
NAME             COMPLETIONS   DURATION   AGE
job-normal-job   0/6           6s

```

**parallelism을 설정해서 병렬로 실행**

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: job-normal-job
spec:
  template:
    spec:
      containers:
      - name: busybox
        image: docker.io/busybox
        command: ["sh", "-c", "sllep 5; exit0"]
      imagePullSecrets:
      - name: regcred
      restartPolicy: Never
  completions: 6
  parallelism: 2
```

```yaml
vagrant@master-node:~$ kubectl apply -f job-normal-end.yaml
job.batch/job-normal-end created

vagrant@master-node:~$ kubectl get job
NAME             COMPLETIONS   DURATION   AGE
job-normal-end   2/6           15s        15s
vagrant@master-node:~$ kubectl get job
NAME             COMPLETIONS   DURATION   AGE
job-normal-end   4/6           28s        28s
vagrant@master-node:~$ kubectl get job
NAME             COMPLETIONS   DURATION   AGE
job-normal-end   6/6           34s        37s

vagrant@master-node:~$ kubectl describe job job-normal-end
Name:             job-normal-end
Namespace:        default
Selector:         batch.kubernetes.io/controller-uid=a2b51be5-f016-4966-bbf4-cb415b78a3d7
Labels:           batch.kubernetes.io/controller-uid=a2b51be5-f016-4966-bbf4-cb415b78a3d7
                  batch.kubernetes.io/job-name=job-normal-end
                  controller-uid=a2b51be5-f016-4966-bbf4-cb415b78a3d7
                  job-name=job-normal-end
Annotations:      batch.kubernetes.io/job-tracking:
**Parallelism:      2**
Completions:      6
Completion Mode:  NonIndexed
Start Time:       Fri, 13 Oct 2023 05:04:43 +0000
Completed At:     Fri, 13 Oct 2023 05:05:17 +0000
Duration:         34s
Pods Statuses:    0 Active (0 Ready) / 6 Succeeded / 0 Failed
Pod Template:
  Labels:  batch.kubernetes.io/controller-uid=a2b51be5-f016-4966-bbf4-cb415b78a3d7
           batch.kubernetes.io/job-name=job-normal-end
           controller-uid=a2b51be5-f016-4966-bbf4-cb415b78a3d7
           job-name=job-normal-end
  Containers:
   busybox:
    Image:      docker.io/busybox
    Port:       <none>
    Host Port:  <none>
    Command:
      sh
      -c
      sleep 5; exit 0
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Events:
  Type    Reason            Age   From            Message
  ----    ------            ----  ----            -------
  Normal  SuccessfulCreate  **81s**   job-controller  Created pod: job-normal-end-kd9zq     **// 파드가 두 개씩 실행되고 종료된 것을 확인 가능**
  Normal  SuccessfulCreate  **81s**   job-controller  Created pod: job-normal-end-cx8zh
  Normal  SuccessfulCreate  **70s**   job-controller  Created pod: job-normal-end-hf4vg
  Normal  SuccessfulCreate  **70s**   job-controller  Created pod: job-normal-end-4dhnb
  Normal  SuccessfulCreate  **58s**   job-controller  Created pod: job-normal-end-bbrcf
  Normal  SuccessfulCreate  **58s**   job-controller  Created pod: job-normal-end-5rqfm
  Normal  Completed         47s   job-controller  Job completed
```

**잡을 이용해서 비정상적으로 종료되는 파드를 실행**

job-abnormal-end.yaml

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: job-abnormal-end
spec:
  template:
    spec:
      containers:
      - name: busybox
        image: docker.io/busybox
        command: ["sh", "-c", "sleep 5; exit 1"] ## exit 1 : 비정상 종료
      imagePullSecrets:
      - name: regcred
      restartPolicy: Never
  # completions: 6      ## 총 실행 회수 (기본값 1)
  # parallelism: 2      ## 동시 실행할 파드의 개수 (기본값 1)
  backoffLimit: 3       ## 실패했을 때 재실행하는 최대 실행 회수
```

```bash
vagrant@master-node:~$ kubectl apply -f job-abnormal-end\ copy.yaml
job.batch/job-abnormal-end created

vagrant@master-node:~$ kubectl get job,pod
NAME                         COMPLETIONS   DURATION   AGE
job.batch/job-abnormal-end   0/1           12m        12m

NAME                         READY   STATUS    RESTARTS   AGE
pod/job-abnormal-end-4vk9c   0/1     Error     0          11m
pod/job-abnormal-end-827v8   0/1     Error     0          10m
pod/job-abnormal-end-fwldb   0/1     Error     0          12m
pod/job-abnormal-end-zj6k5   0/1     Error     0          12m

vagrant@master-node:~$ kubectl describe job job-abnormal-end
Name:             job-abnormal-end
Namespace:        default
Selector:         batch.kubernetes.io/controller-uid=32d16469-595e-41b4-818b-2e0fd55288e3
Labels:           batch.kubernetes.io/controller-uid=32d16469-595e-41b4-818b-2e0fd55288e3
                  batch.kubernetes.io/job-name=job-abnormal-end
                  controller-uid=32d16469-595e-41b4-818b-2e0fd55288e3
                  job-name=job-abnormal-end
Annotations:      batch.kubernetes.io/job-tracking:
**Parallelism:      1
Completions:      1**
Completion Mode:  NonIndexed
Start Time:       Fri, 13 Oct 2023 05:18:31 +0000
Pods Statuses:    0 Active (0 Ready) / 0 Succeeded / **4 Failed**
Pod Template:
  Labels:  batch.kubernetes.io/controller-uid=32d16469-595e-41b4-818b-2e0fd55288e3
           batch.kubernetes.io/job-name=job-abnormal-end
           controller-uid=32d16469-595e-41b4-818b-2e0fd55288e3
           job-name=job-abnormal-end
  Containers:
   busybox:
    Image:      docker.io/busybox
    Port:       <none>
    Host Port:  <none>
    Command:
      sh
      -c
      sleep 5; exit 1
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Events:
  Type     Reason                Age   From            Message
  ----     ------                ----  ----            -------
  Normal   SuccessfulCreate      13m   job-controller  Created pod: job-abnormal-end-zj6k5    ************// 파드가 네 번 실행 (3번 재시작해줌)************
  Normal   SuccessfulCreate      13m   job-controller  Created pod: job-abnormal-end-fwldb
  Normal   SuccessfulCreate      12m   job-controller  Created pod: job-abnormal-end-4vk9c
  Normal   SuccessfulCreate      12m   job-controller  Created pod: job-abnormal-end-827v8
  Warning  BackoffLimitExceeded  12m   job-controller  Job has reached the specified backoff limit
```

**여러 컨테이너 중 일부가 이상 종료할 경우**

job-container-failed.yaml

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: job-container-failed
spec:
  template:
    spec:
      containers:
      - name: busybox-normal
        image: docker.io/busybox
        command: ["sh", "-c", "sleep 5; exit 0"]
      - name: busybox-abnormal
        image: docker.io/busybox
        command: ["sh", "-c", "sleep 5; exit 1"] ## exit 1 : 비정상 종료
      imagePullSecrets:
      - name: regcred
      restartPolicy: Never
  # completions: 6      ## 총 실행 회수 (기본값 1)
  # parallelism: 2      ## 동시 실행할 파드의 개수 (기본값 1)
  backoffLimit: 2       ## 실패했을 때 재실행하는 최대 실행 회수
```

```bash
vagrant@master-node:~$ kubectl apply -f job-container-failed.yaml
job.batch/job-abnormal-end created

vagrant@master-node:~$ kubectl get job,pod
NAME                         COMPLETIONS   DURATION   AGE
job.batch/job-container-failed   0/1           5m35s      5m35s

NAME                         READY   STATUS   RESTARTS   AGE
pod/job-container-failed-4lp8d   0/2     Error    0          4m44s
pod/job-container-failed-f4kbx   0/2     Error    0          5m14s
pod/job-container-failed-htxsj   0/2     Error    0          5m35s
                                         ~~~~~
                                          **정상종료 먼저되면 Completed가 되고, 비정상종료가 먼저되면 Error가 된다.**

vagrant@master-node:~$ kubectl describe job job-container-failed
Name:             job-container-failed
Namespace:        default
Selector:         batch.kubernetes.io/controller-uid=8efb7e10-19ce-4836-a5f3-fa912ebf6ae5
Labels:           batch.kubernetes.io/controller-uid=8efb7e10-19ce-4836-a5f3-fa912ebf6ae5
                  batch.kubernetes.io/job-name=job-abnormal-end
                  controller-uid=8efb7e10-19ce-4836-a5f3-fa912ebf6ae5
                  job-name=job-abnormal-end
Annotations:      batch.kubernetes.io/job-tracking:
Parallelism:      1
Completions:      1
Completion Mode:  NonIndexed
Start Time:       Fri, 13 Oct 2023 05:38:06 +0000
Pods Statuses:    0 Active (0 Ready) / 0 Succeeded / 3 Failed
Pod Template:
  Labels:  batch.kubernetes.io/controller-uid=8efb7e10-19ce-4836-a5f3-fa912ebf6ae5
           batch.kubernetes.io/job-name=job-container-failed
           controller-uid=8efb7e10-19ce-4836-a5f3-fa912ebf6ae5
           job-name=job-container-failed
  Containers:
   busybox-normal:
    Image:      docker.io/busybox
    Port:       <none>
    Host Port:  <none>
    Command:
      sh
      -c
      sleep 5; exit 0
    Environment:  <none>
    Mounts:       <none>
   busybox-abnormal:
    Image:      docker.io/busybox
    Port:       <none>
    Host Port:  <none>
    Command:
      sh
      -c
      sleep 5; exit 1
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Events:
  Type     Reason                Age   From            Message
  ----     ------                ----  ----            -------
  Normal   SuccessfulCreate      88s   job-controller  Created pod: job-abnormal-end-htxsj
  Normal   SuccessfulCreate      67s   job-controller  Created pod: job-abnormal-end-f4kbx
  Normal   SuccessfulCreate      37s   job-controller  Created pod: job-abnormal-end-4lp8d
  Warning  BackoffLimitExceeded  25s   job-controller  Job has reached the specified backoff limit
```

### 잡 컨트롤러를 이용한 소수 계산

**1. 소수를 만들어서 출력하는 프로그램을 numpy로 작성(pc에서)**

prime_number.py

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import math
np.set_printoptions(threshold='nan')

# 소수 판정 함수
def is_prime(n):
    if n % 2 == 0 and n > 2:
        return False
    return all(n % i for i in range(3, int(math.sqrt(n)) + 1, 2))

# 배열에 1부터 차례대로 숫자를 배치
nstart = eval(os.environ.get("A_START_NUM"))  
nsize  = eval(os.environ.get("A_SIZE_NUM"))    
nend   = nstart + nsize                        
ay     = np.arange(nstart, nend)              

# 소수 판정 함수를 벡터화
pvec = np.vectorize(is_prime)

# 배열 요소에 적용
primes_tf = pvec(ay)

# 소수만 추출하여 표시
primes = np.extract(primes_tf, ay)
print primes
```

requirements.txt

```bash
numpy==1.14.1
```

**2. Dockerfile 작성(PC에서)**

```docker
FROM  python:2
COPY  ./requirements.txt  /requirements.txt
COPY  ./prime_number.py   /prime_number.py
RUN   pip install --no-cache-dir -r requirements.txt
CMD   [ "python", "/prime_number.py" ]
```

**3. 도커 이미지 빌드 및 도커 허브에 등록(PC에서)**

```bash
docker image build -t primenumber_generator .
docker container run -e A_START_NUM=1 -e A_SIZE_NUM=20 primenumber_generator
[ 1  2  3  5  7 11 13 17 19]

docker image tag primenumber_generator suahcho/primenumber_generator:1.0
docker login
docker image push suahcho/primenumber_generator:1.0
```

**4. 잡 컨트롤러의 매니페스트 파일 작성(master 노드에서)**

primenumber-job.yaml

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: primenumber-job
spec:
  template:
    spec:
      containers:
      - name: primenumber-generator
        image: docker.io/suahcho/primenumber_generator:1.0
        env:
        - name: A_START_NUM
          value: "2"
        - name: A_SIZE_NUM
          value: "10**6"
      restartPolicy: Never
      imagePullSecrets:
      - name: regcred
  backoffLimit: 4
```

**5. 잡 실행 및 결과 확인**

```bash
vagrant@master-node:~$ kubectl apply -f primenumber-job.yaml
job.batch/primenumber-job created

vagrant@master-node:~$ kubectl get job,pod
NAME                        COMPLETIONS   DURATION   AGE
job.batch/primenumber-job   1/1           116s       14m

NAME                        READY   STATUS      RESTARTS   AGE
pod/primenumber-job-djcvn   0/1     Completed   0          14m

vagrant@master-node:~$ kubectl logs pod/primenumber-job-djcvn
[     2      3      5      7     11     13     17     19     23     29
     31     37     41     43     47     53     59     61     67     71 
     ...  999907 999917 999931 999953 999959 999961 999979 999983]

```

### 메시지 브로커와 잡 컨트로러를 조합

![Alt text](image.png)

**1. 표준입력으로 계산범위를 전달받아서 소수를 계산하는 파이썬 어플리케이션을 제작(PC에서)**

prime_num_generator.py

```bash
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import math
np.set_printoptions(threshold='nan')

# 소수 판정 함수
def is_prime(n):
    if n % 2 == 0 and n > 2:
        return False
    return all(n % i for i in range(3, int(math.sqrt(n)) + 1, 2))

# 소수 생성 함수
def prime_number_generater(nstart, nsize):
    nend = nstart + nsize
    ay = np.arange(nstart, nend)
    # 소수 판정 함수 벡터화
    pvec = np.vectorize(is_prime)
    # 배열 요소에 적용
    primes_t = pvec(ay)
    # 소수만 추출하여 표시
    primes = np.extract(primes_t, ay)
    return primes

if __name__ == '__main__':
    p = sys.stdin.read().split(",")
    print p
    print prime_number_generater(int(p[0]), int(p[1]))
```

**2. Dockerfile 작성(PC에서)**

```docker
FROM  ubuntu:16.04
RUN   apt-get update && \
      apt-get install -y curl ca-certificates amqp-tools python python-pip
COPY  ./requirements.txt  /requirements.txt
COPY  ./prime_num_generator.py  /prime_num_generator.py
RUN   pip install --no-cache-dir -r requirements.txt
CMD   /usr/bin/amqp-consume --url=$BROKER_URL -q $QUEUE -c 1 /prime_num_generator.py

// 설명
CMD   /usr/bin/amqp-consume --url=$BROKER_URL -q $QUEUE -c 1 /prime_num_generator.py
      ~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~ ~~~~~~~~~ ~~~~
      |                     메시지 큐 주소    큐 이름   소비할 메시지 수
      +-- AMQP 서버 상의 큐에서 메세지를 소비하는 명령어
```

**3. 이미지 빌드 및 도커 허브 등록**

```bash
docker image build -t primenumber_generator .
docker image push suahcho/primenumber_generator:2.0
```

**4. 쿠버네티스 클러스에 RabbitMQ 배포**

rabbitmq.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: taskque-deploy
spec:
  selector:
    matchLabels:
      app: taskque
  replicas: 1
  template:
    metadata:
      labels:
        app: taskque
    spec:
      containers:
      - image: docker.io/rabbitmq
        name: rabbitmq
        ports:
        - containerPort: 5672
        resources:
          limits:
            cpu: 100m
      imagePullSecrets:
      - name: regcred
---
apiVersion: v1
kind: Service
metadata:
  name: taskque-svc
spec:
  type: NodePort
  ports:
  - port: 5672
    nodePort: 31672
  selector:
    app: taskque
```

```bash
vagrant@master-node:~$ kubectl apply -f rabbitmq.yaml
deployment.apps/taskque-deploy created
service/taskque-svc created

vagrant@master-node:~$ kubectl get deploy,pod,service
NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/taskque-deploy   1/1     1            1           8m8s

NAME                                  READY   STATUS      RESTARTS   AGE
pod/taskque-deploy-77f7fdd8d6-s8l2c   1/1     Running     0          8m8s

NAME                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/kubernetes           ClusterIP   172.17.0.1      <none>        443/TCP          28h
service/production-service   ClusterIP   172.17.20.176   <none>        80/TCP           29h
service/taskque-svc          NodePort    172.17.20.40    <none>        5672:31672/TCP   8m8s
```

**5. job-initiator.py작성(master노드에서)**

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import yaml
import pika
from kubernetes import client, config

OBJECT_NAME = "pngen"
qname = 'taskque'

# 메시지 브로커 접속
def create_queue():
    qmgr_cred = pika.PlainCredentials('guest', 'guest')  ## rabbitmq 공식 이미지에서 설정한 기본 계정
    qmgr_host = '10.0.0.10'   ## 노드 IP를 설정
    qmgr_port = '31672'       ## 노드 PORT
    qmgr_pram = pika.ConnectionParameters(
        host=qmgr_host,
        port=qmgr_port,
        credentials=qmgr_cred)
    conn = pika.BlockingConnection(qmgr_pram)
    chnl = conn.channel()
    chnl.queue_declare(queue=qname)
    return chnl

# 잡 매니페스트 작성
def create_job_manifest(n_job, n_node):
    container = client.V1Container(
        name="pn-generator",
        image="suahcho/primenumber_generator:2.0", ## 도커 허브에 등록한 이미지
        env=[
            client.V1EnvVar(name="BROKER_URL",
                            value="amqp://guest:guest@taskque-svc:5672"),
            client.V1EnvVar(name="QUEUE", value="taskque")
        ]        
    )
    template = client.V1PodTemplateSpec(
        spec=client.V1PodSpec(containers=[container],
                              restart_policy="Never",
                              image_pull_secrets=[client.V1LocalObjectReference(name='regcred')]
                              ))
    spec = client.V1JobSpec(
        backoff_limit=4,
        template=template,
        completions=n_job,
        parallelism=n_node)
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=OBJECT_NAME),
        spec=spec)
    return job

if __name__ == '__main__':

    job_parms = [[1, 1000], [1001, 1000], [2001, 1000], [3001, 1000]]
    jobs = len(job_parms)
    nodes = 2

    queue = create_queue()
    for param_n in job_parms:
        param = str(param_n).replace('[', '').replace(']', '')
        queue.basic_publish(exchange='', routing_key=qname, body=param)

    config.load_kube_config()
    client.BatchV1Api().create_namespaced_job(
        body=create_job_manifest(jobs, nodes), namespace="default")
```

**6. 파이썬 모듈 설치**

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip
pip3 install pika
pip3 install kubernetes

python3 job-initiator.py
vagrant@master-node:~$ kubectl get job,pod
NAME                        COMPLETIONS   DURATION   AGE
job.batch/pngen             0/4           8s         8s

NAME                                  READY   STATUS              RESTARTS   AGE
pod/pngen-4tv48                       0/1     ContainerCreating   0          8s
pod/pngen-p5j74                       0/1     ContainerCreating   0          8s
pod/taskque-deploy-77f7fdd8d6-s8l2c   1/1     Running             0          46m

vagrant@master-node:~$ kubectl logs pod/pngen-4tv48
['1', ' 1000']
[  1   2   3   5   7  11  13  17  19  23  29  31  37  41  43  47  53  59
  61  67  71  73  79  83  89  97 101 103 107 109 113 127 131 137 139 149
 151 157 163 167 173 179 181 191 193 197 199 211 223 227 229 233 239 241
 251 257 263 269 271 277 281 283 293 307 311 313 317 331 337 347 349 353
 359 367 373 379 383 389 397 401 409 419 421 431 433 439 443 449 457 461
 463 467 479 487 491 499 503 509 521 523 541 547 557 563 569 571 577 587
 593 599 601 607 613 617 619 631 641 643 647 653 659 661 673 677 683 691
 701 709 719 727 733 739 743 751 757 761 769 773 787 797 809 811 821 823
 827 829 839 853 857 859 863 877 881 883 887 907 911 919 929 937 941 947
 953 967 971 977 983 991 997]

```