import os
import tempfile
from dotenv import load_dotenv

# Simulate a .env file you would normally keep out of git
env_text = "API_KEY=supersecret-abc123\nDEBUG=true\n"
with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
    env_path = f.name
    f.write(env_text)

load_dotenv(dotenv_path=env_path, override=True)

print("dotenv api_key:", os.getenv("API_KEY"))   # => dotenv api_key: supersecret-abc123
print("dotenv debug:", os.getenv("DEBUG"))        # => dotenv debug: true

# ⚠️ Common gotcha: load_dotenv() does NOT override an already-set variable
# unless you pass override=True.  Here we prove the default (override=False) behaviour.
os.environ["API_KEY"] = "already-set"
load_dotenv(dotenv_path=env_path, override=False)
print("override=False result:", os.getenv("API_KEY"))  # => override=False result: already-set
