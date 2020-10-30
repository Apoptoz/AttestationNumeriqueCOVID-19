from generate_pdf import generate_pdf
import os
import re
import datetime

def prompt_static_info():
    validation = False
    while not validation:
        first_name = input("Entrez votre prénom (John) :\n")
        last_name = input("Entrez votre nom (Doe) :\n")
        birth_date = input("Entrez votre date de naissance (JJ/MM/AAAA) :\n")
        birth_city = input("Entrez votre lieu de naissance (Paris) :\n")
        address = input("Entrez votre adresse (12 Grande Rue 75666 Paname) :\n")
        current_city = input("Entrez la ville où vous êtes actuellement (Paname) :\n")

        print("Prénom : {}, Nom : {}, Date : {}, Lieu de naissance : {}, Adresse : {}, Ville actuelle : {}".format(first_name, last_name, birth_date, birth_city, address, current_city))
        validation_string = input("Est-ce correct ? [Y/n]\n")
        if validation_string.lower().strip() == 'y' or validation_string == '':
            validation = True
    
    profile_dict = {"first_name":first_name,"last_name":last_name,"birth_date":birth_date,"birth_city":birth_city, "address": address,"current_city":current_city}
    register_file = input("Est-ce que vous voulez enregistrer ces informations (dans le dossier 'profils' à la racine du script) ? [Y/n]\n")
    if register_file == '' or register_file.lower() == 'y':
        write_file(first_name, last_name, birth_date, birth_city, address, current_city)
    
    return profile_dict

def write_file(first_name, last_name, birth_date, birth_city, address, current_city):
    file_name = "profil-"+first_name.lower()+".txt"
    profiles_path = os.path.dirname(os.path.realpath(__file__))+"/profils/"
    if not os.path.exists(profiles_path):
        os.makedirs(profiles_path)
    with open(profiles_path+file_name, "w") as f:
        f.write(first_name+"|"+last_name+"|"+birth_date+"|"+birth_city+"|"+address+"|"+current_city)
        print("Le fichier {} contenant vos informations a été écrit dans le dossier profils à la racine du programme.".format(file_name))

def parse_profile(profile_file):
    profile_list = profile_file.read().split("|")
    return {'first_name':profile_list[0],'last_name':profile_list[1], 'birth_date':profile_list[2], 'birth_city':profile_list[3], 'address':profile_list[4], 'current_city':profile_list[5]}

# Ask for date, time and motive
def prompt_other_info(profile_dict):
    print("\nInformations de sortie pour {} {}".format(profile_dict['first_name'],profile_dict['last_name']))
    
    motif_dict = {"1":"travail", "2":"courses","3":"sante","4":"famille","5":"handicap","6":"sport","7":"judiciaire","8":"missions", "9":"ecole"}
    validation = False
    motif_validation = False

    while not validation:
        current_date = datetime.datetime.today()
        default_date = current_date.strftime("%d/%m/%Y")
        default_time = current_date.strftime("%H:%M")
        date = input("\nEntrez la date de l'attestation au format JJ/MM/AAAA\nAppuyez entrer pour avoir la date du jour : {}\n".format(default_date))
        time = input("Entrez l'heure de l'attestation au format HH:MM \nAppuyez entrer pour avoir l'heure actuelle : {}\n".format(default_time))
        if date == '':
            date = default_date
        if time == '':
            time = default_time
    
        while not motif_validation:
            motifs_string = input("Entrez le ou les motifs de la sortie :\n1 - Travail\n2 - Courses\n3 - Santé\n4 - Famille\n5 - Déplacement Handicap\n6 - Sport\n7 - Judiciaire\n8 - Missions\n9 - Déplacement école ou périscolaire\nEntrez \"1-3-5\" par exemple pour sélectionner plusieurs motifs\n")
            motifs = ""
            
            motif_validation = True # True unless one motif is not in motif_dict
            for motif in motifs_string.split('-'):
                if motif.strip() not in motif_dict:
                    print("\nErreur: le motif \"{}\" ne semble pas exister. Vérifier que vous avez écrit avec le bon format.".format(motif))
                    motif_validation = False
                else:
                    motifs += motif_dict[motif]+"-"
        
        motifs = motifs[:-1] # Remove last '-'
        print("Date: {}, Heure: {}, Motif: {}".format(date, time, motifs))
        validation_string = input("Est-ce correct ? [Y/n]\n")
        if validation_string.lower().strip() == 'y' or validation_string == '':
            validation = True

    profile_dict['leave_date'] = date
    profile_dict['leave_hour'] = time
    profile_dict['motifs'] = motifs
    return profile_dict

def get_profile_files():
    # Create profils folder only if user wants to register one
    try:
        profiles_path = os.path.dirname(os.path.realpath(__file__))+"/profils/"
        directory_file_list = os.listdir(profiles_path)
    except FileNotFoundError:
        return None
    
    profile_regex = re.compile(r"profil-(.*).txt")
    candidate_files = dict()
    for file_name in directory_file_list:
        if profile_regex.match(file_name):
            candidate_files[profile_regex.match(file_name).group(1)] = profiles_path+file_name
    return candidate_files

def choose_profile_file(candidate_files):
    # If no folder profils, then candidate_files is None and so we go to the prompt
    if candidate_files == None:
        return None
    else:
        number_of_profile_files = len(candidate_files)
    profile_file_name = None
    candidate_dict = {}
    cnt = 0
    if number_of_profile_files == 0:
        return None
    else:
        print("Liste des profils enregistrés:\n")
        for candidate_name in candidate_files:
            cnt += 1 
            candidate_dict[cnt] = candidate_name
            print("{} - {}\n".format(cnt, candidate_name))
        validation = False
        while not validation:
            validation_string = input("Entrez le chiffre du profil à utiliser. (Appuyez sur Entrée pour créer un nouveau profil)\n")
            try:
                if int(validation_string) > cnt or int(validation_string) == 0:
                    print("Erreur : Vous avez entré un numéro de profil incorrect.\n")
                else:
                    profile_file_name = candidate_files[candidate_dict[int(validation_string)]]
                    validation = True
            except ValueError:
                print("Nouveau profil:\n")
                validation = True
        
        return profile_file_name



def launch_script(profile_dict):
    # call generator from generate_pdf.py
    generate_pdf(profile_dict['first_name'], profile_dict['last_name'], profile_dict['birth_date'], profile_dict['birth_city'], profile_dict['current_city'], profile_dict['address'], profile_dict['leave_date'], profile_dict['leave_hour'], profile_dict['motifs'])


if __name__ == '__main__':
    candidate_files = get_profile_files()
    chosen_profile_file = choose_profile_file(candidate_files)
    if chosen_profile_file == None:
        profile_dict = prompt_static_info()
    else:
        with open(chosen_profile_file,"r") as profile_file:
            profile_dict = parse_profile(profile_file)

    profile_dict = prompt_other_info(profile_dict)

    launch_script(profile_dict)
