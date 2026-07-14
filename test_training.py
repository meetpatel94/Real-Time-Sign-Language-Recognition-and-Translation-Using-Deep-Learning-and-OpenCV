from training.trainer import train_model

result = train_model(
    epochs=10,
    batch_size=16,
)

print(result)