#supprimer tous les doublons dans le fichier compteOK.txt
def remove_duplicates(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Utiliser un set pour suivre les lignes uniques
    unique_lines = set()
    clean_lines = []  # Stocke les lignes sans doublons

    for line in lines:
        # Si la ligne contient une URL, ajouter un retour à la ligne supplémentaire
        if "Url :" in line:
            line = line.strip() + '\n\n'
        # Si la ligne n'a pas été vue auparavant, l'ajouter aux lignes nettoyées
        if line not in unique_lines:
            clean_lines.append(line)
            unique_lines.add(line)

    # Écrire les lignes nettoyées dans le fichier
    with open("file_name", 'w') as file:
        file.writelines(clean_lines)

    print(f"{len(lines) - len(clean_lines)} doublons supprimés.")

file_name = 'compteOK.txt'
remove_duplicates(file_name)
