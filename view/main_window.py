# view/main_window.py
import tkinter as tk
from view.page_citizen import CitizenPage
from view.page_shelter import ShelterPage
from view.page_result import ResultPage

class MainWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller # เก็บ controller ไว้ใช้งาน
        
        self.title("ระบบจัดสรรที่หลบภัยฉุกเฉิน (Shelter System)")
        self.geometry("900x600")

        # Container สำหรับวางหน้าต่างๆ
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        # วนลูปสร้างหน้าทั้ง 3 หน้าเก็บไว้ใน Memory
        for F in (CitizenPage, ShelterPage, ResultPage):
            page_name = F.__name__
            # ส่ง controller ไปให้แต่ละหน้าด้วย
            frame = F(parent=container, controller=controller, main_window=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("CitizenPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise() # ยกหน้านั้นขึ้นมาแสดง
        
        # ถ้าหน้านั้นมีฟังก์ชัน update_data ให้เรียกทำงานด้วย (เพื่อรีเฟรชข้อมูล)
        if hasattr(frame, 'update_data'):
            frame.update_data()