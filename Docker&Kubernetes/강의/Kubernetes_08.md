## 크론잡(Cronjob)

job을 시간 기준으로 관리하도록 생성

⇒ 지정한 시간에 한 번만 잡을 실행하거나 지정한 시간동안 주기적으로 잡을 반복실행하는 오브젝트

- cron 형식 시간을 지정
    - cron
        - UNIX 계열의 운영체제에 구현된 시간 기반의 스케줄러

주로 애플리케이션 프로그램 데이터, 데이터베이스와 같은 `중요 데이터를 백업`하는 데 사용

생성된 파드의 개수가 정해진 수를 넘어서면 가비지 수집 컨트롤러가 중료된 파드를 삭제

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/82130015-91d4-4e66-833d-0e72344fd3b2/6ad8740d-2b79-4347-8287-c24cafedc693/Untitled.png)

### 크론잡 사용하기

cronjob.yml

```yaml
apiVersion: batch/v1betal
kind: CronJob
metadata:
  name: hello
spec:
  schedule: "*/1 * * * *"
  jobTemplate:
    spec:
      tempTemplate:
        spec:
          template:
            spec:
              containers:
              - name: hello
                image: docker.io/busybox
                args:
                - bin/sh
                - -c
                - date; echo Hello from the Kubernetes Cluster
              restartPolicy: OnFailure  # onFailure오류로 죽으면 다시 시작해라
              imagePullSecrets:
              - name: regcred
```

```bash
vagrant@master-node:~$ kubectl apply -f cronjob.yaml
cronjob.batch/hello created

vagrant@master-node:~$ kubectl get cronjob,job,pod
NAME                  SCHEDULE      SUSPEND   ACTIVE   LAST SCHEDULE   AGE
cronjob.batch/hello   */1 * * * *   False     0        31s             2m12s

NAME                       COMPLETIONS   DURATION   AGE
job.batch/hello-28290331   1/1           7s         91s
job.batch/hello-28290332   1/1           6s         31s

NAME                       READY   STATUS      RESTARTS   AGE
pod/hello-28290331-jsx77   0/1     Completed   0          91s
pod/hello-28290332-j26z9   0/1     Completed   0          31s

vagrant@master-node:~$ kubectl describe cronjob hello
Name:                          hello
Namespace:                     default
Labels:                        <none>
Annotations:                   <none>
Schedule:                      */1 * * * *
Concurrency Policy:            Allow
Suspend:                       False
Successful Job History Limit:  3
Failed Job History Limit:      1
Starting Deadline Seconds:     <unset>
Selector:                      <unset>
Parallelism:                   <unset>
Completions:                   <unset>
Pod Template:
  Labels:  <none>
  Containers:
   hello:
    Image:      docker.io/busybox
    Port:       <none>
    Host Port:  <none>
    Args:
      bin/sh
      -c
      date; echo Hello from the Kubernetes Cluster
    Environment:     <none>
    Mounts:          <none>
  Volumes:           <none>
Last Schedule Time:  Mon, 16 Oct 2023 01:33:00 +0000
Active Jobs:         <none>
Events:
  Type    Reason            Age    From                Message
  ----    ------            ----   ----                -------
  Normal  SuccessfulCreate  **2m40s**  cronjob-controller  **Created** job hello-28290331
  Normal  SawCompletedJob   2m32s  cronjob-controller  Saw completed job: hello-28290331, status: Complete
  Normal  SuccessfulCreate  **100s**   cronjob-controller  **Created** job hello-28290332
  Normal  SawCompletedJob   94s    cronjob-controller  Saw completed job: hello-28290332, status: Complete
  Normal  SuccessfulCreate  **40s**    cronjob-controller  **Created** job hello-28290333
  Normal  SawCompletedJob   34s    cronjob-controller  Saw completed job: hello-28290333, status: Complete

vagrant@master-node:~$ kubectl get pod
NAME                   READY   STATUS      RESTARTS   AGE
hello-28290333-cx49w   0/1     Completed   0          2m42s
hello-28290334-7qch9   0/1     Completed   0          102s
hello-28290335-jlg62   0/1     Completed   0          42s

vagrant@master-node:~$ kubectl delete -f cronjob.yaml
cronjob.batch "hello" deleted

vagrant@master-node:~$ kubectl get cronjob,job,pod
No resources found in default namespace.   **// 크론잡을 삭제하면 함께 생성되었던 파드도 함께 삭제된다.**
```

