import os
import json
import re
import csv
import io
import time
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
STATS_FILE = "converter_stats.json"
LEADERBOARD_FILE = "leaderboard.json"
OFFSET = 0

E = {
    'wave': '<tg-emoji emoji-id="5472055112702629499">👋</tg-emoji>',
    'gear': '<tg-emoji emoji-id="5341715473882955310">⚙️</tg-emoji>',
    'one': '<tg-emoji emoji-id="5359541052745198705">1️⃣</tg-emoji>',
    'two': '<tg-emoji emoji-id="5350673031905692048">2️⃣</tg-emoji>',
    'three': '<tg-emoji emoji-id="5269263198120324184">3️⃣</tg-emoji>',
    'four': '<tg-emoji emoji-id="5366142335874781789">4️⃣</tg-emoji>',
    'download': '<tg-emoji emoji-id="5443127283898405358">🔽</tg-emoji>',
    'check': '<tg-emoji emoji-id="6206185428702206246">✅</tg-emoji>',
    'file': '<tg-emoji emoji-id="5257965810634202885">📄</tg-emoji>',
    'chart': '<tg-emoji emoji-id="6206343625232619150">📊</tg-emoji>',
    'folder': '<tg-emoji emoji-id="5352721946054268944">📁</tg-emoji>',
    'pen': '<tg-emoji emoji-id="5334882760735598374">📝</tg-emoji>',
    'numbers': '<tg-emoji emoji-id="5352862640592949843">🔢</tg-emoji>',
    'infinity': '<tg-emoji emoji-id="5271934788037517525">♾️</tg-emoji>',
    'clock': '<tg-emoji emoji-id="5382194935057372936">⏱️</tg-emoji>',
    'globe': '<tg-emoji emoji-id="5224450179368767019">🌐</tg-emoji>',
    'trophy': '<tg-emoji emoji-id="5188344996356448758">🏆</tg-emoji>',
    'gold': '<tg-emoji emoji-id="6206419981161211268">🥇</tg-emoji>',
    'silver': '<tg-emoji emoji-id="6206222099132978580">🥈</tg-emoji>',
    'bronze': '<tg-emoji emoji-id="6206311275538946838">🥉</tg-emoji>',
    'bulb': '<tg-emoji emoji-id="5422439311196834318">💡</tg-emoji>',
    'user': '<tg-emoji emoji-id="5258011929993026890">👤</tg-emoji>',
    'back': '<tg-emoji emoji-id="5377584064326804458">🔙</tg-emoji>',
    'processing': '<tg-emoji emoji-id="5382194935057372936">⏳</tg-emoji>',
}

EMOJI_ID = {
    'convert': "5352721946054268944",
    'gear': "5341715473882955310",
    'chart': "6206343625232619150",
    'trophy': "5188344996356448758",
    'numbers': "5352862640592949843",
    'pen': "5334882760735598374",
    'download': "5443127283898405358",
    'back': "5377584064326804458",
}

