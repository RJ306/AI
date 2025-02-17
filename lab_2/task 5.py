class DeliveryRobot:
    def __init__(self, name):
        self.name = name
        self.goal = 'Deliver Medicine'
        self.current_location = 'Storage'
        self.staff_alert = True

    def formulate_goal(self, percepts):
        if percepts['medicine_type']:
            self.goal = 'Deliver Medicine'
        elif percepts['staff_availability']:
            self.goal = 'Alert Staff'
        else:
            self.goal = 'No action needed'

    def act(self, percepts):
        self.formulate_goal(percepts)
        
        if self.goal == 'Deliver Medicine':
            self.pick_up_medicine(percepts['medicine_type'])
            self.move_to_location(percepts['room_no'])
            self.deliver_medicine()
        elif self.goal == 'Alert Staff':
            self.alert_staff()
        else:
            return 'Dont do anything'

    def pick_up_medicine(self, medicine_type):
        self.medication = medicine_type
        print(f"{self.name} picked up {medicine_type} from storage.")

    def move_to_location(self, location):
        self.current_location = location
        print(f"{self.name} is moving to {location}.")

    def deliver_medicine(self):
        
        print(f"Scan patient id!!\n{self.name} delivered medicine to patient_room.\n")

    def alert_staff(self):
        self.staff_alert = True
        print(f"{self.name} is alerting staff.")

class Environment:
    def __init__(self, layout):
        self.layout = layout
        self.patient_schedules = {}
        self.staff_availability = {'Nurse Station': True, 'Doctor': False}
        self.medicine_storage = {'Aspirin': 5, 'Penicillin': 3}

    def get_percepts(self, room_no, patient_schedule, medicine_type, staff_availability):
        percepts = {
            'patient_schedule': patient_schedule,
            'staff_availability': staff_availability,
            'room_no':room_no,
            'medicine_type': medicine_type
        }
        return percepts

    def update_patient_schedule(self, patient_room, schedule):
        self.patient_schedules[patient_room] = schedule

def run_agent(robot, environment, steps):
    for step in range(steps):
        patient_room = 'Room 2' 
        medicine_needed = True  
        medicine_type = 'Aspirin'  
        staff_needed = True
        
        percepts = environment.get_percepts(patient_room, medicine_needed, medicine_type, staff_needed)
        
        robot.act(percepts)

robot = DeliveryRobot('DeliveryBot')
hospital_layout = {}  
environment = Environment(hospital_layout)

# Run the simulation for 5 steps
run_agent(robot, environment, 5)
