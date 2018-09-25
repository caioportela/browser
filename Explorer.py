from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *

import sys

class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.setWindowTitle("Explorer")
		self.setWindowIcon(QIcon('icons/browser_icon.png'))

		self.browser = QWebEngineView()
		self.browser.setUrl(QUrl('http://www.google.com'))

		self.setCentralWidget(self.browser)

		navtb = QToolBar("Navigation")
		self.addToolBar(navtb)


		back_btn = QAction(QIcon('icons/arrow-180.png'), "Back", self)
		back_btn.setStatusTip("Back to previous page")
		back_btn.triggered.connect(self.browser.back)
		navtb.addAction(back_btn)

		next_btn = QAction(QIcon('icons/arrow.png'), "Next", self)
		next_btn.setStatusTip("Go to next page")
		next_btn.triggered.connect(self.browser.forward)
		navtb.addAction(next_btn)

		reload_btn = QAction(QIcon('icons/arrow-circle-315.png'), "Reload", self)
		reload_btn.setStatusTip("Reload")
		reload_btn.triggered.connect(self.browser.reload)
		navtb.addAction(reload_btn)

		stop_btn = QAction(QIcon('icons/cross.png'), "Stop", self)
		stop_btn.setStatusTip("Stop loading current page")
		stop_btn.triggered.connect(self.browser.stop)
		navtb.addAction(stop_btn)
		
		navtb.addSeparator()

		self.httpsicon = QLabel()
		navtb.addWidget(self.httpsicon)

		self.urlbar = QLineEdit()
		self.urlbar.returnPressed.connect(self.go_to_url)
		navtb.addWidget(self.urlbar)

		self.browser.urlChanged.connect(self.update_urlbar)

		home_btn = QAction(QIcon('icons/home.png'), "Home", self)
		home_btn.setStatusTip("Go to home page")
		home_btn.triggered.connect(self.nav_home)
		navtb.addAction(home_btn)

		file_menu = self.menuBar().addMenu("&File")

		open_action = QAction(QIcon('icons/blue-folder-open.png'), "Open File", self)
		open_action.setStatusTip("Open from file")
		open_action.triggered.connect(self.open_file)
		file_menu.addAction(open_action)

		save_action = QAction(QIcon('icons/disk-return.png'), "Save Page As...", self)
		save_action.setStatusTip("Save current page")
		save_action.triggered.connect(self.save_file)
		file_menu.addAction(save_action)

		print_action = QAction(QIcon('icons/printer.png'), "Print...", self)
		print_action.setStatusTip("Print current page")
		print_action.triggered.connect(self.print_page)
		file_menu.addAction(print_action) 

	def update_urlbar(self, url_addres):
		if url_addres.scheme() == 'https':
			self.httpsicon.setPixmap(QPixmap('icons/lock-ssl.png'))

		self.urlbar.setText(url_addres.toString())
		self.urlbar.setCursorPosition(0)

	def go_to_url(self):
		link = QUrl(self.urlbar.text())
		
		if link.scheme() == "":
			link.setScheme("http")

		self.browser.setUrl(link)
	
	def nav_home(self):
		self.browser.setUrl(QUrl('http://www.google.com'))

	def print_page(self):
		dlg = QPrintPreviewDialog()
		dlg.exec_()

	def open_file(self):
		filename, _ = QFileDialog.getOpenFileName(self, "Open file", "", 
						"Hypertext Markup Language (*.htm *.html);;"
						"All files (*.*)")

		if filename:
			with open(filename, 'r') as f:
				html = f.read()

			self.urlbar.setText(filename)
			self.browser.setHtml(html)

	def save_file(self):
		filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "",
						"Hypertext Markup Language (*.htm *.html);;"
						"All files (*.*)")

		if filename:
			self.browser.page().save(filename, format=1)

app = QApplication(sys.argv)
app.setApplicationName("Browser")
app.setOrganizationName("Browser")
app.setOrganizationDomain("google.com")

window = MainWindow()
window.show()
app.exec_()