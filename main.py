import os
import json
import pymupdf as fitz
from datetime import datetime


CONFIG_FILE = os.environ.get("CONFIG_FILE", "config.json")

with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

doc = fitz.open(config["inputFile"])

new_doc = fitz.open()
original_page = doc.load_page(0)
total_iterations = round(config["numberOfPages"] / config["amountPerPage"])

n = 1

field_definitions = config["fieldDefintions"]
coordinates = {field["fieldName"]: fitz.Point(
    *field["coordinates"]) for field in field_definitions}


while n <= config["numberOfPages"]:
    for _ in range(config["amountPerPage"]):
        if n > config["numberOfPages"]:
            break
        new_page = new_doc.new_page(
            width=original_page.rect.width, height=original_page.rect.height)
        new_page.show_pdf_page(new_page.rect, doc, 0)

        new_page.insert_text(coordinates["receiptNo1"],
                             text=f"{n:05}",
                             fontname=config["fontFamily"],
                             fontsize=config["fontSize"],
                             color=tuple(config["fontColour"]),
                             rotate=0
                             )

        new_page.insert_text(coordinates["receiptNo2"],
                             f"{n+1:05}",
                             fontname=config["fontFamily"],
                             fontsize=config["fontSize"],
                             color=tuple(config["fontColour"]),
                             rotate=0
                             )

        new_page.insert_text(coordinates["receiptNo3"],
                             f"{n+2:05}",
                             fontname=config["fontFamily"],
                             fontsize=config["fontSize"],
                             color=tuple(config["fontColour"]),
                             rotate=0
                             )

        new_page.insert_text(coordinates["receiptNo4"],
                             f"{n+3:05}",
                             fontname=config["fontFamily"],
                             fontsize=config["fontSize"],
                             color=tuple(config["fontColour"]),
                             rotate=0
                             )

        n += config["amountPerPage"]

output_file = f"{config['outputFile']}-{datetime.now().strftime('%Y-%m-%d %H.%M.%S')}.pdf"

os.makedirs(os.path.dirname(output_file), exist_ok=True)

new_doc.save(output_file)
