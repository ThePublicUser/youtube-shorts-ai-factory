#!/usr/bin/env python3
"""
YouTube Shorts AI Factory - Main Automation Script
Runs on GitHub Actions for free
"""

import os
import json
from datetime import datetime
from content_generator import generate_script
from image_generator import create_background_image
from video_creator import create_short_video
from youtube_uploader import upload_to_youtube

def main():
    print("🚀 Starting YouTube Shorts AI Factory...")
    
    # Step 1: Generate script
    print("📝 Generating script...")
    script_data = generate_script()
    print(f"✅ Generated: {script_data['title']}")
    
    # Step 2: Create background image
    print("🎨 Creating background image...")
    image_path = create_background_image(script_data['title'], script_data['keywords'])
    
    # Step 3: Create video with audio
    print("🎬 Creating video with audio...")
    video_path = create_short_video(
        script_data['script_lines'],
        script_data['title'],
        image_path,
        add_audio=True
    )
    
    # Step 4: Upload to YouTube
    print("📤 Uploading to YouTube...")
    video_url = upload_to_youtube(
        video_path,
        script_data['title'],
        script_data['description'],
        script_data['tags']
    )
    
    print(f"✅ Process complete! Video URL: {video_url}")
    
    # Save metadata for tracking
    save_metadata(script_data, video_url)
    
    return video_url

def save_metadata(script_data, video_url):
    """Save video metadata for analytics"""
    metadata = {
        'title': script_data['title'],
        'video_url': video_url,
        'created_at': datetime.now().isoformat(),
        'script_hash': hash(json.dumps(script_data))
    }
    
    with open('metadata.json', 'a') as f:
        f.write(json.dumps(metadata) + '\n')

if __name__ == "__main__":
    main()