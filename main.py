import base64
from openai import OpenAI
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key="sk-org-uiupjxtl6nhsahmjscumzjdi-e6xVWysw9O3rAOrTJQwET3BlbkFJg0Xy3rI9eHB7YKDoXGaz",
)

def encode_image(image):
    return base64.b64encode(image).decode('utf-8')

@app.post("/analyze-eeg/")
async def analyze_eeg(file: UploadFile = File(...)):
    try:
        image = await file.read()
        
        base64_image = encode_image(image)
        
        prompt = "Ты можешь писать только True или False, есть ли у человека стресс?"
        messages = [
            {"role": "system", "content": "Ты должен написать либо True если у человека стресс, либо False если у него нету стресса"},
            {"role": "user", "content":[{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url":f"data:image/jpeg;base64,{base64_image}"}}]}
        ]
        #Ты профессионал в области нейрофизиологии и главный анализатор диаграм спектрального анализа мозговой активности, пишешь только самочуствие и состояние человека, и не пиши воду, и под конец ты должен сделать итог находится ли человек в Стрессе или нет
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=500,
        )
        
        result = response.choices[0].message.content
        
        return JSONResponse(content={"analysis": result})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
