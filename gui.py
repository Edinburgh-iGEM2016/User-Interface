from Tkinter import *
import tkFileDialog
import lexEncode
import re
import createSentence
import decoding

lexicon = lexEncode.encode("/home/freddie/PycharmProjects/iGEM/ogdan",
                           "/home/freddie/PycharmProjects/iGEM/codeRecord",
                           "/home/freddie/PycharmProjects/iGEM/gBlocks")

currentLexicon = "/home/freddie/PycharmProjects/iGEM/ogdan"

frmMain = Tk()
frmMain.wm_title("BabblED")

logo = PhotoImage(file="/home/freddie/Downloads/programLogo")
header = Label(image=logo)
header.grid(row=0, column=1)

infoDisplay = Text(frmMain, width=120)
infoDisplay.grid(row=1, column=1, rowspan=4)

def getHelp():
    readMe = readIn("/home/freddie/PycharmProjects/iGEM/ReadMe")
    infoDisplay.delete('0.0', 'end')
    for eachLine in readMe:
        infoDisplay.insert(END, eachLine + '\n')

def readIn(filepath):
    with open(filepath) as f:
        text = f.read()
    f.close()
    return re.split('\n', text)

def uploadLex():
    fileHandler = tkFileDialog.askopenfilename()
    lexicon = lexEncode.encode(fileHandler, "/home/freddie/PycharmProjects/iGEM/codeRecord", "/home/freddie/PycharmProjects/iGEM/gBlocks")
    currentLexicon = fileHandler
    infoDisplay.delete('0.0', 'end')
    infoDisplay.insert(END, "The current lexicon is: " + currentLexicon + "\n")
    infoDisplay.insert(END, '\n')
    for eachWord in lexicon:
        infoDisplay.insert(END, '>' + str(eachWord[0]) + ' AB \n')
        infoDisplay.insert(END, str(eachWord[1]) + '\n')
        infoDisplay.insert(END, '>' + str(eachWord[0]) + ' BA \n')
        infoDisplay.insert(END, str(eachWord[2]) + '\n')

def encodeData():
    fileHandler = tkFileDialog.askopenfilename()
    infoDisplay.delete('0.0', 'end')
    infoDisplay.insert(END, "File: " + fileHandler + ", encoded with: " + currentLexicon + " is:" + "\n")
    infoDisplay.insert(END, '\n')
    encodedSentences = createSentence.storeInSeq(fileHandler, lexicon)
    sentenceCount = 0
    for eachSentenceSeq in encodedSentences:
        infoDisplay.insert(END, ">sentence" + str(sentenceCount) + " from " + fileHandler + "\n")
        infoDisplay.insert(END, str(eachSentenceSeq) + ' \n')
        infoDisplay.insert(END, '\n')
        sentenceCount = sentenceCount + 1
    decoded = [decoding.universalLookup(sentence, lexicon) for sentence in encodedSentences]
    decodedWithHangs = map(lambda x: zip([n%2 for n in xrange(0,len(x))], x), decoded)
    decodedWithTextHangs = [map(hangify, assemblyPath) for assemblyPath in decodedWithHangs]
    sentenceCount = 0
    for eachAssemblyPath in decodedWithTextHangs:
        infoDisplay.insert(END, "assembly path for sentence" + str(sentenceCount) + " from " + fileHandler + "\n")
        infoDisplay.insert(END, stringifyAssemblyPath(eachAssemblyPath)[:len(stringifyAssemblyPath(eachAssemblyPath))-1] + '\n')
        sentenceCount = sentenceCount + 1

def hangify(assemblyTuple):
    if assemblyTuple[0] == 0:
        return ('AB', assemblyTuple[1])
    else:
        return ('BA', assemblyTuple[1])

def stringifyAssemblyPath(assemblyPath):
    return " ".join([str(assemblyTuple[1]) + " " + str(assemblyTuple[0]) + " >" for assemblyTuple in assemblyPath])

def decode():
    fileHandler = tkFileDialog.askopenfilename()
    infoDisplay.delete('0.0', 'end')
    backToText = decoding.decodeControl(fileHandler, lexicon)
    infoDisplay.insert(END, "File: " + fileHandler + ", decoded with: " + currentLexicon + " is:" + "\n")
    infoDisplay.insert(END, '\n')
    for eachSentence in backToText:
        infoDisplay.insert(END, stringifyDecode(eachSentence) + "\n")

def stringifyDecode(decodedSentence):
    return " ".join(decodedSentence[0])

help = Button(frmMain, text="ReadMe", command=getHelp, width=22, justify=CENTER)
help.grid(row=1, column=0)
lexUpload = Button(frmMain, text="Upload lexicon file", command=uploadLex, width=22, justify=CENTER)
lexUpload.grid(row=2, column=0)
encode = Button(frmMain, text="Upload a file to encode \n using the selected lexicon", command=encodeData, width=22, justify=CENTER)
encode.grid(row=3, column=0)
decode = Button(frmMain, text="Upload a file to decode", command=decode, width=22, justify=CENTER)
decode.grid(row=4, column=0)

footer = Label(frmMain, text="The University of Edinburgh Undergraduate iGEM Team 2016: BabblED")
footer.grid(row=5, column=0, columnspan=2)

frmMain.mainloop()