### 크론잡 설정

**spec.schedule**

- cron 형식으로 스케줄을 기술
- 분(0-59), 시(0-23), 일(1-31), 월(1-12), 요일(0-7, 0:일요일, 7:일요일)

**spec.startingDeadlineSeconds**

- 지정된 시간에 크론잡이 실행되지 못했을 때 필드 값으로 설정한 시간까지 지나면 크론잡이 실행되지 않게 함

**spec.concurrentPolicy**

- 크론잡이 실행하는 잡의 동시성을 관리
- Allow
    - 기본값, 여러 개 잡을 동시에 실행할 수 있게 한다.
- Forbid
    - 동시 실행을 금지
    - 앞에 잡이 끝나야만 다음 잡을 실행 할 수 있다.
- Replace
    - 이전에 실행했던 잡이 실행 중인 상태에서 새로운 잡을 실행할 시간이 되면, 이전에 실행 중이던 잡을 새로운 잡으로 대체

**spec.successfullJobHistroyLimit**

- 정상적으로 종료된 잡 내역의 보관 개수 (기본값 : 3)

**spec.failedJobHistoryLimt**

- 비정상 종료된 잡 내역의 보관 개수 (기본값 : 1)

cronjob.-currency.yaml

```bash
apiVersion: batch/v1
kind: CronJob
metadata:
  name: hello-concurrency
spec:
  schedule: "*/1 * * * *"
  startingDeadlineSeconds: 600
  concurrencyPolicy: Forbid
  jobTemplate:
    spec:
      template:
        spec:
            containers:
            - name: hello
              image: docker.io/busybox
              args:
              - bin/sh
              - -c
              - date; echo Hello from the Kubernetes Cluster; sleep 6000
            restartPolicy: OnFailure  # onFailure오류로 죽으면 다시 시작해라
            imagePullSecrets:
            - name: regcred
```

```bash
vagrant@master-node:~$ kubectl apply -f cronjob-currency.yaml
cronjob.batch/hello-concurrency created

vagrant@master-node:~$ kubectl get cronjob,job,pod
NAME                              SCHEDULE      SUSPEND   ACTIVE   LAST SCHEDULE   AGE
cronjob.batch/hello-concurrency   */1 * * * *   False     1        11s             58s

NAME                                   COMPLETIONS   DURATION   AGE
job.batch/hello-concurrency-28290373   0/1           11s        11s

NAME                                   READY   STATUS    RESTARTS   AGE
pod/hello-concurrency-28290373-dpbhh   1/1     Running   0          11s

```

1분 간격으로 잡을 실행하도록 스케줄했으나, sleep 6000 코드로 인해 잡이 끝나지 않음

currencyPolicy 필드를 Forbid로 설정하기 때문에 잡을 동시에 실행하지 않고 기다림

⇒ 앞에 잡이 끝나지 않기 때문에 다음 잡을 진행할 수 없음

```bash
vagrant@master-node:~$ kubectl edit cronjob hello-concurrency

spec:
  concurrencyPolicy: **Allow**

cronjob.batch/hello-concurrency edited

****vagrant@master-node:~$ kubectl get cronjob,job,pod
NAME                              SCHEDULE      SUSPEND   ACTIVE   LAST SCHEDULE   AGE
cronjob.batch/hello-concurrency   */1 * * * *   False     3        39s             5m26s

NAME                                   COMPLETIONS   DURATION   AGE
job.batch/hello-concurrency-28290373   0/1           4m39s      4m39s
job.batch/hello-concurrency-28290376   0/1           70s        70s   // 기존 잡이 종료되지 않고 유지
job.batch/hello-concurrency-28290377   0/1           39s        39s   // 새로운 잡이 생성(추가)

NAME                                   READY   STATUS    RESTARTS   AGE
pod/hello-concurrency-28290373-dpbhh   1/1     Running   0          4m39s
pod/hello-concurrency-28290376-btmm2   1/1     Running   0          70s
pod/hello-concurrency-28290377-v5tmk   1/1     Running   0          39s  // 1분마다 하나씩 추가
```

