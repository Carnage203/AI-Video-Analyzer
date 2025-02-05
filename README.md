# AI-Video-Analyzer

This project is a Streamlit-based application that leverages the Google Generative AI API to analyze video content and generate textual responses based on user queries. The app allows users to optionally upload a video file, enter a query for video analysis, and view the resulting response. It also includes functionality in the sidebar to manage (list and delete) uploaded files.

## Features

- **Interactive Video Analysis:**  
  Upload a video file and provide a query to analyze the video content.  
- **Prompt-Only Mode:**  
  If no video is uploaded, the app can generate a response based solely on the query.
- **Efficient File Management:**  
  - Uses Streamlit’s session state to avoid re-uploading the same video.
  - Provides a sidebar interface for listing and deleting previously uploaded files.
- **User-Friendly Interface:**  
  Displays spinners during long operations (video uploading, processing, and analysis) to keep users informed.
- **Error Handling:**  
  Provides friendly messages for common issues such as missing query input or no uploaded files.

## Demo

### Prerequisites

Before you begin, ensure you have met the following requirements:
- **Python 3.7+**  
- **Google Generative AI API Key:**  
  You need a valid API key for Google Generative AI. Store your API key in a Python file named `constants.py` in the same directory, with a variable named `GOOGLE_API_KEY`.

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Carnage203/AI-Video-Analyzer.git
   ```

2. **Set Up Your API Key:**
   Create a file called `constants.py` in the root directory of the project and add:
   ```python
   GOOGLE_API_KEY = "your-google-generativeai-api-key"
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Alternatively, manually install the necessary packages as mentioned above.)*

### Running the Application

Start the Streamlit app by running:
```bash
streamlit run app.py
```

The app should open in your default web browser. Use the main interface to enter a query and optionally upload a video file for analysis. The sidebar allows you to manage (list and delete) previously uploaded files.


## How It Works

1. **User Query & Optional Video Upload:**
   - Users enter a textual query describing what they want to analyze in the video.
   - Optionally, users can upload a video file. If a new video is uploaded, it is saved temporarily and sent to the Google Generative AI API.
   - If no new video is provided, the application generates a response based solely on the prompt.

2. **Video Upload and Processing:**
   - The app checks if the same video has been uploaded before using Streamlit’s session state.
   - If it is a new upload, the video is processed, and its state is checked until it is ready for analysis.

3. **Generating the Analysis:**
   - Once the video is processed (or if no video was uploaded), the prompt along with the video (if available) is sent to the Gemini model.
   - The response is rendered on the main page in Markdown format.

4. **Managing Uploaded Files:**
   - The sidebar lists all uploaded files using the `google.generativeai` API.
   - Users can select a file and delete it directly from the sidebar.

