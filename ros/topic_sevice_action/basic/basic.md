# Topic Public

que는  최대 메시지 보관

 self.create_publisher(어떤 type으로 쓸지 ,topic name  ,que)로 만든다 

- `String` : 텍스트
- `Bool` : True/False
- `Int32`, `Int64` : 정수
- `Float32`, `Float64` : 실수

참고: 로봇에서 자주 쓰는 Twist, LaserScan, Odometry 같은 건 std_msgs가 아니라
geometry_msgs, sensor_msgs, nav_msgs 쪽이야.

```jsx
self.pub = self.create_publisher(String, 'chatter', 10)  
# 10 = 큐 depth (QoS)
```

self.create_timer(몇초 마다 호출할지, callback 함수를 만들다)

콜백 함수에는 

msg = type정의

[msg.data](http://msg.data)= 에 들어갈 내용 정의

마지막으로 

self.pub.publish(msg)  pub내가 만든 함수 public 함수에 publish 매소드에 msg 담기 (Publisher 객체의 publish 메서드에 msg를 인자로 전달)

```jsx

self.timer = self.create_timer(1.0, self.timer_cb)  # 1초마다 호출

def timer_cb(self):

# (3) 보낼 메시지 만들기

msg = String()

msg.data = f'hello {self.count}'

self.count += 1
 # (4) publish
self.pub.publish(msg)

 # (5) 로그 출력 (받는 쪽이 없어도 publish는 그냥 된다)
  self.get_logger().info(f'Publish: {msg.data}'
```

1.public를 만든다

2.시간함수 만든다 (콜백 함수) 메시지를 시간 마다 보내주니까 시간에 메시지를 넣어야지 

3. 콜백 함수를 만든다

# Topic Subcriber

만들 때 callback 받을 함수를 생성해서 만든다 받을 메시지 형태을 적어준다

 

```jsx
 # (1) 서브스크립션 생성: 같은 토픽 'chatter' 를 구독
        self.sub = self.create_subscription(
            String,
            'chatter',
            self.cb,   # 메시지 수신 시 실행할 콜백
            10
        )
        def cb(self, msg: String):
        # (2) msg.data 로 데이터 접근
        self.get_logger().info(f'Recv: {msg.data}')
```

1.subscription 만든다 (콜백 함수가 들어가야 함)

2.콜백 함수 만든다

# Service Client

# Request(a,b) / Response(sum)

topic public 처럼 일방적으로 보내지 않아서 데이터를 얼마나 보관할지 쓰지 않아도 됨

self.create_client(어떤 type, topic 이름 )

- `AddTwoInts` : `int64 a, int64 b -> int64 sum`
- `SetBool` : `bool data -> bool success, string message`
- `example_interfaces.srv.SetBool` (켜기/끄기 같은 on/off)
- `example_interfaces.srv.Trigger` (그냥 실행해줘 / 성공했는지 알려줘)

```jsx
# (1) 서비스 클라이언트 생성 (서버의 서비스 이름과 동일해야 함)
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')

```

topic과 다르게 양방향이라 기다려야함

self.cli.wait_for_service(몇 초 기다릴지 )

```jsx
# (2) 서버가 뜰 때까지 잠깐 기다림
        while not self.cli.wait_for_service(timeout_sec=0.5):
            self.get_logger().info('Waiting for /add_two_ints ...')
```

topic의 public(msg)처럼 어떤 형대로 보낼 지 생성
비동기(`call_async`)를 쓰는 이유는 **요청을 보낸 다음 “응답 올 때까지 기다리는 동안” 노드가 멈추지 않게** 하려는 거야.
동기 호출은 (`call`)

“만들고”.”어떤식으로 내보낼지”(”어떤 형식”)

```jsx
def call(self, a: int, b: int):
# (3) 요청 메시지 생성
req = AddTwoInts.Request()
req.a = a
req.b = b #msg 랑 비슷하네 밑에 

# (4) 비동기 호출 (future 반환)
        future = self.cli.call_async(req) #self.pub.publish(msg) 이느낌이네
        return future
```

- `future.result()` : 성공했을 때 결과(Response)를 줌 (실패면 예외 발생 가능)
- `future.exception()` : 실패했을 때 **발생한 예외(에러 객체)** 를 꺼내줌

```jsx
def main():
    rclpy.init()
    node = MinimalServiceClient()

    # 예시로 3 + 5 요청
    future = node.call(3, 5)

    # (5) 응답 올 때까지 spin(이벤트 처리)
    rclpy.spin_until_future_complete(node, future)
    #node : 이벤트를 처리할 “대상(노드)”
    #이 노드의 executor가 콜백(응답 수신 등)을 처리해야 future가 완료됨.
    #future : “언제까지 돌릴지” 종료 조건
		#future가 완료될 때까지 spin을 계속하라는 뜻.
    

    # (6) 응답 결과 확인
    if future.result() is not None:
        res = future.result()
        #res = future.result() (Response 객체)
				#res.sum (Response 안의 sum 필드 접근)
        node.get_logger().info(f'Result: sum={res.sum}')
    else:
        node.get_logger().error(f'Service call failed: {future.exception()}')

    node.destroy_node()
    rclpy.shutdown()
```

1.만들어

2.얼마나 기다릴지 pub time 같이

3.콜백 만들어 (어떤식으로 보낼지 근데 함수로 쓸꺼니까 return 갈겨)

4.메인에서 함수에 보낼꺼 적어주고 올때까지 node 돌려줘

5.결과를 확인한다 →Response 객체에 접근 

# Service Server

받는쪽은 콜백 포함

```jsx
 # (1) 서비스 서버 생성: 서비스 이름 'add_two_ints'
        self.srv = self.create_service(
            AddTwoInts,
            'add_two_ints',
            self.cb  # 요청이 오면 실행되는 콜백
        )

        self.get_logger().info('Service server ready: /add_two_ints')
```

콜백 함수 만들기 

```jsx
def cb(self, request: AddTwoInts.Request, response: AddTwoInts.Response):
        # (2) 요청값 접근
        a = request.a
        b = request.b

        # (3) 응답값 채우기
        response.sum = a + b

        # (4) 서버 로그
        self.get_logger().info(f'Request: a={a}, b={b} => sum={response.sum}')
        return response
```

# Action

action

- Client → Server : **Goal 보냄**
- Server → Client : **Goal 응답(수락/거절)**
- Server → Client : **Feedback 여러 번** (진행중)
- Server → Client : **Result 한 번** (끝)

이번엔 `example_interfaces/action/Fibonacci` 사용

- Goal: `order`
- Feedback: `partial_sequence` (진행 중 중간 결과)
- Result: `sequence` (최종 결과)

# Action client

만드는데 self가 들어감

# 그냥 create 매서드 없음 

Action: Node의 create 메서드로 안 들어가 있고,
별도 클래스를 직접 만들어 쓰는 형태 

- `create_publisher`는 말 그대로 “노드가 퍼블리셔를 만들어준다”
- `ActionClient(self, ...)`는 “액션 클라이언트를 만들 건데, **이 노드에 소속시켜라**”

결과적으로는 둘 다 **노드에 등록**되고 spin/executor가 돌면서 동작하지만,

코드 스타일이 다를 뿐이야.

```jsx
  # (1) 액션 클라이언트 생성 (서버의 액션 이름과 동일)
        self.client = ActionClient(self, Fibonacci, 'fibonacci')
```

servise clien처럼  기다리기고  비동기로 호출  (어떤 형태인지 ,콜백함수)

- ActionClient가 그 feedback 토픽을 **구독(subscribe)** 해.
- 그 구독으로 들어오는 메시지를 너가 지정한 `feedback_callback`으로 넘겨주는 구조야.
- 네가 직접 `create_subscription()`을 만든 건 아니지만,
- **액션 클라이언트가 내부적으로 구독을 만들고**
- 메시지가 올 때마다 콜백을 호출해주는 거라서

```jsx
def send_goal(self, order: int):
        # (2) goal 메시지 생성
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        # (3) 서버가 준비될 때까지 대기
        self.client.wait_for_server()

        # (4) goal 전송 (feedback 콜백 등록 가능)
        self.get_logger().info(f'Send goal: order={order}')
        return self.client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_cb
        )
```

```jsx
class MinimalActionClient(Node):
    def __init__(self):
        super().__init__('minimal_action_client')

        # (1) 액션 클라이언트 생성 (서버의 액션 이름과 동일)
        self.client = ActionClient(self, Fibonacci, 'fibonacci')
	
	        # (3) 서버가 준비될 때까지 대기
        if not self.client.wait_for_server(timeout_sec=3.0): 
         #while (계속 기다림),if (한 번만 확인)
		       self.get_logger().error("Action server not available")
	   		   return None 

    def send_goal(self, order: int):
        # (2) goal 메시지 생성
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        # (4) goal 전송 (feedback 콜백 등록 가능)
        self.get_logger().info(f'Send goal: order={order}')
        return self.client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_cb
        )
```

`feedback_callback`에 들어오는 `feedback_msg`는 **피드백 내용만 딱 오는 게 아니라**, 그 피드백을 “어떤 goal에 대한 피드백인지” 같은 **메타정보를 같이 담아서** 보내는 형태라서 보통 *wrapper(껍데기/포장)* 라고 불러.

그래서 구조가 이렇게 2겹이야:

- `feedback_msg` : 포장(메타정보 + 실제 피드백)
- `feedback_msg.feedback` : **실제 피드백 내용(진짜 payload)**
즉, 너가 진짜로 쓰고 싶은 데이터는 보통 `feedback_msg.feedback.XXX`로 들어있어.

#그냥 feedback_msg.feedback.partial_sequence로 받음 

```jsx
def feedback_cb(self, feedback_msg):
        # (5) 진행 중 피드백 받는 곳
        partial = feedback_msg.feedback.partial_sequence
        self.get_logger().info(f'Feedback recv: {partial}')
```

#확인은 accepted 로 

`goal_handle.accepted`가 뭐야

- `accepted == True` : 서버가 “이 goal 처리할게” 하고 **수락**
- `accepted == False` : 서버가 **거절** (조건 불만족, 서버 상태 등)

### `if not send_future.result()`로 대체 가능?

추천 X.

- `send_future.result()`는 보통 GoalHandle 객체가 와. 거절이어도 GoalHandle이 오는 경우가 많고(accepted=False),
- “None이면 실패” 같은 의미가 아니라서 `accepted`를 보는 게 정확해.

중요: **goal_handle은 “결과”가 아니라 “목표가 수락된 핸들(손잡이)”**이야.

## 5) `result_future.result().result` 왜 result가 두 번이야?

`result_future.result()`가 주는 건 보통 이런 “포장(wrapper)” 객체야:

- 바깥 `.result()` : Future의 결과(= 액션 결과 응답 메시지, wrapper)
- 그 안의 `.result` : 진짜 액션 Result 메시지

```jsx
def main():
    rclpy.init()
    node = MinimalActionClient()

    # 예시: order=10
    send_future = node.send_goal(10)

    # (6) goal 응답(수락/거절) 올 때까지 spin
    rclpy.spin_until_future_complete(node, send_future)
    goal_handle = send_future.result()  

    if not goal_handle.accepted: #수락 여부 확인 
        node.get_logger().error('Goal rejected')
        node.destroy_node()
        rclpy.shutdown()
        return

    node.get_logger().info('Goal accepted')

    # (7) 최종 결과 요청
    result_future = goal_handle.get_result_async()#feed back 온거까지 완료 결과를 받음
    

    # (8) 결과 올 때까지 spin (그 사이 feedback_cb가 계속 호출될 수 있음)
    rclpy.spin_until_future_complete(node, result_future)
    result = result_future.result().result
    #result_future.result()가 주는 건 보통 이런 “포장(wrapper)” 객체

    node.get_logger().info(f'Final result: {result.sequence}')

    node.destroy_node()
    rclpy.shutdown()
```

- `goal_handle.accepted` : 서버가 goal을 수락했는지
- `goal_handle.goal_id` (또는 비슷한 식별자) : 이 goal의 ID
- `goal_handle.get_result_async()` : “이 goal의 최종 결과를 받는 Future”를 만드는 메서드
- `goal_handle.cancel_goal_async()` : 취소 요청 등

✅ 중요: **goal_handle 자체는 “결과(result)”가 아니라 “수락된 목표에 대한 핸들(손잡이)”**야.

### 한 줄 요약

- 액션 goal 응답(`send_goal_async`) → `future.result()` = **GoalHandle(수락 여부/ID/메서드)**
- 액션 result(`get_result_async`) → `future.result()` = **wrapper**, 그 안 `.result`가 **진짜 Result**
- 서비스 호출(`call_async`) → `future.result()` = **바로 Response**
- 액션 feedback 콜백 인자도 **wrapper**고, `.feedback`가 payload

1. **Goal 요청** → 서버가 수락/거절
    - 결과: `goal_handle` (accepted 여부 포함)
2. **Feedback**(진행 중 계속 옴)
    - `feedback_cb`로 계속 받음
3. **Result**(완료 후 딱 한 번 옴)
    - `goal_handle.get_result_async()`로 “완료 결과”를 비동기로 받음

즉 **goal 응답(accepted)과 최종 result는 다른 통신**이라서 두 번 기다리는 게 맞아.

# 매인 밑에는 잘 이해가 안감

# Action Server

client와 마찬가지로 self써줌 받는 쪽은 만들 때 cb을 넣어줌 

```jsx
 # (1) 액션 서버 생성: 액션 이름 'fibonacci'
        self.server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            execute_callback=self.execute_cb  # goal 받으면 실제 수행하는 함수
        )

        self.get_logger().info('Action server ready: /fibonacci')
```

## 4) `goal_handle.succeed()` 하면 클라이언트의 `get_result_async()`로 들어가?

정확히는 이 흐름이야:

1. 서버 `execute_cb`가 `return result`를 한다 (여기서 result 객체가 만들어짐)
2. 서버가 `goal_handle.succeed()` 상태를 표시한다
3. 클라이언트가 `goal_handle.get_result_async()`로 기다리던 `result_future`가 **완료**되고,
4. 클라이언트는 그 결과를 `result_future.result().result`로 꺼낸다

즉 `succeed()` “한 줄”이 결과를 보내는 게 아니라,

- **succeed() + return result** 가 합쳐져서 “성공 상태의 최종 결과”가 클라이언트로 가는 거야.

```jsx
def execute_cb(self, goal_handle):
        # (2) goal(요청) 값 확인
        order = goal_handle.request.order
        #goal_handle.request = Fibonacci.Goal 객체
				#goal_handle.request.order = 클라이언트가 보낸 order 값
        self.get_logger().info(f'Goal received: order={order}')

        # (3) 피드백/결과 객체 준비
        feedback = Fibonacci.Feedback()
        feedback.partial_sequence = [0, 1] #feedback에 보내는 값

        # (4) “진행 중” 피드백을 여러 번 보내기 (action의 핵심)
        for i in range(2, order):
            # 취소 요청 들어왔는지 체크(최소 구성이라 간단히만)
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                result = Fibonacci.Result()
                result.sequence = feedback.partial_sequence
                return result

            feedback.partial_sequence.append(
                feedback.partial_sequence[i - 1] + feedback.partial_sequence[i - 2]
            )

            # 피드백 publish
            goal_handle.publish_feedback(feedback)
            self.get_logger().info(f'Feedback: {feedback.partial_sequence}')

            time.sleep(0.5)  # “작업이 진행 중”인 것처럼 딜레이

        # (5) 작업 완료 처리
        goal_handle.succeed()

        # (6) 최종 결과 반환
        result = Fibonacci.Result()
        result.sequence = feedback.partial_sequence
        self.get_logger().info(f'Result: {result.sequence}')
        return result
```

### 1) 왜 처음에 `[0, 1]`을 넣어?

피보나치 수열은 **앞의 두 항을 더해서 다음 항을 만드는 규칙**이라 “시작값 2개”가 필요해.

- 규칙: `F(n) = F(n-1) + F(n-2)`
- 그래서 보통 시작을 `F(0)=0`, `F(1)=1`로 둬.
    
    (다른 정의도 있지만 ROS2 예제 Fibonacci는 이걸 씀)
    

시작값이 없으면 “이전 두 개”가 없어서 계산을 시작할 수가 없어.

---

### 2) `i=2 → [1] + [0]` 이게 무슨 의미고 결과가 어떻게 나와?

이미 `partial_sequence = [0, 1]` 상태에서:

- i=2일 때 새 항은
    
    `partial_sequence[1] + partial_sequence[0]`
    
    = `1 + 0 = 1`
    

그래서 리스트가:

- 처음: `[0, 1]`
- i=2 후: `[0, 1, 1]`

다음 i=3이면:

- `partial_sequence[2] + partial_sequence[1] = 1 + 1 = 2`
- `[0, 1, 1, 2]`

i=4:

- `2 + 1 = 3` → `[0, 1, 1, 2, 3]`

이런 식으로 “앞의 두 개를 더해서” 계속 늘어나는 게 피보나치 수열이야.

### 3) `time.sleep(0.5)` 왜 “작업 중인 것처럼” 딜레이를 줘?

액션(Action)의 핵심은 **“오래 걸리는 작업”**을 가정하고,

그동안 **중간 진행상황(feedback)**을 여러 번 보내는 거야.

근데 피보나치 계산은 너무 빨라서 바로 끝나버리면

- 피드백이 “계속 오는 모습”이 잘 안 보여.

그래서 예제에서는 일부러 `sleep`을 넣어서:

- “진짜 시간이 걸리는 작업처럼”
- 피드백이 0.5초마다 한 번씩 오도록 만든 거야.

실제로 로봇에서라면 sleep 대신:

- 이동 중 경로 진행률,
- 센서 처리 진행률,
- 탐색 알고리즘 진행 상황
    
    같은 **진짜 시간이 걸리는 처리**가 들어가겠지.
    

### 4) Goal / Feedback / Result에 값이 “어떻게” 들어가?

예를 들어 클라이언트가 `order=6`을 보냈다고 해보자.

### (1) Goal

- 클라이언트가 goal에 값을 넣음:
    - `goal_msg.order = 6`
- 서버는 그걸 이렇게 읽음:
    - `order = goal_handle.request.order` → `6`

### (2) Feedback (진행 중 여러 번)

서버가 계산하면서 `partial_sequence`를 계속 업데이트하고 publish함:

- 시작: `[0, 1]` (첫 피드백)
- 다음: `[0, 1, 1]`
- 다음: `[0, 1, 1, 2]`
- 다음: `[0, 1, 1, 2, 3]`
- 다음: `[0, 1, 1, 2, 3, 5]`

클라이언트는 그때그때 `feedback_cb`에서 이 리스트를 받는 거야.

### (3) Result (마지막 1번)

서버가 끝나면:

- `result.sequence = feedback.partial_sequence`
- 즉 최종 리스트(예: `[0,1,1,2,3,5]`)를 result에 넣어서 `return result`

클라이언트는:

- `result_future`가 완료되면
- 최종 결과 `sequence`를 한 번에 받음.
