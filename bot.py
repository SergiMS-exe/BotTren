import telebot, os, requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from datetime import datetime
URLs = {
    'asturias': 'https://horarios.renfe.com/cer/hjcer300.jsp?NUCLEO=20&CP=NO&I=s'
}
STATIONS = {
    'asturias': {'Ablaña': 15205, 'Aviles': 16403, 'Barros': 16006,	'Calzada Asturias': 15401, 'Campomanes': 15120,	'Cancienes': 16302,	'Ciaño': 16010,	'El Caleyo': 15210,	'El Entrego': 16011, 'Ferroñes': 16301,	'Gijón': 15410,	'La Cobertoria': 15121,	'La Corredoria': 15217,	'La Felguera': 16008, 'La Frecha': 15119, 'La Pereda-Riosa': 15206,	'La Rocica': 16402,	'Las Segadas': 15209, 'Llamaquique': 15218,	'Los Campos': 16408, 'Lugo de LLanera': 15300, 'Lugones': 15212, 'Mieres-Puente': 15203, 'Monteana': 15303, 'Nubledo': 16400, 'Olloniego': 15207, 'Oviedo': 15211, 'Peña Rubia': 16005,	'Pola de Lena': 15122, 'Puente L.Fierros': 15118, 'Sama': 16009, 'San Juan de Nieva': 16405, 'Santa Eulalia M.': 16001, 'Santullano': 15202, 'Serin': 15302, 'Soto de Rey': 15208, 'Tudela-Veguin': 16002, 'Ujo': 15200, 'Veriña': 15400, 'Villabona Astur': 15301, 'Villabona-Tabladiello': 15305, 'Villalegre': 16401, 'Villallana': 15123}
}
bot = telebot.TeleBot('937926691:AAEKhjrrZM6gYjODPbRvK_KiikJp1BYqn-o')

regiones = {'asturias'}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Este es el bot de renfe, aqui puedes consultar los trenes como en la pagina '
                                      'oficial')

@bot.message_handler(commands=['selectregion'])
def select_region(message):
    markup=telebot.types.ReplyKeyboardMarkup()
    asturias=telebot.types.KeyboardButton('Asturias')
    markup.add(asturias)
    bot.send_message(message.chat.id, 'Escoge una region', reply_markup=markup)

@bot.message_handler(func= lambda message: message.text.lower() in regiones)
def mostrarRegiones(message):
    '''driver=webdriver.Chrome()
    driver.set_page_load_timeout(10)
    driver.get(URLs[message.text.lower()])
    origen = Select(driver.find_element_by_id('o'))
    origen.select_by_visible_text('Lugones')
    destino = Select(driver.find_element_by_id('d'))
    destino.select_by_visible_text('Oviedo')'''
    key=message.text.lower()
    estaciones=STATIONS[key]
    origin=estaciones['Oviedo']
    destination=estaciones['Lugones']
    date=datetime.now()
    from_time='00'
    to_time='26'
    page_content = requests.post(
        f"{URLs[key]}&cp=NO&o={origin}&d={destination}&df={date}&ho={from_time}&hd={to_time}&TXTInfo=").content
    handle_page(page_content)

def handle_page(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    print(soup.prettify())
    trains = soup.find_all("tr")
    print(trains)



print('El bot esta running')
bot.polling()
