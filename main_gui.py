import tkinter.filedialog
import tkinter.messagebox
import tkinter as tk
from gui_run import main


def selectPath():

    global path_
    path_ = tkinter.filedialog.askopenfilename()
    path.set(path_)
    path_ = path_.replace("/","\\\\")

#def filename(
#            title=None,
#            fileName=None,
#            dirName=None,
#            fileExt=".mid",
#            fileTypes=None,
#            asFile=False):
#        if fileTypes is None:
#            fileTypes = [('all files', '.*'), ('midi files', '.mid')]
#        # define options for opening
#        options = {}
#        options['defaultextension'] = fileExt
#        options['filetypes'] = fileTypes
#        options['initialdir'] = dirName
#        options['initialfile'] = fileName
#        options['title'] = title

#        if asFile:
#            filename = tkinter.filedialog.asksaveasfile(mode='w', **options)
#            filename = filename.replace("/","\\\\")
#            print(filename)
#            mid_name.set(filename)
#        # will return "" if cancelled
#        else:
#            filename = tkinter.filedialog.asksaveasfilename(**options)

def run():

    if path_ != "":
        if height.get() >= 1 and height.get() <= 127:
            main(path_, height.get())
        else:
            tk.messagebox.showerror("error", "picture height out of range(0~127)")
    else:
        tk.messagebox.showerror("error", "invalid path")
    

main_box=tk.Tk()

form = tk.Frame(main_box)
form.pack(anchor = "n")

#mid_name = tk.StringVar()
path = tk.StringVar()
path_ = path.get()
height = tk.IntVar()

tk.Label(form, text = "Picture Path ").grid(row = 0, column = 0)
tk.Label(form, text = "Picture height ").grid(row = 1, column = 0)
#tk.Label(form, text = "Filename(.mid) ").grid(row = 2, column = 0)

tk.Entry(form, textvariable = path).grid(row = 0, column = 1)
tk.Entry(form, textvariable = height).grid(row = 1, column = 1)
#tk.Entry(form, textvariable = mid_name).grid(row = 2, column = 1)
tk.Button(form, text = "Browse", command = selectPath).grid(row = 0, column = 2)
tk.Button(form, text = "Run", command = run).grid(row = 1, column = 2)
#tk.Button(form, text = "Browse", command = filename).grid(row = 2, column = 2)
main_box.mainloop()

