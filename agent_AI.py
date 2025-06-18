import streamlit as st
import os
from google.protobuf.json_format import MessageToDict

# Ensure HOME environment variable on Windows
if "HOME" not in os.environ:
    os.environ["HOME"] = os.environ.get("USERPROFILE", "")

from clarifai.client.workflow import Workflow

# Workflow parameters
workflow_url = "https://clarifai.com/n1fc3ew432kq/coding-template-7434ef19007c/workflows/workflow-67c794"
PAT = "e55bf27864ed49c391fb1e4361ba15d4"

# Create workflow instance
image_to_text_workflow = Workflow(url=workflow_url, pat=PAT)

# Streamlit UI
st.set_page_config(page_title="Clarifai Agent - Image to Text", layout="centered")
st.title("🖼️➡️📝 Image-to-Text Generator with Clarifai")

# Image source selection
option = st.radio("", [ "Upload file"])

image_file = None

if option == "Upload file":
    image_file = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])
    
if st.button("Generate Description"):
    with st.spinner("Analyzing image and generating text..."):
        try:
            # Process input image
            if image_file:
                image_bytes = image_file.read()
                result = image_to_text_workflow.predict_by_bytes(
                    image_bytes, input_type="image"
                )
                st.image(image_bytes, caption="Analyzed Image", use_container_width=True)

            else:
                st.warning("Please provide an image to analyze.")
                st.stop()

            # Extract response
            output = result.results[0].outputs[0]
            data = output.data
            text_output = getattr(data, "text", None)

            if text_output and hasattr(text_output, "raw"):
                st.subheader("📝 Generated Description:")
                st.success(text_output.raw)
            else:
                st.warning("⚠️ No text was generated from the image.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
