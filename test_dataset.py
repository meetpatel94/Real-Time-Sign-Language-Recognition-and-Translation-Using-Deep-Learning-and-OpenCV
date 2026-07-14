from training.dataset_loader import load_dataset

X_train, X_test, y_train, y_test, classes = load_dataset("dataset")

print(classes)
print(X_train.shape)
print(y_train.shape)