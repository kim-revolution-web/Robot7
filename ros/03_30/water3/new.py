import os
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

# =========================================================
# 설정
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TRAIN_DIR = os.path.join(BASE_DIR, "data", "train")
VALID_DIR = os.path.join(BASE_DIR, "data", "valid")

# 새 전이학습 모델 저장 파일명
SAVE_MODEL_PATH = os.path.join(BASE_DIR, "water_transfer.keras")

IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 10

# =========================================================
# 데이터 전처리 / 증강
# =========================================================
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255.0,
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    brightness_range=(0.8, 1.2),
    horizontal_flip=True
)

valid_datagen = ImageDataGenerator(
    rescale=1.0 / 255.0
)

train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="binary",
    shuffle=True
)

valid_generator = valid_datagen.flow_from_directory(
    VALID_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="binary",
    shuffle=False
)

print("클래스 인덱스:", train_generator.class_indices)

# =========================================================
# 사전학습 모델 불러오기
# include_top=False :
#   원래 ImageNet 1000개 분류용 마지막 층은 제거
# weights="imagenet" :
#   ImageNet으로 학습된 가중치 사용
# =========================================================
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights="imagenet"
)

# 처음에는 기본 모델을 얼려서
# 마지막 분류층만 먼저 학습
base_model.trainable = False

# =========================================================
# 새 모델 구성
# =========================================================
model = models.Sequential([
    tf.keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
    base_model,
    layers.GlobalAveragePooling2D(),  # Flatten 대신 가볍게 특징 요약
    layers.Dropout(0.3),              # 과적합 방지
    layers.Dense(1, activation="sigmoid")  # 이진분류 출력
])

model.summary()

# =========================================================
# 컴파일
# =========================================================
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

# =========================================================
# 콜백
# =========================================================
early_stop = EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)

reduce_lr = ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.5,
    patience=2,
    min_lr=1e-7
)

checkpoint = ModelCheckpoint(
    filepath=SAVE_MODEL_PATH,
    monitor="val_accuracy",
    save_best_only=True
)

# =========================================================
# 1차 학습
# 사전학습 모델은 고정한 채 마지막 층만 학습
# =========================================================
history = model.fit(
    train_generator,
    validation_data=valid_generator,
    epochs=EPOCHS,
    callbacks=[early_stop, reduce_lr, checkpoint]
)

# =========================================================
# 1차 학습 모델 저장
# =========================================================
model.save(SAVE_MODEL_PATH)
print(f"전이학습 모델 저장 완료: {SAVE_MODEL_PATH}")