
# for deployment on Render
import os
import io
import glob
from flask import Flask, render_template, request, send_file
from PIL import Image
import google.generativeai as genai
import markdown
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Flask setup
app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper: Load image from path
def load_image(image_path):
    with open(image_path, "rb") as img_file:
        image_bytes = img_file.read()
    return Image.open(io.BytesIO(image_bytes))

# Helper: Analyze image using Gemini
def detect_image_content(image_path):
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    image = load_image(image_path)
    try:
        response = model.generate_content([image, "Describe the contents of this image."])
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Route: Home page and image upload
@app.route("/", methods=["GET", "POST"])
def index():
    descriptions = []

    # Clear previous uploads
    for f in glob.glob(os.path.join(UPLOAD_FOLDER, "*")):
        os.remove(f)

    if request.method == "POST":
        files = request.files.getlist("images")
        for file in files:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            try:
                file.save(filepath)
                if filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif")):
                    raw_desc = detect_image_content(filepath)
                    html_desc = markdown.markdown(raw_desc)
                    descriptions.append((filename, html_desc))
                else:
                    descriptions.append((filename, "<p>Unsupported file type.</p>"))
            except Exception as e:
                descriptions.append((filename, f"<p>Error processing file: {e}</p>"))

        # Save all descriptions to a text file
        with open("descriptions.txt", "w", encoding="utf-8") as f:
            for name, desc in descriptions:
                f.write(f"{name}:\n{markdown.markdown(desc)}\n\n")

        return render_template("index.html", results=descriptions)

    return render_template("index.html", results=None)

# Route: Download results
@app.route("/download")
def download():
    return send_file("descriptions.txt", as_attachment=True)

# Run the app (Render-compatible)
if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)
    except KeyboardInterrupt:
        print("\nServer stopped by user.")







# # import os
# # from flask import Flask, render_template, request, send_file
# # from PIL import Image
# # import io
# # import google.generativeai as genai
# # import markdown 
# # from dotenv import load_dotenv

# # load_dotenv()
# # genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# # app = Flask(__name__)
# # UPLOAD_FOLDER = "static/uploads"
# # os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # def load_image(image_path):
# #     with open(image_path, "rb") as img_file:
# #         image_bytes = img_file.read()
# #     return Image.open(io.BytesIO(image_bytes))

# # def detect_image_content(image_path):
# #     model = genai.GenerativeModel("models/gemini-2.0-flash")
# #     image = load_image(image_path)
# #     try:
# #         response = model.generate_content([image, "Describe the contents of this image."])
# #         return response.text
# #     except Exception as e:
# #         return f"Error: {e}"

# # @app.route("/", methods=["GET", "POST"])
# # def index():
# #     descriptions = []
# #     if request.method == "POST":
# #         files = request.files.getlist("images")
# #         for file in files:
# #             filename = file.filename
# #             filepath = os.path.join(UPLOAD_FOLDER, filename)
# #             file.save(filepath)
# #             desc = detect_image_content(filepath)
# #             descriptions.append((filename, desc))

# #         with open("descriptions.txt", "w", encoding="utf-8") as f:
# #             for name, desc in descriptions:
# #                 f.write(f"{name}:\n{desc}\n\n")

# #         return render_template("index.html", results=descriptions)

# #     return render_template("index.html", results=None)

# # @app.route("/download")
# # def download():
# #     return send_file("descriptions.txt", as_attachment=True)

# # if __name__ == "__main__":
# #     app.run(debug=True)


# # import os
# # import io
# # import cv2
# # from flask import Flask, render_template, request, send_file
# # from PIL import Image
# # import google.generativeai as genai
# # import markdown
# # from dotenv import load_dotenv
# # import glob
# # for f in glob.glob(os.path.join(UPLOAD_FOLDER, "*")):
# #     os.remove(f)

# # load_dotenv()
# # genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # app = Flask(__name__)
# # UPLOAD_FOLDER = "static/uploads"
# # os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # def load_image(image_path):
# #     with open(image_path, "rb") as img_file:
# #         image_bytes = img_file.read()
# #     return Image.open(io.BytesIO(image_bytes))

# # def extract_key_frames(video_path, max_frames=5):
# #     cap = cv2.VideoCapture(video_path)
# #     frames = []
# #     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# #     interval = max(1, total_frames // max_frames)

