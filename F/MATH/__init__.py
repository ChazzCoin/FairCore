

def is_even_number(number):
    try:
        if (int(number) % 2) == 0:
            return True
        return False
    except:
        return False