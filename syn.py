import streamlit as st
import PyPDF2
from gtts import gTTS
from io import BytesIO

def main():
    st.set_page_config(page_title="PragyanAI - VVIET Multimedia Hub", layout="wide")
    st.image("PragyanAI_Transperent.png")
    st.title(" PragyanAI Multi-Functional Media Hub")
    
    # Create Tabs for Video, YouTube, and PDF
    tab1, tab2, tab3 = st.tabs(["📹 Local Video", "📺 YouTube Player", "📄 PDF to Audio"])

    # --- TAB 1: LOCAL VIDEO PLAYER ---
    with tab1:
        st.header("Upload & Play Local Video")
        video_file = st.file_uploader("Upload MP4/MOV", type=["mp4", "mov", "avi"])
        if video_file:
            st.video(video_file)

    # --- TAB 2: YOUTUBE PLAYER ---
    with tab2:
        st.header("Stream YouTube Content")
        yt_url = st.text_input("Paste YouTube URL here", placeholder="https://www.youtube.com/watch?v=...")
        if yt_url:
            try:
                st.video(yt_url)
                st.caption("Now streaming from YouTube")
            except Exception as e:
                st.error("Please enter a valid YouTube URL.")

    # --- TAB 3: PDF READER & AUDIO ---
    with tab3:
        st.header("PDF Page-to-Audio Converter")
        pdf_file = st.file_uploader("Upload your PDF document", type=["pdf"])

        if pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            total_pages = len(pdf_reader.pages)
            
            # Layout for controls
            c1, c2 = st.columns([1, 3])
            with c1:
                page_num = st.number_input("Go to Page", min_value=1, max_value=total_pages, value=1) - 1
            
            # Extract content
            page = pdf_reader.pages[page_num]
            text = page.extract_text()

            # Display and Convert
            col_text, col_audio = st.columns(2)
            
            with col_text:
                st.subheader(f"Text Preview (Page {page_num + 1})")
                if text.strip():
                    st.write(text)
                else:
                    st.warning("No text detected on this page (it might be an image).")

            with col_audio:
                st.subheader("Audio Controls")
                if text.strip():
                    if st.button("🔊 Generate Speech for this Page"):
                        with st.spinner("Converting text to speech..."):
                            tts = gTTS(text=text, lang='en')
                            audio_fp = BytesIO()
                            tts.write_to_fp(audio_fp)
                            st.audio(audio_fp, format="audio/mp3")
                else:
                    st.info("Conversion unavailable for empty or image-only pages.")

if __name__ == "__main__":
    main()
