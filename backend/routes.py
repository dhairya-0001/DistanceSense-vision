from fastapi import APIRouter

router = APIRouter()

# If project expands, additional API routes can be mapped here.
@router.get("/status")
def status():
    return {"message": "DriveSense AI API routes initialized."}