FLAG_EMOJI = {
    'TR': '<tg-emoji emoji-id="5293993400767367408">🇹🇷</tg-emoji>',
    'US': '<tg-emoji emoji-id="5294244076533600593">🇺🇸</tg-emoji>',
    'GB': '<tg-emoji emoji-id="5293993521026453119">🇬🇧</tg-emoji>',
    'DE': '<tg-emoji emoji-id="5292013274815028523">🇩🇪</tg-emoji>',
    'FR': '<tg-emoji emoji-id="5291817660529533837">🇫🇷</tg-emoji>',
    'IT': '<tg-emoji emoji-id="5291826830284709120">🇮🇹</tg-emoji>',
    'RU': '<tg-emoji emoji-id="5294335323113807278">🇷🇺</tg-emoji>',
    'CN': '<tg-emoji emoji-id="5294068833277990704">🇨🇳</tg-emoji>',
    'JP': '<tg-emoji emoji-id="5291799063321139445">🇯🇵</tg-emoji>',
    'KR': '<tg-emoji emoji-id="5294408281723262763">🇰🇷</tg-emoji>',
    'IN': '<tg-emoji emoji-id="5291933173674957761">🇮🇳</tg-emoji>',
    'BR': '<tg-emoji emoji-id="5291892229751723900">🇧🇷</tg-emoji>',
    'ES': '<tg-emoji emoji-id="5294513087515216901">🇪🇸</tg-emoji>',
    'NL': '<tg-emoji emoji-id="5291917797692042265">🇳🇱</tg-emoji>',
    'SE': '<tg-emoji emoji-id="5291737091238026321">🇸🇪</tg-emoji>',
    'NO': '<tg-emoji emoji-id="5291761718580502030">🇳🇴</tg-emoji>',
    'DK': '<tg-emoji emoji-id="5294531860817268837">🇩🇰</tg-emoji>',
    'PL': '<tg-emoji emoji-id="5292190970496963836">🇵🇱</tg-emoji>',
    'UA': '<tg-emoji emoji-id="5294263837678131580">🇺🇦</tg-emoji>',
    'SA': '<tg-emoji emoji-id="5294163983983463099">🇸🇦</tg-emoji>',
    'AE': '<tg-emoji emoji-id="5294314831824835370">🇦🇪</tg-emoji>',
    'EG': '<tg-emoji emoji-id="5293992082212409502">🇪🇬</tg-emoji>',
    'MA': '<tg-emoji emoji-id="5292108962391414885">🇲🇦</tg-emoji>',
    'DZ': '<tg-emoji emoji-id="5294048127240655242">🇩🇿</tg-emoji>',
    'TN': '<tg-emoji emoji-id="5294484680601521871">🇹🇳</tg-emoji>',
    'IR': '<tg-emoji emoji-id="5294220170745630736">🇮🇷</tg-emoji>',
    'PK': '<tg-emoji emoji-id="5291825606219029010">🇵🇰</tg-emoji>',
    'BD': '<tg-emoji emoji-id="5291824687096027834">🇧🇩</tg-emoji>',
    'ID': '<tg-emoji emoji-id="5294192317882716626">🇮🇩</tg-emoji>',
    'MY': '<tg-emoji emoji-id="5291858351049696702">🇲🇾</tg-emoji>',
    'PH': '<tg-emoji emoji-id="5291798075478661634">🇵🇭</tg-emoji>',
    'SY': '<tg-emoji emoji-id="5294013428199869487">🇸🇾</tg-emoji>',
    'IQ': '<tg-emoji emoji-id="5294325010897327367">🇮🇶</tg-emoji>',
    'LB': '<tg-emoji emoji-id="5294193108156699621">🇱🇧</tg-emoji>',
    'JO': '<tg-emoji emoji-id="5291988613112814801">🇯🇴</tg-emoji>',
    'KW': '<tg-emoji emoji-id="5292066437920218075">🇰🇼</tg-emoji>',
    'BH': '<tg-emoji emoji-id="5294108398516720753">🇧🇭</tg-emoji>',
    'QA': '<tg-emoji emoji-id="5292166360334357676">🇶🇦</tg-emoji>',
    'OM': '<tg-emoji emoji-id="5291813666209946812">🇴🇲</tg-emoji>',
    'YE': '<tg-emoji emoji-id="5294058972033076492">🇾🇪</tg-emoji>',
    'IL': '<tg-emoji emoji-id="5294069056616289553">🇮🇱</tg-emoji>',
    'PS': '<tg-emoji emoji-id="5294289826525238172">🇵🇸</tg-emoji>',
    'NG': '<tg-emoji emoji-id="5294456308047563965">🇳🇬</tg-emoji>',
    'KE': '<tg-emoji emoji-id="5292111852904416801">🇰🇪</tg-emoji>',
    'UG': '<tg-emoji emoji-id="5294192317882716626">🇺🇬</tg-emoji>',
    'TZ': '<tg-emoji emoji-id="5292146096678658977">🇹🇿</tg-emoji>',
    'ZA': '<tg-emoji emoji-id="5294325281480266304">🇿🇦</tg-emoji>',
    'MX': '<tg-emoji emoji-id="5294535073452809778">🇲🇽</tg-emoji>',
    'AR': '<tg-emoji emoji-id="5292208210495689627">🇦🇷</tg-emoji>',
    'CL': '<tg-emoji emoji-id="5294231037012888049">🇨🇱</tg-emoji>',
    'CO': '<tg-emoji emoji-id="5294010206974397371">🇨🇴</tg-emoji>',
    'VE': '<tg-emoji emoji-id="5294476442854247878">🇻🇪</tg-emoji>',
    'PE': '<tg-emoji emoji-id="5292099427564018941">🇵🇪</tg-emoji>',
    'AF': '<tg-emoji emoji-id="5291937511591925566">🇦🇫</tg-emoji>',
    'AL': '<tg-emoji emoji-id="5294202819077756005">🇦🇱</tg-emoji>',
    'AM': '<tg-emoji emoji-id="5291978717508164018">🇦🇲</tg-emoji>',
    'AT': '<tg-emoji emoji-id="5291975174160145850">🇦🇹</tg-emoji>',
    'AZ': '<tg-emoji emoji-id="5294323533428579078">🇦🇿</tg-emoji>',
    'BE': '<tg-emoji emoji-id="5291774466043435275">🇧🇪</tg-emoji>',
    'BG': '<tg-emoji emoji-id="5294308947719640437">🇧🇬</tg-emoji>',
    'CA': '<tg-emoji emoji-id="5292290347450259214">🇨🇦</tg-emoji>',
    'CH': '<tg-emoji emoji-id="5291791748991835084">🇨🇭</tg-emoji>',
    'CZ': '<tg-emoji emoji-id="5294242852467923382">🇨🇿</tg-emoji>',
    'FI': '<tg-emoji emoji-id="5294049961191690629">🇫🇮</tg-emoji>',
    'GR': '<tg-emoji emoji-id="5291948395039054764">🇬🇷</tg-emoji>',
    'HR': '<tg-emoji emoji-id="5291999676948569127">🇭🇷</tg-emoji>',
    'HU': '<tg-emoji emoji-id="5294229581018975260">🇭🇺</tg-emoji>',
    'IE': '<tg-emoji emoji-id="5294471971793293647">🇮🇪</tg-emoji>',
    'KZ': '<tg-emoji emoji-id="5294227175837290463">🇰🇿</tg-emoji>',
    'LT': '<tg-emoji emoji-id="5294343084119708700">🇱🇹</tg-emoji>',
    'LV': '<tg-emoji emoji-id="5292236016113966127">🇱🇻</tg-emoji>',
    'NZ': '<tg-emoji emoji-id="5294189019347833274">🇳🇿</tg-emoji>',
    'PT': '<tg-emoji emoji-id="5294436555492973610">🇵🇹</tg-emoji>',
    'RO': '<tg-emoji emoji-id="5294107724206856227">🇷🇴</tg-emoji>',
    'RS': '<tg-emoji emoji-id="5294458584380230360">🇷🇸</tg-emoji>',
    'SG': '<tg-emoji emoji-id="5294451304410663668">🇸🇬</tg-emoji>',
    'SK': '<tg-emoji emoji-id="5294538440707166931">🇸🇰</tg-emoji>',
    'TH': '<tg-emoji emoji-id="5293994384314882755">🇹🇭</tg-emoji>',
    'VN': '<tg-emoji emoji-id="5294235963340379688">🇻🇳</tg-emoji>',
    'AU': '<tg-emoji emoji-id="5294444247779399477">🇦🇺</tg-emoji>',
    'CY': '<tg-emoji emoji-id="5294062721539526918">🇨🇾</tg-emoji>',
    'EE': '<tg-emoji emoji-id="5291951143818123103">🇪🇪</tg-emoji>',
    'IS': '<tg-emoji emoji-id="5294354358408859664">🇮🇸</tg-emoji>',
    'LU': '<tg-emoji emoji-id="5294423709245787718">🇱🇺</tg-emoji>',
    'MT': '<tg-emoji emoji-id="5294532213004588353">🇲🇹</tg-emoji>',
    'SI': '<tg-emoji emoji-id="5294279359689938006">🇸🇮</tg-emoji>',
    'HK': '<tg-emoji emoji-id="5292166459118606932">🇭🇰</tg-emoji>',
    'TW': '<tg-emoji emoji-id="5294095745543069603">🇹🇼</tg-emoji>',
    'UY': '<tg-emoji emoji-id="5291928449210932974">🇺🇾</tg-emoji>',
    'BO': '<tg-emoji emoji-id="5294201479047957700">🇧🇴</tg-emoji>',
    'EC': '<tg-emoji emoji-id="5292083733753517221">🇪🇨</tg-emoji>',
    'PY': '<tg-emoji emoji-id="5294525611639852679">🇵🇾</tg-emoji>',
    'CR': '<tg-emoji emoji-id="5292063805105263554">🇨🇷</tg-emoji>',
    'PA': '<tg-emoji emoji-id="5291959935616178405">🇵🇦</tg-emoji>',
    'DO': '<tg-emoji emoji-id="5294522197140857947">🇩🇴</tg-emoji>',
    'GT': '<tg-emoji emoji-id="5294336633078831209">🇬🇹</tg-emoji>',
    'HN': '<tg-emoji emoji-id="5291901034434682297">🇭🇳</tg-emoji>',
    'SV': '<tg-emoji emoji-id="5294337307388695687">🇸🇻</tg-emoji>',
    'NI': '<tg-emoji emoji-id="5294240825243358100">🇳🇮</tg-emoji>',
    'PR': '<tg-emoji emoji-id="5292121516580820347">🇵🇷</tg-emoji>',
    'LY': '<tg-emoji emoji-id="5291858711826946840">🇱🇾</tg-emoji>',
    'SD': '<tg-emoji emoji-id="5294177148058228060">🇸🇩</tg-emoji>',
    'ET': '<tg-emoji emoji-id="5292245976143124155">🇪🇹</tg-emoji>',
    'GH': '<tg-emoji emoji-id="5294347396266873249">🇬🇭</tg-emoji>',
    'CM': '<tg-emoji emoji-id="5291997306126626950">🇨🇲</tg-emoji>',
    'CI': '<tg-emoji emoji-id="5293991322003200135">🇨🇮</tg-emoji>',
    'SN': '<tg-emoji emoji-id="5292087023698466689">🇸🇳</tg-emoji>',
    'ML': '<tg-emoji emoji-id="5292086972158858331">🇲🇱</tg-emoji>',
    'BF': '<tg-emoji emoji-id="5294153164960848949">🇧🇫</tg-emoji>',
    'BJ': '<tg-emoji emoji-id="5293984969746566866">🇧🇯</tg-emoji>',
    'TG': '<tg-emoji emoji-id="5294097669688415562">🇹🇬</tg-emoji>',
    'LR': '<tg-emoji emoji-id="5291793810576137439">🇱🇷</tg-emoji>',
    'SL': '<tg-emoji emoji-id="5294494314213167952">🇸🇱</tg-emoji>',
    'GM': '<tg-emoji emoji-id="5294399820637688352">🇬🇲</tg-emoji>',
    'GW': '<tg-emoji emoji-id="5294409819321550432">🇬🇼</tg-emoji>',
    'MR': '<tg-emoji emoji-id="5294429743674840973">🇲🇷</tg-emoji>',
    'NE': '<tg-emoji emoji-id="5291809418487290691">🇳🇪</tg-emoji>',
    'TD': '<tg-emoji emoji-id="5291780728105753403">🇹🇩</tg-emoji>',
    'CG': '<tg-emoji emoji-id="5294035229453865597">🇨🇬</tg-emoji>',
    'AO': '<tg-emoji emoji-id="5294516785482062829">🇦🇴</tg-emoji>',
    'ZM': '<tg-emoji emoji-id="5294100109229838880">🇿🇲</tg-emoji>',
    'ZW': '<tg-emoji emoji-id="5294422158762592930">🇿🇼</tg-emoji>',
    'MW': '<tg-emoji emoji-id="5294241881805312589">🇲🇼</tg-emoji>',
    'MZ': '<tg-emoji emoji-id="5294086708931874940">🇲🇿</tg-emoji>',
    'BW': '<tg-emoji emoji-id="5294026179957772585">🇧🇼</tg-emoji>',
    'NA': '<tg-emoji emoji-id="5292021761670404922">🇳🇦</tg-emoji>',
    'MG': '<tg-emoji emoji-id="5291991568050312348">🇲🇬</tg-emoji>',
    'MU': '<tg-emoji emoji-id="5294127824653797277">🇲🇺</tg-emoji>',
    'SC': '<tg-emoji emoji-id="5291891186074672309">🇸🇨</tg-emoji>',
    'KM': '<tg-emoji emoji-id="5294351381996521508">🇰🇲</tg-emoji>',
    'RW': '<tg-emoji emoji-id="5294191265615729158">🇷🇼</tg-emoji>',
    'BI': '<tg-emoji emoji-id="5294051631933967760">🇧🇮</tg-emoji>',
    'SO': '<tg-emoji emoji-id="5294058817414255960">🇸🇴</tg-emoji>',
    'DJ': '<tg-emoji emoji-id="5294127214768468283">🇩🇯</tg-emoji>',
    'ER': '<tg-emoji emoji-id="5291922054004625949">🇪🇷</tg-emoji>',
    'CF': '<tg-emoji emoji-id="5294210571493724819">🇨🇫</tg-emoji>',
    'GA': '<tg-emoji emoji-id="5294321325815389139">🇬🇦</tg-emoji>',
    'GQ': '<tg-emoji emoji-id="5292170045416297012">🇬🇶</tg-emoji>',
    'GN': '<tg-emoji emoji-id="5291892096607739008">🇬🇳</tg-emoji>',
    'LS': '<tg-emoji emoji-id="5292040693886247604">🇱🇸</tg-emoji>',
    'SZ': '<tg-emoji emoji-id="5294312482477724867">🇸🇿</tg-emoji>',
    'VU': '<tg-emoji emoji-id="5294448585696368047">🇻🇺</tg-emoji>',
    'TO': '<tg-emoji emoji-id="5294283689016973348">🇹🇴</tg-emoji>',
    'KI': '<tg-emoji emoji-id="5294538934628405146">🇰🇮</tg-emoji>',
    'FM': '<tg-emoji emoji-id="5291838156113470124">🇫🇲</tg-emoji>',
    'MH': '<tg-emoji emoji-id="5294180730060954484">🇲🇭</tg-emoji>',
    'NR': '<tg-emoji emoji-id="5294463274484521342">🇳🇷</tg-emoji>',
    'CK': '<tg-emoji emoji-id="5292098684534675100">🇨🇰</tg-emoji>',
    'NU': '<tg-emoji emoji-id="5294471336138134209">🇳🇺</tg-emoji>',
    'AS': '<tg-emoji emoji-id="5291994273879709721">🇦🇸</tg-emoji>',
    'VI': '<tg-emoji emoji-id="5294228039125718124">🇻🇮</tg-emoji>',
    'GI': '<tg-emoji emoji-id="5292055799286224027">🇬🇮</tg-emoji>',
    'GL': '<tg-emoji emoji-id="5292014752283774878">🇬🇱</tg-emoji>',
    'AX': '<tg-emoji emoji-id="5294077418917616055">🇦🇽</tg-emoji>',
    'AW': '<tg-emoji emoji-id="5294007002928798927">🇦🇼</tg-emoji>',
    'FO': '<tg-emoji emoji-id="5294049961191690629">🇫🇴</tg-emoji>',
    'TC': '<tg-emoji emoji-id="5294320866253884749">🇹🇨</tg-emoji>',
    'JE': '<tg-emoji emoji-id="5291950280529697493">🇯🇪</tg-emoji>',
    'IM': '<tg-emoji emoji-id="5294318478252070646">🇮🇲</tg-emoji>',
    'MC': '<tg-emoji emoji-id="5294378161117614233">🇲🇨</tg-emoji>',
    'LI': '<tg-emoji emoji-id="5292048742654957785">🇱🇮</tg-emoji>',
    'SM': '<tg-emoji emoji-id="5292147350809106831">🇸🇲</tg-emoji>',
    'AD': '<tg-emoji emoji-id="5294215205763434181">🇦🇩</tg-emoji>',
}