# #     for i in range(0, total_frames, interval):
# #         cap.set(cv2.CAP_PROP_POS_FRAMES, i)
# #         success, frame = cap.read()
# #         if success:
# #             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# #             pil_image = Image.fromarray(rgb_frame)
# #             frames.append(pil_image)
# #         if len(frames) >= max_frames:
# #             break
# #     cap.release()
# #     return frames

# # def detect_image_content(image_path):
# #     model = genai.GenerativeModel("models/gemini-2.0-flash")
# #     image = load_image(image_path)
# #     try:
# #         response = model.generate_content([image, "Describe the contents of this image."])
# #         return response.text
# #     except Exception as e:
# #         return f"Error: {e}"

# # def detect_video_content(video_path):
# #     model = genai.GenerativeModel("models/gemini-2.0-pro-vision")
# #     frames = extract_key_frames(video_path)
# #     descriptions = []

# #     for i, frame in enumerate(frames):
# #         try:
# #             response = model.generate_content([frame, f"Describe frame {i+1} of this video."])
# #             descriptions.append(f"**Frame {i+1}:** {response.text}")
# #         except Exception as e:
# #             descriptions.append(f"**Frame {i+1}:** Error - {e}")

# #     return "\n\n".join(descriptions)

# # @app.route("/", methods=["GET", "POST"])
# # def index():
# #     descriptions = []
# #     if request.method == "POST":
# #         files = request.files.getlist("images")
# #         for file in files:
# #             filename = file.filename
# #             filepath = os.path.join(UPLOAD_FOLDER, filename)
# #             file.save(filepath)

# #             if filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
# #                 raw_desc = detect_video_content(filepath)
# #             else:
# #                 raw_desc = detect_image_content(filepath)

# #             html_desc = markdown.markdown(raw_desc)
# #             descriptions.append((filename, html_desc))

# #         with open("descriptions.txt", "w", encoding="utf-8") as f:
# #             for name, desc in descriptions:
# #                 f.write(f"{name}:\n{markdown.markdown(desc)}\n\n")

# #         return render_template("index.html", results=descriptions)

# #     return render_template("index.html", results=None)

# # @app.route("/download")
# # def download():
# #     return send_file("descriptions.txt", as_attachment=True)

# # if __name__ == "__main__":
# #     app.run(debug=True)













# # for Local development

# import os
# import io
# import glob
# from flask import Flask, render_template, request, send_file
# from PIL import Image
# import google.generativeai as genai
# import markdown
# from dotenv import load_dotenv
# from werkzeug.utils import secure_filename

# # Load environment variables and configure Gemini
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # Flask setup
# app = Flask(__name__)
# UPLOAD_FOLDER = "static/uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Helper: Load image from path
# def load_image(image_path):
#     with open(image_path, "rb") as img_file:
#         image_bytes = img_file.read()
#     return Image.open(io.BytesIO(image_bytes))

# # Helper: Analyze image using Gemini
# def detect_image_content(image_path):
#     model = genai.GenerativeModel("models/gemini-2.0-flash")
#     image = load_image(image_path)
#     try:
#         response = model.generate_content([image, "Describe the contents of this image."])
#         return response.text
#     except Exception as e:
#         return f"Error: {e}"

# # Route: Home page and image upload
# @app.route("/", methods=["GET", "POST"])
# def index():
#     descriptions = []

#     # Clear previous uploads
#     for f in glob.glob(os.path.join(UPLOAD_FOLDER, "*")):
#         os.remove(f)

#     if request.method == "POST":
#         files = request.files.getlist("images")
#         for file in files:
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(UPLOAD_FOLDER, filename)
#             file.save(filepath)

#             # Only process image files
#             if filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif")):
#                 raw_desc = detect_image_content(filepath)
#                 html_desc = markdown.markdown(raw_desc)
#                 descriptions.append((filename, html_desc))

#         # Save all descriptions to a text file
#         with open("descriptions.txt", "w", encoding="utf-8") as f:
#             for name, desc in descriptions:
#                 f.write(f"{name}:\n{markdown.markdown(desc)}\n\n")

#         return render_template("index.html", results=descriptions)

#     return render_template("index.html", results=None)


# # Route: Download results
# @app.route("/download")
# def download():
#     return send_file("descriptions.txt", as_attachment=True)

# # Run the app
# if __name__ == "__main__":
#     app.run(debug=True)








