# Prerequisites

- Install Python3
- Install pipenv
  ```shell
  brew install pipenv
  ```

# Installation

- Create a `.env` file from `.env.example` and fill listed variables.
- In the project run pipenv to install dependencies:
  ```shell
  pipenv install
  ```
- Launch python virtuel environment:
  ```shell
  pipenv shell
  ```
- Execute the script with necessary arguments: target manga, start chapter and end chapter.
  For example:
  ```shell
  python3 ./scan-downloader.py jujutsu-kaisen 200 205
  ```
- And you're done ! Go the `generated/` directory to get your PDF files.
