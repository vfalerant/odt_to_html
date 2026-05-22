from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QHBoxLayout
)

from converter.odt_reader import read_odt_blocks
from converter.html_generator import generate_html


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ODT → HTML Converter")
        self.resize(1400, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        self.load_button = QPushButton("ODT fájl betöltése")
        self.load_button.clicked.connect(self.load_odt)

        main_layout.addWidget(self.load_button)

        content_layout = QHBoxLayout()

        # LEFT DEBUG PANEL
        self.source_edit = QTextEdit()
        self.source_edit.setReadOnly(True)

        content_layout.addWidget(self.source_edit)

        # RIGHT
        right_layout = QVBoxLayout()

        self.html_edit = QTextEdit()

        self.preview_edit = QTextEdit()
        self.preview_edit.setReadOnly(True)

        right_layout.addWidget(self.html_edit)
        right_layout.addWidget(self.preview_edit)

        content_layout.addLayout(right_layout)

        main_layout.addLayout(content_layout)

        central_widget.setLayout(main_layout)

        self.html_edit.textChanged.connect(
            self.update_preview
        )

    def load_odt(self):

        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "ODT fájl kiválasztása",
            "",
            "ODT Files (*.odt)"
        )

        if not filepath:
            return

        blocks = read_odt_blocks(filepath)

        # DEBUG VIEW
        self.source_edit.clear()

        for b in blocks:
            self.source_edit.append(
                f"[{b['type']}] {b['text']}"
            )

        # HTML
        html = generate_html(blocks)

        self.html_edit.setPlainText(html)

        self.preview_edit.setHtml(html)

    def update_preview(self):

        html = self.html_edit.toPlainText()

        self.preview_edit.setHtml(html)