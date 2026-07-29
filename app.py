import os
from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory
from gtts import gTTS
import io

DetectorFactory.seed = 0

app = Flask(__name__)

# Expanded World Languages List
LANGUAGES = {
    # Asian Languages
    'hi': 'Hindi (हिंदी)',
    'en': 'English',
    'zh-cn': 'Chinese Simplified (中文)',
    'ja': 'Japanese (日本語)',
    'ko': 'Korean (한국어)',
    'ar': 'Arabic (العربية)',
    'ur': 'Urdu (اردو)',
    'bn': 'Bengali (বাংলা)',
    'ta': 'Tamil (தமிழ்)',
    'te': 'Telugu (తెలుగు)',
    'mr': 'Marathi (मराठी)',
    'gu': 'Gujarati (ગુજરાતી)',
    'pa': 'Punjabi (ਪੰਜਾਬੀ)',
    'th': 'Thai (ไทย)',
    'vi': 'Vietnamese (Tiếng Việt)',
    'id': 'Indonesian (Bahasa Indonesia)',

    # European Languages
    'es': 'Spanish (Español)',
    'fr': 'French (Français)',
    'de': 'German (Deutsch)',
    'it': 'Italian (Italiano)',
    'ru': 'Russian (Русский)',
    'pt': 'Portuguese (Português)',
    'nl': 'Dutch (Nederlands)',
    'el': 'Greek (Ελληνικά)',
    'pl': 'Polish (Polski)',
    'uk': 'Ukrainian (Українська)',
    'sv': 'Swedish (Svenska)',

    # Middle Eastern & Others
    'tr': 'Turkish (Türkçe)',
    'fa': 'Persian (فارسی)',
    'he': 'Hebrew (עברית)',
    'sw': 'Swahili (Kiswahili)'
}

@app.route('/')
def home():
    return render_template('index.html', languages=LANGUAGES)

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        input_text = data.get('text', '').strip()
        target_lang = data.get('target_lang', 'hi')

        if not input_text:
            return jsonify({'error': 'Please enter text to translate'}), 400

        try:
            detected_code = detect(input_text)
        except Exception:
            detected_code = 'auto'

        translated_text = GoogleTranslator(source='auto', target=target_lang).translate(input_text)

        return jsonify({
            'success': True,
            'detected_lang': detected_code.upper(),
            'translated_text': translated_text
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tts', methods=['POST'])
def text_to_speech():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        lang = data.get('lang', 'en')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Dynamic gTTS Generation
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)

        return send_file(fp, mimetype='audio/mpeg')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
