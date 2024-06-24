import sys
import subprocess
import pkg_resources

required_packages = ['streamlit', 'groq']

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check and install required packages
for package in required_packages:
    try:
        pkg_resources.require(package)
    except pkg_resources.DistributionNotFound:
        print(f"{package} not found. Installing...")
        install(package)
        print(f"{package} has been installed.")

import streamlit as st
import os
from groq import Groq
import tempfile

# Set the API key directly in the script
os.environ['GROQ_API_KEY'] = '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'  # Replace with your actual API key

client = Groq(api_key=os.environ['GROQ_API_KEY'])

def transcribe_audio(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as temp_file:
        temp_file.write(file.getvalue())
        temp_file_path = temp_file.name

    try:
        with open(temp_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(temp_file_path), audio_file.read()),
                model="whisper-large-v3",
                response_format="json",
                temperature=0,
            )
        return transcription.text
    finally:
        os.unlink(temp_file_path)

st.title("Audio Transcription App")

uploaded_file = st.file_uploader("Choose an audio file", type=['m4a', 'mp3', 'wav'])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/m4a')
    
    if st.button("Transcribe"):
        with st.spinner("Transcribing..."):
            transcription = transcribe_audio(uploaded_file)
        st.success("Transcription complete!")
        st.text_area("Transcription", transcription, height=300)

if __name__ == "__main__":
    print("All required packages are installed. You can now run the Streamlit app.")
    print("To start the app, run: streamlit run <script_name>.py")
