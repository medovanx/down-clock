"""
Speed test utilities for Down Clock
"""

from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt
import speedtest


class SpeedTestThread(QThread):
    """Thread for running speed test in background"""
    finished = pyqtSignal(float)  # Emits the download speed
    error = pyqtSignal(str)  # Emits error message

    def run(self):
        """Run the speed test"""
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download_speed = st.download() / 10**6
            self.finished.emit(download_speed)
        except Exception as e:
            self.error.emit(f"Speed test error: {str(e)}")


class SpeedTestManager:
    """Manager class for handling speed test functionality"""

    def __init__(self, button, result_label, speed_input, speed_combo):
        """
        Initialize the speed test manager

        Args:
            button: The speed test button widget
            result_label: The result label widget
            speed_input: The speed input field widget
            speed_combo: The speed unit combo box widget
        """
        self.button = button
        self.result_label = result_label
        self.speed_input = speed_input
        self.speed_combo = speed_combo

        # Initialize thread and spinner
        self.speed_test_thread = None
        self.spinner_timer = None
        # Try Unicode spinner first, fallback to simple dots
        try:
            self.spinner_frames = ["⠋", "⠙", "⠹",
                                   "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            # Test if Unicode characters display properly
            test_char = self.spinner_frames[0]
            if not test_char or len(test_char) == 0:
                raise ValueError("Unicode spinner not supported")
        except:
            # Fallback to simple spinner
            self.spinner_frames = ["|", "/", "-", "\\"]

        self.spinner_index = 0
        self.original_style = None

    def start_test(self):
        """Start the speed test"""
        # If thread is already running, don't start another one
        if self.speed_test_thread and self.speed_test_thread.isRunning():
            return

        # Start spinner animation
        self._start_spinner()

        # Create and start the speed test thread
        self.speed_test_thread = SpeedTestThread()
        self.speed_test_thread.finished.connect(self._on_finished)
        self.speed_test_thread.error.connect(self._on_error)
        self.speed_test_thread.start()

    def _start_spinner(self):
        """Start the spinner animation on the speed test button"""
        # Store original style before changing it
        self.original_style = self.button.styleSheet()

        self.button.setEnabled(False)
        self.spinner_index = 0
        self.button.setText(f"{self.spinner_frames[0]} Testing...")
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #3a8a9a;
                color: #ffffff;
                border: 2px solid #257684;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a9aaa;
            }
            QPushButton:pressed {
                background-color: #2a5a6a;
            }
        """)

        # Start spinner timer
        self.spinner_timer = QTimer()
        self.spinner_timer.timeout.connect(self._update_spinner)
        # Update every 100ms for smoother animation
        self.spinner_timer.start(100)

    def _update_spinner(self):
        """Update the spinner animation"""
        self.spinner_index = (self.spinner_index +
                              1) % len(self.spinner_frames)
        spinner_char = self.spinner_frames[self.spinner_index]
        self.button.setText(f"{spinner_char} Testing Speed...")

    def _stop_spinner(self):
        """Stop the spinner animation and restore button"""
        if self.spinner_timer:
            self.spinner_timer.stop()
            self.spinner_timer = None

        self.button.setEnabled(True)
        self.button.setText("Speed Test")
        # Restore original button style
        if self.original_style is not None:
            self.button.setStyleSheet(self.original_style)
        else:
            # Fallback to empty style if original wasn't stored
            self.button.setStyleSheet("")

    def _on_finished(self, download_speed):
        """Handle successful speed test completion"""
        self.speed_input.setText(str(download_speed))
        # Set the combo box to MBit/s (index 4)
        self.speed_combo.setCurrentIndex(4)
        self._show_success("Completed successfully!")
        self._stop_spinner()

    def _on_error(self, error_message):
        """Handle speed test error"""
        self._show_error(error_message)
        self._stop_spinner()

    def _show_success(self, message):
        """Show success message"""
        self.result_label.setTextFormat(Qt.RichText)
        self.result_label.setText(
            f"<div style='text-align: center;'><span style='color: #4ade80; font-size: 16px;'><b>✅ Speed Test</b></span><br><span style='color: #4ade80; font-size: 14px;'>{message}</span></div>")

    def _show_error(self, error_message):
        """Show error message"""
        self.result_label.setTextFormat(Qt.RichText)
        self.result_label.setText(
            f"<div style='text-align: center;'><span style='color: #f87171; font-size: 16px;'><b>❌ Speed Test Error</b></span><br><span style='color: #f87171; font-size: 14px;'>{error_message}</span></div>")

    def cleanup(self):
        """Cleanup resources when closing"""
        # Stop spinner timer
        if self.spinner_timer:
            self.spinner_timer.stop()

        # Stop speed test thread
        if self.speed_test_thread and self.speed_test_thread.isRunning():
            self.speed_test_thread.quit()
            self.speed_test_thread.wait(1000)  # Wait up to 1 second
