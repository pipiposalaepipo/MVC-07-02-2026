import csv
import os
from model.entities import Shelter, Citizen, Assignment
import datetime

class DataManager:
    def __init__(self):
    
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(base_dir, "data")

    def load_shelters(self):
        file_path = os.path.join(self.data_dir, "shelters.csv")
        results = []
        if not os.path.exists(file_path):
            print(f"Warning: File not found {file_path}")
            return []
            
        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                s = Shelter(
                    row['shelter_id'], 
                    row['name'], 
                    row['capacity'], 
                    row['risk_level'], 
                    row['location']
                )
                results.append(s)
        return results

    def load_citizens(self):
        file_path = os.path.join(self.data_dir, "citizens.csv")
        results = []
        if not os.path.exists(file_path): return []
        
        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                c = Citizen(
                    row['citizen_id'], 
                    row['full_name'], 
                    row['age'], 
                    row['health_status'], 
                    row['category']
                )
                results.append(c)
        return results

    def load_assignments(self):
        file_path = os.path.join(self.data_dir, "assignments.csv")
        results = []
        if not os.path.exists(file_path): return []

        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                a = Assignment(
                    row.get('assignment_id', 0), 
                    row['citizen_id'], 
                    row['shelter_id'], 
                    row.get('timestamp', str(datetime.date.today()))
                )
                results.append(a)
        return results