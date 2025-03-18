import data_base
import extract_pdf

#crear base de datos
#data_base.create_database()

#guardar archivos en la bd
#extract_pdf.process_reglamento_transito()

print("Hola, ¡¡¡Bienvenido a la primera version de Abogadazo!!!")
opcion = input("Indique el tipo de consulta que desea hacer\n1)Reglamento de Transito\n2)Agentes Facultados\n")

if opcion == '1':
    keyword = input("Ingrese una o varias palabras clave para su consulta.\n")
    data_base.search_by_keyword(keyword)
elif opcion == '2':
    #En construccion
    plateNo=input("Ingrese el número de placa del oficial.\n")
    data_base.agent_by_platenumber(plateNo)
else:
    print("opcion no válida.")

print("+"*50)
print("Gracias por su consulta. Hasta pronto.")