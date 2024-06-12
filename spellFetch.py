import requests
import unicodedata
import webbrowser
from string import punctuation

base_link = "https://www.aidedd.org/dnd/sorts.php?"

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def full_sub_link(response, semi_complete_link):
    index = response.text.find(semi_complete_link)
    if index == -1:
        return None
    general_response_area = response.text[index:index+len(semi_complete_link)+25]
    spell_link = general_response_area[0:general_response_area.find('\'')]
    return spell_link

def get_vf_link(cleaned_spell):
    return base_link + "vf=" + cleaned_spell

def get_vo_link(cleaned_spell):
    vf_response = requests.get(get_vf_link(cleaned_spell))
    return full_sub_link(vf_response, base_link + "vo=")

def clean_spell(spell):
    spell = remove_accents(str(spell).replace(' ', '-').replace('\'','-'))
    while (spell[-1] in punctuation):
        spell = spell[0:-1]
    
    while (spell[0] in punctuation):
        spell = spell[1:-1]+spell[-1]
        
    return spell

def fetch_vo_spell_from_vf(sort):
    cleaned_sort = clean_spell(sort)
    return get_vo_link(cleaned_sort)

def fetch_vf_spell(sort):
    cleaned_sort = clean_spell(sort)
    return get_vf_link(cleaned_sort)

def open_link_in_browser(url):
    return webbrowser.open(url, 2)

def process_spells_from_file(file_path, open_vo = False):
    with open(file_path, 'r', encoding='utf-8') as file:
        spells = [line.strip() for line in file.readlines()]
    
    failed_spells = []

    for spell in spells:
        try:
            if open_vo: 
                link = fetch_vo_spell_from_vf(spell)
                print(f"Lien VO pour '{spell}': {link}")
            else: 
                link = fetch_vf_spell(spell)
                print(f"Lien VF pour '{spell}': {link}")

            if link:
                open_link_in_browser(link)
            else:
                failed_spells.append(spell)
        except Exception as e:
            print(f"Erreur avec le sort '{spell}': {e}")
            failed_spells.append(spell)

    if failed_spells:
        print("Sorts pour lesquels les liens n'ont pas pu être ouverts :")
        for failed_spell in failed_spells:
            print(f"- {failed_spell}")
            
    file.close()


process_spells_from_file('sorts.txt')