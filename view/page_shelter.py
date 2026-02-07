import tkinter as tk
from tkinter import ttk, messagebox

class ShelterPage(tk.Frame):
    def __init__(self, parent, controller, main_window):
        super().__init__(parent)
        self.controller = controller
        self.main_window = main_window

        tk.Label(self, text="ขั้นตอนที่ 2: เลือกศูนย์พักพิง", font=("Arial", 20)).pack(pady=20)

        cols = ("ID", "Name", "Location", "Risk", "Occupancy")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=15)
        self.tree.heading("Occupancy", text="สถานะ (คน/ความจุ)")
        for c in ["ID", "Name", "Location", "Risk"]: self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True, padx=20)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="< ย้อนกลับ", command=lambda: main_window.show_frame("CitizenPage")).pack(side="left", padx=10)
        tk.Button(btn_frame, text="ยืนยันการเลือก", bg="#2196F3", fg="white", font=("Arial", 12),
                  command=self.confirm).pack(side="left", padx=10)

    def update_data(self):
        # ดึงข้อมูลจาก Controller -> Service
        service = self.controller.get_service()
        shelters = service.get_all_shelters()
        
        for item in self.tree.get_children():
            self.tree.delete(item)

        for s in shelters:
            curr = service.get_occupancy(s.shelter_id)
            status = f"{curr} / {s.capacity}"
            if curr >= s.capacity: status += " (FULL)"
            
            self.tree.insert("", "end", values=(s.shelter_id, s.name, s.location, s.risk_level, status))

    def confirm(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("เตือน", "เลือกที่พักด้วยครับ")
            return
        
        s_id = self.tree.item(selected[0])['values'][0]
        service = self.controller.get_service()
        shelter_obj = next((s for s in service.get_all_shelters() if s.shelter_id == s_id), None)
        
        # ส่งให้ Controller (Controller จะเป็นคนเช็คกฎ และเปลี่ยนหน้าให้ถ้าผ่าน)
        self.controller.set_shelter(shelter_obj)