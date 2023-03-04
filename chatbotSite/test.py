import webscraptool.get_answer_dict as t
from dialogJson.answers import Answers

res = {'answers':t.get_answer('www.richmondpractice.scot.nhs.uk')}
ans = Answers(res)
print('\n\n\n'+ans.get_appointment_info()+'\n\n\n')
print('\n\n\n'+ans.get_hours_info()+'\n\n\n')
print('\n\n\n'+ans.get_loc_info()+'\n\n\n')
print('\n\n\n'+ans.get_phone_info()+'\n\n\n')

