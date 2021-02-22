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
global code_user_logged
code_user_logged = ""


@bot.message_handler(commands=['start'])
def on_command_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,
                     logic.get_welcome_message(bot.get_me()), parse_mode="Markdown")
    bot.send_message(message.chat.id,
                     logic.get_help_message(), parse_mode="Markdown")
####################HELP##############################


@bot.message_handler(commands=['help'])
def on_command_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,
                     logic.get_help_message(), parse_mode="Markdown")
#########################################################


@bot.message_handler(commands=['about'])
def on_command_about(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,
                     logic.get_about_this(config.VERSION), parse_mode="Markdown")


###############################################################
###############################################################
###############################################################

##################IDENTIFICARSE################################
@bot.message_handler(regexp=r"^(identificarse) (c[oó]mo) ([0-9])+$")
def on_command_identificarse(message):
    global code_user_logged

    bot.send_chat_action(message.chat.id, 'typing')

    parts = re.match(r"^(identificarse) (c[oó]mo) ([0-9])+$", message.text)

    # Separar por espacios en blanco para obtener los valores
    parts_split = parts[0].split()

    code = parts_split[2]

    if(str(code)[0] == "2"):
        code_user_logged = code
        patient = logic.get_patient_by_code(code)

        if (not patient):
            bot.reply_to(message, "El paciente con código " +
                         str(code) + " no existe-")
        else:
            bot.reply_to(message, "Bienvenido(a) paciente " +
                         str(patient.name) + " " + str(patient.lastname))

    elif(str(code)[0] == "1"):
        code_user_logged = code
        doctor = logic.get_doctor_by_code(code)
        if (not doctor):
            bot.reply_to(message, "El médico con código " +
                         str(code) + " no existe-")
        else:
            bot.reply_to(message, "Bienvenido(a) Dr(a) " +
                         str(doctor.name) + " " + str(doctor.lastname))
    else:
        bot.reply_to(message, "El usuario no existe.")


##################OBTENER PACIENTES################################
@bot.message_handler(regexp=r"^(obtener|consultar) (pacientes)$")
def on_command_obtener_pacientes(message):
    bot.send_chat_action(message.chat.id, 'typing')
    text = logic.get_all_patients(message.from_user.id)
    bot.reply_to(message, text)

##################OBTENER MEDICOS################################


@bot.message_handler(regexp=r"^(obtener|consultar) (m[eé]dicos?|doctor|doctores)$")
def on_command_obtener_medicos(message):
    bot.send_chat_action(message.chat.id, 'typing')
    text = logic.get_all_doctors(message.from_user.id)
    bot.reply_to(message, text)

##################OBTENER PACIENTES ASOCIADOS A UN MEDICO################################


@bot.message_handler(regexp=r"^(obtener|consultar) (mis) (pacientes?)$")
def on_command_obtener_pacientes_por_medico(message):
    global code_user_logged
    bot.send_chat_action(message.chat.id, 'typing')

    text = ""
    if(not code_user_logged):
        text = "Debe identificarse como médico para consultar pacientes"
        bot.reply_to(
            message, text)
    elif(str(code_user_logged)[0] == "2"):
        text = "Usted debe ser médico para consultar pacientes"
        bot.reply_to(message, text)
    else:
        text = logic.get_patients_by_doctor(code_user_logged)
        bot.reply_to(message, "Sus pacientes son: \n" + text)

##################OBTENER REGISTROS ASOCIADOS A UN PACIENTE (BÚSQUEDA DE PACIENTE################################


@bot.message_handler(regexp=r"^(obtener|consultar) (mis) (registros?)$")
def on_command_obtener_registros_por_paciente(message):
    global code_user_logged
    bot.send_chat_action(message.chat.id, 'typing')

    patient_logged = "Sus registros son: \n"

    if(not code_user_logged):
        bot.reply_to(message, "Debe identificarse para consultar registros")
    elif(str(code_user_logged)[0] == "1"):
        bot.reply_to(message, "Usted no tiene ningún registro")
    else:
        text = logic.get_records_by_patient(code_user_logged)
        bot.reply_to(message, str(patient_logged) + str(text))


