import tkinter as tk
from tkinter import ttk, messagebox

class CitizenPage(tk.Frame):
    def __init__(self, parent, controller, main_window):
        super().__init__(parent)
        self.controller = controller
        self.main_window = main_window 

        tk.Label(self, text="ขั้นตอนที่ 1: รายชื่อประชาชน", font=("Arial", 20)).pack(pady=20)

        filter_frame = tk.Frame(self)
        filter_frame.pack(pady=5)
        tk.Label(filter_frame, text="กรองประเภท: ").pack(side="left")
        self.category_cb = ttk.Combobox(filter_frame, values=["All", "General", "Vulnerable", "VIP"])
        self.category_cb.current(0)
        self.category_cb.pack(side="left")
        self.category_cb.bind("<<ComboboxSelected>>", self.filter_table)


        cols = ("ID", "Name", "Age", "Health", "Category")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=15)
        for c in cols: self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True, padx=20)

       
        tk.Button(self, text="ถัดไป >", bg="#4CAF50", fg="white", font=("Arial", 12),
                  command=self.go_next).pack(pady=20)
        
       
        self.update_data()

    def update_data(self):
  
        self.all_citizens = self.controller.get_service().get_unassigned_citizens()
        self.refresh_table(self.all_citizens)

    def refresh_table(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for c in data:
            self.tree.insert("", "end", values=(c.citizen_id, c.full_name, c.age, c.health_status, c.category))

    def filter_table(self, event):
        cat = self.category_cb.get()
        filtered = [c for c in self.all_citizens if cat == "All" or c.category == cat]
        self.refresh_table(filtered)

    def go_next(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("เตือน", "กรุณาเลือกชื่อประชาชนก่อนครับ")
            return
        
        c_id = self.tree.item(selected[0])['values'][0]
        citizen_obj = next((c for c in self.all_citizens if c.citizen_id == c_id), None)
        
        
        self.controller.set_citizen(citizen_obj)
       
        self.main_window.show_frame("ShelterPage")