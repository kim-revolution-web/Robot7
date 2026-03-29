print("1. 파이썬 시작")

import os
print("2. 현재 작업 폴더:", os.getcwd())

import sys
print("3. 파이썬 경로:", sys.executable)

import tensorflow as tf
print("4. tensorflow import 성공")
print(tf.__version__)

print("5. 끝")