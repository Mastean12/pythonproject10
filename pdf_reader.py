import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PyPDF2 import PdfReader
from nltk import sent_tokenize
import pyttsx3

from PyQt5.QtWidgets import QTextEdit

class PDFReaderApp(QMainWindow):
    def __init__(self, pdf_path):
        super().__init__()

        self.pdf_path = pdf_path
        self.sentences = self.read_pdf()
        self.current_sentence_index = 0

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Reader with Cursor')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QTextEdit(self)
        self.central_widget.setAlignment(Qt.AlignTop)
        self.central_widget.setFont(QFont("Arial", 12))
        self.central_widget.setReadOnly(True)

        self.cursor_position = 0

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.show_sentence()

    def show_sentence(self):
        if self.current_sentence_index < len(self.sentences):
            current_sentence = self.sentences[self.current_sentence_index]
            self.central_widget.setText(current_sentence)
            self.speak_sentence(current_sentence)
            self.move_cursor()
            self.current_sentence_index += 1
        else:
            self.central_widget.setText("End of Document")

    def speak_sentence(self, sentence):
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)  # Adjust the speed as needed
        engine.say(sentence)
        engine.runAndWait()

    def move_cursor(self):
        cursor = self.central_widget.textCursor()
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        self.central_widget.setTextCursor(cursor)

    def read_pdf(self):
        with open(self.pdf_path, "rb") as file:
            pdf_reader = PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        return sent_tokenize(text)




def main():
    app = QApplication(sys.argv)
    pdf_app = PDFReaderApp("C:/Users/USER/OneDrive/Documents/Ezekiel.pdf")  # Replace with the actual path to your PDF file
    pdf_app.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
