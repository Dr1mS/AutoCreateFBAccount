from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import sys
import os

import pandas as pd
import random

# lire les prénoms et les noms de famille
prenoms = pd.read_csv('prenom.csv', header=None)
noms = pd.read_csv('nom.txt', sep='\t', header=None)

# convertir les DataFrame en listes
prenoms_liste = prenoms[0].tolist()
noms_liste = noms[0].tolist()

# sélectionner un prénom et un nom aléatoirement
prenom_aleatoire = random.choice(prenoms_liste)
nom_aleatoire = random.choice(noms_liste)



# mettre en minuscule le prénom et le nom sauf la premiere lettre
prenom_aleatoire = prenom_aleatoire.lower().capitalize()
nom_aleatoire = nom_aleatoire.lower().capitalize()

print(prenom_aleatoire)
print(nom_aleatoire)

# spécifier l'emplacement de geckodriver
geckodriver_path = './geckodriver.exe'

# créer une instance d'Options
firefox_options = Options()

# ajouter une option pour démarrer en mode de navigation privée et headless

# uncomment the line below to run the script in headless mode
#firefox_options.add_argument("--headless")
firefox_options.add_argument("-private")

# instancier le driver du navigateur avec les options
driver = webdriver.Firefox(service=Service(geckodriver_path), options=firefox_options)

#driver.get("http://www.whatsmyip.org/")
#time.sleep(200)


# visiter un site web
print("Visiting temp-mail.io\n\n")
driver.get("https://temp-mail.io/fr")

# pause 5 secondes pour laisser le temps au site de charger
time.sleep(5)

# find class="email__input" et copy text
email = driver.find_element(By.CSS_SELECTOR, ".email__input").get_attribute("value")

# afficher l'email
print("L'email temporaire est : ")
print(email)

# ouvrir un nouvel onglet
driver.execute_script("window.open('');")

# changer pour le nouveau onglet (ici index 1 car les onglets sont indexés à partir de 0)
driver.switch_to.window(driver.window_handles[1])

# aller sur le site de facebook
print("\n\nVisiting facebook.com\n\n")
driver.get("https://www.facebook.com/")
time.sleep(2)

# cliquer sur accepter les cookies
print("Accepting cookies\n\n")
element = driver.find_element(By.XPATH, '//button[@title="Autoriser tous les cookies"]')
driver.execute_script("arguments[0].click();", element)

time.sleep(2)

# cliquer sur créer un compte
print("click on create account\n\n")
element = driver.find_element(By.LINK_TEXT, "Créer nouveau compte")
driver.execute_script("arguments[0].click();", element)


time.sleep(2)

# remplir le formulaire name="firstname"
print("filling form\n\n")
element = driver.find_element(By.NAME, "firstname")
element.send_keys(prenom_aleatoire)

# remplir le formulaire name="lastname"
element = driver.find_element(By.NAME, "lastname")
element.send_keys(nom_aleatoire)

# remplir le formulaire name="reg_email__"
element = driver.find_element(By.NAME, "reg_email__")
element.send_keys(email)

time.sleep(.5)

# remplir le formulaire name="reg_email_confirmation__"
element = driver.find_element(By.NAME, "reg_email_confirmation__")
element.send_keys(email)

# remplir le formulaire name=="reg_passwd__"
element = driver.find_element(By.NAME, "reg_passwd__")
# Set password
password = "SETYOURPASSWORDHERE"
element.send_keys(password)

# remplir le formulaire name="birthday_day"
select_day = Select(driver.find_element(By.NAME, "birthday_day"))
#select by value between random 1 and 30
select_day.select_by_value(str(random.randint(1, 30)))

# remplir le formulaire name="birthday_month"
select_month = Select(driver.find_element(By.NAME, "birthday_month"))
#select by visible text random month jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec
select_month.select_by_visible_text(random.choice(["jan", "fév", "mar", "avr", "mai", "jun", "juil", "août", "sep", "oct", "nov", "déc"]))

# remplir le formulaire name="birthday_year"
select_year = Select(driver.find_element(By.NAME, "birthday_year"))
#select by value between random 1970 and 2003
select_year.select_by_value(str(random.randint(1970, 2003)))

# sélectionner le genre span._5k_2:nth-child(1) > label:nth-child(1)
element = driver.find_element(By.CSS_SELECTOR, "span._5k_2:nth-child(1) > label:nth-child(1)")
driver.execute_script("arguments[0].click();", element)

# cliquer sur le bouton s'inscrire name="websubmit"
element = driver.find_element(By.NAME, "websubmit")
driver.execute_script("arguments[0].click();", element)

#si //*[@id="reg_error_inner"] est detecté, on recommence 50 fois en attendant 2 secondes
count = 0
while True:
    try:
        # on cherche l'erreur avec le xpath pendant 2 secondes
        element = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="reg_error_inner"]'))
        )
        # si l'élément est trouvé, cliquer a nouveau, nombre de tentative max a 30
        element = driver.find_element(By.NAME, "websubmit")
        driver.execute_script("arguments[0].click();", element)
        print(f"Tentative infructueuse, on recommence : {count+1}/30\n\n")
        time.sleep(2)
        count += 1
        # si on arrive a 25 tentative, on affiche un message
        if count == 25:
            print('ON POUSSE MADAME ALLER, HOP HOP HOP\n\n')
        # si on arrive a 30 tentative, on affiche un message et on arrete le programme	
        if count == 30:
            print("Trop de tentative infructueuse, on annule\n\n")
            #stop the program
            driver.quit()
            break            
    except:
        # si l'élément n'est pas trouvé, la boucle s'arrete et on continue
        print("Tentative fructueuse ! On continu...\n\n")
        pass
        break

