from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO


# ============================================================
# Configuration
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "model" / "best.pt"

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


# ============================================================
# Load YOLO Model
# ============================================================

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"YOLO model not found at: {MODEL_PATH}"
    )

model = YOLO(str(MODEL_PATH))


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="Bangladeshi Currency Detection API",
    description="YOLOv11-based Bangladeshi Taka denomination detection API",
    version="1.0.0"
)


# ============================================================
# CORS Configuration
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Health Check
# ============================================================

@app.get("/")
def home():
    return {
        "success": True,
        "message": "Bangladeshi Currency Detection API is running",
        "endpoint": "/predict"
    }


# ============================================================
# Currency Prediction
# ============================================================

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # --------------------------------------------------------
    # Validate filename
    # --------------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided."
        )

    # --------------------------------------------------------
    # Validate file extension
    # --------------------------------------------------------

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a JPG, JPEG, or PNG image."
        )

    # --------------------------------------------------------
    # Create temporary directory
    # --------------------------------------------------------

    temp_dir = BASE_DIR / "temp"
    temp_dir.mkdir(exist_ok=True)

    # Use only filename for safety
    safe_filename = Path(file.filename).name

    temp_path = temp_dir / safe_filename

    try:

        # ----------------------------------------------------
        # Read uploaded image
        # ----------------------------------------------------

        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        # ----------------------------------------------------
        # Save temporary image
        # ----------------------------------------------------

        with open(temp_path, "wb") as f:
            f.write(contents)

        # ----------------------------------------------------
        # Run YOLO inference
        # ----------------------------------------------------

        results = model.predict(
            source=str(temp_path),
            conf=0.30,
            imgsz=640,
            verbose=False
        )

        result = results[0]

        # ----------------------------------------------------
        # Extract detections
        # ----------------------------------------------------

        detections = []

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            detections.append(
                {
                    "denomination": model.names[class_id],
                    "confidence": round(confidence, 4),
                    "bounding_box": {
                        "x1": round(x1, 2),
                        "y1": round(y1, 2),
                        "x2": round(x2, 2),
                        "y2": round(y2, 2)
                    }
                }
            )

        # ----------------------------------------------------
        # Return prediction
        # ----------------------------------------------------

        return {
            "success": True,
            "filename": safe_filename,
            "detections": detections
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

    finally:

        # ----------------------------------------------------
        # Delete temporary image
        # ----------------------------------------------------

        if temp_path.exists():
            temp_path.unlink()