import os
import tempfile
from dotenv import load_dotenv, dotenv_values

# Write a temporary .env file
env_content = "API_KEY=secret-from-dotenv\nDEBUG=true\n"
with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
    f.write(env_content)
    env_path = f.name

# Pre-set the variable in the current process (simulating a shell export)
os.environ["API_KEY"] = "shell-value"

# ✗ GOTCHA: load_dotenv does NOT override existing env vars by default
load_dotenv(env_path)
print("without override:", os.environ["API_KEY"])   # => without override: shell-value

# ✓ override=True forces .env to win — only use in dev/test, never production
load_dotenv(env_path, override=True)
print("with override:", os.environ["API_KEY"])      # => with override: secret-from-dotenv

# dotenv_values returns a plain dict — never touches os.environ
config = dotenv_values(env_path)
print("dotenv_values:", config["DEBUG"])            # => dotenv_values: true
print("DEBUG in os.environ:", "DEBUG" in os.environ)  # => DEBUG in os.environ: False

# Clean up
os.unlink(env_path)
