# Basic Libraries
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import time
# Custom Libraries
#from persistence.json_reader import read_from_json

prev_query = ""
prev_answer = ""


def rate_limited(max_per_second):
    """Decorator function to throttle api requests to max allowed(7) per second"""
    min_interval = 1.0 / float(max_per_second)

    def decorate(func):
        last_time_called = [0.0]

        def rate_limited_function(*args, **kargs):
            elapsed = time.clock() - last_time_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kargs)
            last_time_called[0] = time.clock()
            return ret

        return rate_limited_function

    return decorate

bing_spell_check_api_key = '4f44263fa15e4203920250272f62cc4e'

@rate_limited(7)
def bing_spell_correct(
        text: str,
):
    """Bing spell check request handler"""
    # api key import

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Ocp-Apim-Subscription-Key': bing_spell_check_api_key,
    }

    params = urllib.parse.urlencode({
        'mode': 'proof',
        'mkt': 'en-us',
    })

    global prev_query, prev_answer
    if text == prev_query:
        return prev_answer

    prev_query = text

    formatted_txt = '+'.join(text.split())

    conn: http.client.HTTPSConnection = None

    print(f'BEFORE - {text}')
    try:
        conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("POST", "/bing/v5.0/spellcheck/?%s" % params, "Text=" + formatted_txt, headers)
        response = conn.getresponse()

        data = response.read().decode('utf-8')

        json_obj = json.loads(data)

        # check for response errors
        if 'statusCode' in json_obj.keys():
            print(json_obj)
            raise Exception()

        # spell correction
        corrected_text = text

        flagged_tokens = json_obj['flaggedTokens']

        if len(flagged_tokens) > 0:
            flagged_tokens.sort(key=lambda x: x['offset'], reverse=True)

        for token in flagged_tokens:
            suggestions = token["suggestions"]
            if suggestions:
                suggestion = suggestions[0]['suggestion']
                if suggestion:
                    word = token["token"]
                    start_index = int(token["offset"])
                    end_index = start_index + len(word)

                    corrected_text = corrected_text[:start_index] + suggestion + corrected_text[end_index:]

        print(f'AFTER - {corrected_text}')

        prev_answer = corrected_text
        return corrected_text
    except Exception as e:
        print(f'Exception in BING Spell Check API : {e}')
        raise
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    bing_spell_correct("its 2pm in the mornng")
    bing_spell_correct("I lve by the sea")
    bing_spell_correct("donot go")
