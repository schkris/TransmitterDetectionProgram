from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton, QSlider, QTabWidget, QMainWindow, QVBoxLayout
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QEvent, QTimer
import sys
import os
from testGNU import testGNU  # Import testGNU class
import signal

# Suppress Qt-related warnings
sys.stderr = open(os.devnull, 'w')

class CustomButton(QPushButton):
    def __init__(self, label, parent=None):
        super().__init__(label, parent)
        # Enable touch events for the button
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)  # Adjusted for PyQt5
        button_font = QFont("Times New Roman", 13)
        super().setFont(button_font)
        
        super().setStyleSheet("""
            QPushButton {
                background-color: #932a40;     /* Background color */
                color: white;                  /* Text color */
                border: 2px solid #eb9758;     /* Border color and thickness */
                border-radius: 15px;           /* Border radius for rounded corners */
                padding: 8px 16px;             /* Padding */
            }
            QPushButton:hover {
                background-color: #bb7c94;
            }
            QPushButton:pressed {
                background-color: #b48c9a;
            }
        """)
        
        super().setFixedSize(200, 50)

    # Override the mousePressEvent for the button
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:  # Adjusted for PyQt5
            print(f'{self.text()} button clicked')
        super().mousePressEvent(event)

    # Override touchEvent to capture touchscreen interactions on the button
    def touchEvent(self, event):
        if event.type() == QEvent.TouchBegin or event.type() == QEvent.TouchEnd:
            print(f'{self.text()} button touched')
            return True  # Indicate that the touch event has been handled
        return super().touchEvent(event)

