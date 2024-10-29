import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
from time import time
import random

# random_sleep = round(random.uniform(2, 3), 2)
def scraping_airbnb(url):
    
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-search-engine-choice-screen")
    options.add_argument("--headless")
    options.add_argument('--lang=en')
    options.add_argument('--disable-geolocation')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Esperar que la página cargue y gestionar popup de traducción
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='c1lbtiq8 atm_mk_stnw88 atm_9s_1txwivl atm_fq_1tcgj5g atm_wq_kb7nvz atm_tk_1tcgj5g dir dir-ltr']"))
        ).click()
    except:
        pass
    random_sleep = round(random.uniform(2, 3), 2)
    sleep(random_sleep)
    price = extract_price(driver)
    sleep(random_sleep)
    title = extract_title(driver)
    sleep(random_sleep)
    rating = extract_rating(driver)
    sleep(random_sleep)
    number_reviews = extract_number_reviews(driver)
    sleep(random_sleep)
    guest_favorite = extract_guest_favorite(driver)
    sleep(random_sleep)
    type_host = extract_type_host(driver)
    sleep(random_sleep)
    data_list, hosting_time = extract_data_list(driver)
    sleep(random_sleep)
    id = extraer_id(url)
    sleep(random_sleep)
    all_reviews = extract_reviews(driver, number_reviews)
    
    driver.quit()
    return guest_favorite, rating, number_reviews, type_host, hosting_time, all_reviews, title, data_list, price, id
    
def extract_price(driver):
    # Lista de posibles XPaths para localizar el precio
    xpaths = [
        '//div[@class="l1x1206l atm_7l_jt7fhx atm_r3_1e5hqsa dir dir-ltr"]',
        "//span[contains(text(),'per night')]",
        "//span[contains(text(),'€')]",
        "//div[contains(text(),'€')]",
        '//span[@class="_11jcbg2"]',
        '//div[@class="_1jo4hgw"]',
        '//span[@class="_1qgfaxb1"]',
        '//div[@class="_ati8ih"]',
        '//span[@class="a8jt5op atm_3f_idpfg4 atm_7h_hxbz6r atm_7i_ysn8ba atm_e2_t94yts atm_ks_zryt35 atm_l8_idpfg4 atm_vv_1q9ccgz atm_vy_t94yts aze35hn atm_mk_stnw88 atm_tk_idpfg4 dir dir-ltr"]',
        '//span[@class="a8jt5op atm_3f_idpfg4 atm_7h_hxbz6r atm_7i_ysn8ba atm_e2_t94yts atm_ks_zryt35 atm_l8_idpfg4 atm_vv_1q9ccgz atm_vy_t94yts a1ugchtf atm_mk_stnw88 atm_tk_idpfg4 dir dir-ltr"]'
    ]
    
    # Intentar encontrar el precio usando cada XPath
    for xpath in xpaths:
        try:
            random_sleep = round(random.uniform(2, 3), 2)
            sleep(random_sleep)
            price = driver.find_element(By.XPATH, xpath).text
            # Verificar si el precio es válido (no vacío y no demasiado corto)
            if price and len(price) > 2:
                return price
        except:
            continue
    
    # Si ninguno de los XPaths devuelve un precio válido, retornar NaN
    return np.nan

def extract_title(driver):
    try:
        return driver.find_element(By.XPATH, "//div[@class = '_1czgyoo']").text
    except:
        return np.nan
    
def extract_number_reviews(driver):
    try:
        number_reviews = driver.find_element(By.XPATH, '//div[@class="r16onr0j atm_c8_vvn7el atm_g3_k2d186 atm_fr_1vi102y atm_gq_myb0kj atm_vv_qvpr2i atm_c8_sz6sci__14195v1 atm_g3_17zsb9a__14195v1 atm_fr_kzfbxz__14195v1 atm_gq_idpfg4__14195v1 dir dir-ltr"]').text
        return number_reviews
    except:
        try:
            sleep(2)
            number_reviews = driver.find_element(By.XPATH, '//button[@data-testid="pdp-show-all-reviews-button"]').text
            number_reviews = number_reviews.split(" ")[2]
            return number_reviews
        except:
            try:
                sleep(2)
                number_reviews = driver.find_element(By.XPATH, '//span[@class="ttu4mdj atm_9s_116y0ak dir dir-ltr"]').text
                return number_reviews
            except:
                number_reviews = np.nan
                pass
    try:
        float(number_reviews)
    except:
        pass
    if not isinstance(number_reviews, (int, float, complex)):
        try:
            number_reviews = driver.find_element(By.XPATH, '//span[@class="ttu4mdj atm_9s_116y0ak dir dir-ltr"]').text
            return number_reviews
        except:
            number_reviews = np.nan
    return number_reviews

