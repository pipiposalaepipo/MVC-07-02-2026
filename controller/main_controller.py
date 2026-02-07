
from tkinter import messagebox 
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
        
        
        if self.selected_citizen and self.selected_shelter:
            try:
                
                self.service.assign_citizen(
                    self.selected_citizen.citizen_id, 
                    shelter.shelter_id
                )
                
           
                print(f"บันทึกสำเร็จ: {shelter.name}")
                self.view.show_frame("ResultPage")
                
            except ValueError as e:
              
                messagebox.showerror("ไม่สามารถลงทะเบียนได้", str(e))
              
                self.selected_shelter = None

    def get_shelter(self):
        return self.selected_shelter