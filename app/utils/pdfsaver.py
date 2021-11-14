import os
import string
import random

from fastapi import File

CHUNK_SIZE = 2 ** 20  # 1MB


async def chunked_copy(src, dst):
    await src.seek(0)
    with open(dst, "wb+") as buffer:
        while True:
            contents = await src.read(CHUNK_SIZE)
            if not contents:
                break
            buffer.write(contents)


def generate_path_file(filename: str) -> str:
    current_path = os.path.abspath(os.getcwd())
    random_letters = "".join([random.choice(string.hexdigits) for _ in range(6)])
    file_location = f"{current_path}/files/{random_letters}__{filename}"
    return file_location
