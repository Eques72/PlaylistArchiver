
import random
import tkinter as tk
import tkinter.font as tkF
import tkinter.filedialog as fd
from PlaylistManager import PlaylistManager
from tkinter import ttk

class WindowManager:

    __winDefaultHeight = 600
    __winDefaultWidth = 800
    __winToScreenRatio = 0.8
    __colorThemeMain = "#272822"
    __colorThemeLight = "#7a7b75" #When something has focus
    __colorThemeDark = "#3d3e38"  #When something is inactive
    __mainFont = "Impact"

    def __init__(self, startFullscreen: bool):

        self.window = tk.Tk()
        screen_width = int(self.window.winfo_screenwidth() * WindowManager.__winToScreenRatio)
        screen_height = int(self.window.winfo_screenheight() * WindowManager.__winToScreenRatio)
        self.window.geometry(f"{screen_width}x{screen_height}+{0}+{0}")
        if startFullscreen:
            self.window.state('zoomed')
        
        self.window.title("YouTube Playlist Manager")

        self.window.minsize(WindowManager.__winDefaultWidth,WindowManager.__winDefaultHeight)
        self.window.maxsize(screen_width,screen_height)

        self.mainFrame = tk.LabelFrame(self.window, bg=WindowManager.__colorThemeMain)
        self.mainFrame.pack(fill="both",expand=True)
        self.state = tk.IntVar()
        self.checkVarList = []
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

    def update_label(self, label: tk.Label):
        text = ""
        if(self.state.get() == 0):
            text = "Enter Youtube playlist Url:"
        else:
            text = "Enter Youtube channel Url:"
        label.configure(text=text)
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
        label = tk.Label(frameAddress,background=WindowManager.__colorThemeMain, foreground="#ffffff", text="Enter Youtube playlist Url:")
        label.grid(column=0,row=0,columnspan=2, sticky=tk.NSEW, padx=10, pady=5)   
        addressEntry = tk.Entry(frameAddress)
        addressEntry.grid(column=0,row=1,columnspan=2,sticky=tk.NSEW, padx=10, pady=5)
        frameAddress.grid(column=1, row=1,sticky=tk.NSEW)

        frameRadio = tk.LabelFrame(self.mainFrame, bg =WindowManager.__colorThemeMain, border=3)
        frameRadio.grid_columnconfigure(index=0,weight=1,uniform='columnR')
        frameRadio.grid_columnconfigure(index=1,weight=1,uniform='columnR')
        frameRadio.grid_rowconfigure(index=0,weight=1,uniform='rowR') 
        
        tk.Radiobutton(frameRadio, 
            text="Every playlist from a channel", font=(WindowManager.__mainFont, 12),
            variable=self.state, value=1).grid(column=0,row=0,sticky=tk.NSEW, padx=10, pady=5) 
        tk.Radiobutton(frameRadio, 
            text="Single playlist", font=(WindowManager.__mainFont, 12),
            variable=self.state, value=0).grid(column=1,row=0,sticky=tk.NSEW, padx=10, pady=5)
        
        frameRadio.grid(column=1, row=2,sticky=tk.NSEW)

        self.state.trace_add("write", lambda *args: self.update_label(label))

        frameCheck = tk.LabelFrame(self.mainFrame, bg =WindowManager.__colorThemeMain, border=3)
        frameCheck.grid_columnconfigure(index=0,weight=1,uniform='columnC')
        frameCheck.grid_columnconfigure(index=1,weight=1,uniform='columnC')
        frameCheck.grid_rowconfigure(index=0,weight=1,uniform='rowC') 
        frameCheck.grid_rowconfigure(index=1,weight=1,uniform='rowC') 
        frameCheck.grid_rowconfigure(index=2,weight=1,uniform='rowC') 
        frameCheck.grid_rowconfigure(index=3,weight=1,uniform='rowC') 
        options = ["Video title","Video position","Video address","Author channel address","Video author","Video description","Upload date","Video thumbnail Url"]
        
        for i in range(0,len(options)):
            chbtt = tk.Checkbutton(frameCheck, text=options[i])
            if i <= 2:
                chbtt.select()
                chbtt.config(state='disabled')
            else:
                checkVar = tk.IntVar()
                self.checkVarList.append(checkVar)
                # print(len(self.checkVarList), str(i))
                chbtt.config(variable=self.checkVarList[i-3], onvalue=True,offvalue=False)
                # chbtt = tk.Checkbutton(frameCheck, text=options[i], variable=self.checkVarList[i-2], onvalue=True,offvalue=False)
                # chbtt.grid(column=1,row=i-4,sticky=tk.NSEW, padx=10, pady=5)
            chbtt.grid(column=0 if i < 4 else 1,row=i%4,sticky=tk.NSEW, padx=10, pady=5)

        frameCheck.grid(column=1, row=3,sticky=tk.NSEW)
        
        frameSave = tk.LabelFrame(self.mainFrame, bg =WindowManager.__colorThemeMain, border=3)
        frameSave.grid_columnconfigure(index=0,weight=1,uniform='columnS')
        frameSave.grid_rowconfigure(index=0,weight=1,uniform='rowS') 
        frameSave.grid_rowconfigure(index=1,weight=2,uniform='rowS') 
        #tk.Entry(frameSave).grid(column=0,row=0,sticky=tk.NSEW, padx=10, pady=5)
        tk.Button(frameSave, text="Record Playlist",command=lambda: self.record_playlist(addressEntry.get())).grid(column=0,row=1,sticky=tk.NSEW, padx=10, pady=5)
        frameSave.grid(column=1, row=4,sticky=tk.NSEW)

        pass

    def record_playlist(self, addressEntered:str):
        playlist_manager = PlaylistManager()
        choices = playlist_manager.default_video_params.copy()
        for i in range(0,len(self.checkVarList)):
            choices[list(choices.keys())[i]] = self.checkVarList[i].get()

        if self.state.get() == 1:
            playlist_manager.create_multiple_new_playlist_records(addressEntered, choices)
            pass
        elif self.state.get() == 0:
            playlist_manager.create_new_playlist_record(addressEntered, choices)
            pass

        file_path = fd.asksaveasfilename(filetypes=[("Plik JSON","*.json")], defaultextension = "*.json", 
                                         initialdir = "C:/", title = "Choose save location and file name", 
                                         initialfile = playlist_manager.get_playlist_name())
        # print(file_path)

        if self.state.get() == 1:
            playlist_manager.save_multiple_playlist_records(file_path)
        if self.state.get() == 0:
            playlist_manager.save_playlist_record(file_path, remove_from_list=True)

    def createUpdateListView(self):
        for widget in self.mainFrame.winfo_children():
                widget.destroy()
        
        self.mainFrame.grid_forget()             
        self.mainFrame.grid_columnconfigure(index=0,weight=10,uniform='column') #Padding
        self.mainFrame.grid_columnconfigure(index=1,weight=90,uniform='column') #Content
        self.mainFrame.grid_columnconfigure(index=3,weight=10,uniform='column') #Padding
        self.mainFrame.grid_rowconfigure(index=0,weight=5,uniform='row') #Padding
        self.mainFrame.grid_rowconfigure(index=1,weight=15,uniform='row') #Open file
        self.mainFrame.grid_rowconfigure(index=2,weight=10,uniform='row') #Status
        self.mainFrame.grid_rowconfigure(index=3,weight=30,uniform='row') #New
        self.mainFrame.grid_rowconfigure(index=4,weight=30,uniform='row') #Missing
        self.mainFrame.grid_rowconfigure(index=5,weight=20,uniform='row') #Mismatch ids
        self.mainFrame.grid_rowconfigure(index=6,weight=20,uniform='row') #Select options
        self.mainFrame.grid_rowconfigure(index=7,weight=10,uniform='row') #Confirm
        self.mainFrame.grid_rowconfigure(index=8,weight=5,uniform='row') #Padding

        #Button, invokes method to open playlist file. After that status of the operation or playlist status is displayed in 
         #status frame automatically
        fileFrame = tk.LabelFrame(self.mainFrame, bg =WindowManager.__colorThemeMain, border=3)
        tk.Button(fileFrame, text="Open saved playlist", command=self.openFile).pack(padx=10, pady=15)
        fileFrame.grid(column=1, row=1,sticky=tk.NSEW)
        
        statusFrame = tk.LabelFrame(self.mainFrame, bg =WindowManager.__colorThemeMain, border=3)
        statusFrame.grid_columnconfigure(index=0,weight=1,uniform='column') 
        statusFrame.grid_columnconfigure(index=1,weight=1,uniform='column') 
        tk.Label(statusFrame, text="Status: ").grid(column=0,row=0,sticky=tk.NSEW)
        self.statusLabel = tk.Label(statusFrame, text="None")
        self.statusLabel.grid(column=1,row=0,padx=5,sticky=tk.NSEW)
        statusFrame.grid(column=1, row=2,sticky=tk.NSEW)

        # detailsFrame = tk.LabelFrame(self.mainFrame, bg =WindowManager.__colorThemeMain, border=3)
        # #playlist info from the header and details on included info 
        # detailsFrame.grid(column=1, row=3,sticky=tk.NSEW)

        optionsFrame = tk.LabelFrame(self.mainFrame, bg =WindowManager.__colorThemeMain, border=3)
        #Options for updating. Override or only add to the end, new file or not, force merge or abandon  
        optionsFrame.grid(column=1, row=6,sticky=tk.NSEW)

        confirmFrame = tk.LabelFrame(self.mainFrame, bg =WindowManager.__colorThemeMain, border=3)
        tk.Button(confirmFrame, text="Confirm and Update", command=self.doUpdate).pack(fill='both')
        confirmFrame.grid(column=1, row=7,sticky=tk.NSEW)                        
        
        # Open file
        # Status
        # Details 
        # Select type of update
        # Confirm
        pass
    
    def openFile(self):
        filename = ""
        # print("Debug 1")

        # print("Debug 2")
        filename = fd.askopenfilename(
            initialdir="C:\\Users\\adria\\Desktop", 
            title="Open Playlist", 
            filetypes=[("JSON Files", "*.json*")],
            defaultextension = "*.json"
            )

        playlist_manager = PlaylistManager()
        playlist_manager.load_playlist_record(filename)

        n,m,mm = playlist_manager.compare_playlist_record_with_online()
        # print(n,m,mm)

        tree_new_videos = ttk.Treeview(self.mainFrame, columns=("Column1", "Column2", "Column3"), show='headings')

        tree_scrollbar1 = tk.Scrollbar(tree_new_videos)
        tree_scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scrollbar1.config(command=tree_new_videos.yview)

        tree_new_videos.heading("Column1", text="Index")
        tree_new_videos.heading("Column2", text="Title")
        tree_new_videos.heading("Column3", text="Id")
        tree_new_videos.column("Column1", stretch=False, width=50)
        tree_new_videos.column("Column2", width=200)
        tree_new_videos.column("Column3", stretch=False, width=200)

        for element in n:
            tree_new_videos.insert("", "end", values=(element["position"], element["title"], element["videoId"]))

        tree_new_videos.grid(column=1, row=3,sticky=tk.NSEW)    
