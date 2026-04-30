import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

from flask import Flask, render_template, request
import numpy as np
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

# -----------------------------
# Sample dataset (for demo ML model)
# -----------------------------
X = np.array([
    [2,150,30,0,5],
    [5,300,10,60,9],
    [1,50,40,0,2],
    [3,200,20,30,7]
])
y = np.array([1,0,1,0])

model = LogisticRegression()
model.fit(X, y)

# -----------------------------
# Routes
# -----------------------------
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/assessment')
def assessment():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get input values
    screen = float(request.form['screen'])
    caffeine = float(request.form['caffeine'])
    activity = float(request.form['activity'])
    nap = float(request.form['nap'])
    stress = float(request.form['stress'])

    # -----------------------------
    # Stress Level Label
    # -----------------------------
    if stress <= 3:
        stress_label = "Low"
    elif stress <= 6:
        stress_label = "Moderate"
    else:
        stress_label = "High"

    # -----------------------------
    # Scoring Logic
    # -----------------------------
    screen_score = max(0, (1 - screen / 5)) * 15
    caffeine_score = max(0, (1 - caffeine / 200)) * 15
    activity_score = min(activity / 60, 1) * 25
    nap_score = max(0, (1 - nap / 60)) * 10
    stress_score = max(0, (1 - stress / 10)) * 35

    score = round(screen_score + caffeine_score + activity_score + nap_score + stress_score, 1)
    prob = score / 100

    result = "Good Sleep Quality 😊" if prob > 0.5 else "Poor Sleep Quality 😴"

    # -----------------------------
    # Estimated Sleep Hours
    # -----------------------------
    sleep_hours = round(4 + (prob * 4), 1)  # Range: 4 to 8 hrs

    # -----------------------------
    # Tips & Advice Section
    # -----------------------------
    tips = []

    # Screen Time Tips
    if screen > 2:
        tips.append("Reduce screen time at least 1 hour before bed")
        tips.append("Use blue light filters or night mode on devices")
        tips.append("Avoid using mobile in bed")

    # Caffeine Tips
    if caffeine > 150:
        tips.append("Avoid caffeine at least 6 hours before sleep")
        tips.append("Switch to healthier drinks like herbal tea or milk")

    # Activity Tips
    if activity < 20:
        tips.append("Do at least 30 minutes of exercise daily")
        tips.append("Try yoga or light evening walking")

    # Nap Tips
    if nap > 30:
        tips.append("Limit naps to 20–30 minutes")
        tips.append("Avoid late afternoon naps")

    # Stress Tips
    if stress > 6:
        tips.append("Practice meditation or breathing exercises")
        tips.append("Try journaling before sleep")
        tips.append("Listen to calming music or white noise")

    # General Tips (always shown)
    tips.append("Maintain a consistent sleep schedule")
    tips.append("Keep your room cool, dark, and quiet")
    tips.append("Avoid heavy meals before bedtime")
    tips.append("Follow a relaxing bedtime routine")

    # Personalized Advice
    if prob < 0.5:
        tips.append("Your sleep quality is low — improve habits step by step")
    else:
        tips.append("Great job! Maintain your healthy routine")

    # -----------------------------
    # Render Result
    # -----------------------------
    return render_template(
        'result.html',
        score=score,
        result=result,
        tips=tips,
        stress=stress,
        stress_label=stress_label,
        sleep_hours=sleep_hours
    )

# -----------------------------
# Run App
# -----------------------------
if __name__ == '__main__':
    app.run(debug=False)