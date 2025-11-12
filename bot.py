# bot.py
# Telegram-bot: Glossary UK/US (100 слов)
# Отправляет английские варианты, транскрипции, перевод и озвучку (gTTS)
import os
import random
import tempfile
import logging
from gtts import gTTS
from pydub import AudioSegment
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("TOKEN")
print(token)  # для проверки


# ---------- Настройки ----------
TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

GLOSSARY = [
    {"id":1,"us":"color","uk":"colour","us_pr":"ˈkʌlər","uk_pr":"ˈkʌlə","ru":"цвет"},
    {"id":2,"us":"neighbor","uk":"neighbour","us_pr":"ˈneɪbər","uk_pr":"ˈneɪbə","ru":"сосед"},
    {"id":3,"us":"honor","uk":"honour","us_pr":"ˈɒnər","uk_pr":"ˈɒnə","ru":"честь"},
    {"id":4,"us":"favor","uk":"favour","us_pr":"ˈfeɪvər","uk_pr":"ˈfeɪvə","ru":"одолжение"},
    {"id":5,"us":"center","uk":"centre","us_pr":"ˈsɛntər","uk_pr":"ˈsɛn.tə","ru":"центр"},
    {"id":6,"us":"meter","uk":"metre","us_pr":"ˈmiːtər","uk_pr":"ˈmiːtə","ru":"метр"},
    {"id":7,"us":"theater","uk":"theatre","us_pr":"ˈθiːətər","uk_pr":"ˈθiːətə","ru":"театр"},
    {"id":8,"us":"analyze","uk":"analyse","us_pr":"ˈænəˌlaɪz","uk_pr":"ˈænəlaɪz","ru":"анализировать"},
    {"id":9,"us":"organize","uk":"organise","us_pr":"ˈɔːrɡəˌnaɪz","uk_pr":"ˈɔːɡənaɪz","ru":"организовывать"},
    {"id":10,"us":"realize","uk":"realise","us_pr":"ˈriːəˌlaɪz","uk_pr":"ˈriːəlaɪz","ru":"осознавать"},
    {"id":11,"us":"recognize","uk":"recognise","us_pr":"ˈrɛkəɡˌnaɪz","uk_pr":"ˈrɛkəɡnaɪz","ru":"узнавать"},
    {"id":12,"us":"traveling","uk":"travelling","us_pr":"ˈtrævəlɪŋ","uk_pr":"ˈtrævəlɪŋ","ru":"путешествие"},
    {"id":13,"us":"traveled","uk":"travelled","us_pr":"ˈtrævəld","uk_pr":"ˈtrævəld","ru":"путешествовал"},
    {"id":14,"us":"jewelry","uk":"jewellery","us_pr":"ˈdʒuːəlri","uk_pr":"ˈdʒuːəlri","ru":"ювелирные изделия"},
    {"id":15,"us":"catalog","uk":"catalogue","us_pr":"ˈkætəlɔːɡ","uk_pr":"ˈkætəlɒɡ","ru":"каталог"},
    {"id":16,"us":"dialog","uk":"dialogue","us_pr":"ˈdaɪəlɔːɡ","uk_pr":"ˈdaɪəˌlɒɡ","ru":"диалог"},
    {"id":17,"us":"program","uk":"programme","us_pr":"ˈproʊɡræm","uk_pr":"ˈprəʊɡræm","ru":"программа"},
    {"id":18,"us":"defense","uk":"defence","us_pr":"dɪˈfɛns","uk_pr":"dɪˈfɛns","ru":"защита"},
    {"id":19,"us":"offense","uk":"offence","us_pr":"əˈfɛns","uk_pr":"əˈfɛns","ru":"нападение"},
    {"id":20,"us":"license","uk":"licence","us_pr":"ˈlaɪsəns","uk_pr":"ˈlaɪsəns","ru":"лицензия"},
    {"id":21,"us":"practice","uk":"practise","us_pr":"ˈpræktɪs","uk_pr":"ˈpræktɪs","ru":"практиковать"},
    {"id":22,"us":"aluminum","uk":"aluminium","us_pr":"əˈluːmɪnəm","uk_pr":"ˌæljuːˈmɪniəm","ru":"алюминий"},
    {"id":23,"us":"tire","uk":"tyre","us_pr":"taɪər","uk_pr":"taɪə","ru":"шина"},
    {"id":24,"us":"plow","uk":"plough","us_pr":"plaʊ","uk_pr":"plaʊ","ru":"плуг"},
    {"id":25,"us":"fulfill","uk":"fulfil","us_pr":"fʊlˈfɪl","uk_pr":"fʊlˈfɪl","ru":"выполнять"},
    {"id":26,"us":"enroll","uk":"enrol","us_pr":"ɪnˈroʊl","uk_pr":"ɪnˈrɒl","ru":"зачислять"},
    {"id":27,"us":"gram","uk":"gramme","us_pr":"ɡræm","uk_pr":"ɡræm","ru":"грамм"},
    {"id":28,"us":"check","uk":"cheque","us_pr":"tʃɛk","uk_pr":"tʃɛk","ru":"чек"},
    {"id":29,"us":"gray","uk":"grey","us_pr":"ɡreɪ","uk_pr":"ɡreɪ","ru":"серый"},
    {"id":30,"us":"mom","uk":"mum","us_pr":"mɑːm","uk_pr":"mʌm","ru":"мама"},
    {"id":31,"us":"truck","uk":"lorry","us_pr":"trʌk","uk_pr":"ˈlɒri","ru":"грузовик"},
    {"id":32,"us":"apartment","uk":"flat","us_pr":"əˈpɑːrtmənt","uk_pr":"flæt","ru":"квартира"},
    {"id":33,"us":"cookie","uk":"biscuit","us_pr":"ˈkʊki","uk_pr":"ˈbɪskɪt","ru":"печенье"},
    {"id":34,"us":"fries","uk":"chips","us_pr":"fraɪz","uk_pr":"tʃɪps","ru":"картошка фри"},
    {"id":35,"us":"elevator","uk":"lift","us_pr":"ˈɛləveɪtər","uk_pr":"lɪft","ru":"лифт"},
    {"id":36,"us":"vacation","uk":"holiday","us_pr":"veɪˈkeɪʃən","uk_pr":"ˈhɒlɪdeɪ","ru":"отпуск"},
    {"id":37,"us":"eraser","uk":"rubber","us_pr":"ɪˈreɪzər","uk_pr":"ˈrʌbə","ru":"ластик"},
    {"id":38,"us":"candy","uk":"sweets","us_pr":"ˈkændi","uk_pr":"swiːts","ru":"конфеты"},
    {"id":39,"us":"sneakers","uk":"trainers","us_pr":"ˈsniːkərz","uk_pr":"ˈtreɪnərz","ru":"кроссовки"},
    {"id":40,"us":"diaper","uk":"nappy","us_pr":"ˈdaɪpər","uk_pr":"ˈnæpi","ru":"подгузник"},
    {"id":41,"us":"gas","uk":"petrol","us_pr":"ɡæs","uk_pr":"ˈpɛtrəl","ru":"бензин"},
    {"id":42,"us":"apartment building","uk":"block of flats","us_pr":"əˈpɑːrtmənt ˈbɪldɪŋ","uk_pr":"blɒk əv flæts","ru":"многоквартирный дом"},
    {"id":43,"us":"garbage","uk":"rubbish","us_pr":"ˈɡɑːrbɪdʒ","uk_pr":"ˈrʌbɪʃ","ru":"мусор"},
    {"id":44,"us":"movie","uk":"film","us_pr":"ˈmuːvi","uk_pr":"fɪlm","ru":"фильм"},
    {"id":45,"us":"mail","uk":"post","us_pr":"meɪl","uk_pr":"pəʊst","ru":"почта"},
    {"id":46,"us":"cell phone","uk":"mobile phone","us_pr":"sɛl foʊn","uk_pr":"ˈməʊbaɪl fəʊn","ru":"мобильный телефон"},
    {"id":47,"us":"sidewalk","uk":"pavement","us_pr":"ˈsaɪdwɔːk","uk_pr":"ˈpeɪvmənt","ru":"тротуар"},
    {"id":48,"us":"first floor","uk":"ground floor","us_pr":"fɜːrst flɔːr","uk_pr":"ɡraʊnd flɔː","ru":"первый этаж"},
    {"id":49,"us":"faucet","uk":"tap","us_pr":"ˈfɔːsɪt","uk_pr":"tæp","ru":"кран"},
    {"id":50,"us":"second floor","uk":"first floor","us_pr":"ˈsekənd flɔːr","uk_pr":"fɜːst flɔː","ru":"второй этаж"},
    {"id":51,"us":"flashlight","uk":"torch","us_pr":"ˈflæʃˌlaɪt","uk_pr":"tɔːtʃ","ru":"фонарик"},
    {"id":52,"us":"sweater","uk":"jumper","us_pr":"ˈswɛtər","uk_pr":"ˈdʒʌmpə","ru":"свитер"},
    {"id":53,"us":"soccer","uk":"football","us_pr":"ˈsɑːkər","uk_pr":"ˈfʊtbɔːl","ru":"футбол"},
    {"id":54,"us":"stove","uk":"cooker","us_pr":"stoʊv","uk_pr":"ˈkʊkə","ru":"кухонная плита"},
    {"id":55,"us":"zip code","uk":"postcode","us_pr":"zɪp koʊd","uk_pr":"pəʊstkəʊd","ru":"почтовый индекс"},
    {"id":56,"us":"crib","uk":"cot","us_pr":"krɪb","uk_pr":"kɒt","ru":"детская кроватка"},
    {"id":57,"us":"cookie jar","uk":"biscuit tin","us_pr":"ˈkʊki dʒɑːr","uk_pr":"ˈbɪskɪt tɪn","ru":"банка для печенья"},
    {"id":58,"us":"pacifier","uk":"dummy","us_pr":"ˈpæsɪˌfaɪər","uk_pr":"ˈdʌmi","ru":"соска-пустышка"},
    {"id":59,"us":"math","uk":"maths","us_pr":"mæθ","uk_pr":"mæθs","ru":"математика"},
    {"id":60,"us":"highway","uk":"motorway","us_pr":"ˈhaɪweɪ","uk_pr":"ˈməʊtəweɪ","ru":"шоссе"},
    {"id":61,"us":"movie theater","uk":"cinema","us_pr":"ˈmuːvi ˈθiːətər","uk_pr":"ˈsɪnɪmə","ru":"кинотеатр"},
    {"id":62,"us":"older brother","uk":"elder brother","us_pr":"ˈoʊldər ˈbrʌðər","uk_pr":"ˈeldə ˈbrʌðə","ru":"старший брат"},
    {"id":63,"us":"trash can","uk":"bin","us_pr":"ˈtræʃ kæn","uk_pr":"bɪn","ru":"мусорное ведро"},
    {"id":64,"us":"parking lot","uk":"car park","us_pr":"ˈpɑːrkɪŋ lɒt","uk_pr":"kɑː pɑːk","ru":"парковка"},
    {"id":65,"us":"jump rope","uk":"skipping rope","us_pr":"dʒʌmp roʊp","uk_pr":"ˈskɪpɪŋ rəʊp","ru":"скакалка"},
    {"id":66,"us":"line","uk":"queue","us_pr":"laɪn","uk_pr":"kjuː","ru":"очередь"},
    {"id":67,"us":"triangle","uk":"set square","us_pr":"ˈtraɪæŋɡəl","uk_pr":"set skweə","ru":"угольник"},
    {"id":68,"us":"trunk","uk":"boot","us_pr":"trʌŋk","uk_pr":"buːt","ru":"багажник"},
    {"id":69,"us":"hood","uk":"bonnet","us_pr":"hʊd","uk_pr":"ˈbɒnɪt","ru":"капот"},
    {"id":70,"us":"period","uk":"full stop","us_pr":"ˈpɪriəd","uk_pr":"fʊl stɒp","ru":"точка в конце предложения"},
    {"id":71,"us":"mailman","uk":"postman","us_pr":"ˈmeɪlmæn","uk_pr":"ˈpəʊstmən","ru":"почтальон"},
    {"id":72,"us":"oatmeal","uk":"porridge","us_pr":"ˈoʊtmiːl","uk_pr":"ˈpɒrɪdʒ","ru":"овсяная каша"},
    {"id":73,"us":"airplane","uk":"aeroplane","us_pr":"ˈɛrpleɪn","uk_pr":"ˈeərəpleɪn","ru":"самолёт"},
    {"id":74,"us":"suspenders","uk":"braces","us_pr":"səˈspɛndərz","uk_pr":"ˈbreɪsɪz","ru":"подтяжки"},
    {"id":75,"us":"windshield","uk":"windscreen","us_pr":"ˈwɪndʃiːld","uk_pr":"ˈwɪndskriːn","ru":"лобовое стекло"},
    {"id":76,"us":"pants","uk":"trousers","us_pr":"pænts","uk_pr":"ˈtraʊzəz","ru":"брюки"},
    {"id":77,"us":"underwear","uk":"pants","us_pr":"ˈʌndərweər","uk_pr":"pænts","ru":"нижнее бельё"},
    {"id":78,"us":"pit","uk":"stone","us_pr":"pɪt","uk_pr":"stəʊn","ru":"косточка (вишни, сливы, персика)"},
    {"id":79,"us":"stroller","uk":"pushchair","us_pr":"ˈstroʊlər","uk_pr":"ˈpʊʃtʃeə","ru":"детская коляска"},
    {"id":80,"us":"tuxedo","uk":"dinner jacket","us_pr":"tʌkˈsiːdoʊ","uk_pr":"ˈdɪnə ˈdʒækɪt","ru":"смокинг"},
    {"id":81,"us":"pantyhose","uk":"tights","us_pr":"ˈpæntiˌhoʊz","uk_pr":"taɪts","ru":"колготки"},
    {"id":82,"us":"counterclockwise","uk":"anticlockwise","us_pr":"ˈkaʊntərkɒkwaɪz","uk_pr":"ˌæntɪˈklɒkwaɪz","ru":"против часовой стрелки"},
    {"id":83,"us":"restroom","uk":"toilet","us_pr":"ˈrɛstruːm","uk_pr":"ˈtɔɪlɪt","ru":"туалет"},
    {"id":84,"us":"undershirt","uk":"vest","us_pr":"ˈʌndərˌʃɜːrt","uk_pr":"vest","ru":"майка (нательная)"},
    {"id":85,"us":"drugstore","uk":"chemist","us_pr":"ˈdrʌɡstɔːr","uk_pr":"ˈkɛmɪst","ru":"аптека"},
    {"id":86,"us":"waistcoat","us_pr":"vest","uk_pr":"ˈweɪskəʊt","ru":"жилет"},
    {"id":87,"us":"zipper","uk":"zip","us_pr":"ˈzɪpər","uk_pr":"zɪp","ru":"молния (на одежде)"},
    {"id":88,"us":"overpass","uk":"flyover","us_pr":"ˈoʊvərˌpæs","uk_pr":"ˈflaɪˌəʊvə","ru":"эстакада"},
    {"id":89,"us":"pumps","uk":"court shoes","us_pr":"pʌmps","uk_pr":"kɔːt ʃuːz","ru":"туфли-лодочки"},
    {"id":90,"us":"stepbrother","uk":"stepsibling","us_pr":"ˈstɛpˌbrʌðər","uk_pr":"ˈstɛpˌsɪblɪŋ","ru":"сводный брат"},
    {"id":91,"us":"mailbox","uk":"postbox","us_pr":"ˈmeɪlbɑːks","uk_pr":"ˈpəʊstbɒks","ru":"почтовый ящик"},
    {"id":92,"us":"bill","uk":"note","us_pr":"bɪl","uk_pr":"nəʊt","ru":"банкнота"},
    {"id":93,"us":"store","uk":"shop","us_pr":"stɔːr","uk_pr":"ʃɒp","ru":"магазин"},
    {"id":94,"us":"corn","uk":"maize","us_pr":"kɔːrn","uk_pr":"meɪz","ru":"кукуруза"},
    {"id":95,"us":"grade","uk":"mark","us_pr":"ɡreɪd","uk_pr":"mɑːk","ru":"оценка"},
    {"id":96,"us":"salesclerk","uk":"shop assistant","us_pr":"ˈseɪlzklɜːrk","uk_pr":"ʃɒp əˈsɪstənt","ru":"продавец-консультант"},
    {"id":97,"us":"garbage truck","uk":"dustcart","us_pr":"ˈɡɑːrbɪdʒ trʌk","uk_pr":"ˈdʌstkɑːt","ru":"мусоровоз"},
    {"id":98,"us":"intersection","uk":"junction","us_pr":"ˈɪntərˌsɛkʃən","uk_pr":"ˈdʒʌŋkʃən","ru":"перекрёсток"},
    {"id":99,"us":"sick","uk":"ill","us_pr":"sɪk","uk_pr":"ɪl","ru":"больной"},
    {"id":100,"us":"shopping cart","uk":"trolley","us_pr":"ˈʃɑːpɪŋ kɑːrt","uk_pr":"ˈtrɒli","ru":"тележка для продуктов, покупок"},
    {"id":101,"us":"traffic circle","uk":"roundabout","us_pr":"ˈtræfɪk ˈsɜːrkl","uk_pr":"ˈraʊndəbaʊt","ru":"круговое движение"},
    {"id":102,"us":"subway","uk":"underground","us_pr":"ˈsʌbweɪ","uk_pr":"ˈʌndəɡraʊnd","ru":"метро"},
    {"id":103,"us":"railroad","uk":"railway","us_pr":"ˈreɪlroʊd","uk_pr":"ˈreɪlweɪ","ru":"железная дорога"},
    {"id":104,"us":"one-way ticket","uk":"single","us_pr":"wʌn weɪ ˈtɪkɪt","uk_pr":"ˈsɪŋɡl","ru":"билет в одну сторону"},
    {"id":105,"us":"antenna","uk":"aerial","us_pr":"ænˈtenə","uk_pr":"ˈeəriəl","ru":"антенна"},
    {"id":106,"us":"turn signal","uk":"indicator","us_pr":"tɜːrn ˈsɪɡnəl","uk_pr":"ˈɪndɪkeɪtə","ru":"указатель поворота"},
    {"id":107,"us":"license plate","uk":"number plate","us_pr":"ˈlaɪsəns pleɪt","uk_pr":"ˈnʌmbə pleɪt","ru":"номерной знак"},
    {"id":108,"us":"wrench","uk":"spanner","us_pr":"rentʃ","uk_pr":"ˈspænə","ru":"гаечный ключ"},
    {"id":109,"us":"streetcar","uk":"tram","us_pr":"ˈstriːtkɑːr","uk_pr":"træm","ru":"трамвай"},
    {"id":110,"us":"fall","uk":"autumn","us_pr":"fɔːl","uk_pr":"ˈɔːtəm","ru":"осень"},
    {"id":111,"us":"checkers","uk":"draughts","us_pr":"ˈtʃekərz","uk_pr":"drɑːfts","ru":"шашки"},
    {"id":112,"us":"bangs","uk":"fringe","us_pr":"bæŋz","uk_pr":"frɪndʒ","ru":"чёлка"},
    {"id":113,"us":"nail polish","uk":"nail varnish","us_pr":"neɪl ˈpɒlɪʃ","uk_pr":"neɪl ˈvɑːnɪʃ","ru":"лак для ногтей"},
    {"id":114,"us":"closet","uk":"built-in wardrobe","us_pr":"ˈklɑːzɪt","uk_pr":"ˌbɪlt ɪn ˈwɔːdrəʊb","ru":"встроенный шкаф"},
    {"id":115,"us":"schedule","uk":"timetable","us_pr":"ˈskedʒuːl","uk_pr":"ˈtaɪmˌteɪbl","ru":"расписание"},
    {"id":116,"us":"yard","uk":"garden","us_pr":"jɑːrd","uk_pr":"ˈɡɑːdn","ru":"двор"},
    {"id":117,"us":"zucchini","uk":"courgette","us_pr":"zuˈkiːni","uk_pr":"kɔːˈʒet","ru":"кабачок"},
    {"id":118,"us":"eggplant","uk":"aubergine","us_pr":"ˈeɡplænt","uk_pr":"ˈəʊbəʒiːn","ru":"баклажан"},
    {"id":119,"us":"band-aid","uk":"plaster","us_pr":"ˈbænd eɪd","uk_pr":"ˈplɑːstə","ru":"пластырь"},
    {"id":120,"us":"sweats","uk":"tracksuit","us_pr":"swets","uk_pr":"ˈtræksuːt","ru":"спортивный костюм"},
    {"id":121,"us":"roommate","uk":"flatmate","us_pr":"ˈruːmˌmeɪt","uk_pr":"ˈflætmeɪt","ru":"сосед по жилью"},
    {"id":122,"us":"graduate student","uk":"postgraduate","us_pr":"ˈɡrædʒuət ˈstjuːdənt","uk_pr":"ˌpəʊstˈɡrædʒuət","ru":"аспирант, магистрант"},
    {"id":123,"us":"college professor","uk":"university lecturer","us_pr":"ˈkɒlɪdʒ prəˈfesər","uk_pr":"juːnɪˈvɜːsɪti ˈlektʃərə","ru":"преподаватель университета"},
    {"id":124,"us":"sharpshooter","uk":"marksman","us_pr":"ˈʃɑːrpˌʃuːtər","uk_pr":"ˈmɑːksmən","ru":"меткий стрелок"},
    {"id":125,"us":"ap exams","uk":"a-levels","us_pr":"ˌeɪ piː ɪɡˈzæmz","uk_pr":"ˈeɪ ˌlevəlz","ru":"экзамены для поступления в университет / продвинутые школьные курсы"},
    {"id":126,"us":"ticket office","uk":"booking office","us_pr":"ˈtɪkɪt ˌɒfɪs","uk_pr":"ˈbʊkɪŋ ˌɒfɪs","ru":"билетная касса"},
    {"id":127,"us":"fall semester","uk":"autumn term","us_pr":"fɔːl səˈmestər","uk_pr":"ˈɔːtəm tɜːm","ru":"осенний семестр"},
    {"id":128,"us":"freight train","uk":"goods train","us_pr":"ˈfreɪt treɪn","uk_pr":"ɡʊdz treɪn","ru":"грузовой поезд"},
    {"id":129,"us":"package","uk":"parcel","us_pr":"ˈpækɪdʒ","uk_pr":"ˈpɑːsəl","ru":"посылка"},
    {"id":130,"us":"beet","uk":"beetroot","us_pr":"biːt","uk_pr":"ˈbiːtruːt","ru":"свёкла"},
    {"id":131,"us":"baggage","uk":"luggage","us_pr":"ˈbæɡɪdʒ","uk_pr":"ˈlʌɡɪdʒ","ru":"багаж"},
    {"id":132,"us":"round-trip fare","uk":"return fare","us_pr":"ˌraʊnd ˈtrɪp feər","uk_pr":"rɪˈtɜːn feə","ru":"билет туда-обратно"},
    {"id":133,"us":"one-way fare","uk":"single fare","us_pr":"ˈwʌn weɪ feər","uk_pr":"ˈsɪŋɡəl feə","ru":"билет в одну сторону"},
    {"id":134,"us":"motorcycle","uk":"motorbike","us_pr":"ˈmoʊtərˌsaɪkəl","uk_pr":"ˈməʊtəbaɪk","ru":"мотоцикл"},
    {"id":135,"us":"guardrail","uk":"crash barrier","us_pr":"ˈɡɑːrdreɪl","uk_pr":"ˈkræʃ ˌbæriə","ru":"дорожный отбойник"},
    {"id":136,"us":"janitor","uk":"caretaker","us_pr":"ˈdʒænɪtər","uk_pr":"ˈkeəteɪkə","ru":"смотритель, уборщик, завхоз"},
    {"id":137,"us":"atm","uk":"cashpoint","us_pr":"ˌeɪ tiː ˈem","uk_pr":"ˈkæʃpɔɪnt","ru":"банкомат"},
    {"id":138,"us":"superintendent","uk":"caretaker","us_pr":"ˌsuːpərɪnˈtendənt","uk_pr":"ˈkeəteɪkə","ru":"смотритель, управляющий"},
    {"id":139,"us":"trash can","uk":"rubbish bin","us_pr":"ˈtræʃ kæn","uk_pr":"ˈrʌbɪʃ bɪn","ru":"мусорное ведро"},
    {"id":140,"us":"plastic wrap","uk":"cling film","us_pr":"ˈplæstɪk ræp","uk_pr":"ˈklɪŋ fɪlm","ru":"пищевая плёнка"},
    {"id":141,"us":"wax paper","uk":"greaseproof paper","us_pr":"ˈwæks ˌpeɪpər","uk_pr":"ˈɡriːspruːf ˌpeɪpə","ru":"вощёная бумага"},
    {"id":142,"us":"cafeteria","uk":"canteen","us_pr":"ˌkæfəˈtɪriə","uk_pr":"kænˈtiːn","ru":"столовая"},
    {"id":143,"us":"résumé","uk":"cv","us_pr":"ˈrezəˌmeɪ","uk_pr":"ˈsiːˈviː","ru":"резюме"},
    {"id":144,"us":"principal","uk":"headteacher","us_pr":"ˈprɪnsəpəl","uk_pr":"ˈhedˌtiːtʃə","ru":"директор школы"},
    {"id":145,"us":"vice-principal","uk":"deputy head","us_pr":"ˈvaɪs ˈprɪnsəpəl","uk_pr":"ˈdepjʊti hed","ru":"заместитель директора"},
    {"id":146,"us":"homeroom teacher","uk":"form tutor","us_pr":"ˈhoʊmruːm ˈtiːtʃər","uk_pr":"fɔːm ˈtjuːtə","ru":"классный руководитель"},
    {"id":147,"us":"review","uk":"revision","us_pr":"rɪˈvjuː","uk_pr":"rɪˈvɪʒən","ru":"повторение материала перед экзаменом"},
    {"id":148,"us":"grades","uk":"marks","us_pr":"ɡreɪdz","uk_pr":"mɑːks","ru":"оценки"},
    {"id":149,"us":"raincoat","uk":"mac","us_pr":"ˈreɪnˌkoʊt","uk_pr":"mæk","ru":"дождевик, плащ"},
    {"id":150,"us":"overalls","uk":"dungarees","us_pr":"ˈoʊvərˌɔːlz","uk_pr":"ˌdʌŋɡəˈriːz","ru":"комбинезон"},
    {"id":151,"us":"grading rubric","uk":"mark scheme","us_pr":"ˈɡreɪdɪŋ ˈruːbrɪk","uk_pr":"mɑːk skiːm","ru":"критерии оценивания"},
    {"id":152,"us":"flashlight beam","uk":"torchlight","us_pr":"ˈflæʃlaɪt biːm","uk_pr":"ˈtɔːtʃlaɪt","ru":"луч фонаря"},
    {"id":153,"us":"purse","uk":"handbag","us_pr":"pɜːrs","uk_pr":"ˈhændbæɡ","ru":"женская сумочка"},
    {"id":154,"us":"wallet","uk":"purse","us_pr":"ˈwɒlɪt","uk_pr":"pɜːs","ru":"кошелёк"},
    {"id":155,"us":"funeral director","uk":"undertaker","us_pr":"ˈfjuːnərəl dəˈrektər","uk_pr":"ˈʌndəˌteɪkə","ru":"работник похоронного бюро"},
    {"id":156,"us":"detour","uk":"diversion","us_pr":"ˈdiːtʊr","uk_pr":"daɪˈvɜːʃən","ru":"объезд"},
    {"id":157,"us":"divided highway","uk":"dual carriageway","us_pr":"dɪˈvaɪdɪd ˈhaɪweɪ","uk_pr":"ˈdjuːəl ˈkærɪdʒweɪ","ru":"автомагистраль с разделительной полосой"},
    {"id":158,"us":"flyover","uk":"flypast","us_pr":"ˈflaɪˌoʊvər","uk_pr":"ˈflaɪpɑːst","ru":"пролёт авиации (на параде)"},
    {"id":159,"us":"q-tip","uk":"cotton bud","us_pr":"ˈkjuː tɪp","uk_pr":"ˈkɒtn bʌd","ru":"ватная палочка"},
    {"id":160,"us":"quotation marks","uk":"inverted commas","us_pr":"kwoʊˈteɪʃən mɑːrks","uk_pr":"ɪnˈvɜːtɪd ˈkɒməz","ru":"кавычки"},
    {"id":161,"us":"hair clip","uk":"hair slide","us_pr":"heə klɪp","uk_pr":"heə slaɪd","ru":"заколка для волос"},
    {"id":162,"us":"braid","uk":"plait","us_pr":"breɪd","uk_pr":"plæt","ru":"коса (прическа)"},
    {"id":163,"us":"drapes","uk":"curtains","us_pr":"dreɪps","uk_pr":"ˈkɜːtnz","ru":"шторы"},
    {"id":164,"us":"tv","uk":"telly","us_pr":"ˌtiːˈviː","uk_pr":"ˈtɛli","ru":"телевизор"},
    {"id":165,"us":"news anchor","uk":"newsreader","us_pr":"ˈnuːz ˈæŋkər","uk_pr":"ˈnjuːzˌriːdə","ru":"ведущий новостей"},
    {"id":166,"us":"commercial","uk":"advert","us_pr":"kəˈmɜːʃəl","uk_pr":"ˈædvɜːt","ru":"реклама"},
    {"id":167,"us":"rectangle","uk":"oblong","us_pr":"ˈrektæŋɡəl","uk_pr":"ˈɒblɒŋ","ru":"прямоугольник"},
    {"id":168,"us":"season","uk":"series","us_pr":"ˈsiːzən","uk_pr":"ˈsɪəriːz","ru":"сезон, сериал"},
    {"id":169,"us":"thumbtack","uk":"drawing pin","us_pr":"ˈθʌmˌtæk","uk_pr":"ˈdrɔːɪŋ pɪn","ru":"канцелярская кнопка"},
    {"id":170,"us":"trash can","uk":"dustbin","us_pr":"ˈtræʃ kæn","uk_pr":"ˈdʌstbɪn","ru":"мусорное ведро"},
    {"id":171,"us":"zero","uk":"nought","us_pr":"ˈzɪəroʊ","uk_pr":"nɔːt","ru":"ноль"},
    {"id":172,"us":"zero","uk":"nil","us_pr":"ˈzɪəroʊ","uk_pr":"nɪl","ru":"ноль (в счёте)"},
    {"id":173,"us":"lumber","uk":"timber","us_pr":"ˈlʌmbər","uk_pr":"ˈtɪmbə","ru":"древесина, пиломатериалы"},
    {"id":174,"us":"utilities","uk":"mains","us_pr":"juːˈtɪlɪtiz","uk_pr":"meɪnz","ru":"коммуникации, электросеть, водопровод"},
    {"id":175,"us":"foster parent","uk":"foster carer","us_pr":"ˈfɒstər ˈperənt","uk_pr":"ˈfɒstər ˈkeərə","ru":"приёмный родитель"},
    {"id":176,"us":"blacktop","uk":"tarmac","us_pr":"ˈblækˌtɒp","uk_pr":"ˈtɑːmæk","ru":"асфальт / взлётно-посадочная полоса"},
    {"id":177,"us":"realtor","uk":"estate agent","us_pr":"ˈriːəltər","uk_pr":"ɪˈsteɪt ˌeɪdʒənt","ru":"риэлтор"},
    {"id":178,"us":"real estate developer","uk":"property developer","us_pr":"ˈrɪəl ɪˌsteɪt dɪˈveləpər","uk_pr":"ˈprɒpəti dɪˈveləpə","ru":"застройщик"},
    {"id":179,"us":"conservatory","uk":"conservatoire","us_pr":"kənˈsɜːrvətɔːri","uk_pr":"kənˈsɜːvətwɑː","ru":"музыкальная академия"},
    {"id":180,"us":"public school","uk":"state school","us_pr":"ˈpʌblɪk skuːl","uk_pr":"ˈsteɪt skuːl","ru":"государственная школа"},
    {"id":181,"us":"private school","uk":"public school","us_pr":"ˈpraɪvət skuːl","uk_pr":"ˈpʌblɪk skuːl","ru":"частная школа (в Британии наоборот)"},
    {"id":182,"us":"liquor store","uk":"off-licence","us_pr":"ˈlɪkər stɔːr","uk_pr":"ˈɒf ˌlaɪsəns","ru":"магазин спиртного"},
    {"id":183,"us":"newsstand","uk":"newsagent","us_pr":"ˈnuːzˌstænd","uk_pr":"ˈnjuːzˌeɪdʒənt","ru":"киоск с газетами"},
    {"id":184,"us":"return key","uk":"carriage return","us_pr":"rɪˈtɜːrn kiː","uk_pr":"ˈkærɪdʒ rɪˈtɜːn","ru":"клавиша «ввод»"},
    {"id":185,"us":"thumbtack","uk":"drawing pin","us_pr":"ˈθʌmˌtæk","uk_pr":"ˈdrɔːɪŋ pɪn","ru":"канцелярская кнопка"},
    {"id":186,"us":"scotch tape","uk":"sellotape","us_pr":"ˈskɒtʃ teɪp","uk_pr":"ˈseləʊteɪp","ru":"скотч, клейкая лента"},
    {"id":187,"us":"backpack","uk":"rucksack","us_pr":"ˈbækˌpæk","uk_pr":"ˈrʌksæk","ru":"рюкзак"},
    {"id":188,"us":"zee","uk":"zed","us_pr":"ziː","uk_pr":"zed","ru":"буква Z (произношение)"},
    {"id":189,"us":"sled","uk":"sledge","us_pr":"sled","uk_pr":"sledʒ","ru":"сани"},
    {"id":190,"us":"liter","uk":"litre","us_pr":"ˈliːtər","uk_pr":"ˈliːtə","ru":"литр"},
    {"id":191,"us":"fire truck","uk":"fire engine","us_pr":"ˈfaɪə trʌk ","uk_pr":"ˈfaɪə ˈenʤɪn","ru":"пожарная машина"},
    {"id":192,"us":"bell pepper","uk":"capsicum","us_pr":"ˈbɛl ˈpɛpər","uk_pr":"ˈkæpsɪkəm","ru":"сладкий перец"},
    {"id":193,"us":"checkbook","uk":"cheque book","us_pr":"ˈtʃekbʊk","uk_pr":"ˈtʃek bʊk","ru":"чековая книжка"},
    {"id":194,"us":"caregiver","uk":"carer","us_pr":"ˈkerˌɡɪvər","uk_pr":"ˈkeərə","ru":"сиделка, опекун"},
    {"id":195,"us":"law office","uk":"barrister’s chamber","us_pr":"ˈlɔː ˌɒfɪs","uk_pr":"ˈbærɪstəz ˈtʃeɪmbə","ru":"юридическая контора"},
    {"id":196,"us":"in the hospital","uk":"in hospital","us_pr":"ɪn ðə ˈhɒspɪtl","uk_pr":"ɪn ˈhɒspɪtl","ru":"в больнице (без артикля в UK, с артиклем в US)"},
    {"id":197,"us":"on the weekend","uk":"at the weekend","us_pr":"ɒn ðə ˈwiːkend","uk_pr":"æt ðə ˈwiːkend","ru":"на выходных"},
    {"id":198,"us":"have to","uk":"have got to","us_pr":"hæv tuː","uk_pr":"hæv ɡɒt tuː","ru":"должен / иметь (структурное различие)"},
    {"id":199,"us":"cilantro","uk":"coriander","us_pr":"sɪˈlɑːntroʊ","uk_pr":"ˈkɒriˌændər","ru":"кинза / кориандр"},
    {"id":200,"us":"baking sheet","uk":"baking tray","us_pr":"ˈbeɪkɪŋ ʃiːt","uk_pr":"ˈbeɪkɪŋ treɪ","ru":"противен"}    
]

