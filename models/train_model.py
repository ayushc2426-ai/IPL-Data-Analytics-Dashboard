import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from sklearn.metrics import accuracy_score

# -----------------------------
# Load Data
# -----------------------------
matches = pd.read_csv("data/matches.csv")
deliveries = pd.read_csv("data/deliveries.csv")

# -----------------------------
# Merge
# -----------------------------
matches = matches.dropna(subset=["winner"])

deliveries = deliveries.merge(
    matches[
        [
            "id",
            "city",
            "winner",
            "target_runs"
        ]
    ],
    left_on="match_id",
    right_on="id"
)

# -----------------------------
# Feature Engineering
# -----------------------------

deliveries["current_score"] = (
    deliveries.groupby("match_id")["total_runs"].cumsum()
)

deliveries["balls_bowled"] = (
    (deliveries["over"] - 1) * 6 + deliveries["ball"]
)

deliveries["balls_left"] = 120 - deliveries["balls_bowled"]

deliveries = deliveries[deliveries["balls_left"] > 0]

deliveries["runs_left"] = (
    deliveries["target_runs"] - deliveries["current_score"]
)

deliveries["wickets_fallen"] = (
    deliveries.groupby("match_id")["is_wicket"].cumsum()
)

deliveries["wickets_left"] = 10 - deliveries["wickets_fallen"]

deliveries["current_rr"] = (
    deliveries["current_score"] * 6
) / deliveries["balls_bowled"]

deliveries["current_rr"] = deliveries["current_rr"].replace(float("inf"),0)

deliveries["required_rr"] = (
    deliveries["runs_left"] * 6
) / deliveries["balls_left"]

deliveries["pressure_index"] = (
    deliveries["required_rr"] - deliveries["current_rr"]
)

def phase(over):
    if over <= 6:
        return "Powerplay"
    elif over <= 15:
        return "Middle"
    else:
        return "Death"

deliveries["phase"] = deliveries["over"].apply(phase)

deliveries["result"] = (
    deliveries["batting_team"] == deliveries["winner"]
).astype(int)

# ----------------------------------------
# Keep only valid rows
# ----------------------------------------

deliveries = deliveries[
    (deliveries["runs_left"] >= 0)
]

# ----------------------------------------
# Final Dataset
# ----------------------------------------

final_df = deliveries[
    [
        "batting_team",
        "bowling_team",
        "city",
        "runs_left",
        "balls_left",
        "wickets_left",
        "target_runs",
        "current_rr",
        "required_rr",
        "pressure_index",
        "phase",
        "result"
    ]
].dropna()

# ----------------------------------------
# X and y
# ----------------------------------------

X = final_df.drop("result", axis=1)

y = final_df["result"]

# ----------------------------------------
# Train Test Split
# ----------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ----------------------------------------
# Preprocessing
# ----------------------------------------

categorical = [
    "batting_team",
    "bowling_team",
    "city",
    "phase"
]

preprocessor = ColumnTransformer(
    [
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical
        )
    ],
    remainder="passthrough"
)

# ----------------------------------------
# Models
# ----------------------------------------

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),

    "Random Forest": RandomForestClassifier(
        n_estimators=50,
        random_state=42,
        n_jobs=-1
    ),

    "Gradient Boosting": GradientBoostingClassifier(
        random_state=42
    )
}

best_model = None
best_accuracy = 0

for name, model in models.items():

    pipe = Pipeline(
        [
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    pipe.fit(X_train, y_train)

    pred = pipe.predict(X_test)

    acc = accuracy_score(y_test, pred)

    print(f"{name}: {acc:.4f}")

    if acc > best_accuracy:
        best_accuracy = acc
        best_model = pipe

print("\nBest Accuracy:", best_accuracy)

joblib.dump(best_model, "models/pipe.pkl")

print("\nModel Saved Successfully!")