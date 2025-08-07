from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

students_df = pd.read_csv("students.csv")

@app.route("/", methods=["GET", "POST"])
def home():
    success = False
    error = False
    message = ""

    if request.method == "POST":
        student_id = request.form["student_id"].strip()
        match = students_df[students_df["StudentID"] == student_id]

        if not match.empty:
            name = match.iloc[0]["Name"]
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")
            time = now.strftime("%I:%M %p")

            entry = pd.DataFrame([[student_id, name, date, time]],
                                 columns=["StudentID", "Name", "Date", "Time"])

            if os.path.exists("meal_log.csv"):
                log_df = pd.read_csv("meal_log.csv")
                log_df = pd.concat([log_df, entry], ignore_index=True)
            else:
                log_df = entry

            log_df.to_csv("meal_log.csv", index=False)
            success = True
            message = f"{name} ({student_id}) logged at {time} on {date}"
        else:
            error = True
            message = "Student ID not found."

    return render_template("form.html", success=success, error=error, message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
