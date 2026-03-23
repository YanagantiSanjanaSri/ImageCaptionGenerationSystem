from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Dummy caption generator (replace with your deep learning model)
def generate_caption(image_path):
    return "A person standing near a beautiful landscape."


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return "No file uploaded"

    file = request.files["image"]

    if file.filename == "":
        return "No selected file"

    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)

    caption = generate_caption(path)

    return render_template("result.html", caption=caption, image=file.filename)


if __name__ == "__main__":
    app.run(debug=True)