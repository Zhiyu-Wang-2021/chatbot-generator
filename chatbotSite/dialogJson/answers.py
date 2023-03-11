class Answers:
    def __init__(self, data):
        self.operation_hour = data["answers"]["openingtimepage"]
        self.location = data["answers"]["contactpage"]
        self.phone = data["answers"]["phone"]
        self.appointment = data["answers"]["appointment"]

    def get_appointment_info(self):
        if len(self.appointment) > 0:
            return self.appointment[0]

    def get_loc_info(self):
        if len(self.location) > 0 and type(self.location)!=str:
            return self.location[0]["address"] + self.location[0]["postcode"]
        else:
            return "Sorry, I am not sure about this question based on the information on our website."

    def get_hours_info(self):
        if len(self.operation_hour) > 0 and type(self.operation_hour)!=str and self.operation_hour[0] != '':
            return self.operation_hour[0]
        elif len(self.operation_hour) > 0 and self.operation_hour[0] == '':
            return "Sorry, I am not sure about this question based on the information on our website."            
        else:
            return "Sorry, I am not sure about this question based on the information on our website."

    def get_phone_info(self):
        if len(self.phone) > 0 and type(self.phone)!=str:
            return self.phone[0]
        else:
            return "Sorry, I am not sure about this question based on the information on our website."