##################AGREGAR UN COMENTARIO A UN REGISTRO DE UN PACIENTE################################


@bot.message_handler(regexp=r"^(agregar|añadir) (observaci[oó]n|comentario) ([0-9])+ (del) (paciente) ([0-9])+$")
def on_command_agregar_comentario(message):
    global code_user_logged
    bot.send_chat_action(message.chat.id, 'typing')
    parts = re.match(
        r"^(obtener|consultar) (registro) ([0-9])+ (del) (paciente) ([0-9])+$", message.text)

    # Separar por espacios en blanco para obtener los valores
    parts_split = parts[0].split()

    record_id = parts_split[2]
    patient_code = parts_split[5]

    patient_logged = "Los registros del paciente son: \n"

    if(not code_user_logged):
        bot.reply_to(
            message, "Debe identificarse como médico para consultar los registros de un paciente.")
    elif(str(code_user_logged)[0] == "2"):
        bot.reply_to(
            message, "Usted no puede consultar los registros de un paciente")
    else:
        print("doctor code: "+ str(code_user_logged))
        print("patient code: "+ str(patient_code))
        print("record: "+ str(record_id))
        text = logic.get_record_by_patient_code(
            code_user_logged, patient_code, record_id)
        bot.reply_to(message, str(patient_logged) + str(text))


##################OBTENER REGISTROS ASOCIADOS A UN PACIENTE (BÚSQUEDA DE DOCTOR)################################


@bot.message_handler(regexp=r"^(obtener|consultar) (registro) ([0-9])+ (del) (paciente) ([0-9])+$")
def on_command_obtener_registros_por_paciente_por_codigo(message):
    global code_user_logged
    bot.send_chat_action(message.chat.id, 'typing')
    parts = re.match(
        r"^(obtener|consultar) (registro) ([0-9])+ (del) (paciente) ([0-9])+$", message.text)

    # Separar por espacios en blanco para obtener los valores
    parts_split = parts[0].split()

    record_id = parts_split[2]
    patient_code = parts_split[5]

    patient_logged = "Los registros del paciente son: \n"

    if(not code_user_logged):
        bot.reply_to(
            message, "Debe identificarse como médico para consultar los registros de un paciente.")
    elif(str(code_user_logged)[0] == "2"):
        bot.reply_to(
            message, "Usted no puede consultar los registros de un paciente")
    else:
        print("doctor code: "+ str(code_user_logged))
        print("patient code: "+ str(patient_code))
        print("record: "+ str(record_id))
        text = logic.get_record_by_patient_code(
            code_user_logged, patient_code, record_id)
        bot.reply_to(message, str(patient_logged) + str(text))

##################CREAR MEDICOS################################


@bot.message_handler(regexp=r"^(crear|agregar) (medico|doctor) ([A-Za-z])+ ([A-Za-z])+$")
# @bot.message_handler(commands=["crear_medico"])
def on_command_crear_medico(message):
    parts = re.match(
        r"^(crear|agregar) (medico|doctor) ([A-Za-z])+ ([A-Za-z])+$", message.text)

    # Separar por espacios en blanco para obtener los valores
    parts_split = parts[0].split()

    name = parts_split[2]
    lastname = parts_split[3]

    bot.send_chat_action(message.chat.id, 'typing')
    text = logic.register_doctor(name, lastname)
    bot.reply_to(message, text)

##################CREAR PACIENTE################################


@bot.message_handler(regexp=r"^(crear|agregar) (paciente) ([A-Za-z])+ ([A-Za-z])+ (con) (m[eé]dico|doctora?) ([0-9])+$")
def on_command_crear_paciente(message):
    parts = re.match(
        r"^(crear|agregar) (paciente) ([A-Za-z])+ ([A-Za-z])+ (con) (m[eé]dico|doctora?) ([0-9])+$", message.text)

    # Separar por espacios en blanco para obtener los valores
    parts_split = parts[0].split()

    name = parts_split[2]
    lastname = parts_split[3]
    code = parts_split[6]

    bot.send_chat_action(message.chat.id, 'typing')
    text = logic.register_patient(name, lastname, code)
    bot.reply_to(message, text)

