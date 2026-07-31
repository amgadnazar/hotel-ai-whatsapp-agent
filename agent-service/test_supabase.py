from app.database import supabase

response = supabase.table("guests").select("*").execute()

print(response.data)