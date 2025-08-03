import sys
import os
from moviepy.editor import (
    VideoFileClip,
    CompositeVideoClip,
    TextClip,
    ImageClip,
    concatenate_videoclips,
    ColorClip
)

# ------------------------------
# Configuration globale
# ------------------------------
RESOLUTION = (1080, 1920)
MAX_DURATION = 60  # secondes
WEBCAM_COORDS = {'x1': 5, 'y1': 8, 'x2': 542, 'y2': 282}
ASSETS_DIR = "assets"
OUTPUT_FILE = "output.mp4"

# ------------------------------
# Fonctions utilitaires
# ------------------------------
def load_clip(path):
    clip = VideoFileClip(path)
    if clip.duration > MAX_DURATION:
        clip = clip.subclip(0, MAX_DURATION)
    return clip

def create_background(duration):
    bg_path = os.path.join(ASSETS_DIR, "fond_short.png")
    if os.path.exists(bg_path):
        bg = ImageClip(bg_path).resize(RESOLUTION)
    else:
        bg = ColorClip(RESOLUTION, color=(0, 0, 0))
    return bg.set_duration(duration)

def extract_webcam(clip):
    cam = clip.crop(
        x1=WEBCAM_COORDS['x1'], y1=WEBCAM_COORDS['y1'],
        x2=WEBCAM_COORDS['x2'], y2=WEBCAM_COORDS['y2']
    )
    cam = cam.resize(height=int(RESOLUTION[1]*0.33))
    x_pos = (RESOLUTION[0] - cam.w) // 2
    return cam.set_position((x_pos, 0))

def extract_gameplay(clip):
    game = clip.crop(y1=WEBCAM_COORDS['y2'], y2=clip.h)
    game = game.resize(height=int(RESOLUTION[1]*0.67))
    x_pos = (RESOLUTION[0] - game.w) // 2
    y_pos = int(RESOLUTION[1]*0.33)
    return game.set_position((x_pos, y_pos))

def full_screen_clip(clip):
    c = clip.resize(height=RESOLUTION[1])
    c = c.crop(x_center=c.w/2, width=RESOLUTION[0], y_center=c.h/2, height=RESOLUTION[1])
    return c.set_position((0, 0))

def create_text_clip(text, font, size, stroke, y_pos, duration):
    try:
        txt = TextClip(text, fontsize=size, font=font, color='white', stroke_color='black', stroke_width=stroke)
    except:
        txt = TextClip(text, fontsize=size, color='white', stroke_color='black', stroke_width=stroke)
    return txt.set_position(('center', y_pos)).set_duration(duration)

def append_end_sequence(main_clip):
    end_path = os.path.join(ASSETS_DIR, "fin_de_short.mp4")
    if os.path.exists(end_path):
        end_clip = VideoFileClip(end_path).resize(RESOLUTION)
        return concatenate_videoclips([main_clip, end_clip])
    return main_clip

# ------------------------------
# Main process function
# ------------------------------
def process_clip(video_path, title, streamer, game):
    clip = load_clip(video_path)
    bg = create_background(clip.duration)

    # Layout
    if game.lower() == "just chatting":
        main = full_screen_clip(clip)
        overlays = [main]
    else:
        webcam = extract_webcam(clip)
        gameplay = extract_gameplay(clip)
        overlays = [gameplay, webcam]

    # Text clips
    title_clip = create_text_clip(title, "Roboto-Bold.ttf", 70, 1.5, 'top', clip.duration)
    streamer_clip = create_text_clip(streamer, "Roboto-Regular.ttf", 40, 0.5, 'bottom', clip.duration)
    overlays.extend([title_clip, streamer_clip])

    # Composite
    composed = CompositeVideoClip([bg] + overlays, size=RESOLUTION).set_audio(clip.audio)
    final = append_end_sequence(composed)
    final.write_videofile(OUTPUT_FILE, fps=30, codec="libx264", audio_codec="aac")

# ------------------------------
# Entrée du script
# ------------------------------
if __name__ == "__main__":
    if len(sys.argv) == 5:
        video_path = sys.argv[1]
        title = sys.argv[2]
        streamer = sys.argv[3]
        game = sys.argv[4]
    else:
        test_clip_data = {
            'video_path': 'video.mp4',
            'title': 'Test de montage de clip',
            'broadcaster_name': 'Anyme023',
            'game_name': 'Valorant'
        }
        video_path = test_clip_data['video_path']
        title = test_clip_data['title']
        streamer = test_clip_data['broadcaster_name']
        game = test_clip_data['game_name']

    process_clip(video_path, title, streamer, game)
