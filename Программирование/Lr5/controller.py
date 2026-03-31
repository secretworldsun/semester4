from flask import render_template, request, redirect, url_for, flash
from model import CurrencyRates

currency_rates = CurrencyRates()

def index():
    rates = currency_rates.get_rates()
    return render_template('index.html', 
                         rates=rates,
                         current_currencies=currency_rates.char_codes)

# def update_rates():
#     if currency_rates.update_rates():
#         flash('Курсы валют успешно обновлены!', 'success')
#     else:
#         flash('Не удалось обновить курсы валют', 'danger')
#     return redirect(url_for('index'))

def set_currencies():
    if request.method == 'POST':
        currencies = request.form.get('currencies', '').upper().replace(' ', '').split(',')
        currencies = [c for c in currencies if len(c) == 3]
        
        if currencies:
            currency_rates.char_codes = currencies
            #flash(f'Список валют обновлен: {", ".join(currencies)}', 'success')
        else:
            flash('Указаны недоступные валюты', 'warning')
    
    return redirect(url_for('index'))