def get_flag_html(country_code):
    return FLAG_EMOJI.get(country_code, '❓')

COUNTRY_CODES = {
    '90': {'name': 'Turkey', 'code': 'TR'}, '1': {'name': 'USA', 'code': 'US'},
    '44': {'name': 'UK', 'code': 'GB'}, '49': {'name': 'Germany', 'code': 'DE'},
    '33': {'name': 'France', 'code': 'FR'}, '39': {'name': 'Italy', 'code': 'IT'},
    '7': {'name': 'Russia', 'code': 'RU'}, '86': {'name': 'China', 'code': 'CN'},
    '81': {'name': 'Japan', 'code': 'JP'}, '82': {'name': 'South Korea', 'code': 'KR'},
    '91': {'name': 'India', 'code': 'IN'}, '55': {'name': 'Brazil', 'code': 'BR'},
    '34': {'name': 'Spain', 'code': 'ES'}, '31': {'name': 'Netherlands', 'code': 'NL'},
    '46': {'name': 'Sweden', 'code': 'SE'}, '47': {'name': 'Norway', 'code': 'NO'},
    '45': {'name': 'Denmark', 'code': 'DK'}, '48': {'name': 'Poland', 'code': 'PL'},
    '380': {'name': 'Ukraine', 'code': 'UA'}, '966': {'name': 'Saudi Arabia', 'code': 'SA'},
    '971': {'name': 'UAE', 'code': 'AE'}, '20': {'name': 'Egypt', 'code': 'EG'},
    '212': {'name': 'Morocco', 'code': 'MA'}, '213': {'name': 'Algeria', 'code': 'DZ'},
    '216': {'name': 'Tunisia', 'code': 'TN'}, '98': {'name': 'Iran', 'code': 'IR'},
    '92': {'name': 'Pakistan', 'code': 'PK'}, '880': {'name': 'Bangladesh', 'code': 'BD'},
    '62': {'name': 'Indonesia', 'code': 'ID'}, '60': {'name': 'Malaysia', 'code': 'MY'},
    '63': {'name': 'Philippines', 'code': 'PH'}, '963': {'name': 'Syria', 'code': 'SY'},
    '964': {'name': 'Iraq', 'code': 'IQ'}, '961': {'name': 'Lebanon', 'code': 'LB'},
    '962': {'name': 'Jordan', 'code': 'JO'}, '965': {'name': 'Kuwait', 'code': 'KW'},
    '973': {'name': 'Bahrain', 'code': 'BH'}, '974': {'name': 'Qatar', 'code': 'QA'},
    '968': {'name': 'Oman', 'code': 'OM'}, '967': {'name': 'Yemen', 'code': 'YE'},
    '972': {'name': 'Israel', 'code': 'IL'}, '970': {'name': 'Palestine', 'code': 'PS'},
    '234': {'name': 'Nigeria', 'code': 'NG'}, '254': {'name': 'Kenya', 'code': 'KE'},
    '256': {'name': 'Uganda', 'code': 'UG'}, '255': {'name': 'Tanzania', 'code': 'TZ'},
    '27': {'name': 'South Africa', 'code': 'ZA'}, '52': {'name': 'Mexico', 'code': 'MX'},
    '54': {'name': 'Argentina', 'code': 'AR'}, '56': {'name': 'Chile', 'code': 'CL'},
    '57': {'name': 'Colombia', 'code': 'CO'}, '58': {'name': 'Venezuela', 'code': 'VE'},
    '51': {'name': 'Peru', 'code': 'PE'},
}

