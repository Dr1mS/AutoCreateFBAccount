import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime




# définir le nombre de fois que vous voulez exécuter le script
num_runs = input("Combien de comptes voulez-vous créer ? ")

# convertir la réponse en entier
num_runs = int(num_runs)
# exécuter le script autant de fois que nécessaire
for _ in range(num_runs):
    print(f"Création d'un compte Facebook en cours... {_+1}/{num_runs}\n")
    # subprocess createFBAccount.py
    subprocess.run(["python", "createFBAccount.py"])

print("Tous les comptes ont été créés avec succès !")



