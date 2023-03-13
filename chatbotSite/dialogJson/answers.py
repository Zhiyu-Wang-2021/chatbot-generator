from webscraptool.match_content import match_postcode

class Answers:
    def __init__(self, data):
        self.operation_hour = data["answers"]["openingtimepage"]
        self.location = data["answers"]["contactpage"]
        self.phone = data["answers"]["phone"]
        self.appointment = data["answers"]["appointment"]

    # check the length as some times it contains '' in it
    def length_of_hours_info(self):
        count = 0
        try:
            for s in self.operation_hour:
                if s == '' or s == {} or s == {'title':'','time':''}:
                    count = count
                else:
                    count += 1
            return count
        except Exception as e:
            print(e)
            return count


    def get_appointment_info(self):
        if len(self.appointment) > 0:
            return self.appointment[0]

    def get_loc_info(self):
        if len(self.location) >= 1 and type(self.location)!=str: 
            if self.length_of_hours_info() <= 1:
                # the content in postcode should not be a duplicate
                if self.location[0]["address"] != self.location[0]["postcode"]:
                    return "We are at this address:\n" + self.location[0]["address"] \
                           + self.location[0]["postcode"]
                else:
                    return "We are at this address:\n" + self.location[0]["address"]

            # more than 1 opening hour detected -> multiple clinic on a single page
            if self.length_of_hours_info() > 1:
                combined_addr = ''
                for addr in self.location:
                    if addr["postcode"] != addr["address"]:
                        combined_addr = combined_addr + addr["address"]\
                                        + addr["postcode"] + '\n'
                    else:
                        combined_addr = combined_addr + addr["address"] + '\n'
                return "We are at these addresses:\n" + combined_addr
        else:
            return "Sorry, I am not sure about this question based on the information on our website."

    def get_hours_info(self):
        if self.length_of_hours_info() > 0 and type(self.operation_hour)!=str:
            combined_hour_info = ''
            for hour_info in self.operation_hour:
                if type(hour_info) == dict and hour_info != {}:
                    combined_hour_info = combined_hour_info + "\n" + hour_info["title"] + '\n' + hour_info["time"]
            return "Our trusts opens on:\n" + combined_hour_info
        else:
            return "Sorry, I am not sure about this question based on the information on our website."

    def get_phone_info(self):
        if len(self.phone) > 0 and type(self.phone)!=str:
            return "Please call us with this number:\n" + self.phone[0]
        else:
            return "Sorry, I am not sure about this question based on the information on our website."
