from PyQt5.QtCore import QThread, pyqtSignal, QObject


class WorkerThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, parent=None, method=None, *args, **kwargs):
        super().__init__(parent)
        self.method = method
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.method(*self.args, **self.kwargs)
            self.finished.emit(str(result))
        except Exception as e:
            print(f"Ошибка в потоке: {e}")
            self.error.emit(str(e))


class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        if text and text.strip():
            self.textWritten.emit(text.strip() + '\n')

    def flush(self):
        pass