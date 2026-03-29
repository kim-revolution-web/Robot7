import random
import shutil
from pathlib import Path
from ultralytics import YOLO

# 현재 train_yolo.py 파일이 있는 폴더
BASE_DIR = Path(__file__).resolve().parent


def make_valid_set(base_dir=BASE_DIR, valid_ratio=0.2):
    base = Path(base_dir)

    train_img_dir = base / "raw" / "images"
    train_lbl_dir = base / "raw" / "labels"

    valid_img_dir = base / "valid" / "images"
    valid_lbl_dir = base / "valid" / "labels"

    # raw 폴더 존재 확인
    if not train_img_dir.exists():
        raise FileNotFoundError(f"학습 이미지 폴더가 없습니다: {train_img_dir}")
    if not train_lbl_dir.exists():
        raise FileNotFoundError(f"학습 라벨 폴더가 없습니다: {train_lbl_dir}")

    # valid 폴더 생성
    valid_img_dir.mkdir(parents=True, exist_ok=True)
    valid_lbl_dir.mkdir(parents=True, exist_ok=True)

    image_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    train_images = [p for p in train_img_dir.iterdir() if p.suffix.lower() in image_exts]

    if len(train_images) == 0:
        raise FileNotFoundError(f"학습 이미지가 없습니다: {train_img_dir}")

    # 이미 valid 안에 파일이 있으면 다시 만들지 않음
    existing_valid = list(valid_img_dir.iterdir())
    if existing_valid:
        print("valid 폴더가 이미 있어서 분할을 건너뜁니다.")
        return

    random.shuffle(train_images)
    valid_count = max(1, int(len(train_images) * valid_ratio))
    valid_files = train_images[:valid_count]

    for img_path in valid_files:
        label_path = train_lbl_dir / f"{img_path.stem}.txt"

        shutil.copy2(img_path, valid_img_dir / img_path.name)

        if label_path.exists():
            shutil.copy2(label_path, valid_lbl_dir / label_path.name)
        else:
            print(f"경고: 라벨 없음 -> {label_path.name}")

    print(f"valid 생성 완료: {len(valid_files)}장")


def write_data_yaml(base_dir=BASE_DIR, class_names=None):
    if class_names is None:
        class_names = ["water"]

    base = Path(base_dir)
    yaml_path = base / "data.yaml"

    # YOLO에서 잘 읽히게 절대경로로 저장
    train_path = (base / "raw" / "images").as_posix()
    val_path = (base / "valid" / "images").as_posix()

    content = f"""raw: {train_path}
val: {val_path}

nc: {len(class_names)}
names: {class_names}
"""

    yaml_path.write_text(content, encoding="utf-8")
    print(f"data.yaml 작성 완료: {yaml_path}")


def train_yolo(base_dir=BASE_DIR):
    base = Path(base_dir)
    data_yaml = base / "data.yaml"

    if not data_yaml.exists():
        raise FileNotFoundError(f"data.yaml 파일이 없습니다: {data_yaml}")

    model = YOLO("yolov8n.pt")

    results = model.train(
        data=str(data_yaml),
        epochs=50,
        imgsz=512,
        batch=16,
        project=str(base / "runs"),
        name="water_train",
        patience=15,
        save=True,
        device=0
    )
    print("학습 완료")
    print(results)


if __name__ == "__main__":
    # 클래스가 1개면 이렇게
    class_names = ["water"]

    # raw -> valid 자동 분할
    make_valid_set(valid_ratio=0.2)

    # data.yaml 자동 작성
    write_data_yaml(class_names=class_names)

    # 학습 시작
    train_yolo()