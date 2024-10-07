from dotenv import load_dotenv
import os
load_dotenv()

def generate_price(payment_type:str):
    gelombang = os.getenv('GELOMBANG')

    if gelombang == 'ONE':
        if payment_type == 'PADUS_A':
            return 940000
        if payment_type == 'PADUS_B':
            return 1105000
        if payment_type == 'TATRA_A':
            return 511000
        if payment_type == 'TATRA_B':
            return 522000
        if payment_type == 'TATRA_C':
            return 472500
    else:
        if payment_type == 'PADUS_A':
            return 995000
        if payment_type == 'PADUS_B':
            return 1215000
        if payment_type == 'TATRA_A':
            return 527500
        if payment_type == 'TATRA_B':
            return 566000
        if payment_type == 'TATRA_C':
            return 516500
    
    return None

def generate_category_name(payment_type:str):
    if payment_type == 'PADUS_A':
        return "Paduan Suara A"
    if payment_type == 'PADUS_B':
        return "Paduan Suara B"
    if payment_type == 'TATRA_A':
        return "Tari Tradisional A"
    if payment_type == 'TATRA_B':
        return "Tari Tradisional B"
    if payment_type == 'TATRA_C':
        return "Tari Tradisional C"
    
    return None