#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2009 Nokia Corporation and/or its subsidiary(-ies).
## Contact: Qt Software Information (qt-info@nokia.com)
##
## This file is part of the example classes of the Qt Toolkit.
##
#############################################################################

import pickle

from PySide import QtCore, QtGui


class SortedDict(dict):
    class Iterator(object):
        def __init__(self, sorted_dict):
            self._dict = sorted_dict
            self._keys = sorted(self._dict.keys())
            self._nr_items = len(self._keys)
            self._idx = 0

        def __iter__(self):
            return self

        def next(self):
            if self._idx >= self._nr_items:
                raise StopIteration

            key = self._keys[self._idx]
            value = self._dict[key]
            self._idx += 1

            return key, value

        __next__ = next

    def __iter__(self):
        return SortedDict.Iterator(self)

    iterkeys = __iter__


class ChargeCodeCatalog(QtGui.QWidget):
    NavigationMode, AddingMode, EditingMode = range(3)

    def __init__(self, parent=None):
        super(ChargeCodeCatalog, self).__init__(parent)

        self.chargecodes = SortedDict()
        self.oldChargeCode = ''
        self.oldChargeCodeDescriptioin = ''
        self.currentMode = self.NavigationMode

        chargeCodeLabel = QtGui.QLabel("Charge Code:")
        self.chargeCodeLine = QtGui.QLineEdit()
        self.chargeCodeLine.setReadOnly(True)

        chargeCodeDescriptionLabel = QtGui.QLabel("Description:")
        self.chargeCodeDescriptionText = QtGui.QTextEdit()
        self.chargeCodeDescriptionText.setReadOnly(True)

        self.addButton = QtGui.QPushButton("&Add")
        self.addButton.show()
        self.editButton = QtGui.QPushButton("&Edit")
        self.editButton.setEnabled(False)
        self.removeButton = QtGui.QPushButton("&Remove")
        self.removeButton.setEnabled(False)
        self.findButton = QtGui.QPushButton("&Find")
        self.findButton.setEnabled(False)
        self.submitButton = QtGui.QPushButton("&Submit")
        self.submitButton.hide()
        self.cancelButton = QtGui.QPushButton("&Cancel")
        self.cancelButton.hide()

        self.nextButton = QtGui.QPushButton("&Next")
        self.nextButton.setEnabled(False)
        self.previousButton = QtGui.QPushButton("&Previous")
        self.previousButton.setEnabled(False)

        self.loadButton = QtGui.QPushButton("&Load...")
        self.loadButton.setToolTip("Load codes from a file")
        self.saveButton = QtGui.QPushButton("Sa&ve...")
        self.saveButton.setToolTip("Save codes to a file")
        self.saveButton.setEnabled(False)

        self.exportButton = QtGui.QPushButton("Ex&port")
        self.exportButton.setToolTip("Export as vCard")
        self.exportButton.setEnabled(False)

        self.dialog = FindDialog()

        self.addButton.clicked.connect(self.addContact)
        self.submitButton.clicked.connect(self.submitContact)
        self.editButton.clicked.connect(self.editContact)
        self.removeButton.clicked.connect(self.removeContact)
        self.findButton.clicked.connect(self.findContact)
        self.cancelButton.clicked.connect(self.cancel)
        self.nextButton.clicked.connect(self.next)
        self.previousButton.clicked.connect(self.previous)
        self.loadButton.clicked.connect(self.loadFromFile)
        self.saveButton.clicked.connect(self.saveToFile)
        self.exportButton.clicked.connect(self.exportAsVCard)

        buttonLayout1 = QtGui.QVBoxLayout()
        buttonLayout1.addWidget(self.addButton)
        buttonLayout1.addWidget(self.editButton)
        buttonLayout1.addWidget(self.removeButton)
        buttonLayout1.addWidget(self.findButton)
        buttonLayout1.addWidget(self.submitButton)
        buttonLayout1.addWidget(self.cancelButton)
        buttonLayout1.addWidget(self.loadButton)
        buttonLayout1.addWidget(self.saveButton)
        buttonLayout1.addWidget(self.exportButton)
        buttonLayout1.addStretch()

        buttonLayout2 = QtGui.QHBoxLayout()
        buttonLayout2.addWidget(self.previousButton)
        buttonLayout2.addWidget(self.nextButton)

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(chargeCodeLabel, 0, 0)
        mainLayout.addWidget(self.chargeCodeLine, 0, 1)
        mainLayout.addWidget(chargeCodeDescriptionLabel, 1, 0, QtCore.Qt.AlignTop)
        mainLayout.addWidget(self.chargeCodeDescriptionText, 1, 1)
        mainLayout.addLayout(buttonLayout1, 1, 2)
        mainLayout.addLayout(buttonLayout2, 2, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle("Charge Codes")

    def addContact(self):
        self.oldChargeCode = self.chargeCodeLine.text()
        self.oldChargeCodeDescriptioin = self.chargeCodeDescriptionText.toPlainText()

        self.chargeCodeLine.clear()
        self.chargeCodeDescriptionText.clear()

        self.updateInterface(self.AddingMode)

    def editContact(self):
        self.oldChargeCode = self.chargeCodeLine.text()
        self.oldChargeCodeDescriptioin = self.chargeCodeDescriptionText.toPlainText()

        self.updateInterface(self.EditingMode)

    def submitContact(self):
        chargeCode = self.chargeCodeLine.text()
        address = self.chargeCodeDescriptionText.toPlainText()

        if chargeCode == "" or address == "":
            QtGui.QMessageBox.information(self, "Empty Field",
                    "Please add charge code and description.")
            return

        if self.currentMode == self.AddingMode:
            if chargeCode not in self.chargecodes:
                self.chargecodes[chargeCode] = address
                QtGui.QMessageBox.information(self, "Add Successful",
                        "\"%s\" has been added." % chargeCode)
            else:
                QtGui.QMessageBox.information(self, "Add Unsuccessful",
                        "Sorry, \"%s\" is already in your catalogue." % chargeCode)
                return

        elif self.currentMode == self.EditingMode:
            if self.oldChargeCode != chargeCode:
                if chargeCode not in self.chargecodes:
                    QtGui.QMessageBox.information(self, "Edit Successful",
                            "\"%s\" has been edited in your address book." % self.oldChargeCode)
                    del self.chargecodes[self.oldChargeCode]
                    self.chargecodes[chargeCode] = address
                else:
                    QtGui.QMessageBox.information(self, "Edit Unsuccessful",
                            "Sorry, \"%s\" is already in your address book." % chargeCode)
                    return
            elif self.oldChargeCodeDescriptioin != address:
                QtGui.QMessageBox.information(self, "Edit Successful",
                        "\"%s\" has been edited in your address book." % chargeCode)
                self.chargecodes[chargeCode] = address

        self.updateInterface(self.NavigationMode)

    def cancel(self):
        self.chargeCodeLine.setText(self.oldChargeCode)
        self.chargeCodeDescriptionText.setText(self.oldChargeCodeDescriptioin)
        self.updateInterface(self.NavigationMode)

    def removeContact(self):
        chargeCode = self.chargeCodeLine.text()
        address = self.chargeCodeDescriptionText.toPlainText()

        if chargeCode in self.chargecodes:
            button = QtGui.QMessageBox.question(self, "Confirm Remove",
                    "Are you sure you want to remove \"%s\"?" % chargeCode,
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

            if button == QtGui.QMessageBox.Yes:
                self.previous()
                del self.chargecodes[chargeCode]

                QtGui.QMessageBox.information(self, "Remove Successful",
                        "\"%s\" has been removed from your address book." % chargeCode)

        self.updateInterface(self.NavigationMode)

    def next(self):
        chargeCode = self.chargeCodeLine.text()
        it = iter(self.chargecodes)

        try:
            while True:
                this_chargeCode, _ = it.next()

                if this_chargeCode == chargeCode:
                    next_chargeCode, next_address = it.next()
                    break
        except StopIteration:
            next_chargeCode, next_address = iter(self.chargecodes).next()

        self.chargeCodeLine.setText(next_chargeCode)
        self.chargeCodeDescriptionText.setText(next_address)

    def previous(self):
        chargeCode = self.chargeCodeLine.text()

        prev_chargeCode = prev_address = None
        for this_chargeCode, this_address in self.chargecodes:
            if this_chargeCode == chargeCode:
                break

            prev_chargeCode = this_chargeCode
            prev_address = this_address
        else:
            self.chargeCodeLine.clear()
            self.chargeCodeDescriptionText.clear()
            return

        if prev_chargeCode is None:
            for prev_chargeCode, prev_address in self.chargecodes:
                pass

        self.chargeCodeLine.setText(prev_chargeCode)
        self.chargeCodeDescriptionText.setText(prev_address)

    def findContact(self):
        self.dialog.show()

        if self.dialog.exec_() == QtGui.QDialog.Accepted:
            contactName = self.dialog.getFindText()

            if contactName in self.chargecodes:
                self.chargeCodeLine.setText(contactName)
                self.chargeCodeDescriptionText.setText(self.chargecodes[contactName])
            else:
                QtGui.QMessageBox.information(self, "Contact Not Found",
                        "Sorry, \"%s\" is not in your address book." % contactName)
                return

        self.updateInterface(self.NavigationMode)

    def updateInterface(self, mode):
        self.currentMode = mode

        if self.currentMode in (self.AddingMode, self.EditingMode):
            self.chargeCodeLine.setReadOnly(False)
            self.chargeCodeLine.setFocus(QtCore.Qt.OtherFocusReason)
            self.chargeCodeDescriptionText.setReadOnly(False)

            self.addButton.setEnabled(False)
            self.editButton.setEnabled(False)
            self.removeButton.setEnabled(False)

            self.nextButton.setEnabled(False)
            self.previousButton.setEnabled(False)

            self.submitButton.show()
            self.cancelButton.show()

            self.loadButton.setEnabled(False)
            self.saveButton.setEnabled(False)
            self.exportButton.setEnabled(False)

        elif self.currentMode == self.NavigationMode:
            if not self.chargecodes:
                self.chargeCodeLine.clear()
                self.chargeCodeDescriptionText.clear()

            self.chargeCodeLine.setReadOnly(True)
            self.chargeCodeDescriptionText.setReadOnly(True)
            self.addButton.setEnabled(True)

            number = len(self.chargecodes)
            self.editButton.setEnabled(number >= 1)
            self.removeButton.setEnabled(number >= 1)
            self.findButton.setEnabled(number > 2)
            self.nextButton.setEnabled(number > 1)
            self.previousButton.setEnabled(number >1 )

            self.submitButton.hide()
            self.cancelButton.hide()

            self.exportButton.setEnabled(number >= 1)

            self.loadButton.setEnabled(True)
            self.saveButton.setEnabled(number >= 1)

    def saveToFile(self):
        fileName,_ = QtGui.QFileDialog.getSaveFileName(self,
                "Save Address Book", '',
                "Address Book (*.abk);;All Files (*)")

        if not fileName:
            return

        try:
            out_file = open(str(fileName), 'wb')
        except IOError:
            QtGui.QMessageBox.information(self, "Unable to open file",
                    "There was an error opening \"%s\"" % fileName)
            return

        pickle.dump(self.chargecodes, out_file)
        out_file.close()

    def loadFromFile(self):
        fileName,_ = QtGui.QFileDialog.getOpenFileName(self,
                "Open Address Book", '',
                "Address Book (*.abk);;All Files (*)")

        if not fileName:
            return

        try:
            in_file = open(str(fileName), 'rb')
        except IOError:
            QtGui.QMessageBox.information(self, "Unable to open file",
                    "There was an error opening \"%s\"" % fileName)
            return

        self.chargecodes = pickle.load(in_file)
        in_file.close()

        if len(self.chargecodes) == 0:
            QtGui.QMessageBox.information(self, "No contacts in file",
                    "The file you are attempting to open contains no "
                    "contacts.")
        else:
            for chargeCode, chargeCodeDescription in self.chargecodes:
                self.chargeCodeLine.setText(chargeCode)
                self.chargeCodeDescriptionText.setText(chargeCodeDescription)

        self.updateInterface(self.NavigationMode)

    def exportAsVCard(self):
        name = str(self.chargeCodeLine.text())
        address = self.chargeCodeDescriptionText.toPlainText()

        nameList = name.split()

        if len(nameList) > 1:
            firstName = nameList[0]
            lastName = nameList[-1]
        else:
            firstName = name
            lastName = ''

        fileName = QtGui.QFileDialog.getSaveFileName(self, "Export Contact",
                '', "vCard Files (*.vcf);;All Files (*)")[0]

        if not fileName:
            return

        out_file = QtCore.QFile(fileName)

        if not out_file.open(QtCore.QIODevice.WriteOnly):
            QtGui.QMessageBox.information(self, "Unable to open file",
                    out_file.errorString())
            return

        out_s = QtCore.QTextStream(out_file)

        out_s << 'BEGIN:VCARD' << '\n'
        out_s << 'VERSION:2.1' << '\n'
        out_s << 'N:' << lastName << ';' << firstName << '\n'
        out_s << 'FN:' << ' '.join(nameList) << '\n'

        address.replace(';', '\\;')
        address.replace('\n', ';')
        address.replace(',', ' ')

        out_s << 'ADR;HOME:;' << address << '\n'
        out_s << 'END:VCARD' << '\n'

        QtGui.QMessageBox.information(self, "Export Successful",
                "\"%s\" has been exported as a vCard." % name)


class FindDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(FindDialog, self).__init__(parent)

        findChargeCode = QtGui.QLabel("Enter a charge code:")
        self.lineEdit = QtGui.QLineEdit()

        self.findButton = QtGui.QPushButton("&Find")
        self.findText = ''

        layout = QtGui.QHBoxLayout()
        layout.addWidget(findChargeCode)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.findButton)

        self.setLayout(layout)
        self.setWindowTitle("Find Charge Code")

        self.findButton.clicked.connect(self.findClicked)
        self.findButton.clicked.connect(self.accept)

    def findClicked(self):
        text = self.lineEdit.text()

        if not text:
            QtGui.QMessageBox.information(self, "Empty Field",
                    "Please enter a charge code.")
            return

        self.findText = text
        self.lineEdit.clear()
        self.hide()

    def getFindText(self):
        return self.findText


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    addressBook = ChargeCodeCatalog()
    addressBook.show()

    sys.exit(app.exec_())
