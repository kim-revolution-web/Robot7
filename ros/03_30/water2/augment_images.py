import cv2
import numpy as np
from pathlib import Path
import albumentations as A

BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "raw"
OUTPUT_DIR = BASE_DIR / "augmented"

CLASS_NAMES = ["no_water", "water"]
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

transform = A.Compose([
    A.Affine(
        scale=(0.9, 1.1),
        translate_percent={"x": (-0.08, 0.08), "y": (-0.08, 0.08)},
        rotate=(-15, 15),
        shear=(-8, 8),
        p=0.8
    ),
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(
        brightness_limit=0.2,
        contrast_limit=0.2,
        p=0.6
    ),
    A.OneOf([
        A.GaussianBlur(blur_limit=(3, 5), p=1.0),
        A.MotionBlur(blur_limit=(3, 5), p=1.0),
        A.GaussNoise(std_range=(0.02, 0.06), p=1.0),
    ], p=0.3),
])


def imread_korean(path: Path):
    data = np.fromfile(str(path), dtype=np.uint8)
    if data.size == 0:
        return None
    return cv2.imdecode(data, cv2.IMREAD_COLOR)


def imwrite_korean(path: Path, image):
    ext = path.suffix if path.suffix else ".jpg"
    ok, buf = cv2.imencode(ext, image)
    if not ok:
        return False
    buf.tofile(str(path))
    return True


def augment_one_class(class_name: str):
    input_class_dir = INPUT_DIR / class_name
    output_class_dir = OUTPUT_DIR / class_name
    output_class_dir.mkdir(parents=True, exist_ok=True)

    if not input_class_dir.exists():
        print(f"폴더 없음: {input_class_dir}")
        return

    image_paths = sorted([p for p in input_class_dir.iterdir() if p.suffix.lower() in IMAGE_EXTS])

    if not image_paths:
        print(f"이미지 없음: {input_class_dir}")
        return

    for img_path in image_paths:
        image = imread_korean(img_path)
        if image is None:
            print(f"읽기 실패: {img_path}")
            continue

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        stem = img_path.stem

        for i in range(1, 101):
            augmented = transform(image=image)["image"]
            augmented = cv2.cvtColor(augmented, cv2.COLOR_RGB2BGR)

            save_name = f"{stem}-{i:03d}.jpg"
            save_path = output_class_dir / save_name
            imwrite_korean(save_path, augmented)

        print(f"{class_name} / {img_path.name} -> 100장 완료")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for class_name in CLASS_NAMES:
        augment_one_class(class_name)

    print("전체 완료")


if __name__ == "__main__":
    main()