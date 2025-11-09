# 📘 Machine Learning Project
**Short description**: The project aims to develop three ML/DL models for Win64 malware detection and evaluate their effectiveness on challenge data.

---

## Overview

- **Project Objective**: Develop and compare three Machine Learning and Deep Learning models for malware detection, and evaluate their effectiveness on the EMBER 2024 challenge dataset.

- **Problem Statement**: Detecting Win64 malware is one of the most complex and demanding tasks in cybersecurity. These samples often employ advanced obfuscation, packing, and polymorphism, which make static analysis and classification extremely difficult. This remains a significant challenge for major antivirus vendors and threat intelligence teams.

- **Proposed Solution**: Train two Machine Learning models and one Deep Learning model using the EMBER 2024 dataset. The goal is not only to achieve strong detection performance but also to analyze differences between the training and challenge datasets, in order to understand why certain samples—particularly those in the challenge set—are so difficult to detect.

---

## Features
- Dataset utilities for analysis and handling  
- Functions for training and managing models

---

## Project Structure

- **Introduction and Setup**: Overview of the project goals, the EMBER 2024 dataset, and the environment configuration required to run the experiments.

- **Data Analysis and Normalization**: Exploration of the dataset structure, key statistics, and normalization steps to prepare data for model training.

- **Model Training and Accuracy Analysis**: Training of three selected models (two ML and one DL), performance comparison, and evaluation of accuracy, precision, and recall.

- **Testing on Challenge Data**: Evaluation of the trained models on the unseen challenge dataset to assess generalization and investigate the causes of misclassifications.

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/username/project-name.git
cd project-name

# 2. Create the virtual environment
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)

# 3. Install dependencies
pip install -r requirements.txt
```

## Usage

- The project includes a clear main script with preprocessing and experiments already prepared. You can also run the code step by step.


## Credits

- Special thanks to the creators of the EMBER 2024 dataset.