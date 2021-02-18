import database.db as db
from models.Account import Account
from models.Earning import Earning
from models.Spending import Spending
from models.Doctor import Doctor
from models.Patient import Patient
from models.Record import Record
from datetime import datetime
from sqlalchemy import extract


def get_about_this(VERSION):
    response = (
        f"Desarrollo Inicial del Bot: {VERSION}"
        "\n\n"
        "Desarrollado por  \n"
        "Camilo Tabares V <camilo.tabaresv@autonoma.edu.co>")

    return response
##### aca va ayuda #####


def get_help_message():
    response = (
        "Estos son los comandos y órdenes disponibles:\n"
        "\n"
        "*/start* - Inicia la interacción con el bot (obligatorio)\n" "*/help* - Muestra este mensaje de ayuda\n"
        "*/about* - Muestra detalles de esta aplicación\n" "*gane|gané|g {cantidad}* - Registra un saldo positivo\n" "*gaste|gasté|gg {cantidad}* - Registra un saldo negativo\n" "*listar ganancias|lg en {índice_mes} de {año}* - Lista las ganancias de un mes/año\n"
        "*listar gastos|lgg en {mes} de {año}* - Lista los gastos de un mes - año"
        "*obtener saldo|s* - Muestra el saldo actual (disponible)\n"
        "*remover|r ganancia|g|gasto|gg {índice}* - Remueve una ganancia o un gasto según su índice\n"
        "*listar cuentas|lc* - Lista las cuentas registradas (sólo admin)\n")
    return response

####### START #######


def get_welcome_message(bot_data):
    response = (
        f"Hola, soy *{bot_data.first_name}* "
        f"también conocido como el care chiris:*{bot_data.username}*.\n\n" "¡Estoy aquí para ayudarte a ganar la materia!")
    return response


def register_account(user_id):
    account = db.session.query(Account).get(user_id)
    db.session.commit()

    if account == None:
        account = Account(user_id, 0)
        db.session.add(account)
        db.session.commit()
        return True

    return False

# GANAR DINERO


def earn_money(user_id, amount):
    if amount <= 0:
        return False

    control = update_account(user_id, amount)
    if not control:
        return False
    earn = Earning(
        amount, datetime.now(), user_id)
    db.session.add(earn)
    db.session.commit()
    return True


def update_account(user_id, amount):
    account = db.session.query(Account).get(user_id)
    db.session.commit()
    if not account:
        return False
    account.balance = account.balance + amount
    db.session.commit()
    return True

# OBTENER SALDO


def get_balance(user_id):
    account = db.session.query(Account).get(user_id)
    db.session.commit()
    if not account:
        return None

    return account.balance

# GASTAR DINERO


def spend_money(user_id, amount):
    if amount <= 0:
        return False
    control = update_account(user_id, amount * -1)
    if not control:
        return False
    spend = Spending(amount, datetime.now(), user_id)
    db.session.add(spend)
    db.session.commit()
    return True

 # LISTAR INGRESOS


def list_earnings(user_id, month, year):
    earnings = db.session.query(
        Earning
    ).filter_by(
        accounts_id=user_id
    ).filter(
        extract('month', Earning.when) == month
    ).filter(
        extract('year', Earning.when) == year
    ).all()
    db.session.commit()
    return earnings

# LISTAS GASTOS


def list_spendings(user_id, month, year):
    spendings = db.session.query(
        Spending
    ).filter_by(
        accounts_id=user_id
    ).filter(
        extract('month', Spending.when) == month
    ).filter(
        extract('year', Spending.when) == year
    ).all()
    db.session.commit()
    return spendings

# eliminar registro


def remove_earning(user_id, index):
    record = db.session.query(Earning).filter(
        Earning.accounts_id == user_id).filter(
        Earning.id == index).first()
    if not record:
        db.session.rollback()
    return False
    control = update_account(user_id, record.amount * -1)
    if not control:
        db.session.rollback()
        return False
    db.session.delete(record)
    db.session.commit()
    return True


def remove_spending(user_id, index):
    record = db.session.query(Spending).filter(
        Spending.accounts_id == user_id).filter(
        Spending.id == index).first()
    if not record:
        db.session.rollback()
        return False
    control = update_account(user_id, record.amount)
    if not control:
        db.session.rollback()
        return False
        db.session.delete(record)
        db.session.commit()
    return True


#####################################################################################
##### OBTENER TODOS LOS PACIENTES #####
def get_all_patients(user_id):
    patients = db.session.query(Patient).get(user_id)

    if not patients:
        return None

    return patients

##### OBTENER TODOS LOS MÉDICOS #####
def get_all_doctors(user_id):
    doctors = db.session.query(Doctor).all()
    
    temp = ""
    for doctor in doctors:
        temp = (temp + "Dr(a) " + str(doctor.name) + " " + str(doctor.lastname) + ", código: " + str(doctor.code) + "\n")

    if not doctors:
        return None
    
    # print(temp)
    return temp


###### CREAR PACIENTE ######
# def register_patient(user_id):
#     patient = Patient(user_id, 0)
#     db.session.add(account)
#     db.session.commit()
#     return True

###### CREAR MÉDICO ######
def register_doctor(user_id, name, lastname, code):

    doctor = Doctor(790518283, name, lastname, code)
    db.session.add(doctor)
    db.session.commit()

    return "Doctor creado satisfactoriamente"

# def earn_money (user_id, amount):
#     if amount <= 0:
#         return False

#     control = update_account (user_id, amount)
#     if not control:
#         return False
#     earn = Earning(
#                 amount,datetime.now(), user_id)
#     db.session.add(earn)
#     db.session.commit()
#     return True