```bash
vagrant@master-node:~$ kubectl edit cronjob hello-concurrency

spec:
  concurrencyPolicy: **Replace**

cronjob.batch/hello-concurrency edited

vagrant@master-node:~$ kubectl get cronjob,job,pod
NAME                              SCHEDULE      SUSPEND   ACTIVE   LAST SCHEDULE   AGE
cronjob.batch/hello-concurrency   */1 * * * *   False     1        4s              10m

NAME                                   COMPLETIONS   DURATION   AGE
job.batch/hello-concurrency-28290383   0/1           4s         4s

NAME                                   READY   STATUS        RESTARTS   AGE
pod/hello-concurrency-28290382-2fslp   1/1     **Terminating**   0          64s   **// 기존 잡을 모두 종료하고 새로운 잡을실행**
pod/hello-concurrency-28290383-spd2q   1/1     Running       0          4s

vagrant@master-node:~$ kubectl get cronjob,job,pod
NAME                              SCHEDULE      SUSPEND   ACTIVE   LAST SCHEDULE   AGE
cronjob.batch/hello-concurrency   */1 * * * *   False     1        43s             11m

NAME                                   COMPLETIONS   DURATION   AGE
job.batch/hello-concurrency-28290383   0/1           43s        43s

NAME                                   READY   STATUS    RESTARTS   AGE
pod/hello-concurrency-28290383-spd2q   1/1     Running   0          43s
```

## 스토리지

- 상태 없는 (stateless) 애플리케이션 - 디플로이먼트의 각 파드는 별도의 데이터를 가지고 있지 않으며, 단순히 요청에 대한 응답만 반환
- 상태 있는 (stateful) 애플리케이션- 데이터베이스 처럼 파드 내부에 특정 데이터를 보유해야하는 애플리케이션

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/82130015-91d4-4e66-833d-0e72344fd3b2/8f09fb6d-e05f-499d-a498-eabd041795bf/Untitled.png)

### 로컬 볼륨 ⇒ emptyDir, hostPath

**emptyDir ⇒ 파드 내의 컨테이너 간 임시 데이터 공유**

emptydir-volume-pod.yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: emptydir-volume-pod
spec:
  containers:
  - name: content-creator
    image: docker.io/busybox
    args: ["tail", "-f", "/dev/null"]
    volumeMounts:
    - name: emptydir-volume
      mountPath: /data
  - name: webserver
    image: docker.io/httpd:2
    volumeMounts:
    - name: emptydir-volume
      mountPath: /usr/local/apache2/htdocs/
  imagePullSecrets:
  - name: regcred  
  volumes:
    - name: emptydir-volume
      emptyDir: {}
```

⇒ 두 개의 컨테이너가 같은 볼륨을 마운트하고 있다.

```bash
vagrant@master-node:~$ kubectl apply -f emptydir-volume-pod.yaml
pod/emptydir-volume-pod created

vagrant@master-node:~$ kubectl get pod
NAME                  READY   STATUS    RESTARTS   AGE
emptydir-volume-pod   2/2     Running   0          73s

vagrant@master-node:~$ kubectl exec -it emptydir-volume-pod -c content-creator -- /bin/sh
/ # echo Hello, emptyDir!! > /data/hello.html
/ # cat /data/hello.html
Hello, emptyDir!!
/ # exit

vagrant@master-node:~$ kubectl exec -it emptydir-volume-pod -c webserver -- cat /usr/local/apache2/htdocs/hello.html
Hello, emptyDir!!
```

**hostPath = > 워커 노드의 로컬 디렉터리를 볼륨으로 사용**

hostpath-volume-pod.yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hostpath-volume-pod
spec:
  containers:
  - name: busybox
    image: docker.io/busybox
    args: ["tail", "-f", "/dev/null"]
    volumeMounts:
    - name: hostpath-volume
      mountPath: /etc/data
  imagePullSecrets:
  - name: regcred  
  volumes:
    - name: hostpath-volume
      hostPath: 
        path: /tmp
```

