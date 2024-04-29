from moviepy.editor import *
import os

class VideoGenerator:
    def __init__(self):
        self.folder_path = None

    def generate_video(self, image_folder, audio_folder, output_file="video.mp4"):
        # Check if image folder exists
        if not os.path.exists(image_folder):
            print(f"Image folder {image_folder} does not exist.")
            return

        # Check if audio folder exists
        if not os.path.exists(audio_folder):
            print(f"Audio folder {audio_folder} does not exist.")
            return

        # Get list of image files
        image_files = sorted([
            os.path.join(image_folder, img)
            for img in os.listdir(image_folder)
            if img.endswith(".png") or img.endswith(".jpg")
        ])

        # Check if there are audio files for each image
        if len(image_files) != len(os.listdir(audio_folder)):
            print("Number of image files does not match number of audio files.")
            return

        clips = []
        for i in range(len(image_files)):
            image_file = image_files[i]
            audio_file = os.listdir(audio_folder)[i]

            image_clip = ImageClip(image_file)
            audio_clip = AudioFileClip(os.path.join(audio_folder, audio_file))
            image_duration = audio_clip.duration
            
            # Set duration and resize image clip
            image_clip = image_clip.set_duration(image_duration).resize(width=1024, height=1024)

            # Apply crossfade transition
            if i > 0:
                prev_image_clip = clips[-1]
                crossfade_duration = min(1, image_duration)  # Limit crossfade duration to image duration or 1 second
                image_clip = CompositeVideoClip([prev_image_clip.set_start(image_duration - crossfade_duration).crossfadein(crossfade_duration),
                                                 image_clip.crossfadeout(crossfade_duration)])
            else:
                image_clip = image_clip.crossfadein(1)  # Fade in for the first clip
            
            # Combine image and audio
            combined_clip = image_clip.set_audio(audio_clip)
            clips.append(combined_clip)

        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(output_file, fps=24, audio_codec="aac", codec="libx264")

        return output_file
