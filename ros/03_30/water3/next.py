import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

# =========================================================
# 설정
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TRAIN_DIR = os.path.join(BASE_DIR, "data", "train")
VALID_DIR = os.path.join(BASE_DIR, "data", "valid")

# 기존에 학습해서 저장해둔 내 모델
MODEL_PATH = os.path.join(BASE_DIR, "water_cnn.keras")

# 이어서 학습 후 새로 저장할 모델 이름
SAVE_MODEL_PATH = os.path.join(BASE_DIR, "water_cnn_next.keras")

IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 10

# =========================================================
# 데이터 전처리 / 증강
# train 은 증강
# valid 는 평가용이므로 증강하지 않음
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
    class_mode="binary",   # water / no_water 두 클래스
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
# 기존 모델 불러오기
# =========================================================
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"기존 모델이 없습니다: {MODEL_PATH}")

model = tf.keras.models.load_model(MODEL_PATH)

# 현재 모델 구조 확인
model.summary()

# =========================================================
# 컴파일
# 이어서 학습할 때 learning rate 를 조금 낮게 두는 편이 안전함
# =========================================================
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
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
# 이어서 학습
# =========================================================
history = model.fit(
    train_generator,
    validation_data=valid_generator,
    epochs=EPOCHS,
    callbacks=[early_stop, reduce_lr, checkpoint]
)

# =========================================================
# 마지막 모델도 저장
# =========================================================
model.save(SAVE_MODEL_PATH)
print(f"이어학습 모델 저장 완료: {SAVE_MODEL_PATH}")