import streamlit as st
from ultralytics import YOLO
from PIL import Image

st.title("AI Visual Analytics Platform")

st.write("Upload an image to detect objects")

model = YOLO("yolov8n.pt")

file = st.file_uploader(
    "Choose an image",
    type=["jpg", "png", "jpeg"]
)

if file:
    image = Image.open(file)

    st.image(image, caption="Uploaded Image")

    results = model(image)

    output = results[0].plot()

    st.image(output, caption="Detection Result")

    st.write("Detected Objects")

    for box in results[0].boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        name = model.names[class_id]

        st.write(name, round(confidence, 2))