# if this selector css found then stop the program ".x14z4hjw"
try:
    # on cherche l'erreur avec le xpath pendant 2 secondes
    element = WebDriverWait(driver, 12).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.x14z4hjw'))
    )
    # si l'élément est trouvé, on affiche un message et on arrete le programme
    print("Compte bloqué pendant 180 jours\n\n")
    #stop the program
    driver.quit()
except:
    # si l'élément n'est pas trouvé, on continue
    print("Compte non bloqué, on continu...\n\n")
    pass
# pause 10 secondes pour laisser le temps au site de charger


# retourner sur le premier onglet
print("switching to temp-mail.io\n\n")
driver.switch_to.window(driver.window_handles[0])

# attendre de detecter le mail de facebook class="email-list"
count = 0
while True:
    try:
        # attendre 10 secondes et chercher l'élément
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//li[contains(@class, "message") and contains(@class, "list-complete-item")]'))
        )
        # si l'élément est trouvé, sortir de la boucle
        driver.execute_script("arguments[0].click();", element)
        print("Email found\n\n")
        break
    except:
        # si l'élément n'est pas trouvé, la boucle continue indéfiniment
        print("Waiting for email...\n\n")
        count += 1
        if count == 5:
            print("Email not found, exiting...\n\n")
            #stop the program
            driver.quit()
            os._exit()
            
        pass

wait = WebDriverWait(driver, 10)
# récuperer le code de confirmation
element = wait.until(EC.presence_of_element_located((By.XPATH, '//td[contains(text(), "FB-")]')))
confirmation_code = element.text.split('-')[-1] # pour ne garder que le code après FB-
print(f"Confirmation code is : {confirmation_code}")

# attendre 15 secondes le temps de verifier que tout est ok
time.sleep(5)

# retourner sur le deuxième onglet
print("\n\nswitching to facebook.com\n\n")
driver.switch_to.window(driver.window_handles[1])

# remplir le formulaire name="code"
element = driver.find_element(By.NAME, "code")
element.send_keys(confirmation_code)

# cliquer sur le bouton continuer name="confirm"
element = driver.find_element(By.NAME, "confirm")
driver.execute_script("arguments[0].click();", element)

# pause 10 secondes pour laisser le temps au site de charger
time.sleep(10)



# cliquer sur ok
try:
    # Essayer de trouver le bouton avec le premier XPath
    print("click on ok\n\n")
    element = driver.find_element(By.XPATH, '//a[contains(text(), "OK")]')
    driver.execute_script("arguments[0].click();", element)
except Exception:
    try:
        # Si le premier échoue, essayer avec le second XPath
        print("Not find, click on ok\n\n")
        element = driver.find_element(By.XPATH, '//a[@class="_42ft _42fu layerCancel uiOverlayButton selected _42g- _42gy"]')
        driver.execute_script("arguments[0].click();", element)
    except Exception:
        try:
            # Si le second échoue, essayer avec le troisième XPath
            print("Not find, click on ok\n\n")
            element = driver.find_element(By.XPATH, '//a[@role="button"]')
            driver.execute_script("arguments[0].click();", element)
        except Exception:
            try:
                # Si le troisième échoue, essayer avec le quatrième XPath
                print("Not find, click on ok\n\n")
                element = driver.find_element(By.XPATH, '//a[@href="#"]')
                driver.execute_script("arguments[0].click();", element)
            except Exception:
                try:
                    # Si le quatrième échoue, essayer avec le cinquième XPath
                    print("Not find, click on ok\n\n")
                    element = driver.find_element(By.XPATH, '//a[@role="button" and contains(@class, "layerCancel")]')
                    driver.execute_script("arguments[0].click();", element)
                except Exception:
                    print("Impossible de trouver le bouton OK avec les XPaths fournis.")

# pause 10 secondes pour laisser le temps au site de charger
time.sleep(3)

#cliquer sur autoriser les cookies
element = driver.find_element(By.XPATH, '//div[@aria-label="Autoriser tous les cookies"]')
driver.execute_script("arguments[0].click();", element)

# pause 10 secondes pour laisser le temps au site de charger
time.sleep(10)


# Trouver l'élément avec le texte "{prenom} {nom}"
print("click on my profil\n\n")
element = driver.find_element(By.XPATH, f'//*[contains(text(), "{prenom_aleatoire} {nom_aleatoire}")]')
driver.execute_script("arguments[0].click();", element)
#A tester

# pause 10 secondes pour laisser le temps au site de charger
time.sleep(10)

# copy url
url = driver.current_url
print("Url is : ")
print(url)

# enregistrer le mail, le nom et prénom dans un fichier txt
f = open("compte.txt", "a")
#afficher date et heure
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
f.write(f"\n\n\nDate : {dt_string}\n")
f.write(f"Email : {email}\n")
f.write(f"Nom : {nom_aleatoire}\n")
f.write(f"Prénom : {prenom_aleatoire}\n")
f.write(f"Url : {url}\n")
f.close()

print("Compte enregistré dans le fichier compte.txt\n\n")
print(f"Creation de {nom_aleatoire} {prenom_aleatoire} terminée\n\n")

# fermer le navigateur
driver.quit()
