import requests
import os
import pymupdf
from pathlib import Path
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import shutil
import sys
from dotenv import load_dotenv

load_dotenv(override=True)

# ================== Initial variables =============================

SITE_TARGET = os.getenv("SITE_TARGET")
SPLIT_PAGE_CHAPTER = os.getenv("SPLIT_PAGE")
manga_name = sys.argv[1]
start_chapter = int(sys.argv[2])
end_chapter = int(sys.argv[3])

# ==================================================================
script_directory = Path(os.path.dirname(os.path.realpath(__file__)))
target_directory = script_directory / "generated"
is_split_page_mode = SPLIT_PAGE_CHAPTER == "True"

print(f"Split page mode is {'on' if is_split_page_mode is True else 'off'}")


def convert_img_to_pdf(img):
    return Image.open(BytesIO(img)).convert("RGB")


def download_image(src_url, save_path, index):
    image_response = requests.get(src_url)
    if image_response.status_code == 200:
        # Convert to jpg and save file
        img = convert_img_to_pdf(image_response.content)
        img.save(save_path)
        print(f"Downloaded::page {index} ===> {src_url}")
    else:
        print(f"Fail::Image download. Status code: {
                image_response.status_code
            }"
        )


def download_image_from_xpath(response_url, save_path, i):
    if response_url.status_code == 200:
        # Parse HTML
        soup = BeautifulSoup(response_url.content, "html.parser")

        image_element = soup.find("img", src=True)
        if image_element:
            image_url = image_element["src"]
            # Download image
            image_response = requests.get(f"{SITE_TARGET}{image_url}")

            if image_response.status_code == 200:
                # Save image in specified folder
                with open(save_path, "wb") as f:
                    f.write(image_response.content)
                print(f"Downloaded::page {i}")
                return True
            else:
                print(
                    f"Fail::Image download. Status code: {
                        image_response.status_code
                    }"
                )
                return False
        else:
            print("Fail::No element found.")
            return False
    else:
        print(f"Fail::HTTP request failure. Status code: {
                response_url.status_code
            }"
        )
        return False


def download_one_page_chapter(target_manga, chapter_number, target_folder):
    i = 1  # Page start
    url = f"{SITE_TARGET}/{target_manga}/{chapter_number}"
    print(f"Start_Download::{target_manga} - {chapter_number} from {url}")
    response_url = requests.get(url)

    if response_url.status_code == 200:
        # Parse HTML
        soup = BeautifulSoup(response_url.content, "html.parser")
        # print(soup)
        image_elements = soup.find_all(
            "img",
            attrs={
                "data-id": True,
            },
        )

        i = 1  # Page start
        for image_element in image_elements:
            save_path = f"{target_folder}/{i}.jpg"

            image_element_source = image_element["data-src"]
            if image_element_source:
                download_image(image_element_source, save_path, i)
                i += 1
            else:
                print("Fail:No image source")
    else:
        print(f"Fail::HTTP request failure. Status code: {
                response_url.status_code
            }"
        )
        return False


def download_split_pages_chapter(target_manga, chapter_number, target_folder):
    i = 1  # Page start
    base_url = f"{SITE_TARGET}/scan-{target_manga}"
    print(f"Start_Download::{target_manga} - {chapter_number} from {base_url}")
    while True:
        url = f"{base_url}/{chapter_number}/{i}"
        response_url = requests.get(url)
        save_path = f"{target_folder}/{i}.jpg"
        response = download_image_from_xpath(response_url, save_path, i)
        if response is True:
            i += 1
        else:
            print(f"End_Download::Chapter {target_manga}-{chapter_number}")
            break


def merge_files_in_PDF(file_list, pdf_name, target_path):
    pdf_name_with_extension = str(pdf_name) + ".pdf"
    pdf_path = os.path.join(target_path, pdf_name_with_extension)
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    doc = pymupdf.open()
    for filename in file_list:
        image_path = os.path.join(pdf_name, filename)
        if image_path.endswith(".DS_Store"):
            continue

        try:
            # Assume insert_file is intended to insert images
            doc.insert_file(image_path)
        except Exception as e:
            print(f"Failed to insert file {image_path}: {e}")

    doc.save(pdf_path)
    doc.close()
    print(f"PDF created::${pdf_name_with_extension}")


def delete_download_folder(folder_path):
    shutil.rmtree(folder_path)


for x in range(start_chapter, end_chapter + 1):
    chapter_name = f"chapitre-{x}"
    manga_path = target_directory / manga_name

    if not os.path.exists(manga_path):
        os.makedirs(manga_path)

    chapter_path = manga_path / chapter_name
    if not os.path.exists(chapter_path):
        os.makedirs(chapter_path)

    if is_split_page_mode is True:
        download_split_pages_chapter(manga_name, x, chapter_path)
    else:
        download_one_page_chapter(manga_name, x, chapter_path)

    # list chapter images and sort them by ascending order
    chapter_pages_arr = os.listdir(chapter_path)
    chapter_pages_arr.sort(
        key=lambda x: (
            int("".join(filter(str.isdigit, x)))
            if "".join(filter(str.isdigit, x))
            else float("inf")
        )
    )
    merge_files_in_PDF(chapter_pages_arr, chapter_path, manga_path)

    # clean individual files
    delete_download_folder(chapter_path)

print("Task complete")
