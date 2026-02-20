from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import csv
from io import StringIO

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 92 * 1024
VALID_EXTENSIONS = {".csv", ".json", ".txt"}
UPLOAD_TOKEN = "qheflcbc902lztto"

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    x_upload_token_4267: str = Header(None)
):
    # 🔐 Auth check
    if x_upload_token_4267 != UPLOAD_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    filename = file.filename

    # 📄 File type check
    if not any(filename.endswith(ext) for ext in VALID_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Invalid file type")

    # 📏 File size check
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    # 📊 CSV analysis
    if filename.endswith(".csv"):
        text_data = contents.decode("utf-8")
        reader = csv.DictReader(StringIO(text_data))

        rows = 0
        total_value = 0
        category_counts = {}

        for row in reader:
            rows += 1
            value = float(row["value"])
            total_value += value
            category = row["category"]
            category_counts[category] = category_counts.get(category, 0) + 1

        return {
            "email": "23f3001363@ds.study.iitm.ac.in",
            "filename": filename,
            "rows": rows,
            "columns": reader.fieldnames,
            "totalValue": round(total_value, 2),
            "categoryCounts": category_counts
        }

    return {"message": "File accepted"}