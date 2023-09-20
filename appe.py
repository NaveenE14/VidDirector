import streamlit as st
from gtts import gTTS
import os
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

st.title("VidDirector")
storyname = st.text_input("Create a video about:")
video_tone = st.selectbox("Select video tone:", ["Happy", "Sad", "Inspirational", "Playful", "Mysterious", "Energetic", "Custom"])
if video_tone == "Custom":
    custom_tone = st.text_input("Enter custom video tone:")
    video_tone = custom_tone if custom_tone else video_tone
video_type = st.selectbox("Select video type:", ["Story", "Poem", "Fairy Tale", "Documentary", "Tutorial", "Review", "Custom"])
if video_type == "Custom":
    custom_type = st.text_input("Enter custom video type:")
    video_type = custom_type if custom_type else video_type
video_style = st.selectbox("Select video style:", ["Animation", "Anime", "Natural Art", "Retro", "Digital Art", "Photographic", "Cinematic", "Sci-Fi", "Neon Punk", "Custom"])
if video_style == "Custom":
    custom_style = st.text_input("Enter custom video style:")
    video_style = custom_style if custom_style else video_style
video_aspect = st.selectbox("Select aspect ratio:", ["16:9", "9:16", "1:1", "3:4", "Custom"])
if video_aspect == "Custom":
    custom_aspect = st.text_input("Enter custom aspect ratio:")
    video_aspect = custom_aspect if custom_aspect else video_aspect

# Button to generate script
if st.button("Generate Video"):
    #streamlit success
    st.success("Generating script...")
    st.write("Please note that video creation may take up to 10 minutes.")
    prompt = f"""
    Generate a fully compelling video story script for a YouTube video about "{storyname}".
    You choose the video tone: {video_tone}, style: {video_style}, and the length of the entire video (1 minute). The story must have an ending, and it must be meaningful. For each sentence in the story, provide a related visual image scene description to enhance the storytelling.

    Remember to format the output as follows:

    Image: Insert image description or scene here aspect:{video_aspect}
    Narrator: Write the narration or dialogue for the sentence 

    Image: Insert image description or scene here aspect:{video_aspect}  
    Narrator: Write the narration or dialogue for the sentence 

    Image: Insert image description or scene here aspect:{video_aspect}
    Narrator: Write the narration or dialogue for the sentence 
    And so on until the end of the story.
    Return without commentary. Only the narrator should speak no other characters in the story. Give highly detailed 2 lines image prompts that relate to previous scenes. The prompts should be similar, and the images generated should be similar to each other because I am going to create a video using that."""
    
    from dotenv import load_dotenv
    load_dotenv()
    clarifai_pat = os.getenv('CLARIFAI_PAT')

    PAT = clarifai_pat
    USER_ID = 'openai'
    APP_ID = 'chat-completion'
    MODEL_ID = 'GPT-3_5-turbo'
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', 'Key ' + PAT),)
    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
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

    # Since we have one input, one output will exist here
    output = post_model_outputs_response.outputs[0]
    st.write("Scripts:\n")
    print(output.data.text.raw)
    text=output.data.text.raw
    image_prompts = []
    narrator_prompts = []

    # Split the text into paragraphs
    paragraphs = text.split('\n')

    # Iterate through paragraphs and categorize them as image or narrator prompts
    current_prompt_type = None
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if paragraph.startswith("Image:"):
            current_prompt_type = "Image Prompts"
            paragraph = paragraph[len("Image: "):]  # Remove "Image: " from the beginning
        elif paragraph.startswith("Narrator:"):
            current_prompt_type = "Narrator Prompts"
            paragraph = paragraph[len("Narrator: "):]  # Remove "Narrator: " from the beginning
        
        if current_prompt_type == "Image Prompts":
            image_prompts.append(paragraph)
        elif current_prompt_type == "Narrator Prompts":
            narrator_prompts.append(paragraph)

    # Print the separated prompts
    print("Image Prompts:")
    image_prompts = [prompt for prompt in image_prompts if prompt.strip()]
    for image_prompt in image_prompts:
        print(image_prompt)
    narrator_prompts = [prompt for prompt in narrator_prompts if prompt.strip()]
    for narrator_prompt in narrator_prompts:
        st.write(narrator_prompt)
    st.success("Scripts Generated Sucessfully")
    os.makedirs("audio", exist_ok=True)


    st.success("Generating audio files...")
   

# Iterate through narrator prompts and convert to audio
    for idx, narrator_prompt in enumerate(narrator_prompts):
        # Convert text to audio
        tts = gTTS(text=narrator_prompt, lang='en', slow=False)
        
        # Define the audio filename with a unique index
        audio_filename = f"audio/narrator_audio{idx}.mp3"
        
        # Save the audio file
        tts.save(audio_filename)
        print(f"Saved audio {idx}: {audio_filename}")
        
    st.success("Audio files Generated Sucessfully")

    
