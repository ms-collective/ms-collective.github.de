from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import os
app = Flask(__name__)

# Configure Flask-Mail with your SMTP server (e.g., Gmail)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

@app.route("/send-message", methods=["POST"])
def send_message():
    data = request.json  # Get JSON data from request
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not name or not email or not message:
        return jsonify({"error": "All fields are required."}), 400

    msg = Message("New Contact Form Submission",
                  sender=email,
                  recipients=["info@drinkrack.de"])  # Replace with your recipient email
    msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

    try:
        mail.send(msg)
        return jsonify({"success": "Message sent successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)