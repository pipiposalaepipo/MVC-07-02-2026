import tkinter as tk
from view.page_citizen import CitizenPage
from view.page_shelter import ShelterPage
from view.page_result import ResultPage

class MainWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller 
        
        self.title("ระบบจัดสรรที่หลบภัยฉุกเฉิน (Shelter System)")
        
        
        self.geometry("1200x800") 
        

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        for F in (CitizenPage, ShelterPage, ResultPage):
            page_name = F.__name__
            frame = F(parent=container, controller=controller, main_window=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("CitizenPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise() 
        if hasattr(frame, 'update_data'):
            frame.update_data()