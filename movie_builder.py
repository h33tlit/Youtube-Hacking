import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, ImageSequenceClip
import random
import textwrap
import time

# Define the video properties
width = 1280
height = 720
fps = 30

# Define the desired duration of the final video
total_duration = 15  # Duration in seconds

# Define the timeframes for each background clip
background_clips = [
    {'path': 'Background/v2.mp4', 'duration': 5},  # Background 1 for 5 seconds
    {'path': 'Background/v3.mp4', 'duration': 5},
    {'path': 'Background/v1.mp4', 'duration': 5}
]

# Randomly select 3 background clips
selected_clips = random.sample(background_clips, 3)

# Open the selected background videos
background_videos = []
for clip in selected_clips:
    video_path = clip['path']
    video_duration = clip['duration']
    video = VideoFileClip(video_path).resize((width, height))
    background_videos.append({'video': video, 'duration': video_duration * fps})

# Define the text properties
text_color = (255, 255, 255)  # White color
title_font_path = 'font/TitilliumWeb-Black.ttf'
subtitle_font_path = 'font/TitilliumWeb-Light.ttf'

# Define the titles and subtitles with their font sizes and styles
titles = [
    {
        'title': 'Embrace the Journey',
        'subtitle': 'Exploring the uncharted territories of life leads to remarkable discoveries.',
        'font_size': 60,
        'title_font': ImageFont.truetype(title_font_path, 60),
        'subtitle_font': ImageFont.truetype(subtitle_font_path, 30),
        'duration': 5  # Duration in seconds
    },
    {
        'title': 'The Power of Connections',
        'subtitle': 'In the web of human interactions, profound transformations and endless possibilities await.',
        'font_size': 60,
        'title_font': ImageFont.truetype(title_font_path, 60),
        'subtitle_font': ImageFont.truetype(subtitle_font_path, 30),
        'duration': 5  # Duration in seconds
    },
    {
        'title': 'Illuminate the Darkness',
        'subtitle': 'A single spark of hope can light up even the darkest corners, revealing hidden paths to greatness.',
        'font_size': 60,
        'title_font': ImageFont.truetype(title_font_path, 60),
        'subtitle_font': ImageFont.truetype(subtitle_font_path, 30),
        'duration': 5  # Duration in seconds
    }
]

# Create a list to store video clips with titles
video_clips = []

# Calculate the number of title repetitions to fit the total duration
num_repetitions = int(np.ceil(total_duration / sum(title['duration'] for title in titles)))


gap_duration = 5  # Duration in seconds

# Iterate over the titles and generate video clips with text
for _ in range(num_repetitions):
    for i, title in enumerate(titles):
        title_text = title['title']
        subtitle_text = title['subtitle']
        font_size = title['font_size']
        title_font = title['title_font']
        subtitle_font = title['subtitle_font']
        title_duration = title['duration'] * fps

        # Generate frames with the current title
        title_frames = []
        for frame_count in range(title_duration):
            # Find the corresponding background video based on index
            current_video_index = (i + frame_count // title_duration) % len(background_videos)
            current_video = background_videos[current_video_index]

            # Get the frame from the current background video
            t = (frame_count % current_video['duration']) / fps
            background_frame = current_video['video'].get_frame(t)

            # Create a copy of the background frame
            title_frame = background_frame.copy()

            # Create a PIL Image from the frame with text
            pil_frame = Image.fromarray(title_frame)

            # Check if the current frame is within the gap duration
            if frame_count < (fps * gap_duration):

                # Add the title text
                title_width, title_height = title_font.getsize(title_text)
                title_x = int((width - title_width) * 0.2)
                title_y = int((height - title_height) / 2)
                draw = ImageDraw.Draw(pil_frame)
                title_text_wrapped = textwrap.wrap(title_text, width=int(0.6 * width))
                title_text_wrapped = '\n'.join(title_text_wrapped)
                title_text_size = draw.textsize(title_text_wrapped, font=title_font)

                # Adjust the title position to ensure it stays in the middle
                title_x = int((width - title_text_size[0]) / 2)
                title_y = int((height - title_text_size[1]) / 2)

                draw.text((title_x, title_y), title_text_wrapped, font=title_font, fill=text_color, align='center')

                # Add the subtitle text
                subtitle_width, subtitle_height = subtitle_font.getsize(subtitle_text)
                subtitle_x = int((width - subtitle_width) * 0.2)
                subtitle_y = title_y + title_text_size[1] + 10

                # Adjust the subtitle position to ensure it stays in the middle
                subtitle_x = int((width - subtitle_width) / 2)
                subtitle_y = int((height - subtitle_height) / 2) + title_text_size[1] + 10

                draw.text((subtitle_x, subtitle_y), subtitle_text, font=subtitle_font, fill=text_color, align='center')

            # Convert the PIL Image back to a numpy array
            title_frame = np.array(pil_frame)

            # Append the frame to the list of frames for the current title
            title_frames.append(title_frame)

        # Create a video clip from the frames of the current title
        title_clip = concatenate_videoclips(
            [ImageSequenceClip(title_frames, fps=fps)] * (title_duration // len(title_frames)))

        # Append the title clip to the list of video clips
        video_clips.append(title_clip)

# Concatenate all the video clips with titles
final_clip = concatenate_videoclips(video_clips)

# Set the audio for the final clip and trim the audio as well
audio_path = 'Music/music.mp3'  # Path to the background music
audio_clip = AudioFileClip(audio_path)
final_clip = final_clip.set_audio(audio_clip.set_duration(final_clip.duration))

timestamp = time.time()

# Write the final video to a file
final_video_path = 'Output/final_video'+str(timestamp)+'.mp4'  # Path for the final video
final_clip.write_videofile(final_video_path, codec='libx264', fps=fps)
