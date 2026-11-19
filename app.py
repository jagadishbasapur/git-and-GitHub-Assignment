from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

app = Flask(__name__)

# Load environment variables
load_dotenv()

# MongoDB Atlas connection
MONGO_URI = os.getenv("MONGO_URI")


# Task 1: JSON API Route
@app.route("/api")
def api():

    try:
        with open("data.json", "r") as file:
            data = json.load(file)

        return jsonify(data)

    except Exception as error:
        return jsonify({"error": str(error)}), 500


# Home page with frontend form
@app.route("/", methods=["GET", "POST"])
def home():

    error_message = None

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        course = request.form.get("course")

        if not name or not email or not course:
            error_message = "Please fill in all fields."
            return render_template("index.html", error=error_message), 400

        try:
            if not MONGO_URI:
                raise ValueError("MongoDB connection string is not configured.")

            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

            # Check database connection
            client.admin.command("ping")

            # Select database and collection
            db = client["flask_assignment"]
            collection = db["students"]

            # Insert form data
            student = {
                "name": name,
                "email": email,
                "course": course
            }

            collection.insert_one(student)

            client.close()

            return render_template("success.html")

        except Exception as error:
            error_message = str(error)
            return render_template("index.html", error=error_message), 500

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)