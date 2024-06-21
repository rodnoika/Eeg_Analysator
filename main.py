import openai
import base64
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Настройка CORS
origins = [
    "http://157.230.23.55:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = "ваш ключ API OpenAI"

def encode_image(image):
    return base64.b64encode(image).decode('utf-8')

@app.post("/analyze-eeg/")
async def analyze_eeg(file: UploadFile = File(...)):
    try:
        image = await file.read()
        
        base64_image = encode_image(image)
        
        prompt = "Напиши состояния человека и цифры значений ритм."
        messages = [
            {"role": "system", "content": "Ты профессионал в области нейрофизиологии и главный анализатор диаграм спектрального анализа мозговой активности, который может дать точный анализ данных ЭЭГ, ты разделяешь график на тайм фреймы, и на каждый тайм фрейм пишешь точные значения с числами Альфа, Бета, Тета ритмы"},
            {"role": "user", "content": prompt},
            {"role": "user", "content": f"data:image/jpeg;base64,{base64_image}"}
        ]
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,  
            temperature=0.7
        )
        
        result = response['choices'][0]['message']['content'].strip()
        
        return JSONResponse(content={"analysis": result})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
