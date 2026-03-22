from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import joblib
import xgboost as xgb
from catboost import CatBoostRegressor
import pandas as pd
import os
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ---------- Load Models ----------
rf_model = joblib.load("models/random_forest.pkl")
cat_model = joblib.load("models/catboost.pkl")
ann_model = joblib.load("models/ann.pkl")
xgb_model = xgb.XGBRegressor()
xgb_model.load_model("models/xgboost.json")

# ---------- Routes ----------

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database/users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = email
            return redirect(url_for("predict"))  # ✅ go straight to prediction after login
        else:
            return "Invalid credentials. Please try again."

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database/users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route("/predict", methods=["GET", "POST"])
def predict():
    # ✅ Require login
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        data = {
            "N": float(request.form["N"]),
            "P": float(request.form["P"]),
            "K": float(request.form["K"]),
            "Soil_pH": float(request.form["Soil_pH"]),
            "Soil_Moisture": float(request.form["Soil_Moisture"]),
            "Organic_Carbon": float(request.form["Organic_Carbon"]),
            "Temperature": float(request.form["Temperature"]),
            "Humidity": float(request.form["Humidity"]),
            "Rainfall": float(request.form["Rainfall"]),
            "Sunlight_Hours": float(request.form["Sunlight_Hours"]),
            "Wind_Speed": float(request.form["Wind_Speed"]),
            "Altitude": float(request.form["Altitude"]),
            "Fertilizer_Used": float(request.form["Fertilizer_Used"]),
            "Pesticide_Used": float(request.form["Pesticide_Used"]),
            "Hectares": float(request.form["Hectares"]),
        }

        user_yield = request.form.get("Crop_Yield_ton_per_hectare")
        user_yield = float(user_yield) if user_yield else None

        # Prepare input
        X_input = pd.DataFrame([data])
        df = pd.read_csv("data/crop-yield1.csv")
        X_train = pd.get_dummies(df.drop("Crop_Yield_ton_per_hectare", axis=1))
        X_input = pd.get_dummies(X_input).reindex(columns=X_train.columns, fill_value=0)

        # Predictions
        rf_prediction = rf_model.predict(X_input)[0]
        results = {
            "RandomForest": rf_prediction,
            "XGBoost": xgb_model.predict(X_input)[0],
            "CatBoost": cat_model.predict(X_input)[0],
            "ANN": ann_model.predict(X_input)[0],
        }

        hectares = data["Hectares"]
        total_production = rf_prediction * hectares

        return render_template("result.html",
                               prediction=rf_prediction,
                               results=results,
                               user_yield=user_yield,
                               hectares=hectares,
                               total_production=total_production)

    return render_template("predict.html")

@app.route("/eda")
def eda():
    if "user" not in session:
        return redirect(url_for("login"))

    df = pd.read_csv("data/crop-yield1.csv")
    rainfall_col = [c for c in df.columns if "rain" in c.lower()][0]
    yield_col = [c for c in df.columns if "yield" in c.lower()][0]

    plt.figure(figsize=(6,4))
    plt.scatter(df[rainfall_col], df[yield_col], alpha=0.6)
    plt.xlabel(rainfall_col)
    plt.ylabel(yield_col)
    plt.title(f"{rainfall_col} vs {yield_col}")

    if not os.path.exists("static"):
        os.makedirs("static")
    plt.savefig("static/eda_plot.png")
    plt.close()

    return render_template("eda.html")

# ---------- Main ----------
if __name__ == "__main__":
    app.run(debug=True)
