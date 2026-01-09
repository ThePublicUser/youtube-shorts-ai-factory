import requests
import os
import random  # ADD THIS IMPORT
from PIL import Image, ImageDraw, ImageEnhance  # FIXED IMPORT

def create_background_image(title, keywords):
    """Create or generate background image"""
    
    # Option 1: Use Unsplash API first (more reliable, free)
    try:
        return create_with_unsplash(keywords)
    except Exception as e:
        print(f"Unsplash failed: {e}")
        # Option 2: Try Replicate (needs API token)
        try:
            return generate_with_replicate(title)
        except Exception as e2:
            print(f"Replicate failed: {e2}")
            # Option 3: Fallback to gradient
            return create_gradient_background()

def generate_with_replicate(prompt):
    """Generate AI image using Replicate's free tier"""
    
    # Check if API token exists
    REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
    if not REPLICATE_API_TOKEN:
        raise Exception("No Replicate API token found")
    
    import replicate
    
    # Replicate has a free tier for Stable Diffusion
    output = replicate.run(
        "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
        input={
            "prompt": f"minimalist abstract background for {prompt}, dark theme, mysterious, 9:16 aspect ratio",
            "width": 768,
            "height": 1344,
            "num_outputs": 1
        }
    )
    
    # Download the image
    image_url = output[0]
    response = requests.get(image_url)
    
    # Save locally
    image_path = f"generated_image_{hash(prompt)}.png"
    with open(image_path, 'wb') as f:
        f.write(response.content)
    
    return image_path

def create_with_unsplash(keywords):
    """Get free stock image from Unsplash"""
    
    # Unsplash API (free tier, 50 requests per hour)
    UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
    
    if not UNSPLASH_ACCESS_KEY:
        # Use a public demo key (rate limited)
        UNSPLASH_ACCESS_KEY
