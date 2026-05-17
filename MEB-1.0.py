import sys
import os
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget,
    QLineEdit, QPushButton, QSizePolicy, QToolBar
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile


# ======================
# PATHS
# ======================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_FILE = os.path.join(SCRIPT_DIR, "home-page.html")
HOME_URL = QUrl.fromLocalFile(HOME_FILE)

PROFILE_PATH = os.path.join(SCRIPT_DIR, "profile", "Default")


# ======================
# TAB
# ======================
# class BrowserTab(QWebEngineView):
#     def __init__(self, profile, parent=None):
#         super().__init__(parent)
#         self.setPage(profile.newPage())
from PyQt6.QtWebEngineCore import QWebEnginePage

class BrowserTab(QWebEngineView):
    def __init__(self, profile, parent=None):
        super().__init__(parent)
        page = QWebEnginePage(profile, self)
        self.setPage(page)



# ======================
# MAIN WINDOW
# ======================
class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MEB 1.0")
        self.setGeometry(100, 100, 1200, 800)

        # === PROFILE PERSISTENT (COOKIES)
        self.profile = QWebEngineProfile("BMB_Profile", self)
        self.profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies
        )
        self.profile.setCachePath(PROFILE_PATH)
        self.profile.setPersistentStoragePath(PROFILE_PATH)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        self.setup_toolbar()

        self.add_new_tab(HOME_URL, "Home")

    # ======================
    def setup_toolbar(self):
        back_btn = QPushButton("<")
        back_btn.clicked.connect(lambda: self.tabs.currentWidget().back())
        self.toolbar.addWidget(back_btn)

        forward_btn = QPushButton(">")
        forward_btn.clicked.connect(lambda: self.tabs.currentWidget().forward())
        self.toolbar.addWidget(forward_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate)
        self.url_bar.setSizePolicy(QSizePolicy.Policy.Expanding,
                                  QSizePolicy.Policy.Preferred)
        self.toolbar.addWidget(self.url_bar)

        go_btn = QPushButton("GO")
        go_btn.clicked.connect(self.navigate)
        self.toolbar.addWidget(go_btn)

        new_tab_btn = QPushButton("Tab +")
        new_tab_btn.clicked.connect(
            lambda: self.add_new_tab(HOME_URL, "New Tab")
        )
        self.toolbar.addWidget(new_tab_btn)

    # ======================
    def add_new_tab(self, url, title):
        browser = BrowserTab(self.profile)
        browser.setUrl(url)

        i = self.tabs.addTab(browser, title)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(
            lambda u, b=browser: self.update_url(u, b)
        )
        browser.titleChanged.connect(
            lambda t, i=i: self.tabs.setTabText(i, t)
        )

    def navigate(self):
        text = self.url_bar.text().strip()
        if not text:
            return
        if "://" not in text:
            text = "http://" + text
        self.tabs.currentWidget().setUrl(QUrl(text))

    def update_url(self, qurl, browser):
        if browser != self.tabs.currentWidget():
            return
        self.url_bar.setText(qurl.toString())

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)


# ======================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec())
