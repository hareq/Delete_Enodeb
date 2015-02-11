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

        self.regRBtn = QRadioButton(self.tr("&Delete,Export,Import Enodeb"))
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
            return Main.PageRestartJboss

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

        self.Server_User_for_oracle_Label = QLabel(self.tr("Server_User_for_oracle: "))
        self.Server_User_for_oracle_Edit = QLineEdit()
        self.Server_User_for_oracle_Label.setBuddy(self.Server_User_for_oracle_Edit)

        self.Server_Password_for_oracle_Label = QLabel(self.tr("Server_Password_for_oracle: "))
        self.Server_Password_for_oracle_Edit = QLineEdit()
        self.Server_Password_for_oracle_Label.setBuddy(self.Server_Password_for_oracle_Edit)

        self.registerField("evaluate.Oracle_Ip*", self.Oracle_Ip_Edit)
        self.registerField("evaluate.Oracle_Db*", self.Oracle_Db_Edit)
        self.registerField("evaluate.Oracle_User*", self.Oracle_User_Edit)
        self.registerField("evaluate.Oracle_Password*", self.Oracle_Password_Edit)
        self.registerField("evaluate.Server_User_for_oracle*", self.Server_Password_for_oracle_Edit)
        self.registerField("evaluate.Server_Password_for_oracle*", self.Server_User_for_oracle_Edit)


        grid = QGridLayout()
        grid.addWidget(self.Oracle_Ip_Label, 0, 0)
        grid.addWidget(self.Oracle_Ip_Edit, 0, 1)
        grid.addWidget(self.Oracle_Db_Label, 1, 0)
        grid.addWidget(self.Oracle_Db_Edit, 1, 1)
        grid.addWidget(self.Oracle_User_Label, 2, 0)
        grid.addWidget(self.Oracle_User_Edit, 2, 1)
        grid.addWidget(self.Oracle_Password_Label, 3, 0)
        grid.addWidget(self.Oracle_Password_Edit, 3, 1)
        grid.addWidget(self.Server_User_for_oracle_Label, 4, 0)
        grid.addWidget(self.Server_User_for_oracle_Edit, 4, 1)
        grid.addWidget(self.Server_Password_for_oracle_Label, 5, 0)
        grid.addWidget(self.Server_Password_for_oracle_Edit, 5, 1)
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

        self.btn_refurbish = QPushButton('refurbish',self)
        self.btn_delete = QPushButton('delete',self)
        self.btn_export = QPushButton('export',self)
        self.btn_import = QPushButton('import',self)
        self.btn_file = QPushButton('Choose File',self)
        self.btn_path = QPushButton('Choose Path',self)
        self.edit_export = QLineEdit(self)
        self.edit_import = QLineEdit(self)

        #btn_delete.setGeometry(100,100,10,10)
        grid = QGridLayout()
        grid.addWidget(self.tableview,0,0)
        grid.addWidget(self.btn_refurbish,0,1)
        grid.addWidget(self.btn_delete,0,2)
        grid.addWidget(self.btn_path,1,1)
        grid.addWidget(self.btn_file,2,1)
        grid.addWidget(self.btn_export,1,2)
        grid.addWidget(self.btn_import,2,2)
        grid.addWidget(self.edit_export,1,0)
        grid.addWidget(self.edit_import,2,0)
        self.setLayout(grid)

        self.connect(self.btn_delete, QtCore.SIGNAL('clicked()'),
            self.btn_delete_Clicked)
        self.connect( self.btn_file, QtCore.SIGNAL( 'clicked()' ),
            self.btn_file_clicked )
        self.connect( self.btn_refurbish, QtCore.SIGNAL( 'clicked()' ),
            self.btn_refurbish_clicked )
        self.connect( self.btn_path, QtCore.SIGNAL( 'clicked()' ),
            self.btn_path_clicked )
        self.connect( self.btn_export, QtCore.SIGNAL( 'clicked()' ),
            self.btn_export_clicked )
        self.connect( self.btn_import, QtCore.SIGNAL( 'clicked()' ),
            self.btn_import_clicked )

    def btn_export_clicked(self):
        print OraclePage.Oracle_User_Edit_text
        print OraclePage.Oracle_Password_Edit_text
        print self.fileName
        db2 = "exp"+' '+"'"+OraclePage.Oracle_User_Edit_text+"/"+OraclePage.Oracle_Password_Edit_text+" tables=(imo0,imo1,imo2,imo3,imo4,imo5,imo6,imo7,imo8,imo9,imo10,imo11,imo12,imo13,imo14,imo15,imo16,imo17,imo18,imo19,imo20,imo21,imo22,imo23,imo24,imo25,imo26,imo27,imo28,imo29,imo30,imo31,imo32,imo33,imo34,imo35,imo36,imo37,imo38,imo39,imo40,imo41,imo42,imo43,imo44,imo45,imo46,imo47,imo48,imo49,imo50,imo51,imo52,imo53) grants=y file="+self.fileName+".dmp'"
        print db2

    def btn_export_clicked_other(self):
        sender = self.sender()
        list_length = len(self.tableview.selectedIndexes())
        f = open("log.txt","w+")
        for element in range(0,list_length):
            imo_dn_str = str(self.my_array[self.tableview.selectedIndexes()[element].row()])
            print imo_dn_str
            enodebid = self.find_enodebid('eNodeB=',"',",imo_dn_str)[0]
            print enodebid
            enodebdn = self.find_enodebid('eNodeB=',"',",imo_dn_str)[1]
            print enodebdn
            list_length_imo_dn = len(imo_dn_str)
            imo_dn = imo_dn_str[2:list_length_imo_dn-4]
            enodebimo = int(enodebid)%53 + 1
            enodebimo = str(enodebimo)
            print enodebimo
            print "Start btn_export_clicked"
            oracle_user = "ems"
            oracle_password = "npcoss"
            #db = "exp"&" "&"'"&oracle_user&"/"&oracle_password&"table=("&imo&")"&" "&"file="&imo&".dmp"&" "&"query="&
            #exp 'ems/npcoss tables=(imo3) grants=y file=imo3.dmp query="where dn like 'eNodeB=131017,%' or dn like'eNodeB=131017,%'"'

    def btn_import_clicked( self ):
        print "Start btn_import_clicked"
        db2 = "imp"&' '&"ems/npcoss grants=y file=gg.dmp"

    def btn_file_clicked( self ):
        fileName = QtGui.QFileDialog.getOpenFileName( self, 'Choose File')
        if not fileName.isEmpty():
            self.edit_import.setText(fileName)

    def btn_path_clicked( self ):
        print "Start btn_path_clicked"
        self.fileName = QtGui.QFileDialog.getSaveFileName( self, 'Choose Path' )
        self.fileName = fileName+".dmp"
        if not fileName.isEmpty():
            self.edit_export.setText(fileName)

    def btn_refurbish_clicked( self ):
        print "Start btn_refurbish_clicked"
        self.cursor = self.wizard().connect
        self.cursor.execute("select dn from imo0 where cid=8 order by dn")
        self.my_array = self.cursor.fetchall()
        self.my_array = ['1','1']
        self.tablemodel = MyTableModel( self.my_array, self)
        self.tableview = QTableView()
        self.tableview.setModel(self.tablemodel)

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
            enodebid = self.find_enodebid('eNodeB=',"',",imo_dn_str)[0]
            enodebdn = self.find_enodebid('eNodeB=',"',",imo_dn_str)[1]
            list_length_imo_dn = len(imo_dn_str)
            imo_dn = imo_dn_str[2:list_length_imo_dn-4]
            enodebimo = int(enodebid)%53 + 1
            enodebimo = str(enodebimo)
            sql_delete_imoenodeb = "delete from imo"+enodebimo+" where dn like'"+enodebdn+",%'"+"or dn='"+enodebdn+"'"
            self.cursor.execute(sql_delete_imoenodeb)
            sql_delete_imo0 = "delete from imo0 where dn='"+imo_dn+"'"
            self.cursor.execute(sql_delete_imo0)
            f.write("delete enodeb"+enodebid+" succeeful"+"/")
            print "delete enodeb",enodebid,"succeeful"
            #self.tablemodel.removeRow(self.tableview.selectedIndexes()[element].row())
        sql_commit = "commit"
        #cursor.execute(sql_commit)
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

        Oracle_Ip = QLabel('Choose_file',self)
        Oracle_Ip.setGeometry(50,50,150,30)

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
