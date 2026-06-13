# KQC7016 Assignment 2 - AI for Medicine
# IoMT Sleep-Stress Early Warning Decision Support
# Dataset: SaYoPillow / Human Stress Detection in and through Sleep

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, f1_score, classification_report, mean_absolute_error, r2_score, silhouette_score

df = pd.read_csv("SaYoPillow_sleep_stress_working_dataset.csv")
features = ["sr", "rr", "t", "lm", "bo", "rem", "sr.1", "hr"]
X = df[features]
y = df["sl"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
models = {
    "Logistic Regression": Pipeline([("scaler", StandardScaler()), ("clf", LogisticRegression(max_iter=2000, class_weight="balanced"))]),
    "SVM (RBF)": Pipeline([("scaler", StandardScaler()), ("clf", SVC(C=4, probability=True, class_weight="balanced", random_state=42))]),
    "Random Forest": RandomForestClassifier(n_estimators=220, max_depth=6, random_state=42, class_weight="balanced")
}
for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    print("\n", name)
    print("Accuracy:", round(accuracy_score(y_test, pred), 3))
    print("Macro F1:", round(f1_score(y_test, pred, average="macro"), 3))
    print(classification_report(y_test, pred))

# Clustering
X_scaled = StandardScaler().fit_transform(X)
clusters = KMeans(n_clusters=5, n_init=20, random_state=42).fit_predict(X_scaled)
print("Silhouette score:", round(silhouette_score(X_scaled, clusters), 3))

# Regression: predict sleep hours
reg_features = ["sr", "rr", "t", "lm", "bo", "rem", "hr"]
Xr_train, Xr_test, yr_train, yr_test = train_test_split(df[reg_features], df["sr.1"], test_size=0.25, random_state=42)
reg = RandomForestRegressor(n_estimators=200, max_depth=7, random_state=42)
reg.fit(Xr_train, yr_train)
yr_pred = reg.predict(Xr_test)
print("Sleep-hours MAE:", round(mean_absolute_error(yr_test, yr_pred), 3))
print("Sleep-hours R2:", round(r2_score(yr_test, yr_pred), 3))
