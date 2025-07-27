# Down Clock

A PyQt5 desktop application to calculate download times based on file size and internet speed.

![Down Clock Logo](https://i.ibb.co/RTYT6b0g/ico.png){width=200}

## Screenshot
<div style="display: flex; justify-content: space-between;">
    <img src="https://i.ibb.co/vCvKxHPj/image.png" alt="Down Clock Screenshot 1" width="48%">
    <img src="https://i.ibb.co/V0GGGkVv/image.png" alt="Down Clock Screenshot 2" width="48%">
</div>

## Features

- Calculate download times for various file sizes (B, KB, MB, GB, TB)
- Support for multiple speed units (Bit/s, KBit/s, MBit/s, GBit/s, B/s, KB/s, MB/s)
- Built-in internet speed test functionality
- Modern and intuitive user interface

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/medovanx/down-clock.git
cd down-clock
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python main.py
```

## Usage

1. Enter the file size you want to download
2. Select the appropriate size unit (B, KB, MB, GB, TB)
3. Enter your download speed
4. Select the speed unit (Bit/s, KBit/s, MBit/s, GBit/s, B/s, KB/s, MB/s)
5. Click "Speed Test" to automatically measure your internet speed (optional)
6. Click "Calculate" to see the estimated download time

## Building Executable

Install PyInstaller and build the executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=src/resources/app_icon.png --add-data "src/ui/mainwindow.ui;src/ui" --add-data "src/resources/app_icon.png;src/resources" --name="Down Clock" main.py
```

The executable will be created in the `dist/` folder.

**Note**: The `--add-data` flags are required to include the UI file and icon resources in the bundled executable.

## License

This project is licensed under the MIT License.

## Author

**Mohamed Darwesh** - [@medovanx](https://github.com/medovanx)



