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
        "*/about* - Muestra detalles de esta aplicación\n"
        "*identificarse como|cómo {código}* - Se identifica el usuario como paciente o como médico\n"
        "*obtener|consultar pacientes* - Retorna lista de pacientes creados\n"
        "*obtener|consultar médicos|doctores* - Retorna lista de médicos creados\n"
        "*obtener|consultar mis pacientes* - Retorna lista de pacientes asociados a un médico \n"
        "*obtener|consultar mis registros* - Retorna lista de registros asociados a un paciente \n"
        "*obtener|consultar registro {id_registro} del paciente {codigo_paciente}* - Utilizado para consultar los registros de un paciente asociado a un doctor \n"
        "*crear|agregar medico|doctor {nombre} {apellido}* - Utilizado para crear médicos\n"
        "*crear|agregar paciente {nombre} {apellido}* - Utilizado para crear pacientes\n"
        "*crear|agregar registro con sistólica {sistolica} diastolica {diastolica} frecuencia {frecuencia} peso {peso} * - Utilizado para crear un registro asociado al paciente identificado\n"
        "*borrar|eliminar medicos|doctores* - Utilizado para eliminar todos los medicos creados\n"
        "*borrar|eliminar pacientes* - Utilizado para eliminar todos los pacientes creados\n"
        "*borrar|eliminar mis registros* - Utilizado para eliminar todos los registros del paciente identificado\n"
        "*borrar|eliminar registro {id_registro}* - Utilizado para eliminar un registro del paciente identificado\n"
        "*agregar|añadir observación|comentario al registro {id_registro} del paciente {código_paciente} : {comentario}* - Utilizado para agregar un comentario al registro de un paciente\n")
    return response

####### START #######


def get_welcome_message(bot_data):
    response = (
        f"Hola, soy *{bot_data.first_name}* ")
    return response

#####################################################################################

##### OBTENER TODOS LOS MÉDICOS #####


def get_all_doctors():
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


###### CREAR REGISTRO MÉDICO ######
def register_record(systolic, diastolic, frecuency, weight, patients_code):
    patients = db.session.query(Patient).all()

    if (len(patients) == 0):
        return "No hay pacientes creados, se debe crear por lo menos 1 paciente para asociarlo al registro."

    # Paciente que va a ser asignado al registro
    patient_record = get_patient_by_code(patients_code)

    if(not patient_record):
        available_patients = ""

        for patient in patients:
            available_patients = (available_patients + str(patient.id) + "- Paciente " + str(patient.name) + " " +
                                  str(patient.lastname) + ", código: " + str(patient.code) + "\n")

        return "El paciente con código " + str(patients_code) + " no existe. Los pacientes disponibles son: \n" + available_patients

    # ID DEL PACIENTE AL CUAL SE VA A ASOCIAR EL REGISTRO
    patients_id = patient_record.id

    # OBTENER TODOS LOS REGISTROS PARA GENERAR ID
    records = db.session.query(Record).all()

    id_record = str(len(records) + 1)

    # GENERAR CATEGORÍA
    category = ""

    if (float(systolic) < 120 and float(diastolic) < 80):
        category = "Óptima"
    elif ((float(systolic) >= 120 and float(systolic) <= 129) and (float(diastolic) >= 80 and float(diastolic) <= 84)):
        category = "Normal"
    elif ((float(systolic) >= 130 and float(systolic) <= 139) and (float(diastolic) >= 85 and float(diastolic) <= 89)):
        category = "Normal alta"
    elif ((float(systolic) >= 140 and float(systolic) <= 159) and (float(diastolic) >= 90 and float(diastolic) <= 99)):
        category = "Hipertensión grado 1"
    elif ((float(systolic) >= 160 and float(systolic) <= 179) and (float(diastolic) >= 100 and float(diastolic) <= 109)):
        category = "Hipertensión grado 2"
    elif (float(systolic) > 180 and float(diastolic) > 110):
        category = "Hipertensión grado 3"
    elif (float(systolic) > 140 and float(diastolic) < 90):
        category = "Hipertensión sistólica aislada"

    record = Record(id_record, systolic, diastolic, frecuency, weight,
                    datetime.now(), category, "Sin observaciones", patients_id)
    db.session.add(record)
    db.session.commit()

    return "Registro #" + str(id_record) + " del paciente " + str(patient_record.name) + " " + str(patient_record.lastname) + " con fecha: " + str(datetime.now()) + " Creado satisfactoriamente"


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
                hasRelation = True
                break

    if(hasRelation):
        return "Uno o más médicos tiene pacientes asociados."

    for doctor in doctors:
        db.session.delete(doctor)
        db.session.commit()

    return "Todos los medicos se han borrado satisfactoriamente"


