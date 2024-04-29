from moviepy.editor import *
import os
import numpy as np

class VideoGenerator:
    def __init__(self):
        self.folder_path = None

    def zoom_in_out(self, t):
        return 1.3 + 0.3 * np.sin(t / 3)

    def generate_video(self, image_folder, audio_folder, output_file="video.mp4"):
        
        if not os.path.exists(image_folder):
            print(f"Image folder {image_folder} does not exist.")
            return

        
        if not os.path.exists(audio_folder):
            print(f"Audio folder {audio_folder} does not exist.")
            return

        
        image_files = sorted([
            os.path.join(image_folder, img)
            for img in os.listdir(image_folder)
            if img.endswith(".png") or img.endswith(".jpg")
        ])

        
        if len(image_files) != len(os.listdir(audio_folder)):
            print("Number of image files does not match number of audio files.")
            return

        clips = []
        for image_file, audio_file in zip(image_files, os.listdir(audio_folder)):
            image_clip = ImageClip(image_file)
            audio_clip = AudioFileClip(os.path.join(audio_folder, audio_file))
            image_duration = audio_clip.duration
            
           
            image_clip = image_clip.set_duration(image_duration)
            
            
            combined_clip = CompositeVideoClip([image_clip.set_audio(audio_clip)])
            clips.append(combined_clip)

        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(output_file, fps=24, audio_codec="aac", codec="libx264")

        return output_file