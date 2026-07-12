from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def extraer_con_selenium(url):
    print(f"Abriendo navegador para: {url}...")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3) 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3) 
    elementos = driver.find_elements(By.CSS_SELECTOR, "a.group")
    
    links_startups = set()
    for el in elementos:
        href = el.get_attribute('href')
        if href and href.startswith('http'):
            links_startups.add(href)
            
    driver.quit()
    return list(links_startups)

def encontrar_seccion_empleos(url_empresa):
    palabras_clave = ['careers', 'jobs', 'empleos', 'trabaja', 'sumate', 'puestos', 'vacantes', 'oportunidades']
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        respuesta = requests.get(url_empresa, headers=headers, timeout=5)
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        for enlace in soup.find_all('a'):
            texto_link = enlace.get_text().lower()
            href = enlace.get('href', '').lower()
            if any(p in texto_link for p in palabras_clave) or any(p in href for p in palabras_clave):
                return urljoin(url_empresa, enlace.get('href'))
    except Exception:
        pass
    return None

def limpiar_nombre_empresa(url):
    nombre = url.replace("https://", "").replace("http://", "").replace("www.", "")
    return nombre.split('.')[0].capitalize()

# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    url_directorio = "https://rosariostartups.com/"
    startups = extraer_con_selenium(url_directorio)
    
    datos_empresas = []
    
    print(f"\nIniciando análisis de {len(startups)} empresas...")
    
    for startup in startups:
        nombre = limpiar_nombre_empresa(startup)
        link_empleos = encontrar_seccion_empleos(startup)
        
        # Enlace directo a la pestaña de empleos en LinkedIn
        link_linkedin_jobs = f"https://www.linkedin.com/company/{nombre.lower()}/jobs/"
        
        datos_empresas.append({
            "nombre": nombre,
            "web": startup,
            "bolsa_trabajo": link_empleos,
            "linkedin_jobs": link_linkedin_jobs
        })
        
        if link_empleos:
            print(f"✅ {nombre} -> Bolsa encontrada.", flush=True)
        else:
            print(f"❌ {nombre} -> Sin bolsa directa.", flush=True)

    # --- GUARDAR DATOS EN JSON ---
    print("\nGuardando resultados en 'datos.json'...")
    
    with open("datos.json", "w", encoding="utf-8") as f:
        # Usamos indent=4 para que el archivo JSON quede ordenado y legible
        json.dump(datos_empresas, f, ensure_ascii=False, indent=4)
        
    print("Abrir dashboard web para ver los resultados.")
