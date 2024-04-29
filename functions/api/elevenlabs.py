import os
import shutil
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

def generate_audio_files(narrator_prompts, clarifai_pat):
    USER_ID = 'openai'
    APP_ID = 'tts'
    MODEL_ID = 'openai-tts-1'
    folder_path = "audio"

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        os.makedirs(folder_path)
    else:
        os.makedirs(folder_path)

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', 'Key ' + clarifai_pat),)

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
        print(f"{idx+1} Audio Generated")
        
        base64_audio = output.data.audio.base64
        audio_filename = f"audio/audio_{idx}.mp3"  
        with open(audio_filename, 'wb') as f:
            f.write(base64_audio)

    print("Audio files generated successfully")
