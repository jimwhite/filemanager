from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QLineEdit, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from ui.database import Database
from ui.utils import compute_md5sum

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Manager")
        self.setGeometry(100, 100, 800, 600)

        self.db = Database()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.path_label = QLabel("Path:")
        self.layout.addWidget(self.path_label)

        self.path_input = QLineEdit()
        self.layout.addWidget(self.path_input)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse)
        self.layout.addWidget(self.browse_button)

        self.md5sum_label = QLabel("MD5sum:")
        self.layout.addWidget(self.md5sum_label)

        self.md5sum_output = QTextEdit()
        self.md5sum_output.setReadOnly(True)
        self.layout.addWidget(self.md5sum_output)

        self.compute_button = QPushButton("Compute MD5sum")
        self.compute_button.clicked.connect(self.compute_md5sum)
        self.layout.addWidget(self.compute_button)

        self.save_button = QPushButton("Save to Database")
        self.save_button.clicked.connect(self.save_to_db)
        self.layout.addWidget(self.save_button)

        self.search_button = QPushButton("Search in Database")
        self.search_button.clicked.connect(self.search_in_db)
        self.layout.addWidget(self.search_button)

        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.layout.addWidget(self.result_output)

    def browse(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            self.path_input.setText(file_path)

    def compute_md5sum(self):
        file_path = self.path_input.text()
        if not file_path:
            QMessageBox.warning(self, "Warning", "Please select a file.")
            return

        md5sum = compute_md5sum(file_path)
        self.md5sum_output.setText(md5sum)

    def save_to_db(self):
        file_path = self.path_input.text()
        md5sum = self.md5sum_output.toPlainText()
        if not file_path or not md5sum:
            QMessageBox.warning(self, "Warning", "Please compute the MD5sum first.")
            return

        self.db.insert_file(file_path, md5sum)
        QMessageBox.information(self, "Success", "File path and MD5sum saved to database.")

    def search_in_db(self):
        file_path = self.path_input.text()
        if not file_path:
            QMessageBox.warning(self, "Warning", "Please enter a file path.")
            return

        result = self.db.query_file(file_path)
        if result:
            self.result_output.setText(f"MD5sum: {result[0]}")
        else:
            self.result_output.setText("File not found in database.")
