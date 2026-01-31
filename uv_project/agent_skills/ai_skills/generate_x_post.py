import subprocess
import re
import sys
from pathlib import Path

import subprocess
import os
import tempfile
import sys
from pathlib import Path

def generate_x_post(context: str) -> str:
    """
    Generates an ultra-short X post (max 50 chars) using CCR (Claude Code Router).
    Constraints: Professional builder voice, no emojis, no hashtags, no sales fluff.
    """
    prompt = f"""Task: Write a punchy X post based on the CONTEXT below.
    
    CONSTRAINTS:
    - MAXIMUM 50 CHARACTERS (including spaces).
    - Tone: Professional, direct, builder-focused.
    - NO emojis.
    - NO hashtags.
    - NO salesy language.
    
    CONTEXT:
    {context}
    
    Output ONLY binary content of the post. No JSON, no markdown, just the text.
    """

    # We might need multiple attempts if Claude exceeds 50 chars
    for attempt in range(2):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as tmp:
            tmp.write(prompt)
            tmp_path = tmp.name
        
        try:
            result = subprocess.run(
                ['cmd', '/c', 'ccr', 'code', '--print', tmp_path],
                capture_output=True,
                text=True,
                shell=False,
                stdin=subprocess.DEVNULL
            )
            
            post = result.stdout.strip()
            # Clean up potential markdown or noise
            post = post.strip('"').strip("'").split('\n')[0].strip()
            
            if 0 < len(post) <= 50:
                return post
            
            # If too long, tighten the prompt
            prompt = f"SHORTEN THIS TO UNDER 50 CHARACTERS: {post}\nOutput ONLY the text."
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    # Final fallback: just truncate
    return post[:47] + "..." if post and len(post) > 50 else (post or "Automation loop active.")

if __name__ == "__main__":
    test_context = "I just finished implementing a modular skill-based architecture for an AI employee system. It uses Claude for brains and Playwright for muscles."
    print(f"Testing generate_x_post...")
    post = generate_x_post(test_context)
    print(f"Generated ({len(post)} chars): {post}")
