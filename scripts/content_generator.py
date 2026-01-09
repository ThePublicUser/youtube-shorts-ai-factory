import requests
import random
import json

# Using free APIs for content
TOPICS = [
    "psychology facts", "space mysteries", "dark history",
    "human behavior", "scientific paradoxes", "quantum physics",
    "ancient civilizations", "cognitive biases", "unsolved mysteries"
]

def generate_script():
    """Generate script using free AI APIs"""
    
    # Option 1: Use Hugging Face Inference API (FREE)
    try:
        return generate_with_huggingface()
    except:
        # Fallback to local generation if API fails
        return generate_local_script()

def generate_with_huggingface():
    """Use Hugging Face's free inference endpoints"""
    
    # Using a smaller model that's free
    API_URL = "https://api-inference.huggingface.co/models/gpt2"
    headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
    
    prompt = f"""Create a 45-second YouTube Shorts script about {
        random.choice(TOPICS)}.
    Format:
    TITLE: Catchy title
    HOOK: First 3-second hook
    SCRIPT: 5 bullet points (each 5-7 words)
    TAGS: 5 relevant hashtags
    
    Make it surprising and engaging:"""
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 200,
            "temperature": 0.9,
            "do_sample": True
        }
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        return parse_ai_response(result[0]['generated_text'])
    
    raise Exception("Hugging Face API failed")

def generate_local_script():
    """Local fallback with pre-defined templates"""
    
    templates = [
        {
            "title": f"The {random.choice(['Secret', 'Hidden', 'Unknown'])} Truth About {random.choice(['Deja Vu', 'Dreams', 'Memory'])}",
            "hook": "Your brain is hiding this from you",
            "script_lines": [
                f"Did you know {random.choice(['95%', '80%', '70%'])} of people experience this?",
                f"The {random.choice(['real reason', 'scientific explanation', 'truth'])} will surprise you",
                f"It's called {random.choice(['Jamais vu', 'Presque vu', 'Capgras syndrome'])}",
                f"And it reveals how your {random.choice(['memory', 'perception', 'consciousness'])} works",
                "This happens more when you're tired or stressed"
            ],
            "description": f"Mind-blowing {random.choice(TOPICS)} fact that will change how you think",
            "tags": [random.choice(TOPICS).replace(' ', ''), "facts", "psychology", "shorts"],
            "keywords": random.choice(TOPICS)
        }
    ]
    
    return random.choice(templates)

def parse_ai_response(text):
    """Parse AI response into structured format"""
    # Simple parsing logic
    lines = text.split('\n')
    
    return {
        "title": lines[0].replace("TITLE:", "").strip(),
        "hook": lines[1].replace("HOOK:", "").strip(),
        "script_lines": [line.strip() for line in lines[3:8] if line.strip()],
        "description": "Fascinating fact you won't believe!",
        "tags": ["facts", "psychology", "space", "history", "shorts"],
        "keywords": random.choice(TOPICS)
    }