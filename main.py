"""
Down Clock - Main Entry Point

A PyQt5 application to calculate download times based on file size and internet speed.
"""

import sys
from PyQt5.QtWidgets import QApplication

def main():
    """Main function to run the application"""
    try:
        app = QApplication(sys.argv)
        
        # Import here to catch import errors
        from src.ui.main_window import DownClock
        
        # Create and show the main window
        window = DownClock()
        
        # Make sure window is visible and on top
        window.show()
        window.raise_()
        window.activateWindow()
        
        # Start the application event loop
        return app.exec_()
        
    except ImportError as e:
        print(f"Import Error: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    main() 