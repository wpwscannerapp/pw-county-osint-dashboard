import os
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Make sure it's using Supabase pooler format if needed
if "pooler" not in DATABASE_URL:
    print("Warning: Consider using Supabase Transaction Pooler URL")
