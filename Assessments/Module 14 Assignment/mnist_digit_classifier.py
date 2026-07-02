"""
Handwritten Digit Classifier (MNIST) — Deep Learning Project
==============================================================

A fully-connected deep neural network that classifies handwritten
digits (0-9) from the MNIST dataset, built with TensorFlow/Keras.

Covers:
  1. Dataset loading
  2. Preprocessing (normalization + flattening + one-hot labels)
  3. Model architecture (3 hidden layers, BatchNorm, Dropout)
  4. Training (with validation split, multiple epochs, history logging)
  5. Visualization (accuracy & loss curves)
  6. Evaluation (test accuracy, confusion matrix, sample predictions)

Run with:  python mnist_digit_classifier.py
Requires:  tensorflow >= 2.x, numpy, matplotlib, scikit-learn (optional, for confusion matrix)
"""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping

# Reproducibility
tf.random.set_seed(42)
np.random.seed(42)

# ---------------------------------------------------------------------------
# 1. Dataset loading
# ---------------------------------------------------------------------------
print("Loading MNIST dataset...")
(x_train, y_train), (x_test, y_test) = mnist.load_data()
print(f"Train set: {x_train.shape}, {y_train.shape}")
print(f"Test set:  {x_test.shape}, {y_test.shape}")

# ---------------------------------------------------------------------------
# 2. Preprocessing
# ---------------------------------------------------------------------------
# Normalize pixel values to [0, 1]
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

# Flatten the 28x28 images into 784-length vectors for a dense network
x_train = x_train.reshape(x_train.shape[0], 28 * 28)
x_test = x_test.reshape(x_test.shape[0], 28 * 28)

# One-hot encode the labels (needed for categorical_crossentropy)
num_classes = 10
y_train_cat = to_categorical(y_train, num_classes)
y_test_cat = to_categorical(y_test, num_classes)

print(f"Flattened train shape: {x_train.shape}")
print(f"One-hot label shape:   {y_train_cat.shape}")

# ---------------------------------------------------------------------------
# 3. Model architecture
#    3 hidden layers, Batch Normalization after each, Dropout for
#    regularization.
# ---------------------------------------------------------------------------
model = Sequential([
    Dense(256, activation="relu", input_shape=(784,)),
    BatchNormalization(),
    Dropout(0.3),

    Dense(128, activation="relu"),
    BatchNormalization(),
    Dropout(0.3),

    Dense(64, activation="relu"),
    BatchNormalization(),
    Dropout(0.2),

    Dense(num_classes, activation="softmax"),
])

model.summary()

# ---------------------------------------------------------------------------
# 4. Training
# ---------------------------------------------------------------------------
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)

early_stop = EarlyStopping(
    monitor="val_loss",
    patience=4,
    restore_best_weights=True,
)

EPOCHS = 20
BATCH_SIZE = 128

history = model.fit(
    x_train, y_train_cat,
    validation_split=0.1,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    callbacks=[early_stop],
    verbose=2,
)

# ---------------------------------------------------------------------------
# 5. Visualization — training vs validation accuracy & loss
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Accuracy
axes[0].plot(history.history["accuracy"], label="Train Accuracy", linewidth=2)
axes[0].plot(history.history["val_accuracy"], label="Validation Accuracy", linewidth=2)
axes[0].set_title("Training vs Validation Accuracy")
axes[0].set_xlabel("Epoch")
axes[0].set_ylabel("Accuracy")
axes[0].legend()
axes[0].grid(alpha=0.3)

# Loss
axes[1].plot(history.history["loss"], label="Train Loss", linewidth=2)
axes[1].plot(history.history["val_loss"], label="Validation Loss", linewidth=2)
axes[1].set_title("Training vs Validation Loss")
axes[1].set_xlabel("Epoch")
axes[1].set_ylabel("Loss")
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("training_history.png", dpi=150)
print("Saved training curves to training_history.png")
plt.show()

# ---------------------------------------------------------------------------
# 6. Evaluation
# ---------------------------------------------------------------------------
test_loss, test_accuracy = model.evaluate(x_test, y_test_cat, verbose=0)
print(f"\nFinal Test Loss:     {test_loss:.4f}")
print(f"Final Test Accuracy: {test_accuracy:.4f} ({test_accuracy * 100:.2f}%)")

# Predictions on the test set
y_pred_probs = model.predict(x_test, verbose=0)
y_pred = np.argmax(y_pred_probs, axis=1)

# Optional: confusion matrix (requires scikit-learn)
try:
    from sklearn.metrics import confusion_matrix, classification_report

    cm = confusion_matrix(y_test, y_pred)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, digits=4))

    plt.figure(figsize=(8, 7))
    plt.imshow(cm, cmap="Blues")
    plt.title("Confusion Matrix")
    plt.colorbar()
    plt.xticks(range(10), range(10))
    plt.yticks(range(10), range(10))
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    for i in range(10):
        for j in range(10):
            plt.text(j, i, cm[i, j], ha="center", va="center",
                      color="white" if cm[i, j] > cm.max() / 2 else "black", fontsize=8)
    plt.tight_layout()
    plt.savefig("confusion_matrix.png", dpi=150)
    print("Saved confusion matrix to confusion_matrix.png")
    plt.show()
except ImportError:
    print("scikit-learn not installed; skipping confusion matrix.")

# Visualize a handful of test predictions
fig, axes = plt.subplots(2, 5, figsize=(12, 5))
sample_idx = np.random.choice(len(x_test), 10, replace=False)
for ax, idx in zip(axes.flatten(), sample_idx):
    ax.imshow(x_test[idx].reshape(28, 28), cmap="gray")
    color = "green" if y_pred[idx] == y_test[idx] else "red"
    ax.set_title(f"Pred: {y_pred[idx]} (True: {y_test[idx]})", color=color, fontsize=10)
    ax.axis("off")
plt.tight_layout()
plt.savefig("sample_predictions.png", dpi=150)
print("Saved sample predictions to sample_predictions.png")
plt.show()

# Save the trained model
model.save("mnist_digit_classifier.keras")
print("\nModel saved to mnist_digit_classifier.keras")
