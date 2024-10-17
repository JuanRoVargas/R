# Importar las bibliotecas necesarias
from selenium import webdriver # Para controlar el navegador web
from selenium.webdriver.chrome.service import Service # Para iniciar el servicio de Chrome
import time  # Para hacer pausas durante la ejecución
import pandas as pd  # Para la manipulación y análisis de datos 

# Especificar la ruta del archivo ejecutable de ChromeDriver
path =  # Escribe aquí la ruta a tu archivo de ChromeDriver

# Crear un objeto 'Service' con la ruta del ChromeDriver
service = Service(executable_path=path)

# Inicializar el navegador Chrome usando el servicio creado anteriormente
driver = webdriver.Chrome(service=service)

# Función para extraer los datos faltantes de los mundiales pasados
def get_misssing_data(year):

    # Construye la URL de la página de Wikipedia para un año específico de la Copa Mundial
    web = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'

    # Utiliza Selenium para abrir la página web
    driver.get(web)


    # Busca todos los elementos de partidos en la página usando XPath
    # Busca partidos que se encuentran alineados a la derecha
    matches = driver.find_elements(by='xpath', value='//td[@align="right"]/.. | //td[@style="text-align:right;"]/..')
    

    # Inicializar las listas que almacenarán la información de los equipos locales, marcadores y equipos visitantes
    home = []
    score = []
    away = []


    # Extraer la información de cada partido y almacenarla en las listas correspondientes
    for match in matches:
        home.append(match.find_element(by='xpath', value='./td[1]').text)# Obtiene el equipo local del partido
        score.append(match.find_element(by='xpath', value='./td[2]').text)# Obtiene el marcador del partido
        away.append(match.find_element(by='xpath', value='./td[3]').text) # Obtiene el equipo visitante del partido

    # Crear un diccionario con la información extraída
    dict_football = {'home': home, 'score': score, 'away': away}

    # Convertir el diccionario en un DataFrame de pandas
    df_football = pd.DataFrame(dict_football)

    # Añadir el año de la Copa Mundial al DataFrame
    df_football['year'] = year

    # Pausa de 2 segundos entre cada solicitud para evitar sobrecargar el servidor
    time.sleep(2)

    # Devolver el DataFrame con la información del año específico
    return df_football



# Lista de años de las Copas Mundiales que se van a extraer
years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974,
         1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014,
         2018]


# Llamar a la función para cada año de la lista, almacenando los resultados en una lista
fifa = [get_misssing_data(year) for year in years]

# Cerrar el navegador una vez terminadas las solicitudes
driver.quit()

# Combinar los DataFrames de todos los años en un solo DataFrame
df_fifa = pd.concat(fifa, ignore_index=True)

# Guardar el DataFrame resultante en un archivo CSV
df_fifa.to_csv("fifa_worldcup_missing_data.csv", index=False)
