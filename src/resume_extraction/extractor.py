import json
from pathlib import Path
from datetime import datetime

from .pdf_reader import extract_pdf_text
from .docx_reader import extract_docx_text
from .text_cleaner import clean_text


SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def extract_resume(file_path: str) -> dict:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Resume not found: {file_path}")

    extension = path.suffix.lower()

    if extension == ".pdf":
        raw_text = extract_pdf_text(str(path))

    elif extension == ".docx":
        raw_text = extract_docx_text(str(path))

    else:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    cleaned_text = clean_text(raw_text)

    result = {
        "metadata": {
            "file_name": path.name,
            "file_type": extension.replace(".", "").upper(),
            "file_size_bytes": path.stat().st_size,
            "processed_at": datetime.now().isoformat()
        },
        "extraction": {
            "status": "success",
            "raw_text": raw_text,
            "cleaned_text": cleaned_text,
            "word_count": len(cleaned_text.split()),
            "character_count": len(cleaned_text),
            "text_extracted": bool(cleaned_text)
        }
    }

    return result


def save_extracted_resume(result: dict, output_directory: str) -> str:
    output_dir = Path(output_directory)
    output_dir.mkdir(parents=True, exist_ok=True)

    file_name = result["metadata"]["file_name"]
    output_file = output_dir / f"{Path(file_name).stem}.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            result,
            file,
            indent=4,
            ensure_ascii=False
        )

    return str(output_file)


def process_resume_folder(
    input_directory: str,
    output_directory: str
) -> list:

    input_dir = Path(input_directory)

    if not input_dir.exists():
        raise FileNotFoundError(
            f"Input folder not found: {input_directory}"
        )

    results = []

    for file_path in sorted(input_dir.iterdir()):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            result = extract_resume(str(file_path))

            output_path = save_extracted_resume(
                result,
                output_directory
            )

            results.append({
                "file_name": file_path.name,
                "file_type": file_path.suffix.lower(),
                "status": "PASS",
                "word_count": result["extraction"]["word_count"],
                "output": output_path
            })

        except Exception as error:

            results.append({
                "file_name": file_path.name,
                "file_type": file_path.suffix.lower(),
                "status": "FAIL",
                "error": str(error)
            })

    return results
