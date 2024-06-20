import base64
import openai
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

openai.api_key = "sk-org-uiupjxtl6nhsahmjscumzjdi-e6xVWysw9O3rAOrTJQwET3BlbkFJg0Xy3rI9eHB7YKDoXGaz"

def encode_image(image):
    return base64.b64encode(image).decode('utf-8')

@app.post("/analyze-eeg/")
async def analyze_eeg(file: UploadFile = File(...)):
    image = await file.read()
    
    base64_image = encode_image(image)
    
    prompt = "Напиши состояния человека и цифры значений ритм."
    messages = [
        {"role": "system", "content": "Ты профессионал в области нейрофизиологии и главный анализатор диаграм спектрального анализа мозговой активности, который может дать точный анализ данных ЭЭГ, ты разделяешь график на тайм фреймы, и на каждый тайм фрейм пишешь точные значения с числами Альфа, Бета, Тета ритмы"},
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=1000,
        temperature=0.7
    )
    
    result = response.choices[0].message['content'].strip()
    
    return JSONResponse(content={"analysis": result})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
