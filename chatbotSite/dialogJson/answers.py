class Answers:
    # {
    # "phone": [{"title": "", "num": "Tel: 01302 868421"}],
    # "openingtimepage": [{
    #   "title": "Opening Times",
    #   "time": "Opening Times\nPlease note on two Wednesdays per month we close at 12:00 for training.\nMonday\n07.00 - 18:00\nTuesday\n08:00 - 20.30\nWednesday\n08:00 - 18:00\nThursday\n07:00 - 18:00\nFriday\n08:00 - 18:00\n"
    #   }],
    # "contactpage": [{
    #   "postcode": "Doncaster, DN11 0LP",
    #   "address": "Rossington\nGrange Lane\nThe Rossington Practice\n",
    #   "contact": "Doncaster, DN11 0LPTel: 01302 868421\n"}
    #   ]}
    def __init__(self, data):
        self.operation_hour = data["answers"]["openingtimepage"]
        self.location = data["answers"]["contactpage"]
        self.phone = data["answers"]["phone"]
