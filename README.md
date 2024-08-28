
# Yumpu Tool

Yumpu Tool is a Python-based tool designed to interact with the Yumpu API to download images from Yumpu links and create SIPs (Submission Information Packages) from the downloaded content. It integrates with Alma for managing bibliographic records, holding records, and items, providing an easy-to-use interface for digital librarians and archivists.

## Features
- **Download Yumpu Images**: Fetches images from a given Yumpu link and downloads them.
- **Create Alma Records**: Supports the creation of Alma bibliographic records, holdings, and items.
- **SIP Creation**: Generates SIPs from bibliographic information, suitable for long-term preservation.
- **PySimpleGUI Interface**: An interactive GUI for inputting Yumpu and Alma details.
- **Custom Themes**: Users can switch between different themes for the GUI.

## Prerequisites
- Python 3.x
- `requests` library
- `wget` library
- `PySimpleGUI`
- `filetype`
- `PIL`
- Alma API keys
- Yumpu link to download content

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/yumpu-tool.git
cd yumpu-tool
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the `api_file.txt` with your Alma and Yumpu API keys:

```txt
name = "Your Name"
apikey = "Your Alma API Key"
out_folder = "Path to output folder"
sip_out_folder = "Path to SIP output folder"
themes = ["LightBlue2", "LightGrey2", "GrayGrayGray", "Default1"]
```

## Usage

1. Run the tool:

```bash
python yumpu_tool.py
```

2. A PySimpleGUI window will pop up. Fill in the required Yumpu and Alma details:
   - **MMS ID**: Alma bib record identifier.
   - **PO Line**: Alma Purchase Order Line.
   - **Yumpu URL**: Link to the Yumpu document to download.
   - **Output Folder**: Path where downloaded images and SIPs will be stored.
   - **API Key**: Your Alma API key.

3. Click "Run!" to start the process.

## API Integration

The tool integrates with Alma APIs to perform the following operations:
- Fetch item records by MMS ID and holding ID.
- Update item descriptions automatically.
- Create new Alma item records by PO line.

For more details on Alma APIs, visit the [Ex Libris Developer Network](https://developers.exlibrisgroup.com/alma/apis/).

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
