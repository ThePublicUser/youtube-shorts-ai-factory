import requests
import os
from PIL import Image, ImageDraw, ImageFont
import io

def create_background_image(title, keywords):
    """Create or generate background image"""
    
    # Option 1: Use Stable Diffusion via Replicate (FREE tier)
    try:
        return generate_with_replicate(title)
    except:
        # Option 2: Use Unsplash API (free, no AI but high quality)
        return create_with_unsplash(keywords)

def generate_with_replicate(prompt):
    """Generate AI image using Replicate's free tier"""
    
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
    UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY', 'your_unsplash_key')
    
    url = f"https://api.unsplash.com/photos/random"
    params = {
        "query": keywords,
        "orientation": "portrait",
        "client_id": UNSPLASH_ACCESS_KEY
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        image_url = data['urls']['regular']
        
        # Download image
        img_response = requests.get(image_url)
        image_path = f"background_{keywords.replace(' ', '_')}.jpg"
        
        with open(image_path, 'wb') as f:
            f.write(img_response.content)
        
        # Darken the image for better text contrast
        darken_image(image_path)
        
        return image_path
    
    # Fallback: Create gradient background
    return create_gradient_background()

def create_gradient_background():
    """Create a simple gradient background if APIs fail"""
    
    # Create a gradient image
    from PIL import Image, ImageDraw
    
    img = Image.new('RGB', (768, 1344), color='black')
    draw = ImageDraw.Draw(img)
    
    # Add some random shapes for visual interest
    for _ in range(50):
        x = random.randint(0, 768)
        y = random.randint(0, 1344)
        r = random.randint(5, 50)
        color = (random.randint(0, 100), random.randint(0, 100), random.randint(100, 255))
        draw.ellipse([x-r, y-r, x+r, y+r], fill=color, width=0)
    
    image_path = "fallback_background.png"
    img.save(image_path)
    
    return image_path

def darken_image(image_path):
    """Darken image for better text visibility"""
    img = Image.open(image_path)
    # Darken by 40%
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.6)
    img.save(image_path)