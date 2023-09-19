import streamlit as st
import os
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

st.title("VidDirector")
storyname = st.text_input("Create a video about:")

video_tone = st.selectbox("Select video tone:", ["Happy", "Sad", "Inspirational", "Playful", "Mysterious", "Energetic"])
video_type = st.selectbox("Select video type:", ["Story", "Poem", "Fairy Tale", "Documentary", "Tutorial", "Review"])
video_genre = st.selectbox("Select video genre:", ["Anime", "Animation", "Adventure", "Comedy", "Drama", "Fantasy", "Sci-Fi"])

# Button to generate script
if st.button("Generate Script"):
    st.write("Please note that video creation may take up to 10 minutes.")
    prompt = f"""
    Generate a fully compelling video story script for a YouTube video about "{storyname}".
    You choose the video tone: {video_tone}, genre: {video_genre}, and the length of the entire video (1 minute). The story must have an ending, and it must be meaningful. For each sentence in the story, provide a related visual image scene description to enhance the storytelling.

    Remember to format the output as follows:

    [Image: Insert image description or scene here]
    Narrator: Write the narration or dialogue for the sentence

    [Image: Insert image description or scene here]
    Narrator: Write the narration or dialogue for the sentence

    [Image: Insert image description or scene here]
    Narrator: Write the narration or dialogue for the sentence

    And so on until the end of the story.

    Return without commentary. Only the narrator is telling a story or poem. Give highly detailed image prompts that relate to previous scenes. The prompts should be similar, and the images generated should be similar to each other because I am going to create a video using that.
    """
        
    PAT = CLARIFAI_PAT
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
    st.write(output.data.text.raw)
    print("Completion:\n")
    print(output.data.text.raw)
    paragraphs = output.data.text.raw.split('\n\n')

# Separate narrator prompts and image prompts
    narrator_prompts = []
    image_prompts = []

    for paragraph in paragraphs:
        if paragraph.strip().startswith("[Image:"):
            # Image prompt, store in image_prompts
            image_prompts.append(paragraph)
        elif paragraph.strip().startswith("Narrator:"):
            # Narrator prompt, store in narrator_prompts
            narrator_prompts.append(paragraph)

    # Create folders if they don't exist
    os.makedirs("audio", exist_ok=True)
    os.makedirs("images", exist_ok=True)

    # Save narrator prompts as audio files
    for idx, para in enumerate(narrator_prompts):
        tts = gTTS(text=para.split("Narrator: ")[1], lang='en', slow=False)
        audio_filename = f"audio/voiceover{idx}.mp3"
        tts.save(audio_filename)

    # Save image prompts as text files in the "images" folder
    for idx, iter in enumerate(image_prompts):
        image_prompt = iter.split("]")[1].strip()
        image_filename = f"images/image_prompt{idx}.txt"
        with open(image_filename, 'w') as file:
            file.write(image_prompt)

    # Optionally, you can send image prompts to a model for image generation here

    # Print confirmation
    print(f"Saved {len(narrator_prompts)} audio files and {len(image_prompts)} image prompts.")
