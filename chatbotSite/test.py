import webscraptool.get_answer_dict as t
from dialogJson.answers import Answers
res = {'answers':t.get_answer('www.gosh.nhs.uk')}
ans = Answers(res)
print('\n\n\n---------------------------result\n\n\n')
print(res)
print('\n\nappointment\n'+str(ans.get_appointment_info())+'\n\n\n')
print('\n\ntime\n'+str(ans.get_hours_info())+'\n\n\n')
print('\n\nloc\n'+str(ans.get_loc_info())+'\n\n\n')
print('\n\nphone\n'+str(ans.get_phone_info())+'\n\n\n')

# www.camdengp.co.uk（correct address should be no 'www'）
# run on the server:err500，locally no problem
# similar problem with www.graysinnmedical.co.uk，address should be typed correct
# www.sohosquaregp.co.uk bing no result and alert err500,this error should be handle in get_bing_answer
# reason:noresult for this website