def api_call(method, params=None):
    url = f"{BASE_URL}/{method}"
    data = None
    if params:
        data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"API Error: {e}")
        return None

def get_updates():
    global OFFSET
    result = api_call("getUpdates", {"offset": OFFSET, "timeout": 30})
    if result and result.get("ok"):
        for update in result["result"]:
            OFFSET = update["update_id"] + 1
            yield update

def send_message(chat_id, text, reply_markup=None, parse_mode="HTML"):
    params = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
    if reply_markup:
        params["reply_markup"] = json.dumps(reply_markup)
    return api_call("sendMessage", params)

def edit_message(chat_id, msg_id, text, reply_markup=None):
    params = {"chat_id": chat_id, "message_id": msg_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        params["reply_markup"] = json.dumps(reply_markup)
    return api_call("editMessageText", params)

def answer_callback(callback_id, text=None):
    params = {"callback_query_id": callback_id}
    if text:
        params["text"] = text
    api_call("answerCallbackQuery", params)

def send_document(chat_id, file_bytes, filename, caption=""):
    url = f"{BASE_URL}/sendDocument"
    boundary = "----WebKitFormBoundary" + str(int(time.time()))
    body = []
    
    body.append(f"--{boundary}".encode())
    body.append(f'Content-Disposition: form-data; name="chat_id"'.encode())
    body.append(b"")
    body.append(str(chat_id).encode())
    
    body.append(f"--{boundary}".encode())
    body.append(f'Content-Disposition: form-data; name="caption"'.encode())
    body.append(b"")
    body.append(caption.encode())
    
    body.append(f"--{boundary}".encode())
    body.append(f'Content-Disposition: form-data; name="parse_mode"'.encode())
    body.append(b"")
    body.append(b"HTML")
    
    body.append(f"--{boundary}".encode())
    body.append(f'Content-Disposition: form-data; name="document"; filename="{filename}"'.encode())
    body.append(b"Content-Type: application/octet-stream")
    body.append(b"")
    body.append(file_bytes)
    body.append(f"--{boundary}--".encode())
    
    data = b"\r\n".join(body)
    req = urllib.request.Request(url, data=data)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"Upload Error: {e}")
        return None

