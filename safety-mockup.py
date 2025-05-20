import base64
import json
import streamlit as st
import openai

openai.api_key = st.secrets["openai"]["api_key"]

st.title("Safety Observation Mockup")

# Initialize session state
if "category" not in st.session_state:
    st.session_state["category"] = ""
if "description" not in st.session_state:
    st.session_state["description"] = ""
if "submitted" not in st.session_state:
    st.session_state["submitted"] = False


def analyze_photo(image_bytes: bytes):
    """Send image bytes to the OpenAI API and return category and description."""
    b64_image = base64.b64encode(image_bytes).decode("utf-8")
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Identify any workplace safety observation shown in the photo."
                            " Respond with JSON containing 'category' and 'description'."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"},
                    },
                ],
            }
        ],
    )
    content = response.choices[0].message.content
    try:
        data = json.loads(content)
        return data.get("category", ""), data.get("description", "")
    except json.JSONDecodeError:
        # Fallback if the model does not return valid JSON
        return "", content


if not st.session_state["submitted"]:
    uploaded = st.file_uploader("Upload safety photo", type=["jpg", "jpeg", "png"])
    if uploaded and st.button("Generate Observation"):
        category, description = analyze_photo(uploaded.read())
        st.session_state["category"] = category
        st.session_state["description"] = description

    if st.session_state["category"] or st.session_state["description"]:
        st.text_input("Category", key="category")
        st.text_area("Observation", key="description")
        if st.button("Submit to Safety System"):
            st.session_state["submitted"] = True
else:
    st.success("Thank you for submitting your safety observation!")
