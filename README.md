# Safety Observation Mockup

This project demonstrates a simple Streamlit application that uses the OpenAI API to create workplace safety observations from photos.

Users can upload an image and the app will ask the GPT‑4o model to identify the most relevant safety category and generate a short observation. The suggested values can be edited before submitting the mock observation. After submission a thank you message is displayed.

## Requirements

* Python 3.9+
* [Streamlit](https://streamlit.io)
* [OpenAI Python SDK](https://github.com/openai/openai-python)

Install the dependencies with:

```bash
pip install -r requirements.txt
```

The application expects an OpenAI API key. Create a file named `.streamlit/secrets.toml` and add:

```toml
[openai]
api_key = "YOUR_OPENAI_API_KEY"
```

## Running the app

Launch Streamlit from the repository root:

```bash
streamlit run safety-mockup.py
```

The UI allows you to upload a photo, generate a suggested category and description, adjust the fields, and submit the mock safety observation. The available categories are Housekeeping, PPE Compliance, Equipment Safety, Fire Safety and Ergonomics.

## How it works

1. **Image upload** – The user uploads a JPEG or PNG file.
2. **OpenAI analysis** – The image bytes are encoded in base64 and sent to the GPT‑4o model using the vision API.
3. **Edit fields** – The text response is used to pre‑fill the "Category" and "Observation" fields that the user can modify.
4. **Submit** – Once submitted, the app displays a thank you message. In a real system this is where the data would be sent to your safety backend.

## Customization

* Modify the prompt in `safety-mockup.py` to change how the image is interpreted.
* Replace the submission placeholder with integration to your actual safety system.

This repository only contains a mock implementation. It does not store or transmit any uploaded images or generated text.
