

import uuid
import datetime

last_order_date = None
order_sequence = 1
orider_id = 000
expert_num = 23001
support_num = 2300
def generate_ref_code():
    code = str(uuid.uuid4()).replace("-", "")[:4]
    return code

def generate_order_code():
    global last_order_date, order_sequence
    today = datetime.date.today()
    year_month = today.strftime('%Y%m')
    if last_order_date == today:
        order_sequence += 1
    else:
        order_sequence = 1
    last_order_date = today
    code = f"{year_month}{order_sequence}"
    return code

def generate_expert_code():
    global expert_num
    code = "HE-" + str(expert_num)
    expert_num += 1
    
    return code

def generate_support_code():
    global support_num
    code = "HS-" + str(support_num)
    support_num += 1
    
    return code

 