import os
import time
import streamlit as st
import google.generativeai as genai
from constants import GOOGLE_API_KEY

# key
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Streamlit page
st.set_page_config(page_title="🤖 AI Video Analyzer", layout="wide")

# ---------------------------
# Session State Initialization
# ---------------------------
if "uploaded_video_obj" not in st.session_state:
    st.session_state.uploaded_video_obj = None
if "video_name" not in st.session_state:
    st.session_state.video_name = None

# -------------------------------
# Sidebar: Manage Uploaded Files
# -------------------------------
st.sidebar.header("Manage Uploaded Files")
try:
    
    uploaded_files = genai.list_files() or []
except Exception as e:
    st.sidebar.error("Could not fetch uploaded files.")
    uploaded_files = []

if uploaded_files:
    file_names = [f.name for f in uploaded_files]
    selected_file = st.sidebar.selectbox("Select a file to delete", file_names)
    if st.sidebar.button("Delete Selected File"):
        try:
            file_to_delete = genai.get_file(selected_file)
            file_to_delete.delete()
            st.sidebar.success(f"Deleted file: {selected_file}")
        except Exception as e:
            st.sidebar.error(f"No Uploaded files.")
else:
    st.sidebar.info("No uploaded files available.")

# -------------------------------
# Main Area: Query & Analysis
# -------------------------------
st.markdown("<h1 style='text-align: center;'>🤖 AI Video Analyzer</h1>", unsafe_allow_html=True)

# Get the user query first.
query = st.text_input(
    "Enter your query for video analysis",
    placeholder="Describe the content of the video"
)

# Get an optional video file upload.
video_file = st.file_uploader("Upload a video file (optional)", type=["mp4", "mov", "avi"])

# Build the prompt (system instructions) using the query.
prompt = f"""**System Instructions:**
You are a smart Vision assistant who will take video as input and generate a textual response based on the query.
- Analyze the video and provide comprehensive, detailed responses.
- If the query mentions 'transcribe' or 'timestamps', then return timestamps in hh:mm format.
  
**User Query:** {query}"""

# Process the request when the button is pressed.
if st.button("Generate Analysis"):
    if not query.strip():
        st.error("Please enter a query before proceeding.")
    else:
        # CASE 1: A new video file has been uploaded.
        if video_file is not None:
            # Check if this file is the same as the one previously processed.
            if st.session_state.video_name == video_file.name and st.session_state.uploaded_video_obj:
                st.info("Using previously uploaded video.")
                video_file_obj = st.session_state.uploaded_video_obj
            else:
                # Save the uploaded video file temporarily.
                temp_dir = "temp_videos"
                os.makedirs(temp_dir, exist_ok=True)
                temp_video_path = os.path.join(temp_dir, video_file.name)
                with open(temp_video_path, "wb") as f:
                    f.write(video_file.getbuffer())
                
                # Upload the video file to the GenAI platform.
                with st.spinner("Uploading video..."):
                    try:
                        video_file_obj = genai.upload_file(path=temp_video_path)
                    except Exception as e:
                        st.error(f"Error uploading video: {e}")
                        st.stop()
                st.success(f"Video uploaded successfully! File URI: {video_file_obj.uri}")
                
                # Cache the video in session state.
                st.session_state.uploaded_video_obj = video_file_obj
                st.session_state.video_name = video_file.name

                # Poll until the video processing completes.
                with st.spinner("Processing video..."):
                    while video_file_obj.state.name == "PROCESSING":
                        time.sleep(10)
                        video_file_obj = genai.get_file(video_file_obj.name)
                    if video_file_obj.state.name == "FAILED":
                        st.error("Video processing failed.")
                        st.stop()
                    else:
                        st.success("Video processed successfully!")
            
            # Use the (newly uploaded or cached) video and prompt for analysis.
            with st.spinner("Analyzing video..."):
                try:
                    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                    response = model.generate_content([video_file_obj, prompt],
                                                      request_options={"timeout": 600})
                except Exception as e:
                    st.error(f"Error during analysis: {e}")
                    st.stop()
            st.markdown(response.text)
        
        # CASE 2: No new video file is uploaded.
        else:
            # Do not re-upload any cached video; just generate the result from the prompt.
            st.info("No new video uploaded. Generating response solely based on the prompt.")
            with st.spinner("Generating response..."):
                try:
                    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                    response = model.generate_content([prompt],
                                                      request_options={"timeout": 600})
                except Exception as e:
                    st.error(f"Error during generation: {e}")
                    st.stop()
            st.markdown(response.text)
