from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import os
import logging
from scraper import DelhiHighCourtScraper, DistrictCourtScraper
from captcha.image import ImageCaptcha
import random
import string
from io import BytesIO

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store CAPTCHA answers (in-memory)
captcha_answers = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/captcha')
def generate_captcha():
    image = ImageCaptcha()
    captcha_text = ''.join(random.choices(string.digits, k=5))
    captcha_answers['current'] = captcha_text
    data = image.generate(captcha_text)
    return send_file(BytesIO(data.read()), mimetype='image/png')

@app.route('/api/search', methods=['POST'])
def search_case():
    try:
        data = request.get_json()
        case_type = data.get('caseType')
        case_number = data.get('caseNumber')
        filing_year = data.get('filingYear')
        court_type = data.get('courtType')
        captcha = data.get('captcha')

        if not all([case_type, case_number, filing_year, court_type, captcha]):
            return jsonify({'success': False, 'error': 'All fields are required'}), 400

        if captcha != captcha_answers.get('current'):
            return jsonify({'success': False, 'error': 'Invalid CAPTCHA'}), 400

        if court_type == 'delhi-hc':
            scraper = DelhiHighCourtScraper()
        elif court_type == 'district-courts':
            scraper = DistrictCourtScraper()
        else:
            return jsonify({'success': False, 'error': 'Unsupported court type'}), 400

        case_data = scraper.search_case(case_type, case_number, filing_year)
        return jsonify({'success': True, 'data': case_data})

    except Exception as e:
        logger.exception("Error in /api/search")
        return jsonify({'success': False, 'error': 'Something went wrong'}), 500

if __name__ == '__main__':
    app.run(debug=True)
