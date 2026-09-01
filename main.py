import sys
from pathlib import Path

from audio_extractor import extract_audio
from PySide6.QtCore import (
    QObject,
    QStandardPaths,
    QThread,
    QTimer,
    QUrl,
    Signal,
)
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ExtractionWorker(QObject):
    finished = Signal(str)
    error = Signal(str)
    progress = Signal(int)
    status = Signal(str)

    def __init__(
        self,
        url: str,
        audio_format: str,
        output_folder: str,
    ) -> None:
        super().__init__()

        self.url = url
        self.audio_format = audio_format
        self.output_folder = output_folder

    def run(self) -> None:
        try:
            output_file = extract_audio(
                url=self.url,
                audio_format=self.audio_format,
                output_folder=self.output_folder,
                progress_callback=self.progress.emit,
                status_callback=self.status.emit,
            )
        except Exception as error:
            self.error.emit(str(error))
            return

        self.finished.emit(str(output_file))


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.thread: QThread | None = None
        self.worker: ExtractionWorker | None = None
        self.last_output_file: str | None = None

        self.conversion_dots = 0
        self.conversion_timer = QTimer(self)
        self.conversion_timer.setInterval(400)
        self.conversion_timer.timeout.connect(
            self.update_conversion_animation
        )

        self.setWindowTitle("Audio Extractor")
        self.setMinimumWidth(560)

        self.output_folder = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DownloadLocation
        )

        # Video URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText(
            "Paste a YouTube, TikTok or Instagram URL"
        )

        # Audio format
        self.format_combo = QComboBox()
        self.format_combo.addItems(
            [
                "MP3",
                "M4A",
                "WAV",
            ]
        )

        # Output folder
        self.folder_input = QLineEdit(
            self.output_folder
        )
        self.folder_input.setReadOnly(True)

        choose_folder_button = QPushButton(
            "Choose Folder…"
        )
        choose_folder_button.clicked.connect(
            self.choose_folder
        )

        folder_layout = QHBoxLayout()
        folder_layout.addWidget(
            self.folder_input
        )
        folder_layout.addWidget(
            choose_folder_button
        )

        # Extract button
        self.extract_button = QPushButton(
            "Extract Audio"
        )
        self.extract_button.clicked.connect(
            self.extract
        )

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(
            0,
            100,
        )
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)

        # Status
        self.status_label = QLabel("Ready")

        # Open folder button
        self.open_folder_button = QPushButton(
            "Open Folder"
        )
        self.open_folder_button.setEnabled(False)
        self.open_folder_button.clicked.connect(
            self.open_output_folder
        )

        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(12)

        layout.addWidget(
            QLabel("Video URL")
        )
        layout.addWidget(
            self.url_input
        )

        layout.addWidget(
            QLabel("Audio Format")
        )
        layout.addWidget(
            self.format_combo
        )

        layout.addWidget(
            QLabel("Save to")
        )
        layout.addLayout(
            folder_layout
        )

        layout.addSpacing(8)

        layout.addWidget(
            self.extract_button
        )
        layout.addWidget(
            self.progress_bar
        )
        layout.addWidget(
            self.status_label
        )
        layout.addWidget(
            self.open_folder_button
        )

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def choose_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self,
            "Choose Output Folder",
            self.output_folder,
        )

        if not folder:
            return

        self.output_folder = folder
        self.folder_input.setText(folder)

    def extract(self) -> None:
        self.open_folder_button.setEnabled(False)
        self.last_output_file = None

        self.conversion_timer.stop()
        self.conversion_dots = 0

        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        url = self.url_input.text().strip()

        if not url:
            self.status_label.setText(
                "Please enter a video URL."
            )
            return

        audio_format = (
            self.format_combo
            .currentText()
            .lower()
        )

        self.status_label.setText(
            "Preparing…"
        )

        self.extract_button.setEnabled(False)

        self.thread = QThread()

        self.worker = ExtractionWorker(
            url=url,
            audio_format=audio_format,
            output_folder=self.output_folder,
        )

        self.worker.moveToThread(
            self.thread
        )

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.progress.connect(
            self.progress_bar.setValue
        )

        self.worker.status.connect(
            self.update_extraction_status
        )

        self.worker.finished.connect(
            self.extraction_finished
        )

        self.worker.error.connect(
            self.extraction_failed
        )

        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.error.connect(
            self.thread.quit
        )

        self.worker.finished.connect(
            self.worker.deleteLater
        )

        self.worker.error.connect(
            self.worker.deleteLater
        )

        self.thread.finished.connect(
            self.thread_finished
        )

        self.thread.finished.connect(
            self.thread.deleteLater
        )

        self.thread.start()

    def update_extraction_status(
        self,
        status: str,
    ) -> None:
        if status == "downloading":
            self.conversion_timer.stop()

            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 100)

            self.status_label.setText(
                "Downloading…"
            )

        elif status == "converting":
            self.progress_bar.setVisible(False)

            self.conversion_dots = 0
            self.status_label.setText(
                "Converting."
            )

            self.conversion_timer.start()

    def update_conversion_animation(
        self,
    ) -> None:
        self.conversion_dots = (
            self.conversion_dots % 3
        ) + 1

        dots = "." * self.conversion_dots

        self.status_label.setText(
            f"Converting{dots}"
        )

    def extraction_finished(
        self,
        output_file: str,
    ) -> None:
        self.conversion_timer.stop()

        self.last_output_file = output_file

        file_name = Path(
            output_file
        ).name

        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)

        self.status_label.setText(
            f"✓ Saved as: {file_name}"
        )

        self.extract_button.setEnabled(True)
        self.open_folder_button.setEnabled(True)

    def extraction_failed(
        self,
        message: str,
    ) -> None:
        self.conversion_timer.stop()

        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        self.status_label.setText(
            f"Error: {message}"
        )

        self.extract_button.setEnabled(True)

    def thread_finished(self) -> None:
        self.worker = None
        self.thread = None

    def open_output_folder(self) -> None:
        if not self.last_output_file:
            return

        folder = Path(
            self.last_output_file
        ).parent

        QDesktopServices.openUrl(
            QUrl.fromLocalFile(
                str(folder)
            )
        )


def main() -> None:
    app = QApplication(
        sys.argv
    )

    window = MainWindow()
    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()
