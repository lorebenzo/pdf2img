from fastapi import FastAPI, UploadFile, File, HTTPException
import pdf2image
from fastapi.responses import Response

app = FastAPI(
    root_path="/api",
)

from io import BytesIO
from starlette.concurrency import run_in_threadpool


@app.post(
    "/file",
    responses={
        400: {
            "description": "Bad Request - Invalid file type or empty PDF.",
            "content": {
                "application/json": {
                    "example": {"detail": "File type not supported. Only PDF files are supported."}
                }
            },
        },
        500: {
            "description": "Internal Server Error - Unexpected processing error.",
            "content": {
                "application/json": {
                    "example": {"detail": "Internal Server Error: <error_message>"}
                }
            },
        },
        200: {"description": "Successful response.", "content": {}},
    },
)
async def upload_file(file: UploadFile = File(...)):
    # input validation
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="File type not supported. Only PDF files are supported.",
        )

    try:
        contents = await file.read()

        images = await run_in_threadpool(pdf2image.convert_from_bytes, contents)

        if not images:
            raise HTTPException(
                status_code=400,
                detail="No images found in PDF file. Please upload  not empty PDF file",
            )

        # convert image to bytes
        b_images = BytesIO()

        # save only the first page
        await run_in_threadpool(
            images[0].save,
            b_images,
            format="PNG",
        )

        return Response(content=b_images.getvalue(), media_type="image/png")

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {e}",
        )


@app.get("/hello")
async def hello():
    return "I'm alive"
