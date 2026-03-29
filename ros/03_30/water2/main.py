from tensorflow import keras
import data_reader

EPOCHS = 20

dr = data_reader.DataReader(
    data_dir="augmented",
    image_size=(150, 150),
    train_ratio=0.8
)

model = keras.Sequential([
    keras.layers.Input(shape=(150, 150, 3)),

    keras.layers.Conv2D(16, (3, 3), activation="relu"),
    keras.layers.MaxPooling2D((2, 2)),

    keras.layers.Conv2D(32, (3, 3), activation="relu"),
    keras.layers.MaxPooling2D((2, 2)),

    keras.layers.Conv2D(64, (3, 3), activation="relu"),
    keras.layers.MaxPooling2D((2, 2)),

    keras.layers.Conv2D(64, (3, 3), activation="relu"),
    keras.layers.MaxPooling2D((2, 2)),

    keras.layers.Flatten(),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(1, activation="sigmoid")
])

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

print("\n************ TRAINING START ************")

early_stop = keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)

history = model.fit(
    dr.train_X,
    dr.train_Y,
    epochs=EPOCHS,
    validation_data=(dr.test_X, dr.test_Y),
    callbacks=[early_stop]
)

model.save("water_classifier.keras")
data_reader.draw_graph(history)

loss, acc = model.evaluate(dr.test_X, dr.test_Y, verbose=0)
print(f"\nTest Loss: {loss:.4f}")
print(f"Test Accuracy: {acc:.4f}")