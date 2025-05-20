import base64
import json
import streamlit as st
import openai

openai.api_key = st.secrets["openai"]["api_key"]

st.set_page_config(page_title="Safety Observation Mockup", page_icon="📸", layout="centered")

st.title("Safety Observation Mockup")
st.write("Upload a workplace photo to generate a mock safety observation.")

# Initialize session state
if "category" not in st.session_state:
    st.session_state["category"] = ""
if "description" not in st.session_state:
    st.session_state["description"] = ""
if "submitted" not in st.session_state:
    st.session_state["submitted"] = False

CATEGORIES = [
    "Housekeeping",
    "PPE Compliance",
    "Equipment Safety",
    "Fire Safety",
    "Ergonomics",
]


def analyze_photo(image_bytes: bytes):
    """Send image bytes to the OpenAI API and return category and description."""
    b64_image = base64.b64encode(image_bytes).decode("utf-8")
    cat_list = ", ".join(CATEGORIES)

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Look at the photo and select the most relevant safety observation "
                            f"category from this list: {cat_list}. "
                            "Write one short observation sentence. "
                            "Respond with JSON containing 'category' and 'description'."
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
        category = data.get("category", "")
        description = data.get("description", "")
    except json.JSONDecodeError:
        category = ""
        description = ""
        for line in content.splitlines():
            if line.lower().startswith("category:"):
                category = line.split(":", 1)[1].strip()
            elif line.lower().startswith("observation:"):
                description = line.split(":", 1)[1].strip()
        if not description:
            description = content
    return category, description


if not st.session_state["submitted"]:
    uploaded = st.file_uploader("Upload safety photo", type=["jpg", "jpeg", "png"])

    st.info("Available categories: " + ", ".join(CATEGORIES))

    if uploaded:
        st.image(uploaded, caption="Uploaded photo", use_column_width=True)
        if st.button("Generate Observation"):
            category, description = analyze_photo(uploaded.read())
            st.session_state["category"] = category
            st.session_state["description"] = description

    if st.session_state["category"] or st.session_state["description"]:
        st.selectbox("Category", options=CATEGORIES, key="category")
        st.text_area("Observation", key="description")
        if st.button("Submit to Safety System"):
            st.session_state["submitted"] = True
else:
    st.success("Thank you for submitting your safety observation!")
