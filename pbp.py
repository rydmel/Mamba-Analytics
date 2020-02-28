import bs4

import util

import re



def clean_text(pbp_url):
    start = '1st QuartertimeteamPLAYSCORE'
    end = 'End of Game'
    pbp_req = util.read_request(util.get_request(pbp_url))
    pbp_soup = bs4.BeautifulSoup(pbp_req, 'html5')
    pbp_text = pbp_soup.text
    clean_text = pbp_text[pbp_text.index(start) + len(start):pbp_text.index(end)]
    return clean_text

def find_assister(text):
    assists = re.findall(r"^[\w]")


