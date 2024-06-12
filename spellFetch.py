import requests
import unicodedata
import webbrowser

base_link = "https://www.aidedd.org/dnd/sorts.php?"

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def full_sub_link(response, semi_complete_link):
    index = response.text.find(semi_complete_link)
    general_response_area = response.text[index:index+len(semi_complete_link)+25]
    spell_link = general_response_area[0:general_response_area.find('\'')]
    return spell_link

def get_vf_link(cleaned_spell):
    link = base_link + "vf=" + cleaned_spell
    return link

def get_vo_link(cleaned_spell):
    link = base_link + "vo="
    return full_sub_link(requests.get(get_vf_link(cleaned_spell)),link)
    
def clean_spell(spell):
    return remove_accents(str(spell).replace(' ', '-'))

def fetch_vo_spell_from_vf(sort):
    return get_vo_link(clean_spell(sort))

def fetch_vf_spell(sort):
    return get_vf_link(clean_spell(sort))

def open_link_in_browser(url):
    return webbrowser.open(url,2)

# Exemple d'utilisation
sort = "boule de feu"
vf_link = fetch_vf_spell(sort)
print("Lien VF :", vf_link)

vo_link = fetch_vo_spell_from_vf(sort)
print("Lien VO :", vo_link)

# Ouvrir le lien VO dans le navigateur
open_link_in_browser(vo_link)



"""TODO mettre la liste dans un fichier, puis le lire avec ce script, ce qui ouvre la fenêtre de tout les sorts
+ detecter si pb syntaxe
"""