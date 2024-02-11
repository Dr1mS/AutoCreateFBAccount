import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def get_firefox():
    geckodriver = os.path.join(os.getcwd(), "geckodriver")
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    print("Initialisation du driver Firefox...")
    return webdriver.Firefox(service=Service(geckodriver), options=firefox_options)

def check_url(driver, url):
    print(f"Vérification de l'URL : {url}")
    driver.get(url)
    try:
        WebDriverWait(driver, 1).until(EC.url_changes(url))
        print(f"L'URL a changé pour : {driver.current_url}")
        return True
    except Exception as e:
        print(f"L'URL n'a pas changé. ca doit être un compte invalide. Ca va être supprimé. {url}")
        return False

def main():
    driver = get_firefox()
    valide = 0
    invalide = 0
    with open("compte.txt", "r") as f, open("compteOK.txt", "a") as out:
        block = []
        for line in f:
            if line.strip() == "":
                if block:  # ajoutez cette ligne
                    url_line = block[-1]
                    url = url_line.split(" : ")[-1].strip()
                    print(f"Vérification du bloc d'informations contenant l'URL: {url}")
                    if check_url(driver, url):
                        print(f"Écriture du bloc d'informations valide dans le fichier de sortie.")
                        out.write("\n".join(block))
                        out.write("\n\n")
                        valide += 1
                    else:
                        invalide += 1
                block = []
            else:
                block.append(line.strip())
        if block:
            url_line = block[-1]
            url = url_line.split(" : ")[-1].strip()
            print(f"Vérification du dernier bloc d'informations contenant l'URL: {url}")
            if check_url(driver, url):
                print(f"Écriture du dernier bloc d'informations valide dans le fichier de sortie.")
                out.write("\n".join(block))
                out.write("\n\n")
                valide += 1
            else:
                invalide += 1
    print("Fermeture du driver Firefox...")
    print(f"Nombre de comptes valides : {valide}")
    print(f"Nombre de comptes invalides : {invalide}")
    # donner le ratio de comptes valides sur le nombre total de comptes l'arrondir à 2 chiffres après la virgule
    print(f"Ratio de comptes valides : {round(valide/(valide+invalide), 2)*100}%")
   
    driver.quit()

if __name__ == "__main__":
    main()
