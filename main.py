#!/usr/bin/env python
#coding:utf-8
import sys,time
from ctypes import * 
import win32api, win32con  
User32dll = windll.User32
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
class POINT(Structure):  
	_fields_ = [  
	("x", c_ulong),  
	("y", c_ulong)  
	]
class Picking(QThread):
	trigger = pyqtSignal()
	def __init__(self,parent=None):
		super(Picking,self).__init__(parent)
	def run(self):
		global point
		User32dll.GetCursorPos(byref(point))
		self.trigger.emit()
class Calc(QThread):
	trigger = pyqtSignal()
	def __init__(self,parent=None):
		super(Calc,self).__init__(parent)
	def run(self):
		global point,pix,rgb,image
		img=image.copy(point.x-25,point.y-25,50,50)
		rgb = img.pixel(25, 25)
		img.setPixel(24,25,0xFF6D9EEB)
		img.setPixel(23,25,0xFF6D9EEB)
		img.setPixel(25,24,0xFF6D9EEB)
		img.setPixel(25,23,0xFF6D9EEB)
		img.setPixel(25,26,0xFF6D9EEB)
		img.setPixel(25,27,0xFF6D9EEB)
		img.setPixel(26,25,0xFF6D9EEB)
		img.setPixel(27,25,0xFF6D9EEB)
		img=img.scaled(img.width()*4,img.height()*4,Qt.KeepAspectRatio)
		pix=QPixmap.fromImage(img)
		self.trigger.emit()
class Pick_UI(QWidget):
	trigger = pyqtSignal()
	def __init__(self,parent=None):
		super(Pick_UI,self).__init__(parent)
		global point,point1,pix,image
		iColor_browser_qss_file=open("data/UI/style_sheets/QTextBrowser_rgb.txt","r")
		iColor_browser_qss=iColor_browser_qss_file.read()
		iColor_browser_qss_file.close()
		self.specail="█".decode("utf8")
		image = QPixmap.grabWindow(QApplication.desktop().winId()).toImage()
		point = POINT()
		point1=POINT()
		self.pick_thread=Picking()
		self.calc_thread=Calc()
		self.browser = QTextBrowser()
		self.browser.setStyleSheet(iColor_browser_qss)
		self.browser.setParent(self)
		self.setAttribute(Qt.WA_TranslucentBackground)		
		self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow)
		self.resize(200,200)
		self.setMouseTracking(True)
		User32dll.GetCursorPos(byref(point))
		self.move(point.x-100,point.y-100)
		pix=QPixmap("data/UI/images/pick_bg.png")
		self.setCursor(Qt.BlankCursor)
		self.pick_thread.trigger.connect(self.repos)
		self.calc_thread.trigger.connect(self.show_index)		
	def paintEvent(self,event):
		global pix
		path=QPainterPath()
		painter=QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing, True)
		path.addRoundRect(6, 6, self.width()-12, self.height()-12, 100)
		painter.fillPath(path, QBrush(pix))
		alpha=[120,75,45,25,15,10]
		color=QColor(50, 50, 50, 255)
		for i in range(0,6):
			path=QPainterPath()
			path.addRoundRect(6-i, 6-i, self.width()-(6-i)*2, self.height()-(6-i)*2, 100)
			color.setAlpha(alpha[i])
			painter.setPen(color)
			painter.drawPath(path)
		self.pick_thread.start()
		self.calc_thread.start()
	def mousePressEvent(self,event):
		if event.button()==Qt.LeftButton:
			self.trigger.emit()
			self.close()
			event.accept()	
	def repos(self):
		global point
		self.move(point.x-100,point.y-100)
		time.sleep(0.0001)
		self.pick_thread.start()
	def show_index(self):
		global rgb		
		r=qRed(rgb)
		g=qGreen(rgb)
		b=qBlue(rgb)
		RGB=str(r)+","+str(g)+","+str(b)
		index1=str(QString.number(int(r),16))
		index2=str(QString.number(int(g),16))
		index3=str(QString.number(int(b),16))
		if len(index1)<2:
			index1="0"*(2-len(index1))+index1
		if len(index2)<2:
			index2="0"*(2-len(index2))+index2
		if len(index3)<2:
			index3="0"*(2-len(index3))+index3
		index=index1+index2+index3
		l=len(RGB)-5
		self.browser.setGeometry(int(65-5.5*l),133,70+11*l,32)
		self.browser.clear()
		self.browser.append('<font size="4" color="#'+index+'">%s </font><font size="4" color="#ffffff">%s</font>'%(self.specail,RGB))
		self.update()