def get_file(file_id):
    result = api_call("getFile", {"file_id": file_id})
    if result and result.get("ok"):
        path = result["result"]["file_path"]
        url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{path}"
        with urllib.request.urlopen(url) as resp:
            return resp.read()
    return None

def make_button(text, callback_data, emoji_id=None, style=None):
    btn = {"text": text, "callback_data": callback_data}
    if emoji_id:
        btn["icon_custom_emoji_id"] = str(emoji_id)
    if style:
        btn["style"] = style
    return btn

def main_menu():
    return {
        "inline_keyboard": [
            [make_button("Convert Now", "convert_now", EMOJI_ID['convert'], "primary")],
            [make_button("Convert Mode", "convert_mode", EMOJI_ID['gear'], "primary")],
            [make_button("Status", "status", EMOJI_ID['chart'], "primary")],
            [make_button("Leaderboard", "leaderboard", EMOJI_ID['trophy'], "primary")]
        ]
    }

def mode_menu():
    return {
        "inline_keyboard": [
            [make_button("Number Filter Mode", "mode_number", EMOJI_ID['numbers'], "success")],
            [make_button("Text Mode (Full Text)", "mode_text", EMOJI_ID['pen'], "success")],
            [make_button("Back to Menu", "back_to_menu", EMOJI_ID['back'], "danger")]
        ]
    }

