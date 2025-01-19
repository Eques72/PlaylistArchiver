from WindowManager import WindowManager

if __name__ == "__main__":
    wM = WindowManager(False)
    wM.create_starting_view()
    wM.run_window_loop()