from tkinter import *
import search_engine as se
import webbrowser
import functools
import os

class gui:

  def __init__(self):
    messages = []
    output = []
    def search(event):
      output = se.main(self.entry.get())
      self.button['state'] = DISABLED
      self.button.unbind("<Button-1>")
      if len(output) != 0:
        text = ""
        for i in range(0, len(output[:20])):
          text += "Document #" + str(output[i][0]) + " with score " + str(round((output[i][1]), 5)) + "\n"
        self.message_output['text'] = text
        self.message_output.bind("<Button-1>", functools.partial(callback, index = output[0][0]))
        self.nothing['text'] = "Results: " + str(len(output))
      elif len(output) == 0:
        self.nothing['text'] = "No coincidence"
        self.message_output['text'] = ""
        self.message_output.unbind("<Button-1>")
      else:
        self.nothing['text'] = output
        self.message_output['text'] = ""
        self.message_output.unbind("<Button-1>")

    def callback(event, index):
        path = "../Documents/" + str(index) + ".txt"
        os.system("open " + path)

    self.__mainWindow = Tk()
    self.__mainWindow.title("Search Engine")
    self.__mainWindow.geometry('900x600')
    self.frame = Frame(self.__mainWindow)
    self.labelText = 'Enter your query'
    self.label = Label(self.frame, text = self.labelText)
    self.entry = Entry(self.frame, width = 40)
    self.button = Button(self.frame, text = u"Search")
    self.button.bind("<Button-1>", search)
    self.caution = Label(self.frame, text = "If you press on any document number you will open the first suitable one as an example.")
    self.number_of_doc = Label(self.frame)
    self.message_output = Message(self.frame, width = 850, font = 'arial 14', fg = "blue", cursor = "hand2")
    self.nothing = Label(self.frame)
    self.label.pack()
    self.entry.pack()
    self.button.pack()
    self.caution.pack()
    self.nothing.pack()
    self.message_output.pack()
    self.frame.pack()
    mainloop()

gui = gui()