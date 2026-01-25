Raspberry Pi


# ip route && ping -c 5 8.8.8.8
eth0 : 유선
wlan0 :무선

***라즈베리 파이 원격접속 고정하기
1) SSH가 부팅 때 항상 켜지게

라즈베리에서 한 번만:

sudo systemctl enable --now ssh

2) 다음부터 IP 안 바뀌게(선택)

공유기에서 DHCP 고정(예약) 해두면 제일 편해.
(또는 나중에 netplan으로 고정 IP)
***
DHCP 고정 = 주소(집 주소) 고정
enable ssh = 문(원격 접속문) 항상 열어두기
저 메시지는 “ssh 서비스를 부팅 때 자동 시작(enable) 시켰고, 지금도 즉시 시작(now) 했다”는 뜻이야. 에러가 없으니까 성공.

바로 확인하는 법 (라즈베리에서)
sudo systemctl status ssh --no-pager
여기서 active (running) 나오면 100% 완료.