```bash
vagrant@master-node:~$ kubectl apply -f hostpath-volume-pod.yaml
pod/hostpath-volume-pod created

vagrant@master-node:~$ kubectl exec -it hostpath-volume-pod -- touch /etc/data/mydata

vagrant@master-node:~$ kubectl get pod -o wide
NAME                  READY   STATUS    RESTARTS   AGE   IP              NODE            NOMINATED NODE   READINESS GATES
hostpath-volume-pod   1/1     Running   0          89s   172.16.158.45   worker-node02   <none>           <none>

vagrant@master-node:~$ ssh vagrant@10.0.0.12
The authenticity of host '10.0.0.12 (10.0.0.12)' can't be established.
ED25519 key fingerprint is SHA256:BMSSQvtQmkJhbHJetKeEg+DZXScCAFwjjyrMQu7SYno.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes

vagrant@worker-node02:~$ ls /tmp
mydata
snap-private-tmp
systemd-private-a17ac4b6a053486e9b2390dd4ef889cd-ModemManager.service-FmDwtD
systemd-private-a17ac4b6a053486e9b2390dd4ef889cd-systemd-logind.service-lcOUUP
systemd-private-a17ac4b6a053486e9b2390dd4ef889cd-systemd-resolved.service-ZWpf3w
```

파드가 다른 노드에 생성되면 이전에 생성된 데이터를 참조할 수 없다.

```bash
**// 파드 삭제 후 node02로 접속해서 볼륨 디렉터리 확인**
vagrant@master-node:~$ kubectl delete -f hostpath-volume-pod.yaml
pod "hostpath-volume-pod" deleted       

vagrant@master-node:~$ ssh vagrant@10.0.0.12
vagrant@10.0.0.12's password:
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-83-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Mon Oct 16 03:25:00 AM UTC 2023

  System load:  0.05517578125      Users logged in:        0
  Usage of /:   33.9% of 30.34GB   IPv4 address for eth0:  10.0.2.15
  Memory usage: 21%                IPv4 address for eth1:  10.0.0.12
  Swap usage:   0%                 IPv4 address for tunl0: 172.16.158.0
  Processes:    153

This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
Last login: Mon Oct 16 03:20:19 2023 from 10.0.0.10
vagrant@worker-node02:~$ ls /tmp
**mydata   // 파드가 삭제되어도 유지되고 있는 것을 확인**
snap-private-tmp
systemd-private-a17ac4b6a053486e9b2390dd4ef889cd-ModemManager.service-FmDwtD
systemd-private-a17ac4b6a053486e9b2390dd4ef889cd-systemd-logind.service-lcOUUP
systemd-private-a17ac4b6a053486e9b2390dd4ef889cd-systemd-resolved.service-ZWpf3w
```

동일 노드에 파드가 실행되면 해당 파일을 공유하게 된다.

(노드를 종료하면 데이터가 사라진다.)

**네트워크 볼륨**

**NFS 서버를 위한 디플로이먼트와 서비스를 생성**

nfs-deployment-service.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nfs-deployment
spec:
  selector:
    matchLabels:
      role: nfs-server
  template:
    metadata:
      labels:
        role: nfs-server
    spec:
      containers:
      - name: nfs-server-container
        image: gcr.io/google_containers/volume-nfs:0.8
        ports:
        - name: nfs
          containerPort: 2049
        - name: mountd
          containerPort: 20048
        - name: rpcbind
          containerPort: 111
        securityContext:
          privileged: true
      imagePullSecrets:
      - name: regcred
---
apiVersion: v1
kind: Service
metadata:
  name: nfs-service
spec:
  ports:
  - name: nfs
    port: 2049
  - name: mountd
    port: 20048
  - name: rpcbind
    port: 111
  selector:
    role: nfs-server
```

```bash
vagrant@master-node:~$ kubectl apply -f nfs-deployment-service.yaml
deployment.apps/nfs-deployment created
service/nfs-service created

vagrant@master-node:~$ kubectl get all
NAME                                  READY   STATUS    RESTARTS   AGE
pod/nfs-deployment-65fd996696-wbkfz   1/1     Running   0          77m

NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
service/kubernetes    ClusterIP   172.17.0.1      <none>        443/TCP                      4d1h
service/nfs-service   ClusterIP   172.17.27.194   <none>        **2049/TCP,20048/TCP,111/TCP**   77m

NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nfs-deployment   1/1     1            1           77m

NAME                                        DESIRED   CURRENT   READY   AGE
replicaset.apps/nfs-deployment-65fd996696   1         1         1       77m
```

**모든 워크 노드에 nfs와 관련한 패키지를 설치**

```bash
ssh vagrant@10.0.0.11

// node01
sudo apt-get install nfs-common  //NFS(네트워크 파일 공유 프로토콜로, 여러 컴퓨터 간에 파일 및 디렉터리를 공유하고 액세스하는데 사용) 클라이언트를 지원한 리눅스 패키지
exit
```

- nfs-common
    - NFS 클라이언트를 지원한 리눅스 패키지
    - NFS 서버로부터 파일 및 디렉터리를 마우트하고 읽고 쓸 수 있도록 설정
    - NFS
        - 네트워크 파일 공유 프로토콜로, 여러 컴퓨터 간에 파일 및 디렉터리를 공유하고 액세스하는데 사용

```bash
ssh vagrant@10.0.0.12

sudo apt-get install -y nfs-common
exit
```

**서비스의 CLUSTER-IP를 확인**

```bash
vagrant@worker-node02:~$ kubectl get service
NAME          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
kubernetes    ClusterIP   172.17.0.1      <none>        443/TCP                      4d1h
nfs-service   ClusterIP   **172.17.27.194**   <none>        2049/TCP,20048/TCP,111/TCP   86m
```

nfs-volume-pod.yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nfs-volume-pod
spec:
  containers:
  - name: nfs-volume-container
    image: docker.io/busybox
    args: ['tail', '-f', '/dev/null']
    volumeMounts:
    - name: nfs-volume
      mountPath: /mnt
  imagePullSecrets:
  - name: regcred
  volumes:
  - name: nfs-volume
    nfs:
      path: /
      server: 172.17.27.194  // nfs-service 서비스의 CLUSTER-IP 주소
```

```bash
vagrant@master-node:~$ kubectl apply -f nfs-volume-pod.yaml
pod/nfs-volume-pod created
```

### 퍼시턴트 볼륨과 퍼시스턴트 볼륨 크레임

- 지금까지는 파드의 YAML 파일에 볼륨 정보를 직접 명시하는 방식
- 볼륨과 애플리케이션의 정의가 서로 밀접하게 연관되어 있어 서로 분리하기 어려움
    
    → 네트워크 볼륨 타입과 별도의 YAML 파일 작성이 필요
    
    ⇒ PV, PVC 제공 → 파드가 볼륨의 세부적인 사항을 몰라도 볼륨을 사용할 수 있도록 추상화해주는 역할
    

### **NFS를 퍼스턴트 볼륨으로 사용**

**1. nfs 서버 디플로이먼트와 서비스를 생성**

```bash
vagrant@master-node:~$ kubectl apply -f nfs-deployment-service.yaml
deployment.apps/nfs-deployment created
service/nfs-service created

vagrant@master-node:~$ kubectl get all
NAME                                  READY   STATUS    RESTARTS   AGE
pod/nfs-deployment-65fd996696-7rd8k   1/1     Running   0          22s

NAME                  TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)                      AGE
service/kubernetes    ClusterIP   172.17.0.1    <none>        443/TCP                      4d3h
service/nfs-service   ClusterIP   172.17.40.6   <none>        2049/TCP,20048/TCP,111/TCP   22s

NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nfs-deployment   1/1     1            1           22s

NAME                                        DESIRED   CURRENT   READY   AGE
replicaset.apps/nfs-deployment-65fd996696   1         1         1       22s
```

**2. 퍼시스턴트 볼륨 생성**

nfs-persistentvolume.yaml

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfs-persistentvolume
spec:
  capacity:
    storage: 1Gi
  accessModes:
  - ReadWriteOnce
  nfs:
    path: /
    server: {CLUSTER-IP}
