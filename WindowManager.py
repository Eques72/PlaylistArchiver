
import re
import tkinter as tk
import tkinter.font as tkF
import tkinter.filedialog as fd
from PlaylistManager import PlaylistManager
import os
from tkinter import ttk
from datetime import datetime

class WindowManager:

    __winDefaultHeight = 600
    __winDefaultWidth = 800
    __winToScreenRatio = 0.8
    __color_main = "#2c2c2c"#"#272822"
    __color_activate = "#262726"#"#666960"#"#7a7b75"
    __color_inactive = "#f40532"#"#404239"#"#3d3e38"
    __main_font = "Impact"

    def __init__(self, startFullscreen: bool):
        self.window = tk.Tk()
        screen_width = int(self.window.winfo_screenwidth() * WindowManager.__winToScreenRatio)
        screen_height = int(self.window.winfo_screenheight() * WindowManager.__winToScreenRatio)
        self.window.geometry(f"{screen_width}x{screen_height}+{0}+{0}")
        if startFullscreen:
            self.window.state('zoomed')
        
        self.window.title("YouTube Playlist Archiver")
        self.window.minsize(WindowManager.__winDefaultWidth,WindowManager.__winDefaultHeight)
        self.window.maxsize(screen_width,screen_height)

        self.mainFrame = tk.LabelFrame(self.window, bg=WindowManager.__color_main)
        self.mainFrame.pack(fill="both",expand=True)
        self.state = tk.IntVar()
        self.checkbox_var_list = []
        self.file_loaded = False

        self.window.option_add("*Font", "Helvetica 12 bold")
        self.window.option_add("*Foreground", "white")
        self.window.option_add("*Background", WindowManager.__color_inactive)
        self.window.option_add("*ActiveBackground", WindowManager.__color_activate) #dont work fsr
        self.window.option_add("*Relief", "sunken")

        self.window.option_add("*Entry.Foreground", WindowManager.__color_activate)
        self.window.option_add("*Entry.Background", "white")
        self.window.option_add("*Radiobutton.Background", WindowManager.__color_activate)
        self.window.option_add("*Radiobutton.Foreground", "white")
    def run_window_loop(self):
        self.window.mainloop()

    # ===================================== Views =====================================
    def create_starting_view(self):
        for widget in self.mainFrame.winfo_children():
                widget.destroy()

        self.mainFrame.destroy()
        self.mainFrame = tk.LabelFrame(self.window, bg=WindowManager.__color_main)
        self.mainFrame.pack(fill="both",expand=True)

        self.window.configure(cursor="arrow")
        self.file_loaded = False
        self.checkbox_var_list = []
        self.state = tk.IntVar()

        for i in range(3):
            self.mainFrame.columnconfigure(i, weight=2 if i != 1 else 5, uniform='column')
        for i in range(7):
            self.mainFrame.rowconfigure(i, weight=1, uniform='row')

        buttonNew = tk.Button(self.mainFrame, 
            text="Archive new playlist", 
            command=self.create_new_list_view,
            bd=10,
            font=tkF.Font(family="Helvetica",size=20,weight="bold"),
            activebackground=WindowManager.__color_activate
            )
        buttonNew.grid(column=1, row=1, sticky=tk.NSEW)

        buttonUpdate = tk.Button(self.mainFrame, 
            text="Update existing playlist archive", 
            command=self.create_update_list_view,
            bd=10,
            font=tkF.Font(family="Helvetica",size=20,weight="bold"),
            activebackground=WindowManager.__color_activate
            )
        buttonUpdate.grid(column=1, row=3,sticky=tk.NSEW)

        buttonExport = tk.Button(self.mainFrame, 
            text="Export playlist to Spotify", 
            command=self.create_export_view,
            bd=10,
            font=tkF.Font(family="Helvetica",size=20,weight="bold"),
            activebackground=WindowManager.__color_activate
            )
        buttonExport.grid(column=1, row=5,sticky=tk.NSEW)

    def create_export_view(self):
        for widget in self.mainFrame.winfo_children():
            widget.destroy()

        for i in range(7):
            self.mainFrame.grid_rowconfigure(index=i, weight=[5, 5, 5, 3, 3, 3, 26][i], uniform='row')
        self.mainFrame.grid_columnconfigure(index=0, weight=10, uniform='column')
        self.mainFrame.grid_columnconfigure(index=1, weight=90, uniform='column')
        self.mainFrame.grid_columnconfigure(index=3, weight=10, uniform='column')

        playlist_manager = PlaylistManager()

        self.create_back_button(self.mainFrame)

        fileFrame = tk.LabelFrame(self.mainFrame, bg =WindowManager.__color_main, border=3)
        tk.Button(fileFrame, text="Open Playlist Archive", command=lambda: self.open_file(playlist_manager, fileFrame, True)).pack(padx=10, pady=15)
        fileFrame.grid(column=1, row=1,sticky=tk.NSEW)

        self.title_label = tk.Label(self.mainFrame, text="Playlist : _ , made by: _", anchor="w")
        self.title_label.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        self.description_label = tk.Label(self.mainFrame, text="Playlist description: _", anchor="w")
        self.description_label.grid(row=4, column=1, sticky="w", padx=10, pady=5)

        self.item_count_label = tk.Label(self.mainFrame, text="Items in playlist: 0", anchor="w")
        self.item_count_label.grid(row=5, column=1, sticky="w", padx=10, pady=5)

        tk.Button(self.mainFrame, text="Export to Spotify", command=lambda: self.request_export(playlist_manager)).grid(column=1, row=2,sticky=tk.NSEW)

    def create_new_list_view(self):
        for widget in self.mainFrame.winfo_children():
                widget.destroy()

        for i in range(3):
            self.mainFrame.grid_columnconfigure(index=i, weight=1 if i != 1 else 8, uniform='column')
        for i in range(6):
            self.mainFrame.grid_rowconfigure(index=i, weight=1 if i == 0 or i == 5 else 2, uniform='row')

        self.create_back_button(self.mainFrame)

        frameAddress = tk.LabelFrame(self.mainFrame, bg =WindowManager.__color_main, border=3)# .grid(column=1, row=1,sticky=tk.NSEW)
        frameAddress.grid_columnconfigure(index=0,weight=1,uniform='columnA')
        frameAddress.grid_rowconfigure(index=0,weight=2,uniform='rowA') 
        frameAddress.grid_rowconfigure(index=1,weight=1,uniform='rowA') 

        label = tk.Label(frameAddress, text="Enter Youtube playlist Url:") #background=WindowManager.__color_main, foreground="#ffffff",
        label.grid(column=0,row=0,columnspan=2, sticky=tk.NSEW, padx=10, pady=5)   

        addressEntry = tk.Entry(frameAddress)
        addressEntry.grid(column=0,row=1,columnspan=2,sticky=tk.NSEW, padx=10, pady=5)

        frameAddress.grid(column=1, row=1,sticky=tk.NSEW)

        frameRadio = tk.LabelFrame(self.mainFrame, bg =WindowManager.__color_main, border=3)
        frameRadio.grid_columnconfigure(index=0,weight=1,uniform='columnR')
        frameRadio.grid_columnconfigure(index=1,weight=1,uniform='columnR')
        frameRadio.grid_rowconfigure(index=0,weight=1,uniform='rowR') 

        tk.Radiobutton(frameRadio, 
            text="Every playlist from a channel", font=(WindowManager.__main_font, 12),
            variable=self.state, value=1).grid(column=0,row=0,sticky=tk.NSEW, padx=10, pady=5) 
        tk.Radiobutton(frameRadio, 
            text="Single playlist", font=(WindowManager.__main_font, 12),
            variable=self.state, value=0).grid(column=1,row=0,sticky=tk.NSEW, padx=10, pady=5)

        frameRadio.grid(column=1, row=2,sticky=tk.NSEW)

        self.state.trace_add("write", lambda *args: self.update_label(label))

        frameCheck = tk.LabelFrame(self.mainFrame, bg =WindowManager.__color_main, border=3)
        frameCheck.grid_columnconfigure(index=0,weight=1,uniform='columnC')
        frameCheck.grid_columnconfigure(index=1,weight=1,uniform='columnC')
        frameCheck.grid_rowconfigure(index=0,weight=1,uniform='rowC') 
        frameCheck.grid_rowconfigure(index=1,weight=1,uniform='rowC') 
        frameCheck.grid_rowconfigure(index=2,weight=1,uniform='rowC') 

        options = ["Author channel address","Video author","Video description","Upload date","Video thumbnail Url"]
        for i in range(0,len(options)):
            chbtt = tk.Checkbutton(frameCheck, text=options[i])
            checkVar = tk.BooleanVar()
            self.checkbox_var_list.append(checkVar)
            chbtt.config(variable=self.checkbox_var_list[i], onvalue=True,offvalue=False)
            chbtt.grid(column=0 if i < len(options)/2 else 1,row=i%3,sticky=tk.NSEW, padx=10, pady=5)

        frameCheck.grid(column=1, row=3,sticky=tk.NSEW)

        frameSave = tk.LabelFrame(self.mainFrame, bg =WindowManager.__color_main, border=3)
        frameSave.grid_columnconfigure(index=0,weight=1,uniform='columnS')
        frameSave.grid_rowconfigure(index=0,weight=1,uniform='rowS') 
        frameSave.grid_rowconfigure(index=1,weight=2,uniform='rowS') 

        tk.Button(frameSave, text="Record Playlist",command=lambda: self.record_playlist(addressEntry.get())).grid(column=0,row=1,sticky=tk.NSEW, padx=10, pady=5)

        frameSave.grid(column=1, row=4,sticky=tk.NSEW)

    def create_update_list_view(self):
        for widget in self.mainFrame.winfo_children():
                widget.destroy()

        weights = [10, 90, 10]
        for i, weight in enumerate(weights):
            self.mainFrame.grid_columnconfigure(index=i, weight=weight, uniform='column')

        weights = [5, 15, 10, 80, 15, 10, 5]
        for i, weight in enumerate(weights):
            self.mainFrame.grid_rowconfigure(index=i, weight=weight, uniform='row')

        self.filepath = ""
        playlist_manager = PlaylistManager()

        self.create_back_button(self.mainFrame)

        fileFrame = tk.LabelFrame(self.mainFrame, bg =WindowManager.__color_main, border=3)
        tk.Button(fileFrame, text="Open Playlist Archive", command=lambda: self.open_file_and_update(playlist_manager)).pack(padx=10, pady=15)
        fileFrame.grid(column=1, row=1,sticky=tk.NSEW)

        statusFrame = tk.LabelFrame(self.mainFrame, bg =WindowManager.__color_main, border=3)
        statusFrame.grid_columnconfigure(index=0,weight=1,uniform='column') 
        statusFrame.grid_columnconfigure(index=1,weight=1,uniform='column') 

        tk.Label(statusFrame, text="Loaded playlist archive: ").grid(column=0,row=0,sticky=tk.NSEW)
        self.statusLabel = tk.Label(statusFrame, text="None")
        self.statusLabel.grid(column=1,row=0,padx=5,sticky=tk.NSEW)
        statusFrame.grid(column=1, row=2,sticky=tk.NSEW)

        optionsFrame = tk.LabelFrame(self.mainFrame, bg =WindowManager.__color_main, border=3)
       # optionsFrame.grid_columnconfigure(index=[0,1,2],weight=1,uniform='column') 

        update_options = [tk.IntVar(),tk.IntVar(),tk.IntVar()]
        cb1 = tk.Checkbutton(optionsFrame, text="Remove unavailable videos from archive") 
        cb1.config(variable=update_options[0], onvalue=True,offvalue=False)
        # cb1.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        cb2 = tk.Checkbutton(optionsFrame, text="Add new videos to archive")
        cb2.config(variable=update_options[1], onvalue=True,offvalue=False)
        # cb2.grid(row=0, column=1, padx=5, pady=5)
        cb2.select()
        cb3 = tk.Checkbutton(optionsFrame, text="Override archive file")
        cb3.config(variable=update_options[2], onvalue=True,offvalue=False)
        # cb3.grid(row=0, column=2, padx=5, pady=5,sticky=tk.E)
        cb1.pack( padx=5, pady=5, anchor=tk.W, side=tk.TOP)
        cb2.pack(padx=5, pady=5, anchor="center", side=tk.TOP)
        cb3.pack(padx=5, pady=5, anchor=tk.E, side=tk.TOP)

        optionsFrame.grid(column=1, row=4,sticky=tk.NSEW)

        confirmFrame = tk.LabelFrame(self.mainFrame, bg =WindowManager.__color_main, border=3)
        tk.Button(confirmFrame, text="Confirm and Update", command=lambda: self.do_update(update_options, playlist_manager, self.filepath)).pack(fill='both')
        confirmFrame.grid(column=1, row=5,sticky=tk.NSEW)         

    # ===================================== Actions =====================================
    def update_label(self, label: tk.Label):
        text = ""
        if(self.state.get() == 0):
            text = "Enter Youtube playlist Url:"
        else:
            text = "Enter Youtube channel Url:"
        label.configure(text=text)
        pass

    def request_export(self, playlist_manager: PlaylistManager):
        self.disable_interactions()
        try:
            added_elements = playlist_manager.export_to_spotify(safe_to_save=self.file_loaded)
            self.enable_interactions()
            self.create_pop_up("Export successful", f"Playlist exported successfully with {added_elements} elements.")
        except Exception as e:
            print(f'Error: {e}')
            self.create_pop_up("Export failed", "Export failed, returning to main menu", True)
            self.create_starting_view()

    def record_playlist(self, addressEntered:str):
        if addressEntered == "" or not re.match(r'^https://www\.youtube\.com/playlist', addressEntered):
            self.create_pop_up("Invalid address", "Please enter a valid address")
            return
        playlist_manager = PlaylistManager()
        choices = playlist_manager.default_video_params.copy()
        
        self.disable_interactions()
        for i in range(0,len(self.checkbox_var_list)):
            choices[list(choices.keys())[i]] = self.checkbox_var_list[i].get()
        try:
            if self.state.get() == 1:
                playlist_manager.create_multiple_new_playlist_records(addressEntered, choices)
                pass
            elif self.state.get() == 0:
                playlist_manager.create_new_playlist_record(addressEntered, choices)
                pass

            file_path = fd.asksaveasfilename(filetypes=[("Plik JSON","*.json")], defaultextension = "*.json", 
                                            initialdir = "C:/", title = "Choose save location and file name", 
                                            initialfile = playlist_manager.get_playlist_name())

            success = False
            if self.state.get() == 1:
                success = playlist_manager.save_multiple_playlist_records(file_path)
            if self.state.get() == 0:
                success = playlist_manager.save_playlist_record(file_path, remove_from_list=True)
            if success:
                self.enable_interactions()
                self.create_pop_up("Successfully created a playlist archive", f"File created in: {file_path}")
            else:
                self.create_pop_up("Save failed", "Archive creation failed, returning to main menu", return_not_confirm=True)
            self.create_starting_view()
        except Exception as e:
            print(f'Error: {e}')
            self.create_pop_up("Creation Failed", "Error when creating new archives, returning to main menu", True)
            self.create_starting_view()

    def open_file(self, playlist_manager: PlaylistManager, frame: tk.LabelFrame, is_export: bool = False):
        self.file_loaded = False
        filename = ""

        filename = fd.askopenfilename(
            initialdir="C:", 
            title="Open Playlist", 
            filetypes=[("JSON Files", "*.json*")],
            defaultextension = "*.json"
            )
        try:
            playlist_manager.reset()
            playlist_manager.load_playlist_record(filename)
            pl_info = playlist_manager.get_playlist_basic_info()
            tk.Label(frame, text=str(pl_info)).pack(padx=10, pady=15)
            self.file_loaded = True
            if is_export:
                self.title_label.config(text=f"Playlist : {pl_info['title']} , made by: {pl_info['channelId']}")
                self.description_label.config(text=f"Playlist description: {pl_info['description']}")
                self.item_count_label.config(text=f"Items in playlist: {pl_info['itemCount']}")
        except Exception as e:
            print(f'Error: {e}')
            self.create_pop_up("IO Error", "Error when loading a file, returning to main menu", True)
            self.create_starting_view()

    def open_file_and_update(self, playlist_manager: PlaylistManager):
        self.filepath = ""
        self.filepath = fd.askopenfilename(
            initialdir="C:", 
            title="Open Playlist", 
            filetypes=[("JSON Files", "*.json*")],
            defaultextension = "*.json"
            )
        try:
            self.disable_interactions()
            playlist_manager.reset()
            playlist_manager.load_playlist_record(self.filepath)
            n,m,mm = playlist_manager.compare_playlist_record_with_online()
            self.statusLabel.configure(text=playlist_manager.get_playlist_name())
            self.create_treeview_summary(n, m, mm)
            self.enable_interactions()
        except Exception as e:
            print(f'Error: {e}')
            self.create_pop_up("IO Error", "Error when loading a file, returning to main menu", True)
            self.create_starting_view()

    def do_update(self, update_options: list, playlist_manager: PlaylistManager, filepath:str):
        if filepath == "":
            self.create_pop_up("No file loaded", "Please load a file first")
            return
        update_options_bools = []
        self.disable_interactions()
        for i in range(0,len(update_options)):
            update_options_bools.append(update_options[i].get() == 1)
        datetime_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filepath = os.path.splitext(filepath)[0] + ("" if update_options_bools[2] else f"_updated_{datetime_str}") + ".json"
        playlist_manager.update_playlist_record(remove_missing=update_options_bools[0], add_new=update_options_bools[1])
        if playlist_manager.save_playlist_record(filepath, remove_from_list=True):
            self.enable_interactions()
            self.create_pop_up("Update successful", f"Playlist updated successfully and saved to: {filepath}")
        else:
            self.create_pop_up("Update failed", "Playlist update failed, returning to main menu", return_not_confirm=True)
        self.create_starting_view()
    # ===================================== Utils =====================================
    def create_pop_up(self, title:str, message:str, return_not_confirm:bool = False):
        if return_not_confirm:
            tk.messagebox.showwarning(title, message)
        else:
            tk.messagebox.showinfo(title, message)

    def create_back_button(self, frame):
        button = tk.Button(frame, text="Back", command=self.create_starting_view)
        button.grid(column=1, row=0, sticky=tk.NW)             

    def create_treeview_summary(self, n, m, mm):
        treeviewsFrame = tk.LabelFrame(self.mainFrame, border=1)
        treeviewsFrame.grid_columnconfigure(index=0, weight=1, uniform='column')
        weights = [8,30,8,30,8,25]
        for i, weight in enumerate(weights):
            treeviewsFrame.grid_rowconfigure(index=i, weight=weight, uniform='row')
        treeviewsFrame.grid(column=1, row=3,sticky=tk.NSEW)

        tree_new_videos = ttk.Treeview(treeviewsFrame, columns=("Column1", "Column2", "Column3"), show='headings')

        tree_scrollbar1 = tk.Scrollbar(tree_new_videos)
        tree_scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scrollbar1.config(command=tree_new_videos.yview)

        tree_new_videos.heading("Column1", text="Index")
        tree_new_videos.heading("Column2", text="Video Title")
        tree_new_videos.heading("Column3", text="Video ID")
        tree_new_videos.column("Column1", stretch=False, width=50)
        tree_new_videos.column("Column2", width=200)
        tree_new_videos.column("Column3", stretch=False, width=200)

        for element in n:
            tree_new_videos.insert("", "end", values=(element["position"], element["title"], element["videoId"]))

        tk.Label(treeviewsFrame, text="New videos in remote playlist:").grid(column=0, row=0,sticky=tk.NSEW)
        tree_new_videos.grid(column=0, row=1,sticky=tk.NSEW)

        tree_missing_videos = ttk.Treeview(treeviewsFrame, columns=("Column1", "Column2", "Column3"), show='headings')
        tree_scrollbar2 = tk.Scrollbar(tree_missing_videos)
        tree_scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scrollbar2.config(command=tree_missing_videos.yview)

        tree_missing_videos.heading("Column1", text="Index")
        tree_missing_videos.heading("Column2", text="Video Title")
        tree_missing_videos.heading("Column3", text="Video ID")
        tree_missing_videos.column("Column1", stretch=False, width=50)
        tree_missing_videos.column("Column2", width=200)
        tree_missing_videos.column("Column3", stretch=False, width=200)

        for element in m:
            tree_missing_videos.insert("", "end", values=(element["position"], element["title"], element["videoId"]))

        tk.Label(treeviewsFrame, text="Videos missing in remote playlist:").grid(column=0, row=2,sticky=tk.NSEW)
        tree_missing_videos.grid(column=0, row=3,sticky=tk.NSEW)   

        tree_mismath = ttk.Treeview(treeviewsFrame, columns=("Column1", "Column2", "Column3", "Column4", "Column5"), show='headings')
        tree_scrollbar3 = tk.Scrollbar(tree_mismath)
        tree_scrollbar3.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scrollbar3.config(command=tree_mismath.yview)

        tree_mismath.heading("Column1", text="Index")
        tree_mismath.heading("Column2", text="Archived Video ID")
        tree_mismath.heading("Column3", text="Remote Video ID")
        tree_mismath.heading("Column4", text="Archived Video Title")
        tree_mismath.heading("Column5", text="Remote Video Title")

        tree_mismath.column("Column1", stretch=False, width=50)
        tree_mismath.column("Column2", stretch=False, width=150)
        tree_mismath.column("Column3", stretch=False, width=150)
        tree_mismath.column("Column4", stretch=True, width=200)
        tree_mismath.column("Column5", stretch=True, width=200)

        for element in mm:
            tree_mismath.insert("", "end", values=(element[0], element[1],element[2],element[3], element[4]))

        tk.Label(treeviewsFrame, text="Mismatched positions:").grid(column=0, row=4,sticky=tk.NSEW)
        tree_mismath.grid(column=0, row=5,sticky=tk.NSEW)

    def disable_interactions(self):
        self.window.configure(cursor="watch")
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Button) or isinstance(widget, tk.Checkbutton) or isinstance(widget, tk.Radiobutton) or isinstance(widget, tk.Entry):
                widget.config(state="disabled")
        self.window.update()

    def enable_interactions(self):
        self.window.configure(cursor="arrow")
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Button) or isinstance(widget, tk.Checkbutton) or isinstance(widget, tk.Radiobutton) or isinstance(widget, tk.Entry):
                widget.config(state="normal")
        self.window.update()

if __name__ == "__main__":
    wM = WindowManager(False)
    wM.create_starting_view()
    wM.run_window_loop()
