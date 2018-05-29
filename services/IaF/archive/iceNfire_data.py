import requests

class ice_and_fire:

    def __init__(self):
        self.book_url = 'https://www.anapioficeandfire.com/api/books/1'
        resp = requests.get('https://www.anapioficeandfire.com/api/books/1').json()
        self.char_url_list = resp['characters']
        self.poV = resp['povCharacters']
        self.house_url = 'https://anapioficeandfire.com/api/houses/'
        self.house_list = requests.get('https://anapioficeandfire.com/api/houses/').json()


    def get_all_characters(self):
        # n =  0
        i = ice_and_fire()
        char_list = []
        url_list = i.char_url_list
        for i in url_list:
            response = requests.get(i).json()
            char_list.append(response)
            # n += 1
            # if n >= 100:
            #     return char_list
        return char_list


class characters:
    def __init__(self):
        self.name = None
        self.slug = None
        self.gender = 'Male'
        self.culture = None
        self.titles = None
        self.aliases = None
        self.father = None
        self.mother = None
        self.spouse = None
        self.allegiances = None
        self.seasons = None
        self.actor =  None

    def get_character(self, url):
        # print(url_list)
        obj2 = characters()
        r = requests.get(url).json()
        obj2.name = r['name']
        obj2.slug = r['name'].lower().replace(' ','_')
        obj2.gender = r['gender']
        obj2.culture = r['culture'] if r['culture'] else 'NULL'
        obj2.titles = ' , '.join(r['titles']) if r['titles'] else 'NULL'
        obj2.aliases = ' , '.join( r['aliases']) if r['aliases'] else 'NULL'
        obj2.father = requests.get(r['father']).json()['name'] if r['father'] else 'NULL'
        obj2.mother = requests.get(r['mother']).json()['name'] if r['mother'] else 'NULL'
        obj2.spouse = requests.get(r['spouse']).json()['name'] if r['spouse'] else 'NULL'
        if r['allegiances']:
            p = []
            for i in r['allegiances']:
                m = requests.get(i).json()['name']
                p.append(m)
            obj2.allegiances = ' , '.join(p)
        else:
            obj2.allegiances = 'NULL'
        obj2.seasons = ' , '.join(r['tvSeries']) if r['tvSeries'] else 'NULL'
        obj2.actor = ' , '.join(r['playedBy']) if r['playedBy'] else 'NULL'
        return obj2

# ice = ice_and_fire()
# chars = ice.poV
# c =  characters()
# for url in chars:
#     n = c.get_character(url)
#     print(n.__dict__)

class houses:
    def __init__(self):
        self.name = None
        self.slug = None
        self.name = None
        self.region = None
        self.coatOfArms = None,
        self.words = None
        self.titles = None
        self.seats = None
        self.currentLord = None
        self.overlord = None
        self.swornMembers = None

    def get_house(self):
        h = ice_and_fire().house_list
        self.c = []

        for r in h:
            obj = houses()
            obj.name = r['name']
            if obj.name:
                obj.slug = obj.name.lower().replace(' ', '_')
            else:
                obj.slug = None
            obj.region = r['region'] if r['region'] else 'NULL'
            obj.coatOfArms = r['coatOfArms'] if r['coatOfArms'] else 'NULL'
            obj.words = r['words'] if r['words'] else 'NULL'
            obj.titles = ' , '.join(r['titles']) if r['titles'] else 'NULL'
            obj.seats = ' , '.join(r['seats']) if r['seats'] else 'NULL'
            obj.currentLord = requests.get(r['currentLord']).json()['name'] if r['currentLord'] else 'NULL'
            obj.overlord = requests.get(r['overlord']).json()['name'] if r['overlord'] else 'NULL'

            if r['swornMembers']:
                p = []
                for i in r['swornMembers']:
                    m = requests.get(i).json()['name']
                    p.append(m)
                obj.swornMembers = ' , '.join(p)
            else:
                obj.swornMembers = 'NULL'

            self.c.append(obj)


        return self.c



# k = houses().get_house()
# for i in k:
#     print(i.__dict__)
