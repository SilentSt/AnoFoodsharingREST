import os
import random
import string
from enum import Enum

from fastapi import APIRouter, UploadFile, File, Depends
from pdfminer.pdfparser import PDFSyntaxError
from starlette.responses import JSONResponse

from app.db.crud import CrudDatabase
from app.utils.pdfparser import shop_parse_pdf, user_parse_pdf
from app.utils.pdfsaver import chunked_copy, generate_path_file

file_router = APIRouter()


class ParseEnum(str, Enum):
    SHOP = "shop"
    USER = "user"


@file_router.post("/upload/document")
async def parse_pdf(document_type: ParseEnum, file: UploadFile = File(...)):
    exception = JSONResponse(
            status_code=400,
            content={
                "content": "An error occurred while trying to disband the document,"
                           " please try again later."
            }
        )

    if document_type == ParseEnum.SHOP:
        try:
            result = shop_parse_pdf(path=file.file)
            return result
        except ValueError:
            return exception

    if document_type == ParseEnum.USER:
        try:
            result = user_parse_pdf(path=file.file)
            return result
        except ValueError:
            return exception


