```python
import tensorflow as tf
from tensorflow.keras import layers, models

# 변수 설정
IMG_SIZE = 128
NUM_CLASSES = 5   
BATCH_SIZE = 32

# 데이터셋 로드
train_ds = tf.keras.utils.image_dataset_from_directory(
    './dataset',
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    color_mode='grayscale'
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    './dataset',
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    color_mode='grayscale'
)

# 모델 구성
model = models.Sequential([
    # 128 * 128 인풋
    layers.Input(shape=(IMG_SIZE, IMG_SIZE, 1)),

    # 정규화를 가장 먼저 수행
    layers.Rescaling(1./255),

    # 데이터 증강 (도형의 크기,반전과 회전)
    layers.RandomFlip("horizontal_and_vertical"),
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.1),

    layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
    layers.BatchNormalization(), # 학습 속도와 안정성 향상
    layers.MaxPooling2D(),

    layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(),

    layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(),

    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5), 
    layers.Dense(NUM_CLASSES, activation='softmax')
])

# 4. 컴파일 및 콜백 설정
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# 과적합 방지를 위한 조기 종료 설정
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)

# 5. 학습 시작
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=30,
    callbacks=[early_stopping]
)

print("학습 완료")

# 5. 모델 저장 (나중에 불러다 쓰기 위함)
model.save('shape_model_9.keras')
print("\n 모델이 'shape_model_9.keras'로 저장되었습니다.")
```

```python
#----------------------------
# 모델 테스트 코드
#------------------------------
import tensorflow as tf
import numpy as np
import cv2
import os
import random
import matplotlib.pyplot as plt

# 1. 모델 불러오기
model = tf.keras.models.load_model('shape_model_9.keras')

# 2. 테스트 할 사진들이 들어있는 폴더 경로
test_folder = './test'

# 3. 폴더 내 파일 목록 중 하나를 랜덤하게 선택
file_list = [f for f in os.listdir(test_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
random_file = random.choice(file_list)
file_path = os.path.join(test_folder, random_file)

print(f" 선택된 파일: {random_file}")

# 4. 이미지 전처리 함수 (모델 학습 설정과 동일하게 맞춤)
def prepare_image(path):
    # 그레이스케일로 읽기
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    # 모델 학습 사이즈인 128x128로 리사이즈
    img = cv2.resize(img, (128, 128))

    # [이진화 처리]
    # 학습 데이터가 깨끗한 흑백이라면 유지, 아니라면 이 부분을 주석 처리해도 됩니다.
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # 정규화(/255.0)는 모델의 Rescaling 층에서 수행하므로 여기서는 생략합니다.
    # 모델 입력 형태인 (batch, height, width, channel) -> (1, 128, 128, 1)로 변환
    img = img.reshape(1, 128, 128, 1).astype('float32')
    return img

# 5. 예측 실행
processed_img = prepare_image(file_path)
prediction = model.predict(processed_img)

# 결과 해석
class_names = ['Circle', 'Rectangle', 'Triangle', 'X','xother']
result_index = np.argmax(prediction)
confidence = np.max(prediction) * 100

print("-" * 30)
print(f" 모델의 예측: {class_names[result_index]}")
print(f" 확신도: {confidence:.2f}%")
print("-" * 30)

# 6. 결과 화면에 띄우기
plt.imshow(cv2.imread(file_path, cv2.IMREAD_GRAYSCALE), cmap='gray')
plt.title(f"Predict: {class_names[result_index]} ({confidence:.2f}%)")
plt.axis('off') # 격자 제거
plt.show()

```

```python
import tensorflow as tf
import numpy as np
import cv2
import os
import random
import matplotlib.pyplot as plt

# 1. 모델 불러오기 
model = tf.keras.models.load_model('shape_model_7.keras')

# 2. 사진 폴더 경로
test_folder = './test'
file_list = [f for f in os.listdir(test_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

if not file_list:
    print("❌ './test' 폴더에 이미지가 없습니다.")
    exit()

random_file = random.choice(file_list)
file_path = os.path.join(test_folder, random_file)
print(f"🎲 선택된 파일: {random_file}")

# 4. 이미지 전처리 함수 (학습 데이터 생성기와 로직 일치)
def prepare_image(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    
    # [추가] 실시간 영상 처리와 동일하게 테두리 5px 제거
    margin = 5
    if img.shape[0] > margin*2 and img.shape[1] > margin*2:
        img = img[margin:-margin, margin:-margin]
    
    # 리사이즈
    img = cv2.resize(img, (128, 128))

    # [중요] 실시간/학습 데이터와 이진화 방향 맞추기
    # 만약 배경이 검정, 도형이 흰색이어야 한다면 THRESH_BINARY
    # 반대로 배경이 흰색, 도형이 검정이라면 THRESH_BINARY_INV를 사용하세요.
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # 모델 입력용 시각화 이미지 보관
    visual_img = img.copy()
    
    # (1, 128, 128, 1)로 변환
    img = img.reshape(1, 128, 128, 1).astype('float32')
    return img, visual_img

# 5. 예측 실행
processed_img, visual_img = prepare_image(file_path)
prediction = model.predict(processed_img, verbose=0)

# 5개 클래스 순서 (알파벳 순서 주의)
class_names = ['Circle', 'Rectangle', 'Triangle', 'X', 'xother']
result_index = np.argmax(prediction)
confidence = np.max(prediction) * 100

print("-" * 30)
print(f"🎯 모델의 예측: {class_names[result_index]}")
print(f"📊 확신도: {confidence:.2f}%")
print("-" * 30)

# 6. 결과 화면에 띄우기 (전처리된 이미지와 원본 비교)
plt.figure(figsize=(10, 5))

# 원본 이미지
plt.subplot(1, 2, 1)
plt.imshow(cv2.imread(file_path), cmap='gray')
plt.title("Original Test Image")
plt.axis('off')

# 모델이 실제로 본 이미지 (128x128, 크롭됨)
plt.subplot(1, 2, 2)
plt.imshow(visual_img, cmap='gray')
plt.title(f"Model View: {class_names[result_index]} ({confidence:.1f}%)")
plt.axis('off')

plt.show()
```
