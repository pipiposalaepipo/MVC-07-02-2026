import tkinter as tk
from tkinter import ttk

class ResultPage(tk.Frame):
    def __init__(self, parent, controller, main_window):
        super().__init__(parent)
        self.controller = controller
        self.main_window = main_window

      
        tk.Label(self, text="สรุปผลการดำเนินงาน (Dashboard)", font=("Arial", 20, "bold")).pack(pady=15)

       
        self.msg_label = tk.Label(self, text="", font=("Arial", 12), fg="blue")
        self.msg_label.pack(pady=5)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

    
        self.tab_assigned = tk.Frame(self.notebook)
        self.notebook.add(self.tab_assigned, text="✅ ได้รับที่พักแล้ว (Assigned)")
        
        self.tab_unassigned = tk.Frame(self.notebook)
        self.notebook.add(self.tab_unassigned, text="⚠️ ผู้ตกค้าง (Unassigned)")

     
        cols_assign = ("Citizen", "Shelter", "Risk")
        self.tree_assigned = ttk.Treeview(self.tab_assigned, columns=cols_assign, show="headings", height=10)
        self.tree_assigned.heading("Citizen", text="ชื่อประชาชน")
        self.tree_assigned.heading("Shelter", text="พักที่ศูนย์")
        self.tree_assigned.heading("Risk", text="ประเภทศูนย์")
        
     
        self.tree_assigned.column("Citizen", width=150)
        self.tree_assigned.column("Shelter", width=150)
        self.tree_assigned.column("Risk", width=80)
  
        scroll_y1 = ttk.Scrollbar(self.tab_assigned, orient="vertical", command=self.tree_assigned.yview)
        self.tree_assigned.configure(yscrollcommand=scroll_y1.set)
        scroll_y1.pack(side="right", fill="y")
        self.tree_assigned.pack(fill="both", expand=True)

        cols_unassign = ("Name", "Category", "Health")
        self.tree_unassigned = ttk.Treeview(self.tab_unassigned, columns=cols_unassign, show="headings", height=10)
        self.tree_unassigned.heading("Name", text="ชื่อ-สกุล")
        self.tree_unassigned.heading("Category", text="กลุ่ม")
        self.tree_unassigned.heading("Health", text="สุขภาพ")

        scroll_y2 = ttk.Scrollbar(self.tab_unassigned, orient="vertical", command=self.tree_unassigned.yview)
        self.tree_unassigned.configure(yscrollcommand=scroll_y2.set)
        scroll_y2.pack(side="right", fill="y")
        self.tree_unassigned.pack(fill="both", expand=True)

     
        tk.Button(self, text="กลับหน้าแรก (Home)", bg="#FF9800", fg="white", font=("Arial", 12),
                  command=lambda: main_window.show_frame("CitizenPage")).pack(pady=15)

    def update_data(self):
        
        c = self.controller.get_citizen()
        s = self.controller.get_shelter()
        if c and s:
            self.msg_label.config(text=f"ล่าสุด: คุณ {c.full_name} -> เข้าพักที่ {s.name}")
        else:
            self.msg_label.config(text="รอการทำรายการ...")

      
        for item in self.tree_assigned.get_children():
            self.tree_assigned.delete(item)
            
        assigned_list = self.controller.get_service().get_assignment_details()
        for data in assigned_list:
            self.tree_assigned.insert("", "end", values=(
                data['citizen_name'], 
                data['shelter_name'], 
                data['risk']
            ))

       
        for item in self.tree_unassigned.get_children():
            self.tree_unassigned.delete(item)
            
        unassigned_list = self.controller.get_service().get_unassigned_citizens()
        for p in unassigned_list:
            self.tree_unassigned.insert("", "end", values=(
                p.full_name, 
                p.category,
                p.health_status
            ))