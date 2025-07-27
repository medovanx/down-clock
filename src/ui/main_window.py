"""
Main window for Down Clock
"""

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtGui, uic
from PyQt5.QtCore import Qt

from ..utils.helpers import resource_path, VERSION
from ..utils.speed_test import SpeedTestManager
from ..utils.calculation_manager import CalculationManager


class DownClock(QMainWindow):
    """Main window class for the Down Clock application"""
    
    def __init__(self):
        super().__init__()
        
        # Load the UI file dynamically
        self.ui = uic.loadUi(resource_path("src/ui/mainwindow.ui"), self)
        
        # Set window icon
        self.setWindowIcon(QtGui.QIcon(resource_path("src/resources/app_icon.png")))
        
        # Initialize managers
        self.speed_test_manager = SpeedTestManager(
            self.testSpeedButton, 
            self.Result, 
            self.speedLabelInput, 
            self.speedUnitCombo
        )
        
        self.calculation_manager = CalculationManager(
            self.sizeLabelInput,
            self.sizeUnitCombo,
            self.speedLabelInput,
            self.speedUnitCombo,
            self.Result
        )
        
        # Connect signals
        self.CalculateButton.clicked.connect(self.calculation_manager.calculate)
        self.testSpeedButton.clicked.connect(self.speed_test_manager.start_test)
        self.actionAbout.triggered.connect(self.showAbout)
        
        # Set default values for combo boxes
        self.sizeUnitCombo.setCurrentIndex(2)  # MB (most common)
        self.speedUnitCombo.setCurrentIndex(4)  # MBit/s (most common)



    def showAbout(self):
        """Show about dialog"""
        from PyQt5.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setWindowTitle("About Down Clock")
        msg.setWindowIcon(QtGui.QIcon(resource_path("src/resources/app_icon.png")))
        msg.setIconPixmap(QtGui.QPixmap(resource_path("src/resources/app_icon.png")).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        msg.setTextFormat(Qt.RichText)
        msg.setText(
            f"<h3>Down Clock v{VERSION}</h3>"
            "<p>A simple tool to calculate download times based on file size and internet speed.</p>"
            "<p><b>© 2024 Mohamed Darwesh</b><br>"
            "GitHub: <a href='https://github.com/medovanx'>@medovanx</a></p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>Calculate download times for various file sizes</li>"
            "<li>Support for multiple units (B, KB, MB, GB, TB)</li>"
            "<li>Internet speed testing (requires speedtest-cli)</li>"
            "</ul>"
        )
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    
    def closeEvent(self, event):
        """Handle window close event - cleanup resources"""
        # Cleanup speed test manager
        if hasattr(self, 'speed_test_manager'):
            self.speed_test_manager.cleanup()
        
        event.accept()