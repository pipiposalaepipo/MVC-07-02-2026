class Shelter:
    def __init__(self, shelter_id, name, capacity, risk_level, location):
        self.shelter_id = shelter_id
        self.name = name
        self.capacity = int(capacity)
        self.risk_level = risk_level
        self.location = location

class Citizen:
    def __init__(self, citizen_id, full_name, age, health_status, category):
        self.citizen_id = citizen_id
        self.full_name = full_name
        self.age = int(age) 
        self.health_status = health_status
        self.category = category

class Assignment:
    def __init__(self, assignment_id, citizen_id, shelter_id, timestamp):
        self.assignment_id = assignment_id
        self.citizen_id = citizen_id
        self.shelter_id = shelter_id
        self.timestamp = timestamp