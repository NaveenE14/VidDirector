from moviepy.editor import *
import os

class VideoGenerator:
    def __init__(self):
        self.folder_path = None

    def generate_video(self, image_folder, audio_folder, output_file="video.mp4"):
        # Get list of image files
        image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', '.jpeg'))])
        audio_files = sorted([f for f in os.listdir(audio_folder) if f.endswith('.mp3')])

        # Create list of video clips with transitions
        video_clips = []
        for img in image_files:
            clip = ImageClip(os.path.join(image_folder, img)).set_duration(2)
            video_clips.append(clip.crossfadein(1).crossfadeout(1))

        # Create list of audio clips
        audio_clips = [AudioFileClip(os.path.join(audio_folder, audio)).set_duration(2) for audio in audio_files]

        # Create final video with transitions
        final_clip = concatenate_videoclips(video_clips, method="compose")
        final_clip = final_clip.set_audio(concatenate_audioclips(audio_clips))

        return final_clip