##### BORRAR TODOS LOS PACIENTES #####
def delete_patients():
    patients = db.session.query(Patient).all()
    records = db.session.query(Record).all()

    hasRelation = False

    if (len(patients) == 0):
        return "No hay pacientes para borrar."

    # Validar si el paciente tiene asociado algún registro
    for record in records:
        for patient in patients:
            if(str(patient.id) == str(record.patients_id)):
                hasRelation = True
                break

    if(hasRelation):
        return "Uno o más pacientes tiene registros asociados."

    for patient in patients:
        db.session.delete(patient)
        db.session.commit()

    return "Todos los pacientes se han borrado satisfactoriamente"


##### BORRAR TODOS LOS REGISTROS DE UN PACIENTE #####
def delete_all_records_by_user(patient_code):
    records = db.session.query(Record).all()
    patient_logged = get_patient_by_code(patient_code)

    if (len(records) == 0):
        return "No hay registros para borrar."

    # VALIDAR SI EL PACIENTE TIENE POR LO MENOS 1 REGISTRO ASOCIADO
    cont = 0

    for record in records:
        if(str(record.patients_id) == str(patient_logged.id)):
            cont += 1

    if(cont == 0):
        return "Usted no tiene ningún registro."

    for record in records:
        db.session.delete(record)
        db.session.commit()

    return "Todos los registros del paciente " + str(patient_logged.name) + " " + str(patient_logged.lastname) + " se han borrado satisfactoriamente"

##### BORRAR 1 REGISTRO DE UN PACIENTE POR ID #####
def delete_record_by_id(record_id, patient_code):
    records = db.session.query(Record).all()
    patient_logged = get_patient_by_code(patient_code)

    if (len(records) == 0):
        return "No hay registros para borrar."

    cont = 0
    existRecord = False
    available_records = ""

    for record in records:
        # VALIDAR SI EL PACIENTE TIENE POR LO MENOS 1 REGISTRO ASOCIADO
        if(str(record.patients_id) == str(patient_logged.id)):
            available_records += str(record.id) + "- Registro #" + str(record.id) + " , con fecha " + str(record.date) + "\n"
            cont += 1

        #VALIDAR QUE EL REGISTRO QUE SE ESTÁ BUSCANDO SI EXISTA
        if(str(record.id) == str(record_id)):
            existRecord = True

    if(cont == 0):
        return "Usted no tiene ningún registro."

    if (not existRecord):
        return "El registro no existe, los registros disponibles son: \n" + available_records

    for record in records:
        if(str(record.id) == str(record_id)):
            db.session.delete(record)
            db.session.commit()

    return "El registro se ha borrado satisfactoriamente"


##### CONSULTAR REGISTROS DE UN PACIENTE POR CÓDIGO #####
def get_record_by_patient_code(doctor_code, patient_code, record_id):
    records = db.session.query(Record).all()
    patients = db.session.query(Patient).all()
    patient_search = get_patient_by_code(patient_code)
    doctor_logged = get_doctor_by_code(doctor_code)

    if (len(patients) == 0):
        return "No hay pacientes creados"

    if (len(records) == 0):
        return "No hay registros creados."
    
    if (not patient_search):
        return "El paciente no existe"

    #VALIDAR SI EL DOCTOR TIENE POR LO MENOS 1 PACIENTE ASOCIADO PARA BUSCAR SU REGISTRO
    hasPatient = False

    for patient in patients:
        if (str(patient.doctors_id) == str(doctor_logged.id)):
            hasPatient = True

    if (not hasPatient):
        return "Usted no tiene ningún paciente asociado"

    cont = 0
    existRecord = False
    available_records = ""

    for record in records:
        # VALIDAR SI EL PACIENTE TIENE POR LO MENOS 1 REGISTRO ASOCIADO
        if(str(record.patients_id) == str(patient_search.id)):
            available_records += str(record.id) + "- Registro #" + str(record.id) + " , con fecha " + str(record.date) + "\n"
            cont += 1

        #VALIDAR QUE EL REGISTRO QUE SE ESTÁ BUSCANDO SI EXISTA
        if(str(record.id) == str(record_id)):
            existRecord = True

        #SI ENCUENTRA EL REGISTRO, ALMACENARLO EN VARIABLE PARA RETORNARLO
        if(str(record.id) == str(record_id)):
            recordSearch = record


    if(cont == 0):
        return "El paciente " + str(patient_search.name) + " " + str(patient_search.lastname) + " no tiene ningún registro asociado."

    if (not existRecord):
        return "El registro no existe, los registros disponibles son: \n" + available_records


    return str(recordSearch.id) + "- Registro #" + str(recordSearch.id) + "\n" + "Sistólica: " + str(recordSearch.systolic) + "\n" + "Diastólica: " + str(recordSearch.diastolic) + "\n" + "Frecuencia: " + str(recordSearch.frecuency) + \
                        "\n" + "Peso: " + str(recordSearch.weight) + "\n" + "Fecha: " + str(recordSearch.date) + "\n" + "Categoría: " + str(
                            recordSearch.category) + "\n" + "Observaciones del doctor: " + str(recordSearch.message) + "\n\n"


