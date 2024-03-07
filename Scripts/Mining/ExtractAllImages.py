import fitz
import io
import os
import pathlib
from pathlib import Path
from PIL import Image

sharepoint_path = "/Users/ruben/PycharmProjects/PDFExtract/files/"
Path(f"{sharepoint_path}/Extracted Images").mkdir(parents=True, exist_ok=True)

# Iterate through all files in
filepath = pathlib.Path(sharepoint_path)
for file in filepath.iterdir():
    if file.name.endswith('.pdf'):
        pdf_file = fitz.open(file)
        # Loop through the pages in the document
        for page_no in range(len(pdf_file)):
            page = pdf_file[page_no]
            image_list = page.get_images()
            # printing number of images found in this page
            # if image_list:
            #     print(
            #         f"[+] Found a total of {len(image_list)} images in page {page_no}")
            # else:
            #     print("[!] No images found on page", page_index)
            for image_index, img in enumerate(page.get_images(), start=1):
                # get the XREF of the image
                xref = img[0]

                # extract the image bytes
                base_image = pdf_file.extract_image(xref)
                image_bytes = base_image["image"]

                # get the image extension
                image_ext = base_image["ext"]

                # Load it to PIL
                image = Image.open(io.BytesIO(image_bytes))

                #Create folder for each doc
                # Path(f"{root_folder}/my1/my2").mkdir(parents=True, exist_ok=True)

                # Check if the image meets the minimum dimensions and is not transparent and save it
                if image.width >= 150 and image.height >= 150:
                    file_name = f"{file.name} image{page_no + 1}_{image_index}.{image_ext}"
                    if image.mode == 'RGB':
                        full_file_path = ("Extracted Images/" + file_name)
                        image.save(
                            open(os.path.join(sharepoint_path, full_file_path), "wb"),
                            format=image_ext.upper())
                    # else:
                    #     full_file_path = ("Extracted Images/transparents/" + file_name)
                    #     image.save(
                    #         open(os.path.join(sharepoint_path, full_file_path), "wb"),
                    #         format=image_ext.upper())
                # else:
                #     print(f"[-] Skipping image {image_index} on page {page_no} due to its small size.")

# Sources:
#     https://medium.com/@alexaae9/python-how-to-extract-images-from-pdf-documents-9492a767a613
#     https://www.geeksforgeeks.org/how-to-extract-images-from-pdf-in-python/