def back_btn():
    return {
        "inline_keyboard": [
            [make_button("Back to Menu", "back_to_menu", EMOJI_ID['back'], "danger")]
        ]
    }

def download_btn():
    return {
        "inline_keyboard": [
            [make_button("Download Converted File", "download_file", EMOJI_ID['download'], "success")],
            [make_button("Back to Menu", "back_to_menu", EMOJI_ID['back'], "danger")]
        ]
    }

def load_stats():
    try:
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {'users': {}, 'global': {'daily': {}, 'lifetime': 0}}

def save_stats(stats):
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {'daily': {}}

def save_leaderboard(lb):
    with open(LEADERBOARD_FILE, 'w', encoding='utf-8') as f:
        json.dump(lb, f, ensure_ascii=False, indent=2)

def update_stats(user_id, username):
    stats = load_stats()
    today = datetime.now().strftime('%Y-%m-%d')
    if today not in stats['global']['daily']:
        stats['global']['daily'][today] = 0
    stats['global']['daily'][today] += 1
    stats['global']['lifetime'] += 1
    uid = str(user_id)
    if uid not in stats['users']:
        stats['users'][uid] = {'username': username, 'daily': {}, 'lifetime': 0}
    if today not in stats['users'][uid]['daily']:
        stats['users'][uid]['daily'][today] = 0
    stats['users'][uid]['daily'][today] += 1
    stats['users'][uid]['lifetime'] += 1
    stats['users'][uid]['username'] = username
    save_stats(stats)
    lb = load_leaderboard()
    if today not in lb['daily']:
        lb['daily'][today] = {}
    lb['daily'][today][uid] = lb['daily'][today].get(uid, 0) + 1
    save_leaderboard(lb)

def get_user_stats(user_id):
    stats = load_stats()
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    uid = str(user_id)
    if uid in stats['users']:
        daily_24h = stats['users'][uid]['daily'].get(today, 0) + stats['users'][uid]['daily'].get(yesterday, 0)
        lifetime = stats['users'][uid]['lifetime']
    else:
        daily_24h = 0
        lifetime = 0
    global_daily = stats['global']['daily'].get(today, 0) + stats['global']['daily'].get(yesterday, 0)
    global_lifetime = stats['global']['lifetime']
    return {'daily_24h': daily_24h, 'lifetime': lifetime, 'global_daily': global_daily, 'global_lifetime': global_lifetime}

def get_leaderboard():
    lb = load_leaderboard()
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    daily_data = {}
    for day in [today, yesterday]:
        if day in lb['daily']:
            for uid, count in lb['daily'][day].items():
                daily_data[uid] = daily_data.get(uid, 0) + count
    sorted_users = sorted(daily_data.items(), key=lambda x: x[1], reverse=True)[:10]
    stats = load_stats()
    top_10 = []
    for uid, count in sorted_users:
        username = stats['users'].get(uid, {}).get('username', f'ID:{uid}')
        top_10.append({'username': username, 'files': count})
    return top_10

def extract_numbers(text):
    lines = text.strip().split('\n')
    all_parts = []
    for line in lines:
        parts = line.split(',')
        for part in parts:
            part = part.strip().strip('"').strip("'").strip()
            if part:
                all_parts.append(part)
    numbers = []
    for part in all_parts:
        clean = re.sub(r'[^\d]', '', part)
        if 7 <= len(clean) <= 15:
            if part.startswith('+'):
                clean = '+' + clean
            numbers.append(clean)
    seen = set()
    unique = []
    for n in numbers:
        if n not in seen:
            seen.add(n)
            unique.append(n)
    return '\n'.join(unique)

def detect_country(phone):
    phone_clean = re.sub(r'[^\d]', '', phone)
    for code in sorted(COUNTRY_CODES.keys(), key=len, reverse=True):
        if phone_clean.startswith(code) or phone.startswith('+' + code):
            return COUNTRY_CODES[code]
    if phone_clean.startswith('0'):
        return {'name': 'Local', 'code': 'UN'}
    return {'name': 'Unknown', 'code': 'UN'}

def detect_dominant_country(numbers_text):
    lines = numbers_text.strip().split('\n')
    country_count = {}
    for line in lines:
        line = line.strip()
        if line:
            country = detect_country(line)
            code = country.get('code', 'UN')
            name = country['name']
            if code not in country_count:
                country_count[code] = {'count': 0, 'name': name}
            country_count[code]['count'] += 1
    if not country_count:
        return {'name': 'Unknown', 'code': 'UN'}
    dominant = max(country_count.items(), key=lambda x: x[1]['count'])
    return {'name': dominant[1]['name'], 'code': dominant[0]}

