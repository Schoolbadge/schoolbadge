# this file will contain a script to scan badges and save the data to a google spreadsheet
import RFIDReader as reader
import Logger

rowIndex = Logger.getLastRowIndex()
if (rowIndex == 'FluovestNummer'):
    rowIndex = 0
print(rowIndex)
while (True):
    id, text = reader.Read()
    Logger.logBadge(int(rowIndex) + 1, id)
    rowIndex = rowIndex + 1
