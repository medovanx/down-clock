"""
Calculation manager for Down Clock
"""

from PyQt5.QtCore import Qt
from .calculations import calculateDownloadTime, formatDownloadTime


class CalculationManager:
    """Manager class for handling calculation functionality"""
    
    def __init__(self, size_input, size_combo, speed_input, speed_combo, result_label):
        """
        Initialize the calculation manager
        
        Args:
            size_input: The size input field widget
            size_combo: The size unit combo box widget
            speed_input: The speed input field widget
            speed_combo: The speed unit combo box widget
            result_label: The result label widget
        """
        self.size_input = size_input
        self.size_combo = size_combo
        self.speed_input = speed_input
        self.speed_combo = speed_combo
        self.result_label = result_label
    
    def calculate(self):
        """Calculate and display download time"""
        try:
            size = float(self.size_input.text())
            sizeUnit = self.size_combo.currentText()
            speed = float(self.speed_input.text())
            speedUnit = self.speed_combo.currentText()
        except ValueError:
            self._show_error("Please enter a valid value")
            return

        try:
            time = calculateDownloadTime(size, sizeUnit, speed, speedUnit)
            result_text = formatDownloadTime(time)
            self._show_result(result_text)
        except Exception as e:
            self._show_error(f"Calculation error: {str(e)}")
    
    def _show_result(self, result_text):
        """Show calculation result"""
        self.result_label.setTextFormat(Qt.RichText)
        self.result_label.setText(result_text)
    
    def _show_error(self, error_message):
        """Show error message"""
        self.result_label.setTextFormat(Qt.RichText)
        self.result_label.setText(
            f"<div style='text-align: center;'><span style='color: #f87171; font-size: 16px;'><b>❌ Error</b></span><br><span style='color: #f87171; font-size: 14px;'>{error_message}</span></div>")
    
    def validate_inputs(self):
        """Validate that all inputs have valid values"""
        try:
            size = float(self.size_input.text())
            speed = float(self.speed_input.text())
            return size > 0 and speed > 0
        except ValueError:
            return False
    
    def clear_result(self):
        """Clear the result display"""
        self.result_label.setText("Enter values and click Calculate to see download time...")
        self.result_label.setTextFormat(Qt.PlainText) 