def process_numbers_only(text):
    lines = text.strip().split('\n')
    return '\n'.join(line.strip() for line in lines if line.strip())

def convert_file(file_bytes, filename, mode='number'):
    try:
        text = file_bytes.decode('utf-8')
    except:
        try:
            text = file_bytes.decode('latin-1')
        except:
            text = file_bytes.decode('utf-8', errors='ignore')
    ext = filename.lower().split('.')[-1] if '.' in filename else 'txt'
    if ext == 'csv':
        if mode == 'number':
            return extract_numbers(text)
        else:
            reader = csv.reader(io.StringIO(text))
            return '\n'.join(' | '.join(row) for row in reader)
    elif ext in ['vcf', 'vcard']:
        phones = re.findall(r'TEL[^:]*:([^\n]+)', text)
        if phones:
            text = '\n'.join(phones)
    if mode == 'number':
        return extract_numbers(text)
    return text

CONVERT_NOW = f"""{E['folder']} <b>Please send your file (.vcf, .pdf, .xlsx, .csv, .txt etc) or paste text for conversion.</b>

<b>The final conversion menu will appear after you provide the file.</b>"""

CONVERT_MODE = f"""{E['gear']} <b>Select Conversion Mode:</b>

{E['numbers']} <b>Number Filter (Default):</b>
<b>Extracts only numbers and removes everything else.</b>

{E['pen']} <b>Text Mode:</b>
<b>Converts your file exactly as it is without modifications.</b>"""

user_modes = {}
user_files = {}
pending_files = {}