###############################
        tree_missing_videos = ttk.Treeview(self.mainFrame, columns=("Column1", "Column2", "Column3"), show='headings')
        tree_scrollbar2 = tk.Scrollbar(tree_missing_videos)
        tree_scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scrollbar2.config(command=tree_missing_videos.yview)

        tree_missing_videos.heading("Column1", text="Index")
        tree_missing_videos.heading("Column2", text="Title")
        tree_missing_videos.heading("Column3", text="Id")
        tree_missing_videos.column("Column1", stretch=False, width=50)
        tree_missing_videos.column("Column2", width=200)
        tree_missing_videos.column("Column3", stretch=False, width=200)

        for element in m:
            tree_missing_videos.insert("", "end", values=(element["position"], element["title"], element["videoId"]))

        tree_missing_videos.grid(column=1, row=4,sticky=tk.NSEW)   
###############################
        tree_mismath = ttk.Treeview(self.mainFrame, columns=("Column1", "Column2", "Column3", "Column4", "Column5"), show='headings')
        tree_scrollbar3 = tk.Scrollbar(tree_mismath)
        tree_scrollbar3.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scrollbar3.config(command=tree_mismath.yview)

        tree_mismath.heading("Column1", text="Index")
        tree_mismath.heading("Column2", text="Id1")
        tree_mismath.heading("Column3", text="Id2")
        tree_mismath.heading("Column4", text="Title1")
        tree_mismath.heading("Column5", text="Title2")

        tree_mismath.column("Column1", stretch=False, width=50)
        tree_mismath.column("Column2", stretch=False, width=150)
        tree_mismath.column("Column3", stretch=False, width=150)
        tree_mismath.column("Column4", stretch=True, width=200)
        tree_mismath.column("Column5", stretch=True, width=200)

        for element in mm:
            tree_mismath.insert("", "end", values=(element[0], element[1],element[2],element[3], element[4]))

        tree_mismath.grid(column=1, row=5,sticky=tk.NSEW)

        # CHECKBOXES: Delete Unavalaible, Add New, Remove or keep missing 


        # if filename.endswith(".txt"):
        #     playlistInfo = caller.readExistingPlaylist(type=1, fileData=data)
        #     if playlistInfo[0] == True:
        #         status = "Correct"
        #     else:
        #         status = "Playlist file corrupted"
        #     #display info
            
        #caller to format
        #callers decides of the status, rest gives formatfactory
        #print(data)        
        # self.statusLabel.configure(text=status)
        pass

    def doUpdate(self):
        #caller.manageExistingPlaylistUpdate(playlistInfo["playlistId"],data,1)
            
        pass

    def runWindowLoop(self):
        self.window.mainloop()
        pass



wM = WindowManager(False)
wM.createStartingView()
wM.runWindowLoop()