class iColor_UI(QWidget):  
	def __init__(self,parent=None):
		global index
		super(iColor_UI,self).__init__(parent)
		iColor_close_qss_file=open("data/UI/style_sheets/btn_close.txt","r")
		iColor_close_qss=iColor_close_qss_file.read()
		iColor_close_qss_file.close()
		iColor_small_qss_file=open("data/UI/style_sheets/btn_small.txt","r")
		iColor_small_qss=iColor_small_qss_file.read()
		iColor_small_qss_file.close()
		iColor_pick_qss_file=open("data/UI/style_sheets/btn_pick.txt","r")
		iColor_pick_qss=iColor_pick_qss_file.read()
		iColor_pick_qss_file.close()
		iColor_browser_qss_file=open("data/UI/style_sheets/QTextBrowser.txt","r")
		iColor_browser_qss=iColor_browser_qss_file.read()
		iColor_browser_qss_file.close()
		iColor_label_qss_file=open("data/UI/style_sheets/QLabel.txt","r")
		iColor_label_qss=iColor_label_qss_file.read()
		iColor_label_qss_file.close()
		iColor_lineedit_qss_file=open("data/UI/style_sheets/QLineEdit.txt","r")
		iColor_lineedit_qss=iColor_lineedit_qss_file.read()
		iColor_lineedit_qss_file.close()
		self.btn_close=QPushButton()
		self.btn_small=QPushButton()
		self.btn_pick=QPushButton()
		self.btn_close.setCursor(QCursor(Qt.PointingHandCursor))
		self.btn_small.setCursor(QCursor(Qt.PointingHandCursor))
		self.btn_pick.setCursor(QCursor(Qt.PointingHandCursor))
		self.browser = QTextBrowser()
		self.label=QLabel()
		self.rgb_validator=QIntValidator(0,255,self)
		rgb=iColor_label_qss[iColor_label_qss.index("(")+1:iColor_label_qss.index(")")].split(",")
		self.lineedit1=QLineEdit(rgb[0])
		self.lineedit2=QLineEdit(rgb[1])
		self.lineedit3=QLineEdit(rgb[2])
		index1=str(QString.number(int(rgb[0]),16))
		index2=str(QString.number(int(rgb[1]),16))
		index3=str(QString.number(int(rgb[2]),16))
		if len(index1)<2:
			index1="0"*(2-len(index1))+index1
		if len(index2)<2:
			index2="0"*(2-len(index2))+index2
		if len(index3)<2:
			index3="0"*(2-len(index3))+index3
		index=index1+index2+index3
		self.lineedit4=QLineEdit(index.upper())
		self.lineedit1.setTextMargins(5,0,5,0)
		self.lineedit2.setTextMargins(5,0,5,0)
		self.lineedit3.setTextMargins(5,0,5,0)
		self.lineedit4.setTextMargins(14,0,14,0)
		self.lineedit1.setValidator(self.rgb_validator)
		self.lineedit2.setValidator(self.rgb_validator)
		self.lineedit3.setValidator(self.rgb_validator)
		self.lineedit4.setInputMask("HHHHHH")
		self.btn_close.setStyleSheet(iColor_close_qss)
		self.btn_small.setStyleSheet(iColor_small_qss)
		self.btn_pick.setStyleSheet(iColor_pick_qss)
		self.browser.setStyleSheet(iColor_browser_qss)
		self.label.setStyleSheet(iColor_label_qss)
		self.lineedit1.setStyleSheet(iColor_lineedit_qss)
		self.lineedit2.setStyleSheet(iColor_lineedit_qss)
		self.lineedit3.setStyleSheet(iColor_lineedit_qss)
		self.lineedit4.setStyleSheet(iColor_lineedit_qss)
		self.btn_close.setParent(self)
		self.btn_small.setParent(self)
		self.btn_pick.setParent(self)
		self.browser.setParent(self)
		self.label.setParent(self)
		self.lineedit1.setParent(self)
		self.lineedit2.setParent(self)
		self.lineedit3.setParent(self)
		self.lineedit4.setParent(self)
		self.btn_close.setGeometry(325,10,14,14)
		self.btn_small.setGeometry(300,10,14,14)
		self.btn_pick.setGeometry(285,60,30,30)
		self.browser.setGeometry(6,2,52,28)
		self.label.setGeometry(25,60,110,80)
		self.lineedit1.setGeometry(155,110,50,30)
		self.lineedit2.setGeometry(215,110,50,30)
		self.lineedit3.setGeometry(275,110,50,30)
		self.lineedit4.setGeometry(155,60,110,30)
		self.btn_close.clicked.connect(self.close_clicked)
		self.btn_small.clicked.connect(self.small_clicked)
		self.btn_pick.clicked.connect(self.pick_color)
		self.lineedit1.textChanged.connect(self.calc_index)
		self.lineedit2.textChanged.connect(self.calc_index)
		self.lineedit3.textChanged.connect(self.calc_index)
		self.lineedit4.textChanged.connect(self.calc_rgb)
		self.lineedit4.selectionChanged.connect(self.reselect)
		self.icon = QIcon("data/UI/images/icon.png")
		self.setWindowIcon(self.icon)
		self.setWindowTitle(u"iColor")
		self.browser.append(u'<font size="3" color="#666666">iColor</font>')
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.dragPosition=None
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.resize(350,190)
		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
	def paintEvent(self,event):
		path=QPainterPath()
		painter=QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing, True)
		alpha=[120,75,45,25,15,10]
		path.addRoundRect(6, 6, self.width()-12, self.height()-12, 10)
		painter.fillPath(path, QBrush(QPixmap("data/UI/images/bg.png")))
		color=QColor(0, 0, 0, 255)
		for i in range(0,6):
			path=QPainterPath()
			path.addRoundRect(6-i, 6-i, self.width()-(6-i)*2, self.height()-(6-i)*2, 10)
			color.setAlpha(alpha[i])
			painter.setPen(color)
			painter.drawPath(path)
	def mousePressEvent(self,event):
		if event.button()==Qt.LeftButton:
			self.dragPosition=event.globalPos()-self.frameGeometry().topLeft()
			event.accept()
	def mouseReleaseEvent(self,event):
		if event.button()==Qt.LeftButton:
			event.accept()
	def mouseMoveEvent(self,event):
		if event.buttons() & Qt.LeftButton:
			if self.dragPosition.y()<60:
				self.move(event.globalPos()-self.dragPosition)
				event.accept()
	def reselect(self):
		if len(self.lineedit4.selectedText())<2:
			self.lineedit4.setSelection(0,0)
		elif self.lineedit4.selectedText()!=self.lineedit4.text():
			self.lineedit4.setSelection(0,6)

	def calc_rgb(self):
		index=unicode(self.lineedit4.text())
		cursor_pos=self.lineedit4.cursorPosition()
		if len(index)<6:
			if len(index)==5:
				cursor_pos+=1
			if len(index)==1:
				index=index+"0"*(6-len(index))
			else:
				index="0"*(6-len(index))+index
		self.lineedit4.setText(index.upper())
		self.lineedit4.setCursorPosition(cursor_pos)
		r=str(int(index[:2],16))
		g=str(int(index[2:4],16))
		b=str(int(index[4:],16))
		self.lineedit1.setText(r)
		self.lineedit2.setText(g)
		self.lineedit3.setText(b)
		iColor_label_qss="QLabel{background:rgba("+r+","+g+","+b+",100%);border:0px;border-radius:10px}"
		self.label.setStyleSheet(iColor_label_qss)
		iColor_label_qss_file=open("data/UI/style_sheets/QLabel.txt","w")
		iColor_label_qss_file.write(iColor_label_qss)
		iColor_label_qss_file.close()
	def calc_index(self):
		r=unicode(self.lineedit1.text())
		g=unicode(self.lineedit2.text())
		b=unicode(self.lineedit3.text())
		if len(r)==0:
			r="0"
		if len(g)==0:
			g="0"
		if len(b)==0:
			b="0"
		index1=str(QString.number(int(r),16))
		index2=str(QString.number(int(g),16))
		index3=str(QString.number(int(b),16))
		if len(index1)<2:
			index1="0"*(2-len(index1))+index1
		if len(index2)<2:
			index2="0"*(2-len(index2))+index2
		if len(index3)<2:
			index3="0"*(2-len(index3))+index3
		index=index1+index2+index3
		cursor_pos=self.lineedit4.cursorPosition()
		self.lineedit4.setText(index.upper())
		self.lineedit4.setCursorPosition(cursor_pos)
		iColor_label_qss="QLabel{background:rgba("+r+","+g+","+b+",100%);border:0px;border-radius:10px}"
		self.label.setStyleSheet(iColor_label_qss)
		iColor_label_qss_file=open("data/UI/style_sheets/QLabel.txt","w")
		iColor_label_qss_file.write(iColor_label_qss)
		iColor_label_qss_file.close()
	def pick_color(self):
		global lastMousePosition
		self.hide()
		self.pick_ui=Pick_UI()
		self.pick_ui.trigger.connect(self.show_ui)
		self.pick_ui.show()
	def show_ui(self):
		global rgb
		self.lineedit1.setText(str(qRed(rgb)))
		self.lineedit2.setText(str(qGreen(rgb)))
		self.lineedit3.setText(str(qBlue(rgb)))
		self.show()
	def close_clicked(self):
		self.close()
	def small_clicked(self):
		self.showMinimized()
app=QApplication(sys.argv)
form=iColor_UI()
form.show()
sys.exit(app.exec_())