# ---------- Вспомогательные функции ----------

from gtts import gTTS
import os

async def generate_audio_files(word_text):
    """Создаёт два MP3-файла (US и UK) без ffmpeg"""
    # Создаём папку audio, если её нет
    if not os.path.exists("audio"):
        os.makedirs("audio")

    us_path = f"audio/{word_text}_us.mp3"
    uk_path = f"audio/{word_text}_uk.mp3"

    # 🇺🇸 Американское произношение
    tts_us = gTTS(word_text, lang="en", tld="com")
    tts_us.save(us_path)

    # 🇬🇧 Британское произношение
    tts_uk = gTTS(word_text, lang="en", tld="co.uk")
    tts_uk.save(uk_path)

    return us_path, uk_path

def get_word_by_text(word_text: str):
    """Ищет слово в GLOSSARY по американской или британской версии"""
    word_text = word_text.lower()
    for item in GLOSSARY:
        if word_text == item.get("us", "").lower() or word_text == item.get("uk", "").lower():
            return item
    return None

def format_word_entry(entry):
    """Форматирует слово для вывода"""
    us = entry.get("us", "")
    uk = entry.get("uk", "")
    us_pr = entry.get("us_pr", "")
    uk_pr = entry.get("uk_pr", "")
    ru = entry.get("ru", "")
    text = (
        f"🇺🇸 *{us}* — {ru}\n"
        f"US: {us_pr}\n"
        f"🇬🇧 {uk} — {uk_pr}"
    )
    return text

