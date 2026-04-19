from flask import Flask, request

app = Flask(__name__)

# 허용 명령만 받기(실수/장난 URL 방지)
ALLOWED = {"UP","DOWN","LEFT","RIGHT","STOP","GO","BACK","AUTO"}

def send(cmd: str):
    # 발표 시연용: 서버 터미널에 찍기
    ip = request.remote_addr
    print(f"[CMD] {cmd}  from {ip}")
    return f"OK: {cmd}\n"

@app.get("/")
def home():
    # PyQt UI 비슷하게 배치(대충 같은 느낌)
    return """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OneTouch Remote</title>
<style>
  body { font-family: Arial, sans-serif; margin: 20px; }
  .board {
    position: relative;
    width: 844px; height: 529px;
    border: 2px solid #55aa00;
    background: #f7f7f7;
    overflow: hidden;
  }
  button {
    position: absolute;
    width: 101px; height: 61px;
    border: 1px solid #bbb;
    background: white;
    font-weight: 700;
    border-radius: 8px;
    cursor: pointer;
  }
  /* PyQt 스타일 비슷하게 */
  #go, #stop, #right {
    background: #2d6cdf; color: white; border: none;
  }
  #go { border-radius: 30px; }
  #stop { border-radius: 12px; }
  #right { border-radius: 25px; }
  #back {
    background: #ff00ff; color: white; border: none; border-radius: 12px;
  }
  #stop:hover { background: #ff0000; }
  #go:hover, #right:hover { background: #1f4fa8; }
  #back:hover { background: #1f4fa8; }

  .status { margin-top: 10px; font-size: 16px; }
</style>
</head>
<body>
  <h2>OneTouch Remote</h2>
  <div class="board">
    <!-- 좌측 버튼들 (ui 좌표 참고) -->
    <button id="up"   style="left:170px; top:230px;" onclick="cmd('UP')">up</button>
    <button id="auto" style="left:170px; top:320px;" onclick="cmd('AUTO')">auto</button>
    <button id="down" style="left:170px; top:400px;" onclick="cmd('DOWN')">down</button>

    <!-- 중앙/우측 버튼들 -->
    <button id="go"    style="left:530px; top:220px;" onclick="cmd('GO')">go</button>
    <button id="left"  style="left:400px; top:320px;" onclick="cmd('LEFT')">left</button>
    <button id="stop"  style="left:530px; top:320px;" onclick="cmd('STOP')">stop</button>
    <button id="right" style="left:670px; top:320px;" onclick="cmd('RIGHT')">right</button>
    <button id="back"  style="left:530px; top:410px;" onclick="cmd('BACK')">back</button>
  </div>

  <div class="status" id="status">버튼을 누르면 서버 터미널에 출력됩니다.</div>

<script>
async function cmd(c){
  const r = await fetch('/cmd/' + c);
  const t = await r.text();
  document.getElementById('status').innerText = t.trim();
}
</script>
</body>
</html>
"""

@app.get("/cmd/<c>")
def cmd(c):
    c = c.upper()
    if c not in ALLOWED:
        return "BAD CMD\n", 400
    return send(c)

if __name__ == "__main__":
    # 같은 와이파이에서 폰으로 접속하려면 0.0.0.0
    app.run(host="0.0.0.0", port=5000)