class Application(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Transmission Location System')
        self.setWindowIcon(QIcon('icon.ico'))
        
        # Open the window maximized
        self.showMaximized()
        
        #self.setGeometry(100, 100, 1600, 800)
        
        # Enable touch events for the main widget
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)  # Adjusted for PyQt5
        
        # Create main layout using QGridLayout
        self.main_layout = QGridLayout()
        
        # Load the image and set it in a QLabel
        #label_with_image = QLabel()
        #pixmap = QPixmap("icon.ico")  # Replace with the path to your image
        #label_with_image.setPixmap(pixmap)

        # Optionally, adjust the size of the QLabel to fit the image
        #label_with_image.setScaledContents(True)
        #label_with_image.setFixedSize(200, 200)  # Optional: Use the image size
        #label_with_image.setAlignment(Qt.AlignCenter) 
        # Add the QLabel with the image to the layout
        #self.main_layout.addWidget(label_with_image, 0, 0, 1, 2)
        
        # Create a label and place it in row 0, column 0, spanning 2 columns
        self.label = QLabel('F24-17 Design Project\n\nTransmission Location System', self)
        self.label.setAlignment(Qt.AlignCenter)  # Adjusted for PyQt5
        self.label.setStyleSheet("""
            QLabel {
                color: #932a40;                  /* Text color */
                /*border: 2px solid #eb9758;      Border color and thickness */
                /*border-radius: 10px;            Rounded corners */
                /*padding: 8px;                  Padding around the text */
                font-size: 30px;               /* Font size */
                font-weight: bold;             /* Font weight */
                text-align: center;            /* Center-align text */
                font-family: Times New Roman;
            }
        """)
        self.main_layout.addWidget(self.label, 1, 0, 1, 2)
        

        # Create a second label and place it in row 1, column 0, spanning 2 columns
        self.label2 = QLabel('Tap Anywhere to Continue', self)
        self.label2.setAlignment(Qt.AlignCenter)  # Adjusted for PyQt5
        self.label2.setStyleSheet("font-size: 15px;")
        self.main_layout.addWidget(self.label2, 3, 0, 1, 2)
        
        self.state = "home"

        # Set the main layout
        self.setLayout(self.main_layout)
    
    def changeEvent(self, event):
        # Check if the window state has changed
        if event.type() == QEvent.WindowStateChange:
            # If the window is now in "normal" mode, set it to a specific size
            if self.windowState() == Qt.WindowNoState:
                self.setGeometry(100, 100, 1600, 800)  # Adjust to your desired size

        # Call the parent changeEvent to ensure normal processing
        super().changeEvent(event)

    # Override the mousePressEvent to capture mouse clicks anywhere on the widget
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.state == "home":  # Adjusted for PyQt5
            print("Screen clicked")
            self.continue_clicked()

    # Override touchEvent to capture touchscreen interactions
    def touchEvent(self, event):
        if event.type() == QEvent.TouchBegin or event.type() == QEvent.TouchEnd:
            print("Screen touched")
            self.continue_clicked()
            return True  # Indicate that the touch event has been handled
        return super().touchEvent(event)

    def continue_clicked(self):
         # Clear the current layout and create a new frame
        self.clear_layout(self.main_layout)
    
        # Create buttons and place them in specific rows and columns
        self.guide_button = CustomButton('Guide', self)
        self.guide_button.clicked.connect(self.guide_clicked)
        self.main_layout.addWidget(self.guide_button, 0, 0, alignment=Qt.AlignRight)  # Adjusted for PyQt5
        

        self.freq_button = CustomButton('2.4GHz', self)
        self.freq_button.clicked.connect(self.freq_clicked)
        self.main_layout.addWidget(self.freq_button, 0, 2, alignment=Qt.AlignLeft)  # Adjusted for PyQt5
        
        
        self.state = "continue"

    def guide_clicked(self):
        self.clear_layout(self.main_layout)
        
        self.label = QLabel('Guide Section', self)
        self.label.setAlignment(Qt.AlignCenter)  # Adjusted for PyQt5
        self.label.setStyleSheet("font-size: 30px;")
        self.main_layout.addWidget(self.label, 0, 0, 1, 2)

        back_button = CustomButton('Back', self)
        back_button.clicked.connect(self.continue_clicked)
        self.main_layout.addWidget(back_button, 1, 1)
        
        self.state = "guide"

    def freq_clicked(self):
                # Clear the current layout and open the testGNU window
        self.clear_layout(self.main_layout)
        
        # Create a QTabWidget to hold multiple tabs
        tab_widget = QTabWidget()

        # Add the QTabWidget to a specific position in the grid layout
        self.main_layout.addWidget(tab_widget, 0, 0, 1, 2) 
        
        # Add the compass tab
        self.compass_tab = QWidget()
        self.setup_compass_tab()
        tab_widget.addTab(self.compass_tab, "Compass")

        # Add the debugging tab
        self.debugging_tab = QWidget()
        self.setup_debugging_tab()
        tab_widget.addTab(self.debugging_tab, "Debugging")

        # Additional widget example
        info_label = QLabel("Additional Information Panel")
        self.main_layout.addWidget(info_label, 1, 0)  # Placing in the grid below the tabs

        # Placeholder for another widget
        placeholder_label = QLabel("Status: Active")
        self.main_layout.addWidget(placeholder_label, 1, 1)  # Next to the additional information panel

        back_button = CustomButton('Back', self)
        back_button.clicked.connect(self.back_to_main)
        self.main_layout.addWidget(back_button, 2, 1)
        
        self.state = "frequency"
    
    def setup_compass_tab(self):
        # Layout for the compass tab
        layout = QGridLayout()
        
        # Add a label with directional information
        direction_label = QLabel("Direction: North")  # Replace with actual data
        layout.addWidget(direction_label, 0, 0)

        # Set the layout for the compass tab
        self.compass_tab.setLayout(layout)

    def setup_debugging_tab(self):
        # Layout for the debugging tab
        layout = QGridLayout()

        
        def set_slider_style(slider):
            slider.setStyleSheet("""
                QSlider {
                    margin: 25px;                /* Add margin around the slider */
                }
                QSlider::groove:vertical {
                    border: 1px solid #999;
                    width: 4px;
                    background: lightgray;
                    margin: 20px;  /* Margin inside the groove to act like padding */
                }
                QSlider::handle:vertical {
                    background: lightblue;
                    border: 1px solid #5c5c5c;
                    width: 30px;
                    height: 20px;
                    margin: -15px;  /* Negative margin to reduce handle padding */
                }
            """)
            
        self.sample_rate_label = QLabel('Sample Rate:', self)
        self.sample_rate_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.sample_rate_label, 0, 1, alignment = Qt.AlignTop)
        
        self.sample_rate_label2 = QLabel('5M', self)
        self.sample_rate_label2.setStyleSheet("font-size: 20px;")
        layout.addWidget(self.sample_rate_label2, 1, 1, alignment = Qt.AlignBottom)
        
        # Instantiate testGNU and show it as a secondary window
        self.gnu = testGNU()
        self.gnu.start()
        self.gnu.show()
        
        if not self.gnu.usb_found:
            label_no_usb = QLabel('No USB Found! Check Connections!', self)
            label_no_usb.setAlignment(Qt.AlignCenter)  # Adjusted for PyQt5
            label_no_usb.setStyleSheet("font-size: 30px; color: red;")
            layout.addWidget(label_no_usb, 1, 0)
        
        layout.addWidget(self.gnu, 2, 0)
        
        def sig_handler(sig=None, frame=None):
            self.gnu.stop()
            self.gnu.wait()
            
        signal.signal(signal.SIGINT, sig_handler)
        signal.signal(signal.SIGTERM, sig_handler)
        timer = QTimer()
        timer.start(500)
        timer.timeout.connect(lambda: None)

        # Create a slider for frequency adjustment
        sample_rate_slider = QSlider(Qt.Horizontal, self)
        sample_rate_slider.setRange(0, 100)  # Set proper range
        sample_rate_slider.setValue(50)  # Set the default value (midpoint)
        sample_rate_slider.setTickInterval(1000)
        sample_rate_slider.setFixedWidth(150)
        sample_rate_slider.setTickPosition(QSlider.TicksBelow)
        sample_rate_slider.valueChanged.connect(self.update_value1)
        set_slider_style(sample_rate_slider)
        #self.main_layout.addWidget(sample_rate_slider, 0, 0)        # Add the slider below the 2.4GHz button in row 1, column 1
        layout.addWidget(sample_rate_slider, 2, 1)

        # Set the layout for the debugging tab
        self.debugging_tab.setLayout(layout)
    
    def update_value1(self, value):
        if self.gnu.usb_found:
            self.gnu.set_samp_rate(value*(10**5))
        val = value / 10
        self.sample_rate_label2.setText(f'{val}M')
    
    def back_to_main(self):
        # Stop and clean up the GNU Radio process if it’s running
        if hasattr(self, 'gnu'):
            self.gnu.stop()
            self.gnu.wait()
            self.gnu.setParent(None)  # Detach from the layout

        # Clear the layout and switch to the main screen
        self.clear_layout(self.main_layout)
        self.continue_clicked()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

# Run the application
if __name__ == '__main__':
    app = QApplication([])
    ex = Application()
    ex.show()
    app.exec()
