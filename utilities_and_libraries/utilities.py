from utilities_and_libraries.libraries import *

def dataset_download(dataset_path):
    """Download the EMBER/Thrember Win64 dataset into the specified path."""
    os.makedirs(dataset_path, exist_ok=True)
    thrember.download_dataset(
        download_dir=dataset_path,
        file_type="Win64"
    )
    os.chdir("..")


def clean_challenge_non_win64(path):
    """Remove non-Win64 samples from challenge files (keeps only Win64 lines)."""
    for f in os.listdir(path):
        if "challenge" not in f:
            continue
        lines = [l for l in open(os.path.join(path, f)) if json.loads(l).get("file_type") == "Win64"]
        open(os.path.join(path, f), "w").writelines(lines)


def count_files_and_rows(path):
    """Count the number of JSONL files and total lines for train/test/challenge."""
    sets = ["train", "test", "challenge"]
    for s in sets:
        files = [f for f in os.listdir(path) if s in f and f.endswith(".jsonl")]
        rows = sum(sum(1 for _ in open(os.path.join(path, f))) for f in files)
        print(f"{s}: {len(files)} files, {rows} lines")


def count_labels(dataset="dataset"):
    """Count the number of benign and malicious samples in train/test/challenge sets."""
    groups = {"train": Counter(), "challenge": Counter(), "test": Counter()}

    for file in Path(dataset).rglob("*.jsonl"):
        name = file.name.lower()
        g = "train" if "train" in name else "challenge" if "challenge" in name else "test" if "test" in name else None
        if not g:
            continue
        for line in file.open(encoding="utf-8", errors="ignore"):
            try:
                lbl = json.loads(line).get("label")
                if lbl in (0, 1):
                    groups[g][lbl] += 1
            except:
                pass

    for k, v in groups.items():
        if sum(v.values()):
            print(f"{k}: benign={v[0]}, malicious={v[1]}")


def print_features(dataset_path):
    """Print the feature keys (first sample) from one dataset file."""
    for f in os.listdir(dataset_path):
        if f.endswith(".jsonl"):
            with open(os.path.join(dataset_path, f)) as file:
                first = json.loads(next(file))
                print(list(first.keys()))
            break


def vectorize_dataset(vectorized_dataset_path):
    """Generate and store vectorized features for the dataset."""
    os.makedirs(vectorized_dataset_path, exist_ok=True)
    thrember.create_vectorized_features(
        data_dir=vectorized_dataset_path,
        label_type="label"
    )

def load_vectorized_datasets(path):
    """Load vectorized train, test, and challenge datasets."""
    x_train, y_train = thrember.read_vectorized_features(path, "train")
    x_test, y_test = thrember.read_vectorized_features(path, "test")
    x_chal, y_chal = thrember.read_vectorized_features(path, "challenge")
    return x_train, y_train, x_test, y_test, x_chal, y_chal

def plot_feature_comparison(x1, y1, x2, y2,
                            label1_type='malicious',
                            label2_type='malicious',
                            name1='Train',
                            name2='Test/Chall',
                            step=10):
    """Compare the mean feature values between two datasets (train/test/challenge)."""
    label_map = {'benign': 0, 'malicious': 1}

    if label1_type not in label_map or label2_type not in label_map:
        raise ValueError("label_type must be 'benign' or 'malicious'.")

    lbl1 = label_map[label1_type]
    lbl2 = label_map[label2_type]

    idx = np.arange(0, x1.shape[1], step)
    mean1 = x1[y1 == lbl1].mean(0)[idx]
    mean2 = x2[y2 == lbl2].mean(0)[idx]

    plt.figure(figsize=(12, 4))
    plt.plot(idx, mean1, 'g', lw=1.2, label=f"{name1} {label1_type.capitalize()}")
    plt.plot(idx, mean2, 'b', lw=1.2, label=f"{name2} {label2_type.capitalize()}", alpha=0.8)
    plt.fill_between(idx, mean1, mean2, color='purple', alpha=0.15)

    plt.title(f"Feature Means – {name1} {label1_type.capitalize()} vs {name2} {label2_type.capitalize()}")
    plt.xlabel("Feature Index")
    plt.ylabel("Mean Value")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

def train_and_plot_times(models, x_train, y_train, save_path="trained_models"):
    """Train multiple models, record training times, save them, and display a time comparison bar chart."""
    os.makedirs(save_path, exist_ok=True)
    times = {}
    trained_models = {}

    for name, model in models.items():
        print(f"⏳ Training {name}...")
        start = time.time()
        model.fit(x_train, y_train)
        elapsed = time.time() - start
        times[name] = elapsed
        trained_models[name] = model
        print(f"✅ {name} completed in {elapsed:.2f} seconds")

        model_file = os.path.join(save_path, f"{name.replace(' ', '_')}.pkl")
        with open(model_file, "wb") as f:
            pickle.dump(model, f)
        print(f"💾 Saved to: {model_file}\n")

    plt.figure(figsize=(7, 4))
    plt.bar(times.keys(), times.values(), color="skyblue")
    plt.title("Training Time per Model")
    plt.ylabel("Seconds")
    plt.xlabel("Model")
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.show()

    return trained_models


def evaluate_accuracy(models, x_test, y_test):
    """Compute and plot the accuracy of each model on test data."""
    accuracies = {}
    print("📊 Model accuracies:")
    for name, model in models.items():
        y_pred = model.predict(x_test)
        acc = accuracy_score(y_test, y_pred)
        accuracies[name] = acc
        print(f"{name}: {acc:.4f}")

    plt.figure(figsize=(6, 4))
    plt.bar(accuracies.keys(), accuracies.values())
    plt.title("Model Accuracy")
    plt.ylabel("Accuracy")
    plt.ylim(0, 1)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.show()

    return accuracies


def save_models(models, save_dir="models/saved_models"):
    """Save trained models as .pkl files in the specified directory."""
    os.makedirs(save_dir, exist_ok=True)
    for name, model in models.items():
        path = os.path.join(save_dir, f"{name.replace(' ', '_')}.pkl")
        with open(path, "wb") as f:
            pickle.dump(model, f)
        print(f"💾 Saved: {path}")


def load_models(path="models/saved_models"):
    """Load all .pkl models from a directory."""
    models = {}
    for f in os.listdir(path):
        if f.endswith(".pkl"):
            p = os.path.join(path, f)
            try:
                with open(p, "rb") as file:
                    models[f[:-4]] = pickle.load(file)
            except Exception as e:
                print(f"❌ Error loading {f}: {e}")
    print("✅ Models loaded:", ", ".join(models.keys()) if models else "none")
    return models