def speak_word(text: str, lang: str):
    """Создаёт аудиофайл gTTS и возвращает путь (ogg)"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts = gTTS(text=text, lang=lang)
        tts.save(tmp.name)
        mp3_path = tmp.name

    ogg_path = mp3_path.replace(".mp3", ".ogg")
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(ogg_path, format="ogg")
    os.remove(mp3_path)
    return ogg_path

def split_text(text: str, max_length: int = 4000):
    """
    Разбивает длинный текст на несколько сообщений
    :param text: исходный текст
    :param max_length: макс. длина одной части
    :return: список частей
    """
    lines = text.split("\n")
    chunks = []
    current_chunk = ""

    for line in lines:
        if len(current_chunk) + len(line) + 1 > max_length:
            chunks.append(current_chunk)
            current_chunk = ""
        current_chunk += line + "\n"

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def generate_glossary(text, max_words=200):
    words = text.split()
    unique_words = list(dict.fromkeys(words))  # убираем дубликаты
    glossary = unique_words[:max_words]
    return glossary

def show_glossary():
    chunk_size = 50  # Сколько слов показывать за раз
    for i in range(0, len(glossary), chunk_size):
        print(glossary[i:i+chunk_size])

# ---------- Обработчики ----------
from telegram import ReplyKeyboardMarkup, KeyboardButton

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие и клавиатура"""
    keyboard = ReplyKeyboardMarkup(
        [
            [KeyboardButton("/random"), KeyboardButton("/translate")],
            [KeyboardButton("/glossary"), KeyboardButton("/help")]
        ],
        resize_keyboard=True
    )
    text = "Привет! Я бот-глоссарий US vs UK. Выбери команду:"
    await update.message.reply_text(text, reply_markup=keyboard)

