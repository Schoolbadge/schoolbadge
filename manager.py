# this file will contain a script to scan badges and save the data to a google spreadsheet
import RFIDReader as reader
import Logger

while (True):
    id, text = reader.Read()
    Logger.LogBadge(id, text)
