import os
import random
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


class DataReader:
    def __init__(self, data_dir="augmented", image_size=(150, 150), train_ratio=0.8):
        self.data_dir = data_dir
        self.image_size = image_size
        self.train_ratio = train_ratio

        self.labels = ["no_water", "water"]

        self.train_X = []
        self.train_Y = []
        self.test_X = []
        self.test_Y = []

        self.read_images()

    def read_images(self):
        data = []
        print("Reading Data...")

        for i, cls in enumerate(self.labels):
            class_dir = os.path.join(self.data_dir, cls)

            if not os.path.isdir(class_dir):
                print(f"폴더 없음: {class_dir}")
                continue

            print(f"Opening {cls}/")

            for file_name in os.listdir(class_dir):
                img_path = os.path.join(class_dir, file_name)

                try:
                    img = Image.open(img_path).convert("RGB")
                    img = img.resize(self.image_size)
                    arr = np.asarray(img)
                    data.append((arr, i))
                    img.close()
                except Exception as e:
                    print(f"읽기 실패: {img_path}, 오류: {e}")

        random.shuffle(data)

        split_idx = int(len(data) * self.train_ratio)

        for idx, (img, label) in enumerate(data):
            if idx < split_idx:
                self.train_X.append(img)
                self.train_Y.append(label)
            else:
                self.test_X.append(img)
                self.test_Y.append(label)

        self.train_X = np.asarray(self.train_X, dtype=np.float32) / 255.0
        self.train_Y = np.asarray(self.train_Y, dtype=np.float32)

        self.test_X = np.asarray(self.test_X, dtype=np.float32) / 255.0
        self.test_Y = np.asarray(self.test_Y, dtype=np.float32)

        print("\nData Read Done!")
        print("Training X Size :", self.train_X.shape)
        print("Training Y Size :", self.train_Y.shape)
        print("Test X Size     :", self.test_X.shape)
        print("Test Y Size     :", self.test_Y.shape)
        print()

    def show_processed_images(self):
        plt.figure(figsize=(10, 10))
        for i in range(min(25, len(self.train_X))):
            plt.subplot(5, 5, i + 1)
            plt.xticks([])
            plt.yticks([])
            plt.grid(False)
            plt.imshow(self.train_X[i])
            plt.xlabel(self.labels[int(self.train_Y[i])])
        plt.show()


def draw_graph(history):
    train_loss = history.history["loss"]
    val_loss = history.history["val_loss"]

    fig = plt.figure(figsize=(8, 8))
    plt.title("Loss History")
    plt.xlabel("EPOCH")
    plt.ylabel("Loss")
    plt.plot(train_loss, "red", label="raw")
    plt.plot(val_loss, "blue", label="val")
    plt.legend()
    fig.savefig("train_history.png")

    train_acc = history.history["accuracy"]
    val_acc = history.history["val_accuracy"]

    fig = plt.figure(figsize=(8, 8))
    plt.title("Accuracy History")
    plt.xlabel("EPOCH")
    plt.ylabel("Accuracy")
    plt.plot(train_acc, "red", label="raw")
    plt.plot(val_acc, "blue", label="val")
    plt.legend()
    fig.savefig("accuracy_history.png")