async def random_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    entry = random.choice(GLOSSARY)
    await send_word_entry(update, context, entry)

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗️ Укажи слово для поиска: /translate color")
        return

    word_text = " ".join(context.args)
    entry = get_word_by_text(word_text)
    if not entry:
        await update.message.reply_text("❗️ Слово не найдено.")
        return

    await send_word_entry(update, context, entry)
 
async def glossary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет весь словарь, разбитый на несколько сообщений"""
    if not GLOSSARY:
        await update.message.reply_text("Словарь пуст.")
        return

    # Форматируем все слова в строки
    lines = []
    for entry in GLOSSARY:
        us = entry.get("us", "")
        uk = entry.get("uk", "")
        us_pr = entry.get("us_pr", "")
        uk_pr = entry.get("uk_pr", "")
        ru = entry.get("ru", "")
        wid = entry.get("id", "")
        line = f"{wid}. {us} ({us_pr}) / {uk} ({uk_pr}) — {ru}"
        lines.append(line)

    full_text = "\n".join(lines)
    chunks = split_text(full_text)  # разбиваем на части

    # Отправляем все части по очереди
    for chunk in chunks:
        await update.message.reply_text(chunk)
        
async def send_word_entry(update: Update, context: ContextTypes.DEFAULT_TYPE, entry):
    text = format_word_entry(entry)
    try:
        await update.message.reply_markdown_v2(text)
    except Exception:
        # Fallback if markdown v2 fails for the client
        await update.message.reply_text(text)

    # 🎧 Озвучка — 🇺🇸 и 🇬🇧
    us_audio = None
    uk_audio = None
    try:
        us_word = entry.get("us", "")
        uk_word = entry.get("uk", "")

        # Генерируем разные аудиофайлы для US и UK
        us_audio, _ = await generate_audio_files(us_word)
        _, uk_audio = await generate_audio_files(uk_word)

        # Отправляем 🇺🇸 американскую озвучку
        with open(us_audio, "rb") as f_us:
            await update.message.reply_voice(f_us, caption=f"🇺🇸 {us_word} — US pronunciation")

        # Отправляем 🇬🇧 британскую озвучку
        with open(uk_audio, "rb") as f_uk:
            await update.message.reply_voice(f_uk, caption=f"🇬🇧 {uk_word} — UK pronunciation")

    except Exception as e:
        logger.error(f"Ошибка при создании или отправке озвучек: {e}")

    finally:
        # Удаляем временные файлы
        for file_path in [us_audio, uk_audio]:
            try:
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)
            except Exception:
                pass

# ---------- Основная функция ----------

def split_text(text: str, max_length: int = 4000):
    """
    Разбивает длинный текст на несколько сообщений
    """
    lines = text.split("\n")
    chunks = []
    current_chunk = ""

    for line in lines:
        if len(current_chunk) + len(line) + 1 > max_length:
            chunks.append(current_chunk)
            current_chunk = ""
        current_chunk += line + "\n"

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


async def glossary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет весь словарь, разбитый на несколько сообщений"""
    if not GLOSSARY:
        await update.message.reply_text("Словарь пуст.")
        return

    # Форматируем все слова в строки
    lines = []
    for entry in GLOSSARY:
        us = entry.get("us", "")
        uk = entry.get("uk", "")
        us_pr = entry.get("us_pr", "")
        uk_pr = entry.get("uk_pr", "")
        ru = entry.get("ru", "")
        wid = entry.get("id", "")
        line = f"{wid}. {us} ({us_pr}) / {uk} ({uk_pr}) — {ru}"
        lines.append(line)

    full_text = "\n".join(lines)

    # Разбиваем на части (примерно по 6000 символов, обычно выходит 4-5 сообщения)
    chunks = split_text(full_text)

    for chunk in chunks:
        await update.message.reply_text(chunk)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("random", random_word))
    app.add_handler(CommandHandler("translate", translate))
    app.add_handler(CommandHandler("glossary", glossary))
    print("🤖 Bot started... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()