##################CREAR REGISTRO MÉDICO################################


@bot.message_handler(regexp=r"^(crear|agregar) (registro) (con) (sist[oó]lica) ([0-9])+ (diast[oó]lica) ([0-9])+ (frecuencia) ([0-9])+ (peso) ([0-9])+$")
def on_command_crear_registro(message):
    parts = re.match(
        r"^(crear|agregar) (registro) (con) (sist[oó]lica) ([0-9])+ (diast[oó]lica) ([0-9])+ (frecuencia) ([0-9])+ (peso) ([0-9])+$", message.text)

    # Separar por espacios en blanco para obtener los valores
    parts_split = parts[0].split()

    systolic = parts_split[4]
    diastolic = parts_split[6]
    frecuency = parts_split[8]
    weight = parts_split[10]

    global code_user_logged
    bot.send_chat_action(message.chat.id, 'typing')

    if(not code_user_logged):
        bot.reply_to(
            message, "Debe identificarse como paciente para crear registros médicos")
    elif(str(code_user_logged)[0] == "1"):
        bot.reply_to(message, "Usted debe ser paciente para crear registros")
    else:
        text = logic.register_record(float(systolic), float(
            diastolic), float(frecuency), float(weight), code_user_logged)
        bot.reply_to(message, text)

##################ELIMINAR MEDICOS################################


@bot.message_handler(regexp=r"^(eliminar|borrar) (medicos|doctores)$")
def on_command_borrar_medicos(message):
    bot.send_chat_action(message.chat.id, 'typing')
    text = logic.delete_doctors()
    bot.reply_to(message, text)


##################ELIMINAR PACIENTES################################
@bot.message_handler(regexp=r"^(eliminar|borrar) (pacientes)$")
def on_command_borrar_pacientes(message):
    bot.send_chat_action(message.chat.id, 'typing')
    text = logic.delete_patients()
    bot.reply_to(message, text)

##################ELIMINAR TODOS LOS REGISTROS DE UN PACIENTE################################


@bot.message_handler(regexp=r"^(eliminar|borrar) (mis) (registros?)$")
def on_command_borrar_registros_por_paciente(message):
    global code_user_logged
    bot.send_chat_action(message.chat.id, 'typing')

    if(not code_user_logged):
        bot.reply_to(
            message, "Debe identificarse como paciente para eliminar sus registros médicos")
    elif(str(code_user_logged)[0] == "1"):
        bot.reply_to(
            message, "Usted debe ser paciente para eliminar sus registros médicos")
    else:
        text = logic.delete_all_records_by_user(code_user_logged)
        bot.reply_to(message, text)

##################ELIMINAR 1 REGISTRO DE UN PACIENTE POR ID################################


@bot.message_handler(regexp=r"^(eliminar|borrar) (registro) ([0-9])+$")
def on_command_borrar_registro_por_paciente_por_id(message):
    parts = re.match(
        r"^(eliminar|borrar) (registro) ([0-9])+$", message.text)

    # Separar por espacios en blanco para obtener los valores
    parts_split = parts[0].split()

    record_id = parts_split[2]

    global code_user_logged
    bot.send_chat_action(message.chat.id, 'typing')

    if(not code_user_logged):
        bot.reply_to(
            message, "Debe identificarse como paciente para eliminar sus registros médicos")
    elif(str(code_user_logged)[0] == "1"):
        bot.reply_to(
            message, "Usted debe ser paciente para eliminar sus registros médicos")
    else:
        text = logic.delete_record_by_id(record_id, code_user_logged)
        bot.reply_to(message, text)

#########################################################


@bot.message_handler(func=lambda message: True)
def on_fallback(message):
    pass


#########################################################
if __name__ == '__main__':
    bot.polling(timeout=20)
#########################################################
