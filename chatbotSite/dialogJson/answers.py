class Answers:
    # {
    #     'phone': ['020 8363 4156'],
    #     'openingtimepage':
    #         ['Monday\n08:00-18:30\nTuesday\n08:00-18:30\nWednesday\n08:00-18:30\nThursday\n08:00-18:30\nFriday\n08:00-18:30\n'],
    #     'contactpage': [{'postcode': 'EN2 6NL', 'address': 'Enfield\n105-109 Chase Side\n', 'contact': ''}]
    # }
    def __init__(self, data):
        self.operation_hour = data["answers"]["openingtimepage"]
        self.location = data["answers"]["contactpage"]
        self.phone = data["answers"]["phone"]
        self.appointment = data["answers"]["appointment"]

    def get_appointment_info(self):
        return self.appointment[0]

    def get_loc_info(self):
        if len(self.location) > 0:
            return self.location[0]["address"] + self.location[0]["postcode"]
        else:
            return "Not Found"

    def get_hours_info(self):
        if len(self.operation_hour) > 0:
            return self.operation_hour[0]
        else:
            return "Not Found"

    def get_phone_info(self):
        if len(self.phone) > 0:
            return self.phone[0]
        else:
            return "Not Found"
