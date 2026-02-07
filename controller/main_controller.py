# controller/main_controller.py
from tkinter import messagebox # เพิ่มบรรทัดนี้เพื่อใช้แจ้งเตือน
from model.service import ShelterService
from view.main_window import MainWindow

class MainController:
    def __init__(self):
        self.service = ShelterService()
        self.selected_citizen = None
        self.selected_shelter = None
        self.view = MainWindow(self)

    def run(self):
        self.view.mainloop()
    
    def get_service(self):
        return self.service

    def set_citizen(self, citizen):
        self.selected_citizen = citizen

    def get_citizen(self):
        return self.selected_citizen

    def set_shelter(self, shelter):
        self.selected_shelter = shelter
        
        # --- ตรวจสอบ Logic ตรงนี้ ---
        if self.selected_citizen and self.selected_shelter:
            try:
                # พยายามบันทึก
                self.service.assign_citizen(
                    self.selected_citizen.citizen_id, 
                    shelter.shelter_id
                )
                
                # ถ้าไม่มี Error ให้เปลี่ยนหน้าไปสรุปผล
                print(f"บันทึกสำเร็จ: {shelter.name}")
                self.view.show_frame("ResultPage")
                
            except ValueError as e:
                # ถ้าติดกฎข้อไหน ให้เด้งแจ้งเตือน และไม่เปลี่ยนหน้า
                messagebox.showerror("ไม่สามารถลงทะเบียนได้", str(e))
                # Reset ค่า Shelter ที่เลือกผิดออกไป
                self.selected_shelter = None

    def get_shelter(self):
        return self.selected_shelter