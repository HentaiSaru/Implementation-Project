import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QLabel, QWidget
from PyQt6.QtGui import QFont
import matplotlib.pyplot as plt

class FileAnalyzerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Analyzer")
        self.button = QPushButton("Select Folder", self)
        self.button.clicked.connect(self.select_folder)
        self.setCentralWidget(self.button)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            file_types = self.get_file_types(folder_path)
            self.show_pie_chart(file_types)

    def get_file_types(self, folder_path):
        file_types = {}
        for dirpath, _, filenames in os.walk(folder_path):
            for filename in filenames:
                file_extension = os.path.splitext(filename)[1].lower()
                file_types[file_extension] = file_types.get(file_extension, 0) + 1
        return file_types

    def show_pie_chart(self, file_types):
        labels = list(file_types.keys())
        sizes = list(file_types.values())

        fig, ax = plt.subplots()
        pie = ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

        # 添加鼠标点击事件处理函数
        def on_click(event):
            if event.inaxes == ax:
                index = event.ind[0]
                selected_label = labels[index]
                print(f"Selected file type: {selected_label}")

        fig.canvas.mpl_connect("button_press_event", on_click)

        plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileAnalyzerWindow()
    window.show()
    sys.exit(app.exec())