```

```bash
vagrant@master-node:~$ cat nfs-persistentvolume.yaml | sed "s/{CLUSTER-IP}/$(kubectl get service nfs-service -o jsonpath='{.spec.clusterIP}')/g" | kubectl apply -f -
persistentvolume/nfs-persistentvolume created
vagrant@master-node:~$ kubectl get pv
NAME                   CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   REASON   AGE
nfs-persistentvolume   1Gi        RWO            Retain           Available                                   5s
                                                                 ~~~~~~~~~~~
                                                          Available = 사용 가능 = 아직 클레임에 바인딩되지 않은 사용할 수 있는 리소스
                                                          Bound = 바인딩 = 볼륨이 클레임에 바인딩됨    
                                                          Released = 릴리스 = 크레임이 삭제되었지만 클러스터에서 아직 리소를 반환하지 않음
                                                          Failed = 실패 = 볼륨이 자동 반환에 실패됨
```

**3. 퍼시스턴트 볼륨 크레임과 파드를 생성**

nfs-persistentvolumeclaim-pod.yaml

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nfs-persistentvolumeclaim
spec:
  storageClassName: ""
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
---
apiVersion: v1
kind: Pod
metadata:
  name: nfs-mount-container
spec:
  containers:
  - name: nfs-mount-container
    image: docker.io/busybox
    args: ["tail", "-f", "/dev/null"]
    volumeMounts:
    - name: nfs-volume
      mountPath: /mnt
  imagePullSecrets:
    - name: regcred
  volumes:
  - name: nfs-volume
    persistentVolumeClaim:
      claimName: nfs-persistentvolumeclaim
```

```bash
vagrant@master-node:~$ kubectl apply -f nfs-persistentvolumeclaim-pod.yaml
persistentvolumeclaim/nfs-persistentvolumeclaim created

vagrant@master-node:~$ kubectl get pv,pvc,pod
NAME                                    CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                               STORAGECLASS   REASON   AGE
persistentvolume/nfs-persistentvolume   1Gi        RWO            Retain           **Bound**    default/nfs-persistentvolumeclaim                           10m

NAME                                              STATUS   VOLUME                 CAPACITY   ACCESS MODES   STORAGECLASS   AGE
persistentvolumeclaim/nfs-persistentvolumeclaim   **Bound**    nfs-persistentvolume   1Gi        RWO                           61s

NAME                                  READY   STATUS    RESTARTS   AGE
pod/nfs-deployment-65fd996696-7rd8k   1/1     Running   0          21m
pod/nfs-mount-container               0/1     Pending   0          74s
```

**RECLAIM POLICY** 

퍼시스턴트 볼륨 클레임이 삭제될 때 퍼시스턴트 볼륨과 연결되어 있던 저장소에 저장된 파일에 대한 처리 정책

- Retain
    - 퍼시스턴트 볼륨 클레임이 삭제되어도 저장소에 있던 파일을 삭제하지 않는 정책
- Delete
    - 퍼시스턴트 볼륨 클레임이 삭제되면 퍼시스턴트 볼륨과 연결된 저장소 자체를 삭제하는 정책
- Recycle
    - 퍼시스턴트 볼륨 클레임이 삭제되면 퍼시스턴트 볼륨과 연결된 저장소 데이터는 삭제하지만 저장소 볼륨 자체는 삭제하지 않고 유지하는 정책

ACCESS MODES

- RWO = ReadWriteOnce
    - 하나의 노드에서 해당 볼륨이 읽기-쓰기로 마운트된다.
- ROX = ReadOnlyWay
    - 볼륨은 많은 노드에서 읽기 전용으로 마운트된다.
- RWX = ReadWriteMany
    - 볼륨은 많은 노드에서 읽기-쓰기로 마운트된다.
- RWOP = ReadWriteOncePod
    - 볼륨이 단일 파드에서 읽기-쓰기로 마운트된다.
    - 전체 클러스터에서 단 하나의 파드만 해당
    - 퍼시스턴트 볼륨 클레임을 읽거나 쓸 수 있어야하는 경우에 사용
    

내일부터 리액트

리액트끝나면 모듈 프로젝트

모듈 프로젝트

최소 요구사항

- 프론트(react)&백엔드(python)&디비(mysql) 구성된 애플리케이션 개발 (팀)
- 컨테이너 이미지화 (개인)
- 로컬에서 docker compose (개인
- 가상머신 클러스터에 배포 → yaml (개인)
    - deployment
    - service(NodePort or LoadBalancer)