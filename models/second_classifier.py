from sklearn.neural_network import MLPClassifier

mlp_model = MLPClassifier(
    hidden_layer_sizes=(256, 128, 64),
    activation="relu",
    solver="adam",
    alpha=1e-4,
    batch_size=1024,
    learning_rate_init=1e-3,
    max_iter=100,
    early_stopping=True,
    n_iter_no_change=8,
    random_state=42,
    verbose=True
)