import database.db as db
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
    
#####################################################################################

##### OBTENER TODOS LOS MÉDICOS #####
def get_all_doctors(user_id):
    doctors = db.session.query(Doctor).all()

    temp = ""
    for doctor in doctors:
        temp = (temp + str(doctor.id) + "- Dr(a) " + str(doctor.name) + " " +
                str(doctor.lastname) + ", código: " + str(doctor.code) + "\n")

    if (len(doctors) == 0):
        temp = "No se ha creado ningún médico."
        return temp

    # print(temp)
    return temp

##### OBTENER TODOS LOS PACIENTES #####


def get_all_patients(user_id):
    patients = db.session.query(Patient).all()

    temp = ""
    for patient in patients:
        doctor = str(get_doctor_by_id(patient.doctors_id))

        data = doctor.split("/")

        temp = (temp + "- Paciente " + str(patient.name) + " " + str(patient.lastname)
                + ", código: " + str(patient.code) + ". Su médico asignado es " +
                str(data[1]) + " " + str(data[2]) + " con código " + str(data[3]) + "\n")

    if (len(patients) == 0):
        temp = "No se ha creado ningún paciente."
        return temp

    # print(temp)
    return temp


###### CREAR MÉDICO ######
def register_doctor(name, lastname):
    # OBTENER TODOS LOS DOCTORES PARA DETERMINAR LONGITUD Y GENERAR CODE Y ID
    doctors = db.session.query(Doctor).all()

    id_doctor = str(len(doctors) + 1)

    if (len(doctors) < 10):
        code = "100" + str(id_doctor)
    else:
        code = "10" + str(id_doctor)

    doctor = Doctor(id_doctor, name, lastname, code)
    db.session.add(doctor)
    db.session.commit()

    return "Dr(a) " + name + " " + lastname + ", código: " + code + ". Creado satisfactoriamente"


###### CREAR PACIENTE ######
def register_patient(name, lastname, doctor_code):
    doctors = db.session.query(Doctor).all()

    if (len(doctors) == 0):
        return "No hay médicos creados, se debe crear por lo menos 1 médico para asociarlo al paciente."

    # Doctor que va a ser asignado al paciente
    doctor_by_user = get_doctor_by_code(doctor_code)
    if(not doctor_by_user):
        available_doctors = ""

        for doctor in doctors:
            available_doctors = (available_doctors + str(doctor.id) + "- Dr(a) " + str(doctor.name) + " " +
                    str(doctor.lastname) + ", código: " + str(doctor.code) + "\n")

        return "El médico con código " + str(doctor_code) + " no existe. Los médicos disponibles son: \n" + available_doctors

    # OBTENER TODOS LOS PACIENTES PARA DETERMINAR LONGITUD Y GENERAR CODE Y ID
    patients = db.session.query(Patient).all()

    id_patient = str(len(patients) + 1)

    if (len(patients) < 10):
        code = "200" + str(id_patient)
    else:
        code = "20" + str(id_patient)

    patient = Patient(id_patient, name, lastname, code, 1)
    db.session.add(patient)
    db.session.commit()

    return "Paciente " + name + " " + lastname + ", código: " + code + ". Creado satisfactoriamente"


##### BORRAR TODOS LOS MÉDICOS #####
def delete_doctors():
    doctors = db.session.query(Doctor).all()
    patients = db.session.query(Patient).all()

    hasRelation = False

    if (len(doctors) == 0):
        return "No hay médicos para borrar."

    # Validar si el doctor tiene asociado algún paciente
    for doctor in doctors:
        for patient in patients:
            if(str(patient.doctors_id) == str(doctor.id)):
                print("paciente: " + str(patient.doctors_id))
                print("medico: " + str(doctor.id))
                hasRelation = True

    if(hasRelation):
        return "Uno o más médicos tiene pacientes asociados."

    for doctor in doctors:
        db.session.delete(doctor)
        db.session.commit()

    return "Todos los medicos se han borrado satisfactoriamente"


##### BORRAR TODOS LOS PACIENTES #####
def delete_patients():
    patients = db.session.query(Patient).all()

    for patient in patients:
        db.session.delete(patient)
        db.session.commit()

    if (len(patients) == 0):
        return "No hay pacientes para borrar."

    return "Todos los pacientes se han borrado satisfactoriamente"


##### OBTENER DOCTOR POR ID #####
def get_doctor_by_id(doctor_id):
    doctor = db.session.query(Doctor).get(doctor_id)

    print(doctor)

    # print(temp)
    return doctor

##### OBTENER DOCTOR POR CODE #####
def get_doctor_by_code(code):
    doctor = db.session.query(Doctor).filter_by(code=code).first()
    print(doctor)
    return doctor

##### OBTENER PACIENTE POR CODE #####
def get_patient_by_code(code):
    patient = db.session.query(Patient).filter_by(code=code).first()
    print(patient)
    return patient


##### CONSULTAR PACIENTES ASOCIADOS A UN MÉDICO #####
def get_patients_by_doctor(doctor_code):
    doctors = db.session.query(Doctor).all()
    patients = db.session.query(Patient).all()
    doctor_logged = get_doctor_by_code(doctor_code)
    
    output = ""

    if (not doctor_logged):
        return "El médico con código " + str(doctor_code) + " no existe."

    if (len(doctors) == 0):
        return "No hay ningún médico creado."

    if (len(patients) == 0):
        return "No hay ningún paciente creado."

    # Validar si el doctor tiene asociado algún paciente
    for doctor in doctors:
        for patient in patients:
            if(str(doctor.code) == str(doctor_code)):
                if(str(patient.doctors_id) == str(doctor.id)):
                    output += str(patient.id) + "- Paciente " + str(patient.name) + " " + str(patient.lastname) + " con código " + str(patient.code) + "\n"

    return output