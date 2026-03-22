import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
import xgboost as xgb
from catboost import CatBoostRegressor

# 1. Load dataset
df = pd.read_csv("data/crop-yield1.csv")

# ✅ Separate features and target
X = df.drop("Crop_Yield_ton_per_hectare", axis=1)
y = df["Crop_Yield_ton_per_hectare"]

# ✅ Convert categorical columns into numeric (one-hot encoding)
X = pd.get_dummies(X)

# 2. Train RandomForest
rf_model = RandomForestRegressor()
rf_model.fit(X, y)
joblib.dump(rf_model, "models/random_forest.pkl")

# 3. Train XGBoost
xgb_model = xgb.XGBRegressor()
xgb_model.fit(X, y)
xgb_model.save_model("models/xgboost.json")

# 4. Train CatBoost
# CatBoost can handle categorical directly, but here we use encoded X for consistency
cat_model = CatBoostRegressor(verbose=0)
cat_model.fit(X, y)
joblib.dump(cat_model, "models/catboost.pkl")

# 5. Train ANN
ann_model = MLPRegressor(max_iter=500)
ann_model.fit(X, y)
joblib.dump(ann_model, "models/ann.pkl")

print("✅ Models trained and saved successfully!")
