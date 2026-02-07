
from model.data_manager import DataManager
from model.entities import Assignment
import datetime

class ShelterService:
    def __init__(self):
        self.data_manager = DataManager()
        self.shelters = self.data_manager.load_shelters()
        self.citizens = self.data_manager.load_citizens()
        self.assignments = self.data_manager.load_assignments()

    def get_all_shelters(self):
        return self.shelters

    def get_occupancy(self, shelter_id):
        count = 0
        for assign in self.assignments:
            if assign.shelter_id == shelter_id:
                count += 1
        return count

    def get_unassigned_citizens(self):
        assigned_ids = {a.citizen_id for a in self.assignments}
        # เรียงลำดับความสำคัญ (Priority Sorting)
        # ให้กลุ่มเปราะบาง (Vulnerable) ขึ้นก่อน, ตามด้วยเรียงตามอายุ (มากไปน้อย)
        unassigned = [c for c in self.citizens if c.citizen_id not in assigned_ids]
        
       
        unassigned.sort(key=lambda c: (c.category != 'Vulnerable', -int(c.age)))
        
        return unassigned

  
    def assign_citizen(self, citizen_id, shelter_id):
        
        citizen = next((c for c in self.citizens if c.citizen_id == citizen_id), None)
        shelter = next((s for s in self.shelters if s.shelter_id == shelter_id), None)
        
        if not citizen or not shelter:
            raise ValueError("ไม่พบข้อมูลประชาชนหรือที่พัก")

        #  ประชาชนหนึ่งคนลงทะเบียนได้เพียงครั้งเดียว
        for assign in self.assignments:
            if assign.citizen_id == citizen_id:
                raise ValueError(f"คุณ {citizen.full_name} ได้ลงทะเบียนไปแล้วครับ")

        #  ศูนย์พักพิงที่เต็มแล้วไม่สามารถรับเพิ่มได้
        current_occupancy = self.get_occupancy(shelter_id)
        if current_occupancy >= int(shelter.capacity):
            raise ValueError(f"เสียใจด้วยครับ {shelter.name} เต็มแล้ว")

        #  ผู้มีความเสี่ยงด้านสุขภาพ ต้องไปศูนย์เสี่ยงต่ำ (Low Risk) เท่านั้น
        # สมมติกลุ่มเสี่ยงคือ 'Chronic' (โรคเรื้อรัง) หรือ 'Critical'
        high_risk_health = ['Chronic', 'Critical', 'Bedridden'] 
        if citizen.health_status in high_risk_health:
            if shelter.risk_level != 'Low':
                raise ValueError(f"สุขภาพของคุณ {citizen.full_name} ({citizen.health_status}) \nต้องพักในศูนย์ความเสี่ยงต่ำ (Low Risk) เท่านั้นครับ")

        new_id = len(self.assignments) + 1
        new_assign = Assignment(new_id, citizen_id, shelter_id, datetime.date.today())
        self.assignments.append(new_assign)
        return True
    def get_assignment_details(self):
        """ดึงข้อมูลรายละเอียดการจอง (ชื่อคน + ชื่อที่พัก)"""
        results = []
        for assign in self.assignments:
            
            citizen = next((c for c in self.citizens if c.citizen_id == assign.citizen_id), None)
            shelter = next((s for s in self.shelters if s.shelter_id == assign.shelter_id), None)
            
            if citizen and shelter:
                results.append({
                    "citizen_name": citizen.full_name,
                    "shelter_name": shelter.name,
                    "category": citizen.category,
                    "risk": shelter.risk_level
                })
        return results