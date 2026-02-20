from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import csv
from io import StringIO

app = FastAPI()

# ✅ CORS — REQUIRED FOR GRADER
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all origins
    allow_credentials=True,
    allow_methods=["*"],        # allow POST + OPTIONS
    allow_headers=["*"],        # allow custom headers
)

# ✅ Constants
MAX_FILE_SIZE = 92 * 1024
VALID_EXTENSIONS = {".csv", ".json", ".txt"}
UPLOAD_TOKEN = "qheflcbc902lztto"

# ✅ Root route (optional but helps health checks)
@app.get("/")
def root():
    return {"status": "ok"}

# ✅ Explicit OPTIONS handler for preflight safety
@app.options("/upload")
async def options_upload():
    return {}

# ✅ Upload endpoint
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    x_upload_token_4267: str = Header(None)
):
    # 🔐 Authentication
    if x_upload_token_4267 != UPLOAD_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    filename = file.filename

    # 📄 File type validation
    if not any(filename.endswith(ext) for ext in VALID_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Invalid file type")

    contents = await file.read()

    # 📏 File size validation
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    # 📊 CSV Processing
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

    # For valid non-CSV files
    return {"message": "File accepted"}