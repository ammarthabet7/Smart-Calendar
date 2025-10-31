from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path('.env')
print(f"[DEBUG] Looking for .env at: {env_path.absolute()}")
print(f"[DEBUG] .env exists: {env_path.exists()}")

if env_path.exists():
    print(f"[DEBUG] .env file size: {env_path.stat().st_size} bytes")
    load_dotenv(dotenv_path=env_path)
    print(f"[DEBUG] OPENROUTER_API_KEY loaded: {os.getenv('OPENROUTER_API_KEY')}")
else:
    print("[DEBUG] .env file NOT FOUND")
