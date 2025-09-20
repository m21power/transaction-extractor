from fastapi import FastAPI, File, UploadFile
import pytesseract
from PIL import Image
import asyncio
import platform
import os

app = FastAPI()

async def extract_transaction_number(image):
    img = Image.open(image.file)
    text = pytesseract.image_to_string(img)
    for line in text.split('\n'):
        if "Transaction Number:" in line:
            return line.split("Transaction Number:")[1].strip()
    return "Transaction number not found"

@app.post("/extract_transaction/")
async def extract_transaction(file: UploadFile = File(...)):
    transaction_number = await extract_transaction_number(file)
    return {"transaction_number": transaction_number}

if platform.system() == "Emscripten":
    asyncio.ensure_future(extract_transaction())
else:
    if __name__ == "__main__":
        import uvicorn
        port = int(os.environ.get("PORT", 8000))
        uvicorn.run(app, host="0.0.0.0", port=port)