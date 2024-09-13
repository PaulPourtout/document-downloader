## Document Downloader

**Requirements:**

- Python 3
- pipenv

**Installation:**

1. Clone or download this repository.
2. Install the required libraries using `pipenv`:

```bash
pipenv install
```

**Usage:**

1. Create a `.env` file in the same directory as the script. Add the following line, replacing `<target_url>` with the base URL of the site containing the documents you want to target:

```
SITE_TARGET=<target_url>
```

**Optional:**

- Set `SPLIT_PAGE="True"` in the `.env` file if the manga chapters are displayed on a single page. Defaults to `False`.

2. Run the script with the following arguments:

```bash
pipenv run python script_name.py <manga_name> <start_chapter> <end_chapter>
```

**Example:**

```bash
pipenv run python script_name.py One_Piece 1000 1005
```

This will download chapters 1000 to 1005 of the "One Piece" manga and create separate PDF files for each chapter in a dedicated folder.

**Notes:**

- Downloading copyrighted content without permission may be illegal. Use this script responsibly.
- The script assumes chapter numbers are sequential integers.
- The script currently only works with LeLScans.net.
- This script is for educational purposes only.

**Additional Information:**

- This script utilizes various libraries to handle network requests, file manipulation, image processing, and PDF generation.
- The script handles different chapter layouts: one-page chapters and split-page chapters.
- Downloaded chapter images are cleaned up after successful PDF creation.

**Disclaimer:**

The authors are not responsible for any misuse of this script. Please use this script ethically and legally.
