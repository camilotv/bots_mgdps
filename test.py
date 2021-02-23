import unittest
import logic

class Pruebas(unittest.TestCase):
    def testGetDoctors(self):
        text = logic.get_all_doctors()
        print(text)
        self.assertTrue(text != "")

    # def testLogin(self):
    #     patient = logic.get_patient_by_code("1001")

    #     if (not patient):
    #         patient = "El paciente no existe"

    #     print(patient)
    #     self.assertTrue(patient)

if __name__ == "__main__":
    unittest.main()