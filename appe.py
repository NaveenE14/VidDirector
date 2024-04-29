import streamlit as st
import os
import shutil
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from functions.api import gpt
import functions.api.elevenlabs as elevenlabs
import functions.api.dalle as dalle
from streamlit_card import card
import streamlit.components.v1 as components
from functions.generate import makeprompt, makevideo
from pytube import YouTube


st.sidebar.image('./icon.png', width=250) 
st.sidebar.title("VidDirector")
clarifai_pat = st.sidebar.text_input("**Enter your Clarifai Personal Access Token**")


st.sidebar.subheader("Don't Have one ?")
url ="https://clarifai.com/signup?utm_campaign=AI5&utm_source=LNK&utm_medium=REF"
st.sidebar.link_button("Get your Personal Access Token Here" ,url)

st.sidebar.subheader("Steps to Get Clarifai Personal Access Token:")
st.sidebar.markdown("1. Sign up on Clarifai.It's free")
st.sidebar.markdown("2. Click on your profile.")
st.sidebar.markdown("3. Under your profile, click on 'Security.'")
st.sidebar.markdown("4. Create your Personal Access Token.")

st.sidebar.subheader("Ready to Go!")
st.sidebar.markdown("You've successfully obtained your Clarifai Personal Access Token.")
st.sidebar.markdown("Copy and paste it into the 'Enter your Clarifai Personal Access Token' field above")
st.title("VidDirector: Prompt to Video 🎥🌟")
st.subheader("Create stunning videos effortlessly with VidDirector, the ultimate AI-powered video creation platform! 🚀")

st.markdown(
    """
    Step into the world of limitless creativity with VidDirector, your all-in-one AI video generation platform. 
    Harness the power of artificial intelligence to craft mesmerizing videos with just a single prompt. 
    From script generation to image selection and text-to-speech narration, VidDirector has it all. ✨
    """
)

st.subheader("Features 🎉")
st.markdown(
    """
    - AI-generated scripts and images 🤖📝🖼️
    - Natural voiceovers 🗣️🎙️
    - One-click video creation 🚀🎬
    
    **Create Stories of Any Genre**
    Craft stories of any genre, from drama to comedy, fantasy to documentary. 
    VidDirector adapts to your creative vision, allowing you to explore limitless storytelling possibilities. 📚🎭
    """
)


st.markdown(
    """
    **About VidDirector**

    VidDirector is powered by DALLE3 for stunning image selection and Eleven Labs speech synthesis model for natural voiceovers. 
    GPT-4 is used for generating scripts and content. 🚀
    """
)

st.subheader("Get Started 🚀🎬")
st.markdown(
    """
    **To create a custom video with VidDirector, follow these steps:**
    
    1. Enter the name of your story in the text input field. 📝
    2. Select a video tone from the options provided: "Happy," "Sad," "Inspirational," "Playful," "Mysterious," "Energetic," or "Custom." 
    3. If you choose "Custom" for the video tone, enter your custom tone in the text input field. 🎨
    4. Select a video type from the options provided: "Story," "Poem," "Fairy Tale," "Documentary," "Tutorial," "Review," or "Custom." 📜
    5. If you choose "Custom" for the video type, enter your custom type in the text input field. 🎞️
    6. Select a video style from the options provided: "Animation," "Anime," "Natural Art," "Retro," "Digital Art," "Photographic," "Cinematic," "Sci-Fi," "Neon Punk," or "Custom." 🎨🎬
    7. If you choose "Custom" for the video style, enter your custom style in the text input field. 🌟
    """
)
st.image('./loading.png',width=700)


storyname = st.text_input("**Create a video about:**")
video_tone = st.selectbox("Select video tone:", ["Happy", "Sad", "Inspirational", "Playful", "Mysterious", "Energetic", "Custom"])
if video_tone == "Custom":
    custom_tone = st.text_input("**Enter custom video tone:**")
    video_tone = custom_tone if custom_tone else video_tone
video_type = st.selectbox("Select video type:", ["Story", "Poem", "Fairy Tale", "Documentary", "Tutorial", "Review", "Custom"])
if video_type == "Custom":
    custom_type = st.text_input("Enter custom video type:")
    video_type = custom_type if custom_type else video_type
image_model = st.selectbox("Choose a Image Generation Model:",["DALLE3","STABLEDIFFUSION XL","IMAGEN"])  

video_style = st.selectbox("Select video style:", ["Animation", "Anime", "Natural Art", "Retro", "Digital Art", "Photographic", "Cinematic", "Sci-Fi", "Neon Punk", "Custom"])
if video_style == "Custom":
    custom_style = st.text_input("Enter custom video style:")
    video_style = custom_style if custom_style else video_style