def extract_guest_favorite(driver):
    guest_favorite = False
    guest = "no"
    try:
        guest = driver.find_element(By.XPATH, '//div[@class="lbjrbi0 atm_le_1y44olf atm_lk_1y44olf atm_ll_1y44olf dir dir-ltr"]').text
    except:
        pass
    if guest != "no":
        guest_favorite = True
    return guest_favorite

def extract_rating(driver):
    try:
        rating = driver.find_element(By.XPATH, '//div[@class="r1lutz1s atm_c8_o7aogt atm_c8_l52nlx__oggzyc dir dir-ltr"]').text
    except:
        try:
            random_sleep = round(random.uniform(2, 3), 2)
            sleep(random_sleep)
            rating = driver.find_element(By.XPATH, '//div[@class="a8jhwcl atm_c8_vvn7el atm_g3_k2d186 atm_fr_1vi102y atm_9s_1txwivl atm_ar_1bp4okc atm_h_1h6ojuz atm_cx_t94yts atm_le_14y27yu atm_c8_sz6sci__14195v1 atm_g3_17zsb9a__14195v1 atm_fr_kzfbxz__14195v1 atm_cx_1l7b3ar__14195v1 atm_le_1l7b3ar__14195v1 dir dir-ltr"]').text
        except:
            rating = np.nan
    return rating

def extract_type_host(driver):
    try:
        type_host = driver.find_element(By.XPATH, '//li[@class="l7n4lsf atm_9s_1o8liyq_keqd55 dir dir-ltr"]').text
    except:
        type_host = np.nan
    return type_host

def extract_data_list(driver):
    try:
        complete_data_list_primer = driver.find_elements(By.XPATH, '//div[@class="o1kjrihn atm_c8_km0zk7 atm_g3_18khvle atm_fr_1m9t47k atm_h3_1y44olf atm_c8_2x1prs__oggzyc atm_g3_1jbyh58__oggzyc atm_fr_11a07z3__oggzyc dir dir-ltr"]')
        complete_data_list = [x.text for x in complete_data_list_primer]
        hosting_time = driver.find_element(By.XPATH, '//div[@class="s1l7gi0l atm_c8_km0zk7 atm_g3_18khvle atm_fr_1m9t47k atm_7l_1esdqks dir dir-ltr"]').text
    except:
        complete_data_list = np.nan
        hosting_time = "New host"
    return complete_data_list, hosting_time

def extract_reviews(driver, number_reviews):
    try:
        show_more_reviews(driver, number_reviews)
        all_reviews = scroll_reviews(driver)
    except:
        try:
            all_reviews = driver.find_elements(By.XPATH, '//div[@class="r1bctolv atm_c8_1sjzizj atm_g3_1dgusqm atm_26_lfmit2_13uojos atm_5j_1y44olf_13uojos atm_l8_1s2714j_13uojos dir dir-ltr"]')
            all_reviews = [x.text for x in all_reviews]
        except:
            all_reviews = np.nan
    return all_reviews

def show_more_reviews(driver, number_reviews):
    try:
        more_reviews_button_xpath = f"//button[contains(text(), 'Show all {number_reviews} reviews')]"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, more_reviews_button_xpath))
        ).click()
        sleep(2)
    except (TimeoutException, NoSuchElementException):
        pass

def scroll_reviews(driver):
    random_sleep = round(random.uniform(2, 3), 2)
    all_reviews = []

    try:
        review_popup = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_17itzz4")))
        last_height = driver.execute_script("return arguments[0].scrollHeight", review_popup)
    except:
        return all_reviews

    while len(list(set(all_reviews))) < 100:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", review_popup)
        sleep(random_sleep)
        reviews_list = driver.find_elements(By.XPATH, "//div[@class='r1bctolv atm_c8_1sjzizj atm_g3_1dgusqm atm_26_lfmit2_13uojos atm_5j_1y44olf_13uojos atm_l8_1s2714j_13uojos dir dir-ltr']")
        all_reviews.extend([review.text for review in reviews_list if len(review.text) > 3])
        sleep(random_sleep)
        new_height = driver.execute_script("return arguments[0].scrollHeight", review_popup)
        if new_height == last_height:
            break
        last_height = new_height
    return list(set(all_reviews))

def extraer_city(url):
    try:
        city_full = url.split('www.airbnb.com/s/')[1].split('/homes')[0]
        # Si contiene '--', divide y toma el primer elemento
        city = city_full.split('--')[0]
        return city
    except:
        return None
