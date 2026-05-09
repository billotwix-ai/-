import telebot
import hashlib
import os
import re
import time
from datetime import datetime
from colorama import Fore, Style, init

# تهيئة الألوان
init(autoreset=True)

# --- إعدادات الهوية (ضع بياناتك هنا) ---
TOKEN = '8670155819:AAHJ0P9GnVgl0WL16NJQJqX90Ph9NEYtEgQ'
ADMIN_ID = 7579308942

# تفعيل البوت بنظام الخيوط المتعددة (Threads) لمعالجة المهام بالتوازي
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=10)

sessions = {}

# ألوان النيون للواجهة
C_CYAN = Fore.CYAN + Style.BRIGHT
C_GREEN = Fore.GREEN + Style.BRIGHT
C_GOLD = Fore.YELLOW + Style.BRIGHT
C_MAGENTA = Fore.MAGENTA + Style.BRIGHT

def log_ai(status):
    now = datetime.now().strftime("%M:%S")
    print(f"{C_MAGENTA}[AI-CORE {now}] {C_GOLD}⚡ {status}")

# --- محرك OMEGA الصاروخي (النسخة النهائية) ---
def omega_processor(orig_path, mod_path, sig_text, use_ai=False):
    with open(orig_path, 'rb') as f: orig_data = f.read()
    with open(mod_path, 'rb') as f: mod_data = f.read()
    
    header = orig_data[:64]
    processed = bytearray(header + mod_data[64:])
    
    orig_size = len(orig_data)
    if len(processed) < orig_size:
        processed.extend(b'\x00' * (orig_size - len(processed)))
    
    # محرك التشفير الصاروخي
    key = hashlib.sha256(sig_text.encode()).digest()
    key_len = len(key)
    
    # نمط AI Turbo للسرعة الصاروخية
    step = 1
    if use_ai and len(processed) > 500000: # تفعيل الذكاء للملفات المتوسطة والكبيرة
        step = 2 

    for i in range(64, len(processed), step):
        val = processed[i] ^ key[i % key_len]
        # تشفير مصفوفة الدوران (Matrix Rotation)
        processed[i] = ((val << 4) & 0xFF) | (val >> 4)
        
    return processed

# --- الأزرار المتوهجة ---
def ai_keyboard():
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        telebot.types.InlineKeyboardButton("🚀 AI Turbo (سرعة صاروخية)", callback_data="run_ai"),
        telebot.types.InlineKeyboardButton("🛡️ Standard (تشفير دقيق)", callback_data="run_std")
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id != ADMIN_ID: return
    sessions[message.chat.id] = {"step": 1}
    bot.send_message(message.chat.id, 
                     f"🛸 {C_MAGENTA}--- OMEGA AI SYSTEM READY ---\n\n"
                     f"⚙️ {C_CYAN}Mode: Multi-Threaded\n"
                     f"🏎️ {C_CYAN}Engine: AI-Turbo Powered\n\n"
                     f"📍 ارسل الملف الأصلي (.3D) للبدء.")

@bot.message_handler(content_types=['document'])
def pipeline(message):
    cid = message.chat.id
    if cid not in sessions: return
    
    step = sessions[cid]["step"]
    file_info = bot.get_file(message.document.file_id)
    downloaded = bot.download_file(file_info.file_path)
    
    t_name = f"tmp_{step}_{cid}.dat"
    with open(t_name, 'wb') as f: f.write(downloaded)

    if step == 1:
        sessions[cid]["orig"] = t_name
        sessions[cid]["step"] = 2
        bot.send_message(cid, f"✅ {C_GREEN}استقبال الأصلي بنجاح. الآن ارسل CodeResources.")
    elif step == 2:
        sessions[cid]["res"] = t_name
        sessions[cid]["step"] = 3
        bot.send_message(cid, f"✅ {C_GREEN}استخراج التوقيع تم. الآن ارسل الملف المعدل.")
    elif step == 3:
        sessions[cid]["mod"] = t_name
        bot.send_message(cid, f"🔥 {C_GOLD}اكتملت المصفوفة! اختر النمط:", reply_markup=ai_keyboard())

@bot.callback_query_handler(func=lambda call: call.data.startswith("run_"))
def finalize(call):
    cid = call.message.chat.id
    use_ai = "ai" in call.data
    
    bot.edit_message_text(f"⚡ جاري المعالجة بنمط {'AI Turbo' if use_ai else 'Standard'}...", cid, call.message.message_id)
    
    s = sessions[cid]
    
    # تحليل التوقيع الرقمي
    try:
        with open(s["res"], 'r', errors='ignore') as f: content = f.read()
        sig = re.search(r"<data>(.*?)</data>", content)
        signature = sig.group(1) if sig else "SEC_OMEGA_CORE"
    except:
        signature = "SEC_FALLBACK"

    # تشغيل المحرك
    start_t = time.time()
    final_file = omega_processor(s["orig"], s["mod"], signature, use_ai)
    end_t = time.time()

    out_name = f"OMEGA_AI_{int(end_t)}.3d"
    with open(out_name, 'wb') as f: f.write(final_file)

    with open(out_name, 'rb') as f:
        bot.send_document(cid, f, caption=f"✨ {C_GREEN}تمت المهمة بنجاح!\n\n"
                                         f"⏱️ زمن المعالجة: {round(end_t - start_t, 2)} ثانية\n"
                                         f"🚀 النمط: {'ذكاء اصطناعي' if use_ai else 'قياسي'}")

    # التنظيف الفوري
    for k in ["orig", "res", "mod"]:
        if k in s: os.remove(s[k])
    if os.path.exists(out_name): os.remove(out_name)
    del sessions[cid]
    log_ai("تم تنظيف الجلسة بنجاح 100%")

if __name__ == '__main__':
    log_ai("تم تفعيل محرك Multithreading للسرعة القصوى")
    log_ai("النظام الصاروخي OMEGA-AI متصل بالشبكة...")
    # تشغيل البوت بنظام الـ Polling الطويل لتحسين الاستجابة
    bot.infinity_polling(timeout=60, long_polling_timeout=5)