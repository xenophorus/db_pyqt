import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication, QTabWidget, QStyle, QVBoxLayout, QMainWindow
from PyQt5.QtCore import QDate


class ServerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()
        self.tab0 = QTabWidget()
        self.tab1 = QTabWidget()
        self.tab2 = QTabWidget()

        self.tabs.addTab(self.tab0, 'Client list')
        self.tabs.addTab(self.tab1, 'Client stats')
        self.tabs.addTab(self.tab2, 'Server options')

        self.tab0.layout = QGridLayout()

        self.tab1.layout = QGridLayout()

        self.tab2.layout = QGridLayout()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.statusBar().showMessage(f'Status bar message')

        self.server_win()

    def server_win(self):
        self.setWindowTitle('Server UI')

        # TODO a. отображение списка всех клиентов;
        # TODO b. отображение статистики клиентов;
        # TODO c.настройка сервера (подключение к БД, идентификация).


def main():
    app = QApplication(sys.argv)
    s_app = ServerWindow()
    # TODO: Вынести переменные в ini и обернуть в try/except
    scr_width, scr_height = app.desktop().screenGeometry().width(), app.desktop().screenGeometry().height()
    win_width, win_height = 800, 600
    s_app.setGeometry(int((scr_width - win_width) / 2), int((scr_height - win_height) / 2), win_width, win_height)

    s_app.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