##### AGREGAR COMENTARIO AL REGISTRO DE UN PACIENTE #####
def add_comment_to_record(doctor_code, patient_code, record_id, comment):
    records = db.session.query(Record).all()
    patients = db.session.query(Patient).all()
    patient_search = get_patient_by_code(patient_code)
    doctor_logged = get_doctor_by_code(doctor_code)

    if (len(patients) == 0):
        return "No hay pacientes creados"

    if (len(records) == 0):
        return "No hay registros creados."
    
    if (not patient_search):
        return "El paciente no existe"

    #VALIDAR SI EL DOCTOR TIENE POR LO MENOS 1 PACIENTE ASOCIADO PARA BUSCAR SU REGISTRO
    hasPatient = False

    for patient in patients:
        if (str(patient.doctors_id) == str(doctor_logged.id)):
            hasPatient = True

    if (not hasPatient):
        return "Usted no tiene ningún paciente asociado"

    cont = 0
    existRecord = False
    available_records = ""

    for record in records:
        # VALIDAR SI EL PACIENTE TIENE POR LO MENOS 1 REGISTRO ASOCIADO
        if(str(record.patients_id) == str(patient_search.id)):
            available_records += str(record.id) + "- Registro #" + str(record.id) + " , con fecha " + str(record.date) + "\n"
            cont += 1

        #VALIDAR QUE EL REGISTRO QUE SE ESTÁ BUSCANDO SI EXISTA
        if(str(record.id) == str(record_id)):
            existRecord = True

        #SI ENCUENTRA EL REGISTRO, ALMACENARLO EN VARIABLE PARA RETORNARLO
        if(str(record.id) == str(record_id)):
            record.message = str(comment)
            db.session.commit()

    if(cont == 0):
        return "El paciente " + str(patient_search.name) + " " + str(patient_search.lastname) + " no tiene ningún registro asociado."

    if (not existRecord):
        return "El registro no existe, los registros disponibles son: \n" + available_records


    return "La observación se ha guardado exitosamente."

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
                    output += str(patient.id) + "- Paciente " + str(patient.name) + " " + str(
                        patient.lastname) + " con código " + str(patient.code) + "\n"

    return output


##### CONSULTAR REGISTROS ASOCIADOS A UN PACIENTE #####
def get_records_by_patient(patient_code):
    records = db.session.query(Record).all()
    patients = db.session.query(Patient).all()
    patient_logged = get_patient_by_code(patient_code)

    output = ""

    if (not patient_logged):
        return "El paciente con código " + str(patient_code) + " no existe."

    if (len(patients) == 0):
        return "No hay ningún paciente creado."

    if (len(records) == 0):
        return "No hay ningún registro creado."

    # Validar si el paciente tiene asociado algún registro
    for record in records:
        for patient in patients:
            if(str(patient.code) == str(patient_code)):
                if(str(patient.id) == str(record.patients_id)):
                    output += str(record.id) + "- Registro #" + str(record.id) + "\n" + "Sistólica: " + str(record.systolic) + "\n" + "Diastólica: " + str(record.diastolic) + "\n" + "Frecuencia: " + str(record.frecuency) + \
                        "\n" + "Peso: " + str(record.weight) + "\n" + "Fecha: " + str(record.date) + "\n" + "Categoría: " + str(
                            record.category) + "\n" + "Observaciones del doctor: " + str(record.message) + "\n\n"

    return output
