import streamlit as st
import os
import shutil
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

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


if st.button("Generate Video"):
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
    

    PAT = clarifai_pat
    USER_ID = 'openai'
    APP_ID = 'chat-completion'
    MODEL_ID = 'gpt-4-turbo'
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', 'Key ' + PAT),)
    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject, 
            model_id=MODEL_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=prompt
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception(f"Post model outputs failed, status: {post_model_outputs_response.status.description}")


    output = post_model_outputs_response.outputs[0]
    st.write("Scripts:\n")
    print(output.data.text.raw)
    text = output.data.text.raw
    image_prompts = []
    narrator_prompts = []
    paragraphs = text.split('\n')

    current_prompt_type = None
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if paragraph.startswith("Image:"):
            current_prompt_type = "Image Prompts"
            paragraph = paragraph[len("Image: "):]
            image_prompts.append(paragraph)
        elif paragraph.startswith("Narrator:"):
            current_prompt_type = "Narrator Prompts"
            paragraph = paragraph[len("Narrator: "):]
            narrator_prompts.append(paragraph)

    print("Image Prompts:")
    for image_prompt in image_prompts:
        print(image_prompt)

    print("\nNarrator Prompts:")
    for narrator_prompt in narrator_prompts:
        print(narrator_prompt)

    print("Image Prompts:")
    image_prompts = [prompt for prompt in image_prompts if prompt.strip()]
    for image_prompt in image_prompts:
        print(image_prompt)
    narrator_prompts = [prompt for prompt in narrator_prompts if prompt.strip()]
    for narrator_prompt in narrator_prompts:
        st.write(narrator_prompt)
    st.success("Scripts Generated Sucessfully")
    os.makedirs("audio", exist_ok=True)

    
    st.success("Generating audio files using Eleven Labs speech synthesis model")
   
    USER_ID = 'eleven-labs'
    APP_ID = 'audio-generation'
    MODEL_ID = 'speech-synthesis'
    folder_path = "audio"
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        os.makedirs(folder_path)
    else:
        os.makedirs(folder_path)
    for idx, narrator_prompt in enumerate(narrator_prompts):
        userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)
        post_model_outputs_response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,
                model_id=MODEL_ID,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                raw=narrator_prompt
                            )
                        )
                    )
                ]
            ),
            metadata=metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)
        output = post_model_outputs_response.outputs[0]
        print(f"{idx+1}Audio Generated")
        for concept in output.data.concepts:
            print("%s %.2f" % (concept.name, concept.value))
        my_bar = st.progress((idx + 1) / len(narrator_prompts))
        base64_audio = output.data.audio.base64
        audio_filename = f"audio/audio_{idx}.mp3"  
        with open(audio_filename, 'wb') as f:
            f.write(base64_audio)

    st.success("Audio files Generated Sucessfully")
    st.success("Generating images using "+ image_model)
    if image_model== "DALLE3":
        USER_ID = 'openai'
        APP_ID = 'dall-e'
        MODEL_ID = 'dall-e-3'
    elif image_model == "IMAGEN":
        USER_ID = 'gcp'
        APP_ID = 'generate'
        MODEL_ID = 'Imagen'
    elif image_model == "STABLEDIFFUSION XL":
        USER_ID = 'stability-ai'
        APP_ID = 'stable-diffusion-2'
        MODEL_ID = 'stable-diffusion-xl'

    folder_path = "image"
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        os.makedirs(folder_path)
    else:
        os.makedirs(folder_path)
    for idx, image_prompt in enumerate(image_prompts):
        userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)
        post_model_outputs_response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,
                model_id=MODEL_ID,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                raw=image_prompt
                            )
                        )
                    )
                ]
            ),
            metadata=metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)
        output = post_model_outputs_response.outputs[0]
        print(f"{idx+1}image generated")
        my_bar = st.progress((idx + 1) / len(image_prompts))
        for concept in output.data.concepts:
            print("%s %.2f" % (concept.name, concept.value))

        base64_image = output.data.image.base64
        image_filename = f"image/image_{idx}.jpg"   
        with open(image_filename, 'wb') as f:
            f.write(base64_image)
    
    st.success("Images Generated Sucessfully")

    st.success("Generating video using moviepy")

    import cv2
    import os
    import numpy as np
    from pydub import AudioSegment
    import streamlit as st

    def draw_text_with_background(img, text, font, font_scale, font_thickness, font_color, bg_color, position):
        # Draw text with background
        img_with_text = img.copy()
        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)

        # Create a black background behind the text
        bg_position = position
        img_with_text = cv2.rectangle(img_with_text, bg_position, 
                                    (bg_position[0] + text_width, bg_position[1] + text_height), bg_color, thickness=cv2.FILLED)

        # Draw text on the black background
        text_position = (position[0], position[1] + text_height - baseline)
        cv2.putText(img_with_text, text, text_position, font, font_scale, font_color, font_thickness, cv2.LINE_AA)

        return img_with_text

    def split_subtitle(subtitle, max_chars_per_row):
        # Split subtitle into two lines with an appropriate number of words
        words = subtitle.split()
        wrapped_text = []
        current_line = []
        current_line_length = 0
        max_line_length = max_chars_per_row
        for word in words:
            if current_line_length + len(word) + 1 <= max_line_length:
                current_line.append(word)
                current_line_length += len(word) + 1
            else:
                wrapped_text.append(" ".join(current_line))
                current_line = [word]
                current_line_length = len(word) + 1
        if current_line:
            wrapped_text.append(" ".join(current_line))
        return wrapped_text

    output_video_filename = "output_video.mp4"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    font_color = (255, 255, 255)
    bg_color = (0, 0, 0)
    audio_folder = r"audio"
    image_folder = r"image"
    max_chars_per_row = 40  # Adjust the maximum characters per row as needed

    image_filenames = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder) if filename.endswith(".jpg")]
    audio_filenames = [os.path.join(audio_folder, filename) for filename in os.listdir(audio_folder) if filename.endswith(".mp3")]

    image_filenames.sort()
    audio_filenames.sort()

    audio_clips = [AudioSegment.from_file(audio_filename) for audio_filename in audio_filenames]
    subtitle_durations = [len(audio_clip) for audio_clip in audio_clips]
    subtitle_start_times = [sum(subtitle_durations[:i]) for i in range(len(subtitle_durations))]
    subtitle_end_times = [start_time + duration for start_time, duration in zip(subtitle_start_times, subtitle_durations)]
    frame_width, frame_height = cv2.imread(image_filenames[0]).shape[1], cv2.imread(image_filenames[0]).shape[0]
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_video_filename, fourcc, 30, (frame_width, frame_height))

    for idx, (image_filename, audio_clip) in enumerate(zip(image_filenames, audio_clips)):
        img = cv2.imread(image_filename)
        start_time, end_time = subtitle_start_times[idx] / 1000, subtitle_end_times[idx] / 1000
        subtitle = narrator_prompts[idx]
        subtitle_lines = split_subtitle(subtitle, max_chars_per_row)

        # Process each line of subtitle
        for line_idx, subtitle_line in enumerate(subtitle_lines):
            # Calculate position for center alignment
            text_position = ((frame_width - cv2.getTextSize(subtitle_line, font, font_scale, font_thickness)[0][0]) // 2, frame_height - 50)

            # Add subtitle text with background to the image
            img_with_text = draw_text_with_background(img, subtitle_line, font, font_scale, font_thickness, font_color, bg_color, text_position)
            img_with_text = cv2.cvtColor(img_with_text, cv2.COLOR_BGR2RGB)

            # Write to video
            for i in range(int(audio_clip.duration_seconds * 30)):
                out.write(cv2.cvtColor(img_with_text, cv2.COLOR_BGR2RGB))

    # Release the video writer
    out.release()

    # Save the final video with audio
    final_audio = sum(audio_clips)  # Combine all audio clips
    final_audio.export("temp_audio.wav", format="wav")
    os.system(f"ffmpeg -y -i output_video.mp4 -i temp_audio.wav -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 final_output_video.mp4")
    st.success("Video Generated Successfully")
    st.balloons()
    st.video("final_output_video.mp4")





    

    

            
