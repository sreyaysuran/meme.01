import streamlit as st
import PyPDF2
from gtts import gTTS
from io import BytesIO

# Must be the first Streamlit command
st.set_page_config(
    page_title="PragyanAI - VVIET Multimedia Hub",
    layout="wide"
)


def main():
    # Logo (Optional)
    try:
        st.image("PragyanAI_Transperent.png")
    except:
        pass

    st.title("🎓 PragyanAI Multi-Functional Media Hub")

    # Create Tabs
    tab1, tab2, tab3 = st.tabs(
        ["📹 Local Video", "📺 YouTube Player", "📄 PDF to Audio"]
    )

    # -------------------------------
    # TAB 1 : LOCAL VIDEO PLAYER
    # -------------------------------
    with tab1:
        st.header("Upload & Play Local Video")

        video_file = st.file_uploader(
            "Upload MP4/MOV/AVI",
            type=["mp4", "mov", "avi"],
            key="video"
        )

        if video_file is not None:
            st.video(video_file)

    # -------------------------------
    # TAB 2 : YOUTUBE PLAYER
    # -------------------------------
    with tab2:
        st.header("Stream YouTube Content")

        yt_url = st.text_input(
            "Paste YouTube URL",
            placeholder="https://www.youtube.com/watch?v=..."
        )

        if yt_url:
            st.video(yt_url)
            st.success("Streaming YouTube Video")

    # -------------------------------
    # TAB 3 : PDF TO AUDIO
    # -------------------------------
    with tab3:
        st.header("PDF Page-to-Audio Converter")

        pdf_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"],
            key="pdf"
        )

        if pdf_file is not None:

            try:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
            except Exception as e:
                st.error(f"Error reading PDF:\n{e}")
                return

            total_pages = len(pdf_reader.pages)

            st.info(f"Total Pages : {total_pages}")

            page_num = st.number_input(
                "Select Page",
                min_value=1,
                max_value=total_pages,
                value=1,
                step=1
            )

            page = pdf_reader.pages[page_num - 1]

            # Prevent NoneType error
            text = page.extract_text()

            if text is None:
                text = ""

            col1, col2 = st.columns(2)

            with col1:
                st.subheader(f"Text Preview (Page {page_num})")

                if text.strip():
                    st.write(text)
                else:
                    st.warning("No readable text found on this page.")

            with col2:
                st.subheader("Audio")

                if text.strip():

                    if st.button("🔊 Generate Speech"):

                        with st.spinner("Generating Audio..."):

                            try:
                                tts = gTTS(text=text, lang="en")

                                audio_fp = BytesIO()

                                tts.write_to_fp(audio_fp)

                                audio_fp.seek(0)

                                st.audio(audio_fp, format="audio/mp3")

                                st.success("Audio Generated Successfully!")

                            except Exception as e:
                                st.error(f"TTS Error:\n{e}")

                else:
                    st.info("Cannot generate speech because no text was found.")


if __name__ == "__main__":
    main()