video_aspect = st.selectbox("Select aspect ratio:(In development)", ["1:1","16:9", "9:16", "3:4", "Custom"])
if video_aspect == "Custom":
    custom_aspect = st.text_input("Enter custom aspect ratio:")
    video_aspect = custom_aspect if custom_aspect else video_aspect

def download_audio_from_youtube(video_url, output_path):
    try:
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(output_path=output_path, filename="downloadedaudio.mp3")
        return True
    except Exception as e:
        st.error(f"Error occurred while downloading audio: {str(e)}")
        return False

youtube_link = st.text_input("Enter YouTube video link for background music:", key="youtube_link")

# Generate audio file based on the provided YouTube link
if st.button("Download Audio"):
    output_path = "Downloadedaudio"
    if download_audio_from_youtube(youtube_link, output_path):
        st.success(f"Audio file '{output_path}' downloaded successfully.")
        # Play the downloaded audio
        audio_file_path = os.path.join(output_path, "downloadedaudio.mp3")
        st.audio(audio_file_path)

if st.button("Generate Video"):
    if not clarifai_pat:
        st.error("Please enter your Clarifai Personal Access Token.")
        st.stop() 
    st.success("Generating script...")
    st.write("Please note that video creation may take up to 10 minutes.")
    prompt = f"""
    Generate a fully compelling video script for a YouTube video about "{storyname}".
    You choose the video tone: {video_tone}, style: {video_style}, and the length of the entire video (1 minute). The story must have an ending, and it must be meaningful. For each sentence in the story, provide a related visual image scene description to enhance the storytelling.

    Reply me in the below format:

    1st line has image description or scene starting with Image: {video_style}
    2nd line is empty
    3rd line has the narration or dialogue starting with Narrator:
    4th line is empty

    for example:
    Image: image description here {video_style}
    Narrator: Scripts for narrator

    Image: image description here {video_style}
    Narrator: Scripts for narrator

    And so on until the end of the story.

    Return without commentary. Only the narrator should speak and no other characters in the story. Give highly detailed 3 lines image prompts that are related to previous scenes and in touch with the story which will be fed into dalle ai image model . The prompts should be similar, and the images generated should be similar to each other because I am going to create a video using that.
    """
    

    try:
        output_text = gpt.call_gpt_api(prompt, clarifai_pat)
    except Exception as e:
        st.error(f"Error occurred during API call: {str(e)}")
        st.stop()

    
    image_prompts, narrator_prompts = makeprompt.generate_prompts(output_text)

   
    st.write("Image Prompts:")
    for image_prompt in image_prompts:
        st.write(image_prompt)

    st.write("\nNarrator Prompts:")
    for narrator_prompt in narrator_prompts:
        st.write(narrator_prompt)

    st.success("Scripts Generated Successfully")
    os.makedirs("audio", exist_ok=True)

    
    st.success("Generating audio files using Eleven Labs speech synthesis model")
   
    try:
        elevenlabs.generate_audio_files(narrator_prompts, clarifai_pat)
    except Exception as e:
        st.error(f"Error occurred during audio generation: {str(e)}")
        st.stop()

    
    audio_folder = "audio"
    audio_files = os.listdir(audio_folder)
    for audio_file in audio_files:
        st.audio(os.path.join(audio_folder, audio_file))

    st.success("Generating images using " + image_model)

    try:
        dalle.generate_images(image_model, image_prompts, clarifai_pat)
    except Exception as e:
        st.error(f"Error occurred during image generation: {str(e)}")
        st.stop()
    
    st.success("Images Generated Successfully")

    image_folder = "image"
    audio_folder = "audio"

    image_files = os.listdir(image_folder)
    audio_files = os.listdir(audio_folder)

    num_images = len(image_files)
    num_audios = len(audio_files)

    num_cols = 2
    st.header("Images and Audios")
    if num_images > 0 and num_audios > 0:
        col1, col2 = st.columns(num_cols)

        for i, (audio_file, image_file) in enumerate(zip(audio_files, image_files)):
            audio_path = os.path.join(audio_folder, audio_file)
            image_path = os.path.join(image_folder, image_file)
            
            
            download_button_key = f"download_button_{i}"
            
            with col1 if i < num_audios // num_cols else col2:
                st.audio(audio_path, format='audio/mp3')
                st.image(image_path, width=325)
                
                
                st.download_button(
                    label="Download Image",
                    data=open(image_path, "rb").read(),
                    file_name=image_file,
                    mime="image/jpeg",
                    key=download_button_key
                )
                
    st.balloons()
    video_generator = makevideo.VideoGenerator()  
    image_folder = "image" 
    audio_folder = "audio"  
    output_file = "output_video.mp4"  
    video_file = video_generator.generate_video(image_folder, audio_folder, output_file)
    st.success("Video Generated Successfully")
    st.video(video_file)

    

    

            
