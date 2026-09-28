import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np


# -------------------------------
# Page Title
# -------------------------------

st.title("🦺 PPE Detection using YOLOv8")


# -------------------------------
# Load Trained YOLO Model
# -------------------------------

model = YOLO("best.pt")


# -------------------------------
# Upload Image
# -------------------------------

uploaded_file = st.file_uploader(
    "Upload a construction worker image",
    type=["jpg", "jpeg", "png"]
)


# -------------------------------
# Process Uploaded Image
# -------------------------------

if uploaded_file is not None:

    # Read uploaded image
    image = Image.open(uploaded_file)

    # Display original image
    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    # Convert image to NumPy array
    img_array = np.array(image)

    # YOLO prediction
    results = model(img_array)

    # Draw bounding boxes on image
    result_image = results[0].plot()

    # Display detection result
    st.subheader("PPE Detection Result")
    st.image(result_image, use_container_width=True)

    # Display detected objects
    st.subheader("Detected PPE")

    # Get detected bounding boxes
    boxes = results[0].boxes

    if boxes is not None and len(boxes) > 0:

        for box in boxes:

            # Get class ID
            class_id = int(box.cls[0])

            # Get confidence score
            confidence = float(box.conf[0])

            # Get class name
            class_name = model.names[class_id]

            # Display detection
            st.write(
                f"**{class_name}** → "
                f"Confidence: {confidence:.2%}"
            )

    else:
        st.warning("No PPE detected.")