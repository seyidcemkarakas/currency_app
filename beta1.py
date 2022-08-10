from tasarımlar.tasarım3 import Ui_MainWindow
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import QIcon
import sys
import numpy as np
import datetime
import yfinance as yf
from datetime import datetime
import pandas as pd

class myApp(QtWidgets.QMainWindow):

    def __init__(self):
        super(myApp,self).__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) # accessing widgets
        self.setWindowTitle("Currency App") # başlık
        self.change_currency()
        self.current()
        
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.current)
        self.timer.timeout.connect(self.change)
        self.timer.start(2000)  # for x seconds delay => x*1000  
        
        self.ui.pushButton3.clicked.connect(self.change)
        self.ui.pushButton4.clicked.connect(self.change_currency)
        self.ui.pushButton1.clicked.connect(self.show_past)
    
    # qt5 functions
    def show_past(self):
        
        gun=str(self.ui.comboBox1.currentText()) #get value from box
        ay=str(self.ui.comboBox2.currentText())  #get value from box
        yil=str(self.ui.comboBox3.currentText()) #get value from box
        
        self.date_maker(int(yil),int(ay),int(gun)) # run date_maker 
        value=self.past(self.ticker,self.tarih_guncel,self.tarih_once,self.tarih_sonra)
        
        self.ui.label6.setText(str(value)) #the value comes from past is written to label
        self.ui.label7.setText(f"{gun}/{ay}/{yil}")   #date info is written to label
    def change_currency(self):
        self.etiket = str(self.ui.comboBox4.currentText())
        
        #kullanıcı etiketi => ticker
        if self.etiket == "USD/TRY":
            self.ticker = "USDTRY=X"
        if self.etiket == "EUR/TRY":
            self.ticker = "EURTRY=X"
        if self.etiket == "GBP/TRY":
            self.ticker = "GBPTRY=X"
        if self.etiket == "CAD/TRY":
            self.ticker = "CADTRY=X"
        if self.etiket == "CHF/TRY":
            self.ticker = "CHFTRY=X"    
        
        self.current()
        self.show_past()
        
        if self.ticker == "EURTRY=X":
            self.ui.label9.setText("1 EUR")
            self.ui.label10.setText("1 EUR")
        if self.ticker == "USDTRY=X":
            self.ui.label9.setText("1 USD")
            self.ui.label10.setText("1 USD")  
        if self.ticker == "GBPTRY=X":
            self.ui.label9.setText("1 GBP")
            self.ui.label10.setText("1 GBP")
        if self.ticker == "CADTRY=X":
            self.ui.label9.setText("1 CAD")
            self.ui.label10.setText("1 CAD")
        if self.ticker == "CHFTRY=X":
            self.ui.label9.setText("1 CHF")
            self.ui.label10.setText("1 CHF")
    def change(self):
        if self.ui.label6.text() == "invalid":
            self.ui.label8.setText("Incomputable")
        else:
            x1=float(self.ui.label6.text())   
            x2=float(self.ui.label2.text())
            degisim=round(100*((x2-x1)/x1),2)
            self.ui.label8.setText("% "+str(degisim))
    
    # algoritma fonksiyonları
    def current(self):
        self.etiket=yf.Ticker(self.ticker) # ticker data is acquired from yahoo
        self.data=self.etiket.history(period="curent") # only current value is wanted
        self.value=round(self.data["Close"].iloc[-1],3)
        self.ui.label2.setText(str(self.value))  # valuee value is written to associated label
    def date_maker(self,y,a,g):

        y=str(y)
        a=str(a)
        g=str(g)
        t= y + "-" + a + "-" + g

        #tarihi saniyeye çevir
        tarih_guncel=datetime.fromtimestamp(int(pd.Timestamp(t).timestamp())) #current date
        tarih_once=datetime.fromtimestamp(int(pd.Timestamp(t).timestamp())-3*86400) #3 days backwards
        tarih_sonra=datetime.fromtimestamp(int(pd.Timestamp(t).timestamp())+3*86400) #3 days forewards

        #seconds to date

        
        # if day and month value is one digit, these codes put 0 to their left in order to be 2 digits
        #gunceller
        yil_guncel=str(tarih_guncel.year)
        if len(str(tarih_guncel.month))==1:
            ay_guncel="0"+str(tarih_guncel.month)
        else:
            ay_guncel=str(tarih_guncel.month)
        if len(str(tarih_guncel.day))==1:
            gun_guncel="0"+str(tarih_guncel.day)
        else:
            gun_guncel=str(tarih_guncel.day) 

        #onceler
        yil_once=str(tarih_once.year)
        if len(str(tarih_once.month))==1:
            ay_once="0"+str(tarih_once.month)
        else:
            ay_once=str(tarih_once.month)
        if len(str(tarih_once.day))==1:
            gun_once="0"+str(tarih_once.day)
        else:
            gun_once=str(tarih_once.day) 

        #sonralar
        yil_sonra=str(tarih_sonra.year)
        if len(str(tarih_sonra.month))==1:
            ay_sonra="0"+str(tarih_sonra.month)
        else:
            ay_sonra=str(tarih_sonra.month)
        if len(str(tarih_sonra.day))==1:
            gun_sonra="0"+str(tarih_sonra.day)
        else:
            gun_sonra=str(tarih_sonra.day) 
            
        
        # values which are ready is combined to string properly
        
	self.tarih_guncel= yil_guncel + "-" + ay_guncel + "-" + gun_guncel
        self.tarih_once= yil_once + "-" + ay_once + "-" + gun_once
        self.tarih_sonra= yil_sonra + "-" + ay_sonra + "-" + gun_sonra 

    def past(self,ticker,tarih_guncel,tarih_once,tarih_sonra):
        self.etiket=yf.Ticker(self.ticker)
        data=self.etiket.history(start=self.tarih_once,end=self.tarih_sonra) 
        data.index = data.index.format() # for searching, dataframe index part will be reformatted
        
        
	#if there is a currency value for selected date, it is written
        if self.tarih_guncel in list(data.index):
            value=round(data.loc[tarih_guncel]["Close"],3)
            return value
     
        else: 
            value="invalid"
            return value

def app():
    app = QtWidgets.QApplication(sys.argv)
    win = myApp()
    win.show()
    sys.exit(app.exec_())
app()