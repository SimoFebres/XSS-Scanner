# XSS Vulnerability Scanner

Esta es una herramienta para detectar vulnerabilidades XSS (Cross-Site Scripting) en sitios web.

## Requisitos

1. **Instalar Firefox** en tu computadora.
2. **Instalar Selenium** y **Geckodriver** para que la herramienta pueda interactuar con el navegador.
3. Podemos forzar la instalacion de **selenium**: 

   sudo pip3 install --break-system-packages selenium

4. Ingresamos en el siguiente repositorio para instalar **Geckodriver**:

   https://github.com/mozilla/geckodriver/releases
   
   tar -xvzf geckodriver-v0.35.0-linux64.tar.gz
   
   sudo mv geckodriver /usr/local/bin
   
   chmod +x /usr/local/bin/geckodriver
   
   which geckodriver
      
### Cómo instalar XSS-Scanner

1. Clona el repositorio:

   git clone https://github.com/SimoFebres/XSS-Scanner.git

2. cd XSS-Scanner

3. Instala las dependencias necesarias:
   pip install selenium
   pip install geckodriver-autoinstaller

4. Ejecuta el script:
   python3 xss_scanner.py
   
 
