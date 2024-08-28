# Let's create the markdown file for the user with proper formatting.

readme_content = """
# Podcast Processing Pipeline

![Logo](./logo.ico)

## Overview

This repository contains a set of Python scripts designed to automate the collection, management, and processing of podcast metadata and media files. It includes integration with APIs (e.g., Vimeo and Yumpu) and tools for managing metadata, creating Submission Information Packages (SIPs) for systems like Ex Libris Alma and Rosetta, and cleaning files.

## Features

- **Podcast Metadata Collection**: Automates downloading and storing podcast metadata and media files.
- **SIP Creation**: Create Submission Information Packages (SIPs) for Ex Libris Alma and Rosetta.
- **API Integration**: Integrate with external services like Vimeo and Yumpu for automatic media download and metadata collection.
- **Error Handling**: Gracefully skips files with errors during metadata extraction and handles API errors.
- **File Cleaning**: Automatically clean and organize files.
- **Metadata Extraction**: Extracts and saves metadata and comments related to media files.

## Files

1. **`podcasts.py`**: The main script for processing podcasts, downloading metadata, and integrating with APIs.
2. **`podcasts_database_handler.py`**: Manages database operations related to podcast metadata.
3. **`yumpu_tool.py`**: Handles media downloads and processing from Yumpu.
4. **`description_maker.py`**: Extracts descriptions from media files and generates associated metadata.
5. **`api_file.txt`**: Configuration file that stores API keys and output paths.

## Prerequisites

- Python 3.10+
- Required Python libraries are listed in `requirements.txt`.

To install dependencies, run:

```
pip install -r requirements.txt
```

```
git clone https://github.com/nlnzcollservices/Yumpu-tool
cd Yumpu-tool
```
```
name = "Your Name"
apikey = "your_api_key"
out_folder = "path/to/output/folder"
sip_out_folder = "path/to/sip/output/folder"
```
```
python yumpu_tool.py
```




