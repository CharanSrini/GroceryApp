import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="GroceryApp AI Backend")

# Configure Gemini
# Make sure to set GOOGLE_API_KEY in your .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("Warning: GOOGLE_API_KEY not found in environment variables.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

class RecipeRequest(BaseModel):
    ingredients: list[str]

@app.get("/")
def read_root():
    return {"message": "GroceryApp AI Backend is running"}

@app.post("/api/generate-recipe")
async def generate_recipe(request: RecipeRequest):
    if not GOOGLE_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API Key not configured")
    
    try:
        # Using Gemini 1.5 Flash for speed/efficiency
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        ingredients_str = ", ".join(request.ingredients)
        prompt = f"I have the following ingredients: {ingredients_str}. Suggest a quick recipe I can make."
        
        response = model.generate_content(prompt)
        return {"recipe": response.text}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))