def extraer_id(url):
    try:
        # Divide la URL por '/rooms/' y toma la parte después
        return url.split('/rooms/')[1].split('?')[0]
    except IndexError:
        return None 
    
def scraping_urls(city_url):
    # WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-search-engine-choice-screen")
    options.add_argument("--headless")
    options.add_argument('--lang=en')
    options.add_argument('--disable-geolocation')
    driver = webdriver.Chrome(options=options)

    driver.get(city_url)

    all_urls: list = []

    # Scraping para la pagina en la que está
    def scrape_urls():
        wait = WebDriverWait(driver, 15)  # Espera hasta 15 segundos
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/rooms/")]')))
        # sleep(8) # espera a que carge
        listings = driver.find_elements(By.XPATH, '//a[contains(@href, "/rooms/")]')
        urls = [listing.get_attribute('href') for listing in listings]
        sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.7);")  # Baja al 90% de la página
        sleep(2)
        wait2 = WebDriverWait(driver, 10)
        element2 = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="_11jcbg2"]')))
        return urls

    # Loop para todas las paginas
    while True:
        page_urls = scrape_urls() # Esto funciona porque cada vez que vamos a una pagina nueva la url principal no cambia
        all_urls.extend(page_urls)        
        try:
            sleep(2)
            next_button = driver.find_element(By.XPATH, '//a[@aria-label="Next"]')
            driver.execute_script("arguments[0].click();", next_button)  # Forzar clic en el botón "Next" usando JavaScript
            sleep(2)  # Espera a que el desplazamiento se complete
        except NoSuchElementException:
            break
    driver.quit()
    all_urls = list(set(all_urls))
    all_urls_dicc = {}
    for url in all_urls:
        all_urls_dicc[url] = extraer_city(city_url)
    return all_urls_dicc


def get_type_host(hosting_time):
    if isinstance(hosting_time, str) and '·' in hosting_time:
        return hosting_time.split('·')[0].strip()  # Extrae la primera parte antes del "·"
    else:
        return "normal_host"  # Si no hay "·" o no es string, lo marca como "normal host"

# Función para limpiar la columna "hosting_time"
def clean_hosting_time(hosting_time):
    if isinstance(hosting_time, str) and '·' in hosting_time:
        return hosting_time.split('·')[1].strip()  # Toma la parte después del "·"
    else:
        return hosting_time  # Si no hay "·" o no es string, no cambia el valor


urls_cities = [#"https://www.airbnb.com/s/San-Francisco--California--United-States/homes",
               #"https://www.airbnb.com/s/las-vegas/homes",
               "https://www.airbnb.com/s/Chicago--Illinois--United-States/homes",
            #    "https://www.airbnb.com/s/Charlotte--North-Carolina--United-States/homes",
            #    "https://www.airbnb.com/s/Austin--Texas--United-States/homes",
            #    "https://www.airbnb.com/s/Seattle--Washington--United-States/homes",
               "https://www.airbnb.com/s/Miami--Florida--United-States/homes"
               ]

df_full =  pd.read_csv("Airbnb.csv")
#df_full = pd.read_csv('all_url.csv')
all_ids = df_full["id_url"]

urls_dicc = {}
for url_city in urls_cities:
    urls = scraping_urls(url_city)
    # print(extraer_city(url_city))
    urls_dicc.update(urls)
new_urls_dicc = {}
for url, city in urls_dicc.items():
    id = extraer_id(url)
    # print(id)
    if id not in all_ids:
        new_urls_dicc[url] = city
print(len(new_urls_dicc))


df = pd.DataFrame(columns=['title', 'city', 'guest_favorite', 'rating', 'number_reviews', 'type_host', 'hosting_time', 'price', 'all_reviews', 'complete_data_list', 'url', 'id_url'])

n = 0
for url, city in urls_dicc.items():
    n = n + 1
    guest_favorite, rating, number_reviews, type_host, hosting_time, all_reviews, title, complete_data_list, price, id = scraping_airbnb(url) # price,
    
    # print(f"{n} {price} {url}")
    new_row = pd.DataFrame({
                'title' : [title],
                'city' : [city],
                'guest_favorite': [guest_favorite],
                'rating': [rating],
                'number_reviews': [number_reviews],
                'type_host': [type_host],
                'hosting_time': [hosting_time],
                'price': [price],
                'all_reviews': [all_reviews],
                'complete_data_list' : [complete_data_list],
                'url' : [url],
                'id_url' : [id]
            })
    df = pd.concat([df, new_row], ignore_index=True)
    # if n > 2:
        
        # break
df['type_host'] = df['hosting_time'].apply(get_type_host)
df['hosting_time'] = df['hosting_time'].apply(clean_hosting_time)
df.to_csv("SFyLV.csv")
