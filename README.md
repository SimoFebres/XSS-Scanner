# XSS Vulnerability Scanner

XSS-Scanner es una herramienta que automatiza las pruebas y la carga de payloads en campos vulnerables, específicamente para detectar vulnerabilidades de XSS en aplicaciones web. 
Está hecha en Python, usando Selenium y Firefox como navegador. Tiene la capacidad de escanear campos en páginas web para detectar posibles fallos de seguridad.
La herramienta interactúa con páginas web, identifica los campos vulnerables y carga automáticamente diferentes payloads para detectar posibles vulnerabilidades de manera eficiente.

## Requisitos

1. **Instalar Firefox** en tu ordenador, si utilizas Kali-Linux como distribución, viene por defecto.
2. **Instalar Selenium** y **Geckodriver** para que la herramienta pueda interactuar con el navegador.
3. Podemos forzar la instalacion de **Selenium**: 

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

3. Ejecuta el script:

   python3 xss_scanner.py
   
 **Nota:** Para que la herramienta funcione correctamente, debes tener instalado correctamente **Selenium y Geckodriver.** 

 **Si quieres saber mas acerca de mi herramienta, les envito a revisar mi Gitbook:** https://noon3.gitbook.io/blog/tools/xss-scanner.py
