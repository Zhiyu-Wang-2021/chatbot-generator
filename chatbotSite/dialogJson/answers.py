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
