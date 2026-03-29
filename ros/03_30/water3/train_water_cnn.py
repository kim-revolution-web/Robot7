import os
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from tensorflow.keras.callbacks import ModelCheckpoint

# =========================
# 설정
# =========================
IMG_SIZE = 224        # 입력 이미지 크기 (224x224)
BATCH_SIZE = 16       # 한 번에 학습할 이미지 개수
EPOCHS = 15          # 전체 데이터셋을 몇 번 반복 학습할지

TRAIN_DIR = "data/train"          # 학습용 이미지 폴더 경로
VALID_DIR = "data/valid"          # 검증용 이미지 폴더 경로
MODEL_PATH = "water_cnn.keras"  # 학습 완료 후 저장할 모델 파일명

# =========================
# 데이터 전처리/증강
# =========================
# train 데이터는 학습용이므로 약간씩 변형해서 데이터 수를 늘리는 효과를 줌
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255.0,        # 픽셀값을 0~255 → 0~1로 정규화
    rotation_range=10,          # 이미지를 -10도~+10도 정도 회전
    width_shift_range=0.1,      # 가로 방향으로 최대 10% 이동
    height_shift_range=0.1,     # 세로 방향으로 최대 10% 이동
    zoom_range=0.1,             # 최대 10% 확대/축소
    brightness_range=(0.8, 1.2),# 밝기를 조금 어둡게/밝게 변경
    horizontal_flip=True        # 좌우 반전 허용
)

# valid 데이터는 평가용이므로 증강하지 않고 정규화만 함
valid_datagen = ImageDataGenerator(
    rescale=1.0 / 255.0
)

# train 폴더에서 이미지를 읽어서 배치 단위로 만들어줌
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),  # 모든 이미지를 224x224로 맞춤
    batch_size=BATCH_SIZE,
    class_mode="binary",               # 이진 분류 (water / no_water)
    shuffle=True                       # 학습 시 이미지를 섞음
)

# valid 폴더에서 이미지를 읽어서 배치 단위로 만들어줌
valid_generator = valid_datagen.flow_from_directory(
    VALID_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="binary",
    shuffle=False                      # 검증은 보통 순서 유지
)

# 가장 성능 좋은 모델만 저장하고 싶을 때 쓰는 코드
# checkpoint = ModelCheckpoint(
#     "best_water_model.keras",
#     monitor="val_accuracy",   # 검증 정확도 기준으로 저장
#     save_best_only=True       # 가장 좋은 결과만 저장
# )

# 현재 클래스 이름과 숫자 매핑 확인
print("클래스 인덱스:", train_generator.class_indices)
# 예: {'no_water': 0, 'water': 1}

# =========================
# CNN 모델
# =========================
model = models.Sequential([
    # 입력 이미지 크기 지정
    layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),

    # 첫 번째 합성곱 층
    # 필터 256개로 특징 추출
    layers.Conv2D(256, (3, 3), activation="relu"),
    # 특징맵 크기를 절반으로 줄임
    layers.MaxPooling2D((2, 2)),

    # 두 번째 합성곱 층
    layers.Conv2D(128, (3, 3), activation="relu"),
    layers.MaxPooling2D((2, 2)),

    # 세 번째 합성곱 층
    layers.Conv2D(64, (3, 3), activation="relu"),
    layers.MaxPooling2D((2, 2)),

    # 네 번째 합성곱 층
    layers.Conv2D(32, (3, 3), activation="relu"),
    layers.MaxPooling2D((2, 2)),

    # 아래는 예전에 쓰던 Flatten 방식
    # Flatten은 모든 특징을 한 줄로 펼쳐서 넘기기 때문에
    # 파라미터 수가 많아질 수 있음
    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.3),

    # GlobalAveragePooling2D는 각 채널의 평균만 뽑아서
    # 모델을 더 가볍게 만들어 줌

    # layers.GlobalAveragePooling2D(),
    # # 완전연결층
    # layers.Dense(64, activation="relu"),
    # # 과적합 방지를 위해 일부 뉴런을 랜덤하게 끔
    # layers.Dropout(0.3),

    # 마지막 출력층
    # sigmoid는 0~1 사이 값 출력
    # 1에 가까우면 water, 0에 가까우면 no_water
    layers.Dense(1, activation="sigmoid")
])

# =========================
# 모델 학습 설정
# =========================
model.compile(
    optimizer="adam",               # 가중치 업데이트 방법
    loss="binary_crossentropy",     # 이진 분류용 손실 함수
    metrics=["accuracy"]            # 정확도 출력
)

# 모델 구조 출력
model.summary()

# =========================
# 학습
# =========================
history = model.fit(
    train_generator,                # 학습용 데이터
    validation_data=valid_generator,# 검증용 데이터
    epochs=EPOCHS                   # 반복 학습 횟수
)

# =========================
# 저장
# =========================
# 학습이 끝난 모델을 파일로 저장
model.save(MODEL_PATH)
print(f"모델 저장 완료: {MODEL_PATH}")