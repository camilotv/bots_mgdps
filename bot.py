from telebot import TeleBot
from config import bot
from time import sleep
import re
import database.db as db
import logic
import config


if __name__ == '__main__': 
    db.Base.metadata.create_all(db.engine)
####################START###########################

@bot.message_handler(commands=['start']) 
def on_command_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message( message.chat.id,
    logic.get_welcome_message(bot.get_me()), parse_mode="Markdown")
    bot.send_message( message.chat.id,
    logic.get_help_message(), parse_mode="Markdown")
    logic.register_account(message.from_user.id)
####################HELP##############################
@bot.message_handler(commands=['help']) 
def on_command_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message( message.chat.id,
    logic.get_help_message(), parse_mode="Markdown")
#########################################################
@bot.message_handler(commands=['about']) 
def on_command_about(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message( message.chat.id,
    logic.get_about_this(config.VERSION),parse_mode="Markdown")
    
####################GANAR DINERO##########################
@bot.message_handler(regexp=r"^(gane|gané|g) ([+-]?([0-9]*[.])?[0-9]+)$") 
def on_earn_money(message):
    bot.send_chat_action(message.chat.id, 'typing')
    parts = re.match(
    r"^(gane|gané|g) ([+-]?([0-9]*[.])?[0-9]+)$", message.text)
# print (parts.groups())
    amount = float(parts[2])
    control = logic.earn_money (message.from_user.id, amount)
    bot.reply_to( message,
            f"\U0001F4B0 ¡Dinero ganado!: {amount}" if control == True
            else "\U0001F4A9 Tuve problemas registrando la transacción, ejecuta /start y vuelve a intentarlo")

################GASTAR DINERO#############################
@bot.message_handler(regexp=r"^(gaste|gasté|gg) ([+-]?([0-9]*[.])?[0-9]+)$") 
def on_spend_money(message):
    bot.send_chat_action(message.chat.id, 'typing')
    parts = re.match(r"^(gaste|gasté|gg) ([+-]?([0-9]*[.])?[0-9]+)$", message.text)
    amount = float(parts[2])
    control = logic.spend_money (message.from_user.id, amount)
    bot.reply_to( message,
            f"\U0001F4B8 ¡Dinero gastado!: {amount}" if control == True
            else "\U0001F4A9 Tuve problemas registrando la transacción, ejecuta/start y vuelve a intentarlo")
###################LISTAR LAS GANANCIAS############################
@bot.message_handler(regexp=r"^(listar ganancias|lg) en ([0-9]{1,2}) de ([0-9]{4})$")
def on_list_earnings(message):
    bot.send_chat_action(message.chat.id, 'typing')
    parts = re.match(r"^(listar ganancias|lg) en ([0-9]{1,2}) de ([0-9]{4})$", message.text)
    month = int(parts[2])
    year = int(parts[3])
    if month < 1 or month > 12:
        bot.reply_to(message, f"Error, mes inválido: {month}") 
        return
    if year < 1990 or year > 2050:
        bot.reply_to(message, f"Error, año inválido: {year}") 
        return
    earnings = logic.list_earnings (message.from_user.id, month, year) 
    text = ""
    total = 0
    if not earnings:
        text = f"\U0001F633 No tienes ganancias registradas en {month}/{year}"
    else:
        text = "Listado de ganancias:\n"
        text +="- - - - - - - - - - - - - - - - - \n"
        text +="x Nro     |     VALOR  |    FECHA     x\n"
    
    for e in earnings: 
        total += e.amount
        text += f"| {e.id} | ${e.amount} | ({e.when.strftime('%d/%m/%Y -%H:%M')})|\n"
    text += f"\nTOTAL = ${total}"    
        
    bot.reply_to(message, text, parse_mode="Markdown")

##################LISTAR GASTOS###########################
@bot.message_handler(regexp=r"^(listar gastos|lgg) en ([0-9]{1,2}) de ([0-9]{4})$") 
def on_list_spendings(message):
    parts = re.match(r"^(listar gastos|lgg) en ([0-9]{1,2}) de ([0-9]{4})$", message.text)
    month = int(parts[2])
    year = int(parts[3])
    if month < 1 or month > 12:
        bot.reply_to(message, f"Error, mes inválido: {month}") 
        return
    if year < 1990 or year > 2050:
        bot.reply_to(message, f"Error, año inválido: {year}") 
        return
    spendings = logic.list_spendings (message.from_user.id, month, year) 
    text = ""
    total = 0
    if not spendings:
        text = f"\U0001F633 No tienes gastos registradas en {month}/{year}"
    else:
        text = "Listado de gastos:\n"
        text +="- - - - - - - - - - - - - - - - - \n"
        text +="x Nro     |     VALOR  |    FECHA     x\n"
    
    for s in spendings: 
        total += s.amount
        text += f"| {s.id} | ${s.amount} | ({s.when.strftime('%d/%m/%Y -%H:%M')})|\n"
    text += f"\nTOTAL = ${total}"    
        
    bot.reply_to(message, text, parse_mode="Markdown")





##################OBTENER SALDO################################
@bot.message_handler(regexp=r"^(obtener saldo|s)$") 
def on_get_balance(message):
    bot.send_chat_action(message.chat.id, 'typing')
    balance = logic.get_balance (message.from_user.id)
    text = "\U0000274C Aún no tienes una cuenta asociada, ejecuta /start para arreglarlo."
    if balance != None:
            text = f"Tu saldo actual es ${balance}"
    bot.reply_to(message, text)
####################ELIMINAR ########################
@bot.message_handler(regexp=r"^(remover|r) (ganancia|g|gasto|gg) ([0-9]+)$") 
def on_remove_record(message):
    bot.send_chat_action(message.chat.id, 'typing')
    parts = re.match(r"^(remover|r) (ganancia|g|gasto|gg) ([0-9]+)$", message.text)
    record_type = parts[2] 
    index = int(parts[3])
    if record_type not in ["ganancia", "g", "gasto", "gg"]: 
        bot.reply_to(message, f"Error, tipo de registro inválido:{record_type}")
        return
    if index < 0:
        bot.reply_to(message, f"Error, índice inválido: {index}") 
        return
    response = False
    if record_type == "ganancia" or record_type == "g":
        response = logic.remove_earning (message.from_user.id, index)
    elif record_type == "gasto" or record_type == "gg":
        response = logic.remove_spending (message.from_user.id, index)
    if response:
        bot.reply_to(message, f"Registro removido: {record_type}, {index}")
    else:
        bot.reply_to(message, f"No se pudo remover el registro: {index}")


###############################################################
###############################################################
###############################################################

##################OBTENER PACIENTES################################
@bot.message_handler(commands=["obtener_pacientes"]) 
def on_command_obtener_pacientes(message):
    bot.send_chat_action(message.chat.id, 'typing')
    text = logic.get_all_patients(message.from_user.id)
    bot.reply_to(message, text)

##################OBTENER MEDICOS################################
@bot.message_handler(commands=["obtener_medicos"]) 
def on_command_obtener_medicos(message):
    bot.send_chat_action(message.chat.id, 'typing')
    text = logic.get_all_doctors(message.from_user.id)
    bot.reply_to(message, text)


##################CREAR MEDICOS################################
@bot.message_handler(commands=["crear_medico"]) 
def on_command_crear_medico(message):
    bot.send_chat_action(message.chat.id, 'typing')
    text = logic.register_doctor(5,"asd","dsa", "100")
    print("text: " + str(text))
    print("message: " + (str(message)))
    bot.reply_to(message, text)
        
#########################################################
@bot.message_handler(func=lambda message: True) 
def on_fallback(message):
    pass
#########################################################
if __name__ == '__main__': bot.polling(timeout=20)
#########################################################
