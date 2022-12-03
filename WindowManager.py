
import tkinter as tk
import tkinter.font as tkF

class WindowManager:

    __winHeight = 600
    __winWidth = 800
    __colorThemeMain = "#272822"
    __colorThemeLight = "#7a7b75" #When something has focus
    __colorThemeDark = "#3d3e38"  #When something is inactive
    __mainFont = "Impact"

    def __init__(self, startFullscreen: bool):

        self.window = tk.Tk()
        self.window.geometry(str(WindowManager.__winWidth)+"x"+str(WindowManager.__winHeight))
        if startFullscreen:
            self.window.state('zoomed')
        
        self.window.title("YT Playlist Manager")

        self.window.minsize(WindowManager.__winWidth,WindowManager.__winHeight)
        self.window.maxsize(WindowManager.__winWidth,WindowManager.__winHeight)

        self.mainFrame = tk.LabelFrame(self.window, bg=WindowManager.__colorThemeMain)
        self.mainFrame.pack(fill="both",expand=True)
        self.state = tk.IntVar()
        pass

    def createStartingView(self):
        
        for widget in self.mainFrame.winfo_children():
                widget.destroy()
        
        self.mainFrame.grid_forget()
        self.mainFrame.columnconfigure(0,weight=2,uniform='column')
        self.mainFrame.columnconfigure(1,weight=5,uniform='column')
        self.mainFrame.columnconfigure(2,weight=2,uniform='column')
        self.mainFrame.rowconfigure(0,weight=1,uniform='row')
        self.mainFrame.rowconfigure(1,weight=1,uniform='row')
        self.mainFrame.rowconfigure(2,weight=1,uniform='row')
        self.mainFrame.rowconfigure(3,weight=1,uniform='row')
        self.mainFrame.rowconfigure(4,weight=1,uniform='row')

        buttonNew = tk.Button(self.mainFrame, 
            text="Document new playlists", 
            command=self.createNewListView,
            bd=10,
            font=tkF.Font(family="Helvetica",size=20,weight="bold"),
            bg=WindowManager.__colorThemeDark,
            activebackground=WindowManager.__colorThemeLight
            )
        buttonNew.grid(column=1, row=1, sticky=tk.NSEW)
        buttonUpdate = tk.Button(self.mainFrame, 
            text="Update existing documentation", 
            command=self.createUpdateListView,
            bd=10,
            font=tkF.Font(family="Helvetica",size=20,weight="bold"),
            bg=WindowManager.__colorThemeDark,
            activebackground=WindowManager.__colorThemeLight
            )
        buttonUpdate.grid(column=1, row=3,sticky=tk.NSEW)
        pass

    def createNewListView(self):
                
        for widget in self.mainFrame.winfo_children():
                widget.destroy()
        
        self.mainFrame.grid_forget()             
        self.mainFrame.grid_columnconfigure(index=0,weight=1,uniform='column') #Padding
        self.mainFrame.grid_columnconfigure(index=1,weight=8,uniform='column') #Content
        self.mainFrame.grid_columnconfigure(index=2,weight=1,uniform='column') #Padding
        self.mainFrame.grid_rowconfigure(index=0,weight=1,uniform='row') #Padding
        self.mainFrame.grid_rowconfigure(index=1,weight=2,uniform='row') #Address
        self.mainFrame.grid_rowconfigure(index=2,weight=2,uniform='row') #RadioButtons - Options
        self.mainFrame.grid_rowconfigure(index=3,weight=2,uniform='row') #CheckButtons - Configuration
        self.mainFrame.grid_rowconfigure(index=4,weight=2,uniform='row') #Saving
        self.mainFrame.grid_rowconfigure(index=5,weight=1,uniform='row') #Padding

        frameAddress = tk.LabelFrame(self.mainFrame, bg =WindowManager.__colorThemeMain, border=3)# .grid(column=1, row=1,sticky=tk.NSEW)
        frameAddress.grid_columnconfigure(index=0,weight=1,uniform='columnA')
        frameAddress.grid_rowconfigure(index=0,weight=2,uniform='rowA') 
        frameAddress.grid_rowconfigure(index=1,weight=1,uniform='rowA') 
        tk.Label(frameAddress,background=WindowManager.__colorThemeMain, foreground="#ffffff", text="Enter Youtube channel or Youtube playlist html address:").grid(column=0,row=0,columnspan=2, sticky=tk.NSEW, padx=10, pady=5)   
        tk.Entry(frameAddress, ).grid(column=0,row=1,columnspan=2,sticky=tk.NSEW, padx=10, pady=5)
        frameAddress.grid(column=1, row=1,sticky=tk.NSEW)

        frameRadio = tk.LabelFrame(self.mainFrame, bg =WindowManager.__colorThemeMain, border=3)
        frameRadio.grid_columnconfigure(index=0,weight=1,uniform='columnR')
        frameRadio.grid_columnconfigure(index=1,weight=1,uniform='columnR')
        frameRadio.grid_rowconfigure(index=0,weight=1,uniform='rowR') 
        
        tk.Radiobutton(frameRadio, 
            text="All playlist form the channel", font=(WindowManager.__mainFont, 12),
            variable=self.state, value=1).grid(column=0,row=0,sticky=tk.NSEW, padx=10, pady=5) 
        tk.Radiobutton(frameRadio, 
            text="One playlist", font=(WindowManager.__mainFont, 12),
            variable=self.state, value=0).grid(column=1,row=0,sticky=tk.NSEW, padx=10, pady=5)
        
        frameRadio.grid(column=1, row=2,sticky=tk.NSEW)

        frameCheck = tk.LabelFrame(self.mainFrame, bg =WindowManager.__colorThemeMain, border=3)
        frameCheck.grid_columnconfigure(index=0,weight=1,uniform='columnC')
        frameCheck.grid_columnconfigure(index=1,weight=1,uniform='columnC')
        frameCheck.grid_rowconfigure(index=0,weight=1,uniform='rowC') 
        frameCheck.grid_rowconfigure(index=1,weight=1,uniform='rowC') 
        frameCheck.grid_rowconfigure(index=2,weight=1,uniform='rowC') 
        frameCheck.grid_rowconfigure(index=3,weight=1,uniform='rowC') 
        options = ["Video name","Video address","Video author", "Playlist info","Video description","Upload date","Video thumbnail url",  "Playlist author"]
        for i in range(0,len(options)):
            chbtt = tk.Checkbutton(frameCheck, text=options[i])
            if i <= 3:
                chbtt.select()
                chbtt.grid(column=0,row=i,sticky=tk.NSEW, padx=10, pady=5)
            else:
                chbtt.grid(column=1,row=i-4,sticky=tk.NSEW, padx=10, pady=5)

        frameCheck.grid(column=1, row=3,sticky=tk.NSEW)
        
        frameSave = tk.LabelFrame(self.mainFrame, bg =WindowManager.__colorThemeMain, border=3)
        frameSave.grid_columnconfigure(index=0,weight=1,uniform='columnS')
        frameSave.grid_rowconfigure(index=0,weight=1,uniform='rowS') 
        frameSave.grid_rowconfigure(index=1,weight=2,uniform='rowS') 
        tk.Entry(frameSave).grid(column=0,row=0,sticky=tk.NSEW, padx=10, pady=5)
        tk.Button(frameSave, text="Get and Save").grid(column=0,row=1,sticky=tk.NSEW, padx=10, pady=5)
        frameSave.grid(column=1, row=4,sticky=tk.NSEW)

        pass

    def createUpdateListView(self):
        pass

    def runWindowLoop(self):
        self.window.mainloop()
        pass

    
wM = WindowManager(False)
wM.createStartingView()
wM.runWindowLoop()
