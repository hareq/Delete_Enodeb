#!/usr/bin/env python3
        # -*- coding: utf-8 -*-
#exp ems/npcoss@TESTfile=d:daochu.dmp tables=(imo33) query="where filed 1 like '' compress=y"
#imp system/manager@TEST file=d:daochu.dmp
#
import sys
import os
from PyQt4 import QtGui, QtCore,QtSql
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import cx_Oracle

class Main(QWizard):

    NUM_PAGES = 4
    (PageFirst, PageOracle,PageEnodeb,PageRestartJboss) = range(NUM_PAGES)

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.setPage(self.PageFirst, FirstPage(self))
        self.setPage(self.PageOracle, OraclePage())
        self.setPage(self.PageEnodeb, EnodebPage())
        self.setPage(self.PageRestartJboss, RestartJbossPage())

        self.setStartId(self.PageFirst)

        self.setWizardStyle(self.ModernStyle)
        self.setWindowTitle(self.tr("Oracle Enodeb"))

class FirstPage(QWizardPage):
    def __init__(self, parent=None):
        super(FirstPage, self).__init__(parent)

        self.regRBtn = QRadioButton(self.tr("&Delete Enodeb"))
        #self.evalRBtn = QRadioButton(self.tr("&Import_Enodeb"))
        self.Restart_Jboss_Btn = QRadioButton(self.tr("&Restart_Jboss"))
        self.regRBtn.setChecked(True)

        layout = QVBoxLayout()
        layout.addWidget(self.regRBtn)
        #layout.addWidget(self.evalRBtn)
        layout.addWidget(self.Restart_Jboss_Btn)
        self.setLayout(layout)

    def nextId(self):
        if self.regRBtn.isChecked():
            return Main.PageOracle
        if self.Restart_Jboss_Btn.isChecked():
            reply = QtGui.QMessageBox.question(self, 'Message',
                "Undone", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            #return Main.PageRestartJboss

class OraclePage(QWizardPage):
    def initializePage(self):

        self.Oracle_Ip_Label = QLabel("Oracle_Ip: ")
        self.Oracle_Ip_Edit = QLineEdit()
        self.Oracle_Ip_Label.setBuddy(self.Oracle_Ip_Edit)

        self.Oracle_Db_Label = QLabel("Oracle_Db: ")
        self.Oracle_Db_Edit = QLineEdit()
        self.Oracle_Db_Label.setBuddy(self.Oracle_Db_Edit)

        self.Oracle_User_Label = QLabel("Oracle_User: ")
        self.Oracle_User_Edit = QLineEdit()
        self.Oracle_User_Label.setBuddy(self.Oracle_User_Edit)

        self.Oracle_Password_Label = QLabel(self.tr("Oracle_Password: "))
        self.Oracle_Password_Edit = QLineEdit()
        self.Oracle_Password_Label.setBuddy(self.Oracle_Password_Edit)

        self.registerField("evaluate.Oracle_Ip*", self.Oracle_Ip_Edit)
        self.registerField("evaluate.Oracle_Db*", self.Oracle_Db_Edit)
        self.registerField("evaluate.Oracle_User*", self.Oracle_User_Edit)
        self.registerField("evaluate.Oracle_Password*", self.Oracle_Password_Edit)

        grid = QGridLayout()
        grid.addWidget(self.Oracle_Ip_Label, 0, 0)
        grid.addWidget(self.Oracle_Ip_Edit, 0, 1)
        grid.addWidget(self.Oracle_Db_Label, 1, 0)
        grid.addWidget(self.Oracle_Db_Edit, 1, 1)
        grid.addWidget(self.Oracle_User_Label, 2, 0)
        grid.addWidget(self.Oracle_User_Edit, 2, 1)
        grid.addWidget(self.Oracle_Password_Label, 3, 0)
        grid.addWidget(self.Oracle_Password_Edit, 3, 1)
        self.setLayout(grid)

    def validatePage(self):
            self.Oracle_Ip_Edit_text = self.Oracle_Ip_Edit.text()
            self.Oracle_Db_Edit_text = self.Oracle_Db_Edit.text()
            self.Oracle_User_Edit_text = self.Oracle_User_Edit.text()
            self.Oracle_Password_Edit_text = self.Oracle_Password_Edit.text()
            self.Oracle_Ip_Edit_text = str(self.Oracle_Ip_Edit_text)
            self.Oracle_Db_Edit_text = str(self.Oracle_Db_Edit_text)
            self.Oracle_User_Edit_text = str(self.Oracle_User_Edit_text)
            self.Oracle_Password_Edit_text = str(self.Oracle_Password_Edit_text)
            if self.Oracle_Ip_Edit_text != "" and self.Oracle_Db_Edit_text != "" and self.Oracle_User_Edit_text != "" and self.Oracle_Password_Edit_text != "":
                self.db=cx_Oracle.connect(self.Oracle_User_Edit_text,self.Oracle_Password_Edit_text,self.Oracle_Ip_Edit_text+"/"+self.Oracle_Db_Edit_text)
                self.wizard().connect = self.db.cursor()
                return Main.PageEnodeb

class EnodebPage(QWizardPage):

    def initializePage(self):
    #def __init__(self, *args):
        #QWidget.__init__(self,*args)
        self.cursor = self.wizard().connect
        self.cursor.execute("select dn from imo0 where cid=8 order by dn")
        self.my_array = self.cursor.fetchall()
        self.tablemodel = MyTableModel( self.my_array, self)
        self.tableview = QTableView()
        self.tableview.setModel(self.tablemodel)
        self.resize(500, 400)
        self.setWindowTitle("enodeb list")

        self.btn_delete = QPushButton('delete',self)

        #btn_delete.setGeometry(100,100,10,10)
        grid = QGridLayout()
        grid.addWidget(self.tableview,0,0)
        grid.addWidget(self.btn_delete,0,2)
        self.setLayout(grid)
        self.connect(self.btn_delete, QtCore.SIGNAL('clicked()'),
            self.btn_delete_Clicked)

    def find_enodebid(self,start_str,end_str,s1):
        start = s1.find(start_str)
        end = s1.find(end_str)
        enodebid = s1[start+7:end]
        enodebdn = s1[start:end]
        return enodebid,enodebdn

    def btn_delete_Clicked(self):
        sender = self.sender()
        list_length = len(self.tableview.selectedIndexes())
        f = open("log.txt","w+")
        for element in range(0,list_length):
            imo_dn_str = str(self.my_array[self.tableview.selectedIndexes()[element].row()])
            print imo_dn_str
            enodebid = self.find_enodebid('eNodeB=',"',",imo_dn_str)[0]
            enodebdn = self.find_enodebid('eNodeB=',"',",imo_dn_str)[1]
            list_length_imo_dn = len(imo_dn_str)
            imo_dn = imo_dn_str[2:list_length_imo_dn-3]
            print imo_dn
            enodebimo = int(enodebid)%53 + 1
            enodebimo = str(enodebimo)
            sql_delete_imoenodeb = "delete from imo"+enodebimo+" where dn like'"+enodebdn+",%'"+"or dn='"+enodebdn+"'"
            self.cursor.execute(sql_delete_imoenodeb)
            sql_delete_imo0 = "delete from imo0 where dn='"+imo_dn+"'"
            self.cursor.execute(sql_delete_imo0)
            f.write("delete enodeb"+enodebid+" succeeful"+"/")
            print "delete enodeb",enodebid,"succeeful"
            #self.tablemodel.removeRow(self.tableview.selectedIndexes()[element].row())
        self.cursor.execute("commit")
        f.close()
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Commit Succeeful!", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
    def btn_export_Clicked(self):
        print"..."

    def nextId(self):
         return -1

class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, parent = None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return (self.arraydata[index.row()][index.column()])

class ImportPage(QWizardPage):
    def initializePage(self):

        btn_delete = QPushButton('Done',self)
        btn_export = QPushButton('Back',self)
        btn_Link_Oracle = QPushButton('Import',self)
        btn_delete.setGeometry(250,320,80,30)
        btn_export.setGeometry(350,320,80,30)
        btn_Link_Oracle.setGeometry(50,200,80,30)
        text = QLabel('result:',self)
        text.setGeometry(200,200,80,30)

        Oracle_Ip_Edit = QLineEdit('',self)
        Oracle_Ip_Edit.setGeometry(200,50,150,30)

        self.radioButton = QtGui.QRadioButton()
        self.radioButton.setGeometry(QtCore.QRect(90, 40, 89, 16))

    def btn_export_Clicked(self):
        print"..."

    def nextId(self):
        return -1

class RestartJbossPage(QWizardPage):
    def __init__(self, parent=None):
        super(RestartJbossPage, self).__init__(parent)

        self.Jboss_Ip_Label = QLabel("Jboss_Ip: ")
        self.Jboss_Ip_Edit = QLineEdit()
        self.Jboss_Ip_Label.setBuddy(self.Jboss_Ip_Edit)

        self.Jboss_User_Label = QLabel("Jboss_User: ")
        self.Jboss_User_Edit = QLineEdit()
        self.Jboss_User_Label.setBuddy(self.Jboss_User_Edit)

        self.Jboss_Password_Label = QLabel("Jboss_Password: ")
        self.Jboss_Password_Edit = QLineEdit()
        self.Jboss_Password_Label.setBuddy(self.Jboss_Password_Edit)

        self.registerField("evaluate.Jboss_Ip*", self.Jboss_Ip_Edit)
        self.registerField("evaluate.Jboss_User*", self.Jboss_User_Edit)
        self.registerField("evaluate.Jboss_Password*", self.Jboss_Password_Edit)

        grid = QGridLayout()
        grid.addWidget(self.Jboss_Ip_Label, 0, 0)
        grid.addWidget(self.Jboss_Ip_Edit, 0, 1)
        grid.addWidget(self.Jboss_User_Label, 1, 0)
        grid.addWidget(self.Jboss_User_Edit, 1, 1)
        grid.addWidget(self.Jboss_Password_Label, 2, 0)
        grid.addWidget(self.Jboss_Password_Edit, 2, 1)
        self.setLayout(grid)
    def nextId(self):
         return -1


def main():
    import sys
    app = QApplication(sys.argv)
    wiz = Main()
    wiz.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
