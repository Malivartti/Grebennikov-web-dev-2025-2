import re

def validate_phone(phone):
    cleaned_phone = re.sub(r'[+\s().-]', '', phone)
    if not cleaned_phone.isdigit():
        return False, "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
    
    digit_count = len(cleaned_phone)
    if phone.startswith('+7') or phone.startswith('8'):
        if digit_count != 11:
            return False, "Недопустимый ввод. Неверное количество цифр."
    else:
        if digit_count != 10:
            return False, "Недопустимый ввод. Неверное количество цифр."
    
    if digit_count == 11:
        formatted = f"8-{cleaned_phone[1:4]}-{cleaned_phone[4:7]}-{cleaned_phone[7:9]}-{cleaned_phone[9:11]}"
    else:
        formatted = f"8-{cleaned_phone[0:3]}-{cleaned_phone[3:6]}-{cleaned_phone[6:8]}-{cleaned_phone[8:10]}"
    
    return True, formatted