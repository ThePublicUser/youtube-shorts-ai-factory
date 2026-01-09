import moviepy.editor as mp
from moviepy.editor import *
import gtts
import requests
import os
from PIL import Image, ImageDraw, ImageFont

def create_short_video(script_lines, title, background_path, add_audio=True):
    """Create video with text animations and audio"""
    
    # Load background image
    clip = mp.ImageClip(background_path).set_duration(60)
    
    # Create text clips with kinetic typography
    text_clips = []
    y_positions = [0.2, 0.35, 0.5, 0.65, 0.8]  # Relative Y positions
    
    for i, line in enumerate(script_lines):
        # Create text clip with animation
        txt_clip = (mp.TextClip(line, fontsize=70, color='white', 
                               font='Arial', stroke_color='black', 
                               stroke_width=2, method='caption',
                               size=(700, None), align='center')
                   .set_position(('center', y_positions[i]))
                   .set_start(i * 10)  # Appear every 10 seconds
                   .set_duration(8)
                   .crossfadein(1)     # Fade in
                   .crossfadeout(1))   # Fade out
        
        text_clips.append(txt_clip)
    
    # Create audio
    if add_audio:
        audio_path = create_audio(" ".join(script_lines), title)
        audio = mp.AudioFileClip(audio_path)
        clip = clip.set_audio(audio)
    
    # Add background music
    bg_music = add_background_music()
    if bg_music:
        # Lower volume for background music
        bg_music = bg_music.volumex(0.3)
        clip = clip.set_audio(mp.CompositeAudioClip([clip.audio, bg_music]))
    
    # Composite all clips
    final_video = mp.CompositeVideoClip([clip] + text_clips)
    
    # Add intro/outro animations
    final_video = add_transitions(final_video)
    
    # Export video
    output_path = f"shorts_output_{hash(title)}.mp4"
    final_video.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True
    )
    
    return output_path

def create_audio(text, title):
    """Generate audio using free TTS services"""
    
    # Option 1: Google Text-to-Speech (FREE, unlimited)
    try:
        return create_with_gtts(text)
    except:
        # Option 2: Edge TTS (FREE, Microsoft's voices)
        return create_with_edge_tts(text)

def create_with_gtts(text):
    """Use Google TTS (completely free)"""
    tts = gtts.gTTS(text=text, lang='en', slow=False)
    audio_path = "audio_output.mp3"
    tts.save(audio_path)
    return audio_path

def create_with_edge_tts(text):
    """Use Microsoft Edge TTS (free, good quality)"""
    import asyncio
    import edge_tts
    
    async def generate():
        communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
        await communicate.save("audio_output.mp3")
    
    # Run async function
    asyncio.run(generate())
    return "audio_output.mp3"

def add_background_music():
    """Add royalty-free background music"""
    
    # Use YouTube Audio Library music (download one track to your repo)
    music_path = "assets/music/background.mp3"
    
    if os.path.exists(music_path):
        return mp.AudioFileClip(music_path).subclip(0, 60)
    
    # If no music file, create silent audio
    return None

def add_transitions(video_clip):
    """Add smooth transitions"""
    
    # Fade in/out
    video_clip = video_clip.fadein(1).fadeout(1)
    
    # Add zoom effect
    video_clip = video_clip.resize(lambda t: 1 + 0.01 * t)
    
    return video_clip