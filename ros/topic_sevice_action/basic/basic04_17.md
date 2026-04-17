# ROS2 통신 한 장 요약

## 1) Topic

**상대 응답 없이 그냥 보냄 / 받음**

### Publisher

```
self.pub=self.create_publisher(String,'chatter',10)
```

뜻:

- `String` : 메시지 타입
- `'chatter'` : topic 이름
- `10` : QoS depth = **메시지를 몇 개까지 큐에 쌓아둘지**

주의:

- `10`은 **몇 초마다 보내는지**가 아님
- 몇 초마다 보낼지는 `timer`, `while`, 버튼 클릭 등으로 따로 정함

### Subscriber

```
self.sub=self.create_subscription(String,'chatter',self.cb,10)
```

뜻:

- topic 이름, 타입 맞아야 함
- 메시지 오면 ROS가 알아서 콜백 호출

```
defcb(self,msg:String):
print(msg.data)
```

**Topic 핵심**

- pub : 보내기
- sub : 콜백으로 받기
- 이름 / 타입 / QoS 맞추기

---

## 2) Service

**요청 1번 → 응답 1번**

### Client

```
self.cli=self.create_client(AddTwoInts,'add_two_ints')
```

서버 대기:

```
self.cli.wait_for_service()
```

요청:

```
future=self.cli.call_async(req)
```

- 비동기 = 보내고 바로 다음으로 넘어감
- 결과는 나중에 `future`에 들어옴

메인:

```
rclpy.spin_until_future_complete(node,future)
res=future.result()
```

- 응답 올 때까지 기다림
- `res`가 결과

### Server

```
self.srv=self.create_service(AddTwoInts,'add_two_ints',self.cb)
```

```
defcb(self,request,response):
response.sum=request.a+request.b
returnresponse
```

**Service 핵심**

- client : 요청
- server : 계산 후 응답
- `request` 받음, `response` 채워서 return

---

## 3) Action

**goal 요청 → 중간 feedback → 마지막 result**

긴 작업용:

- 이동
- 경로 탐색
- 오래 걸리는 계산

### Action Client

```
self.client=ActionClient(self,Fibonacci,'fibonacci')
```

goal 만들기:

```
goal_msg=Fibonacci.Goal()
goal_msg.order=10
```

goal 보내기:

```
send_future=self.client.send_goal_async(
goal_msg,
feedback_callback=self.feedback_cb
)
```

goal 응답 대기:

```
rclpy.spin_until_future_complete(node,send_future)
goal_handle=send_future.result()
```

- 여기서 오는 건 **수락/거절**

최종 결과 요청:

```
result_future=goal_handle.get_result_async()
rclpy.spin_until_future_complete(node,result_future)
result=result_future.result().result
```

### feedback 콜백

```
deffeedback_cb(self,feedback_msg):
print(feedback_msg.feedback.partial_sequence)
```

---

### Action Server

```
self.server=ActionServer(
self,Fibonacci,'fibonacci',
execute_callback=self.execute_cb
)
```

```
defexecute_cb(self,goal_handle):
order=goal_handle.request.order

feedback=Fibonacci.Feedback()
feedback.partial_sequence= [0,1]
goal_handle.publish_feedback(feedback)

goal_handle.succeed()

result=Fibonacci.Result()
result.sequence=feedback.partial_sequence
returnresult
```

**Action 핵심**

- client가 goal 보냄
- server가 중간 feedback 보냄
- 마지막 result 반환

---

# 제일 짧은 핵심

## Topic

**그냥 보냄**

- pub → sub
- 응답 없음
- 계속 데이터 흐름

## Service

**묻고 답 받음**

- client → server → client
- 요청 1번, 응답 1번

## Action

**목표 주고 / 중간상태 받고 / 마지막 결과 받음**

- goal
- feedback
- result

---

# 외우기용 한 줄

- **Topic = 방송**
- **Service = 질문/답**
- **Action = 목표 + 진행상황 + 최종결과**

---

# 제일 많이 나오는 코드만 따로

## Topic

```
create_publisher(String,'chatter',10)
create_subscription(String,'chatter',self.cb,10)
```

## Service

```
create_client(AddTwoInts,'add_two_ints')
create_service(AddTwoInts,'add_two_ints',self.cb)
call_async(req)
future.result()
```

## Action

```
ActionClient(self,Fibonacci,'fibonacci')
ActionServer(self,Fibonacci,'fibonacci',execute_callback=self.execute_cb)
send_goal_async(...)
get_result_async()
publish_feedback(...)
```