def handle_update(update):
    if "message" in update:
        msg = update["message"]
        chat_id = msg["chat"]["id"]
        user_id = msg["from"]["id"]
        username = msg["from"].get("username") or msg["from"].get("first_name", f"ID:{user_id}")
        uid = str(user_id)
        
        if "text" in msg:
            text = msg["text"]
            if text == "/start":
                welcome_msg = f"""{E['wave']} <b>Welcome to Premium Batch Converter, {username}!</b>

{E['user']} <b>Hello, {username}!</b>

{E['bulb']} <b>How to use:</b>

{E['one']} <b>Send files (.vcf, .pdf, .xlsx, .csv, .docx, .txt etc) or paste text.</b>
{E['two']} <b>I will extract and clean your data automatically.</b>
{E['three']} <b>I will detect the Country &amp; Flag for numbers.</b>
{E['four']} <b>Click Convert Now to get your ready-to-use file.</b>

{E['gear']} <b>Use the buttons below to navigate options.</b>

{E['folder']} <b>Source Code:</b> <b>https://github.com/IegaIize/File-Converter.git</b>"""
                send_message(chat_id, welcome_msg, main_menu())
                return
            if text.startswith("/"):
                return
            
            mode = user_modes.get(uid, 'number')
            try:
                converted = extract_numbers(text) if mode == 'number' else text
                if mode == 'number':
                    converted = process_numbers_only(converted)
                
                user_files.pop(uid, None)
                country = detect_dominant_country(converted)
                total_lines = len(converted.split('\n'))
                flag_html = get_flag_html(country['code'])
                
                user_files[uid] = {
                    'text': converted,
                    'filename': f"converted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    'country': country,
                    'total': total_lines,
                    'flag_html': flag_html
                }
                update_stats(user_id, username)
                
                preview = converted[:400]
                if len(converted) > 400:
                    preview += f"\n... (+{len(converted)-400} chars)"
                
                mode_name = "Number Filter" if mode == 'number' else "Text"
                msg_text = f"""{E['check']} <b>Text Processed!</b>

{E['gear']} <b>Mode:</b> <b>{mode_name}</b>
{E['chart']} <b>Lines:</b> <b>{total_lines}</b>
{flag_html} <b>Country:</b> <b>{country['name']}</b>

<b>Preview:</b>
<pre>{preview}</pre>

{E['download']} <b>Click button below to download:</b>"""
                send_message(chat_id, msg_text, download_btn())
            except Exception as e:
                send_message(chat_id, f"<b>❌ Error:</b> <b>{e}</b>", back_btn())
        
        elif "document" in msg:
            doc = msg["document"]
            file_id = doc["file_id"]
            original_filename = doc.get("file_name", "file.txt")
            
            result = send_message(chat_id, f"{E['processing']} <b>Processing file...</b>", None)
            if result and result.get("ok"):
                pending_files[uid] = result["result"]["message_id"]
            else:
                pending_files[uid] = None
            
            file_bytes = get_file(file_id)
            if file_bytes is None:
                if pending_files.get(uid):
                    edit_message(chat_id, pending_files[uid], "<b>❌ Could not download file. Try again.</b>", back_btn())
                else:
                    send_message(chat_id, "<b>❌ Could not download file. Try again.</b>", back_btn())
                pending_files.pop(uid, None)
                return
            
            mode = user_modes.get(uid, 'number')
            try:
                converted = convert_file(file_bytes, original_filename, mode)
                user_files.pop(uid, None)
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                base_name = original_filename.rsplit('.', 1)[0]
                new_filename = f"{base_name}_converted_{timestamp}.txt"
                country = detect_dominant_country(converted)
                total_lines = len(converted.split('\n'))
                flag_html = get_flag_html(country['code'])
                
                user_files[uid] = {
                    'text': converted,
                    'filename': new_filename,
                    'country': country,
                    'total': total_lines,
                    'flag_html': flag_html
                }
                update_stats(user_id, username)
                
                preview = converted[:400]
                if len(converted) > 400:
                    preview += f"\n... (+{len(converted)-400} chars)"
                
                mode_name = "Number Filter" if mode == 'number' else "Text"
                msg_text = f"""{E['check']} <b>File Processed!</b>

{E['file']} <b>File:</b> <b>{original_filename}</b>
{E['gear']} <b>Mode:</b> <b>{mode_name}</b>
{E['chart']} <b>Lines:</b> <b>{total_lines}</b>
{flag_html} <b>Country:</b> <b>{country['name']}</b>

<b>Preview:</b>
<pre>{preview}</pre>

{E['download']} <b>Click button below to download:</b>"""
                
                if pending_files.get(uid):
                    edit_message(chat_id, pending_files[uid], msg_text, download_btn())
                else:
                    send_message(chat_id, msg_text, download_btn())
                
                pending_files.pop(uid, None)
            except Exception as e:
                if pending_files.get(uid):
                    edit_message(chat_id, pending_files[uid], f"<b>❌ Error:</b> <b>{e}</b>", back_btn())
                else:
                    send_message(chat_id, f"<b>❌ Error:</b> <b>{e}</b>", back_btn())
                pending_files.pop(uid, None)
    
    elif "callback_query" in update:
        query = update["callback_query"]
        chat_id = query["message"]["chat"]["id"]
        msg_id = query["message"]["message_id"]
        user_id = query["from"]["id"]
        uid = str(user_id)
        data = query["data"]
        answer_callback(query["id"])
        
        if data == "convert_now":
            edit_message(chat_id, msg_id, CONVERT_NOW, back_btn())
        elif data == "convert_mode":
            edit_message(chat_id, msg_id, CONVERT_MODE, mode_menu())
        elif data == "mode_number":
            user_modes[uid] = 'number'
            edit_message(chat_id, msg_id, f"{E['check']} <b>Number Filter Mode activated!</b>\n\n<b>Only numbers will be extracted from files.</b>", back_btn())
        elif data == "mode_text":
            user_modes[uid] = 'text'
            edit_message(chat_id, msg_id, f"{E['check']} <b>Text Mode (Full Text) activated!</b>\n\n<b>Files will be converted without modifications.</b>", back_btn())
        elif data == "status":
            s = get_user_stats(user_id)
            text = f"""{E['chart']} <b>CONVERSION STATUS</b>

{E['user']} <b>Your Stats:</b>
{E['clock']} <b>Last 24 Hours:</b> <b>{s['daily_24h']} Files</b>
{E['infinity']} <b>Life-Time:</b> <b>{s['lifetime']} Files</b>

{E['globe']} <b>Global Stats (All Users):</b>
{E['clock']} <b>Last 24 Hours:</b> <b>{s['global_daily']} Files</b>
{E['infinity']} <b>Life-Time:</b> <b>{s['global_lifetime']} Files</b>"""
            edit_message(chat_id, msg_id, text, back_btn())
        elif data == "leaderboard":
            top = get_leaderboard()
            medals = [E['gold'], E['silver'], E['bronze']]
            text = f"{E['trophy']} <b>Top 10 Converter (24h)</b>\n\n"
            if not top:
                text += "<b>No conversions yet today!</b>"
            else:
                for i, u in enumerate(top):
                    prefix = medals[i] if i < 3 else f"<b>{i+1}.</b>"
                    text += f"{prefix} <b>{u['username']} - {u['files']} Files</b>\n"
            edit_message(chat_id, msg_id, text, back_btn())
        elif data == "back_to_menu":
            back_msg = f"""{E['wave']} <b>Welcome to Premium Batch Converter, {username}!</b>

{E['user']} <b>Hello, {username}!</b>

{E['bulb']} <b>How to use:</b>

{E['one']} <b>Send files (.vcf, .pdf, .xlsx, .csv, .docx, .txt etc) or paste text.</b>
{E['two']} <b>I will extract and clean your data automatically.</b>
{E['three']} <b>I will detect the Country &amp; Flag for numbers.</b>
{E['four']} <b>Click Convert Now to get your ready-to-use file.</b>

{E['gear']} <b>Use the buttons below to navigate options.</b>

{E['folder']} <b>Source Code:</b> <b>https://github.com/IegaIize/File-Converter.git</b>"""
            edit_message(chat_id, msg_id, back_msg, main_menu())
        elif data == "download_file":
            if uid not in user_files:
                answer_callback(query["id"], "❌ No file found! Please upload a new file.")
                return
            fd = user_files[uid]
            caption = f"<blockquote>{fd['flag_html']} <b>Region:</b> <b>{fd['country']['name']}</b>\n{E['chart']} <b>Total Count:</b> <b>{fd['total']}</b></blockquote>"
            send_document(chat_id, fd['text'].encode('utf-8'), fd['filename'], caption)
            user_files.pop(uid, None)
            answer_callback(query["id"], "✅ File sent!")

def main():
    print("🤖 Premium Batch Converter Bot starting...")
    print("✅ Bot is ready! Waiting for messages...")
    while True:
        try:
            for update in get_updates():
                handle_update(update)
        except KeyboardInterrupt:
            print("\n👋 Bot stopped.")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    main()
