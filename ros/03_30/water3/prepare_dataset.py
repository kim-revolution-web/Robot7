import os
import random
import shutil
from pathlib import Path

import cv2
import numpy as np

# =========================
# 설정
# =========================
BASE_DIR = Path(__file__).resolve().parent

RAW_DIR = BASE_DIR / "data" / "raw"
TRAIN_DIR = BASE_DIR / "data" / "train"
VALID_DIR = BASE_DIR / "data" / "valid"

CLASSES = ["water", "no_water"]

VALID_RATIO = 0.2
AUG_PER_TRAIN_IMAGE = 9   # 원본 1장 + 증강 9장 = 총 10장
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

random.seed(42)
np.random.seed(42)


# =========================
# 폴더 비우고 다시 만들기
# =========================
def reset_dir(path: Path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def ensure_class_dirs(root: Path):
    for cls in CLASSES:
        (root / cls).mkdir(parents=True, exist_ok=True)


# =========================
# 이미지 목록 가져오기
# =========================
def get_image_files(folder: Path):
    return sorted([
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    ])


# =========================
# 증강 함수
# =========================
def augment_image(img):
    h, w = img.shape[:2]

    # 1) 작은 회전
    angle = random.uniform(-10, 10)
    center = (w // 2, h // 2)
    rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)

    # 2) 약간 이동
    tx = random.uniform(-0.05 * w, 0.05 * w)
    ty = random.uniform(-0.05 * h, 0.05 * h)
    rot_mat[0, 2] += tx
    rot_mat[1, 2] += ty

    aug = cv2.warpAffine(
        img,
        rot_mat,
        (w, h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT_101
    )

    # 3) 밝기/대비 약간 변경
    alpha = random.uniform(0.9, 1.1)   # contrast
    beta = random.uniform(-10, 10)     # brightness
    aug = cv2.convertScaleAbs(aug, alpha=alpha, beta=beta)

    # 4) 가끔 좌우 반전
    if random.random() < 0.5:
        aug = cv2.flip(aug, 1)

    return aug


# =========================
# 저장
# =========================
def save_jpg(path: Path, img):
    path.parent.mkdir(parents=True, exist_ok=True)
    success = cv2.imwrite(str(path), img)
    if not success:
        raise IOError(f"이미지 저장 실패: {path}")


# =========================
# 메인 처리
# =========================
def main():
    # train, valid 새로 만들기
    reset_dir(TRAIN_DIR)
    reset_dir(VALID_DIR)
    ensure_class_dirs(TRAIN_DIR)
    ensure_class_dirs(VALID_DIR)

    for cls in CLASSES:
        src_dir = RAW_DIR / cls
        if not src_dir.exists():
            print(f"[오류] 폴더 없음: {src_dir}")
            continue

        files = get_image_files(src_dir)
        if len(files) == 0:
            print(f"[경고] 이미지 없음: {src_dir}")
            continue

        random.shuffle(files)

        valid_count = max(1, int(len(files) * VALID_RATIO))
        valid_files = files[:valid_count]
        train_files = files[valid_count:]

        print(f"\n[{cls}] 전체 {len(files)}장")
        print(f"  train 원본: {len(train_files)}장")
        print(f"  valid 원본: {len(valid_files)}장")

        # -----------------
        # valid: 원본만 복사
        # -----------------
        for idx, file_path in enumerate(valid_files, start=1):
            img = cv2.imread(str(file_path))
            if img is None:
                print(f"[스킵] 읽기 실패: {file_path}")
                continue

            out_name = f"{idx:03d}_val.jpg"
            save_jpg(VALID_DIR / cls / out_name, img)

        # -----------------
        # train: 원본 + 증강
        # -----------------
        for idx, file_path in enumerate(train_files, start=1):
            img = cv2.imread(str(file_path))
            if img is None:
                print(f"[스킵] 읽기 실패: {file_path}")
                continue

            # 원본 저장
            original_name = f"{idx:03d}_01.jpg"
            save_jpg(TRAIN_DIR / cls / original_name, img)

            # 증강 저장
            for aug_idx in range(2, AUG_PER_TRAIN_IMAGE + 2):
                aug_img = augment_image(img)
                aug_name = f"{idx:03d}_{aug_idx:02d}.jpg"
                save_jpg(TRAIN_DIR / cls / aug_name, aug_img)

    print("\n데이터셋 준비 완료!")
    print(f"원본 위치: {RAW_DIR}")
    print(f"학습 위치: {TRAIN_DIR}")
    print(f"검증 위치: {VALID_DIR}")


if __name__ == "__main__":
    main()