from flask import Flask, flash, get_flashed_messages
from controller import index, set_currencies
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

app.add_url_rule('/', 'index', index)
app.add_url_rule('/set_currencies', 'set_currencies', set_currencies, methods=['POST'])

@app.context_processor
def inject_vars():
    return {
        'message': get_flashed_messages(with_categories=True),
        'current_time': datetime.now().strftime('%d.%m.%Y %H:%M')
    }

if __name__ == '__main__':
    app.run(debug=True)