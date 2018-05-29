import numpy as np 
import pandas as pd 
from os import path
import urllib.request


def get_file(URI, DATA_DIR, file):
    file_path = DATA_DIR + file
    if not path.exists(file_path):
        urllib.request.urlretrieve(URI + file, file_path)


class KAGGLE:

    def __init__(self):
        self.data_dir = '../data/'
        self.uri = 'https://www.kaggle.com/mylesoneill/game-of-thrones/downloads/'

    def battles(self):
        """
        Parameters:

        Returns:
        :name:
        :year:
        :battle_number:
        :attacker_king:
        :defender_king:
        :attacker_1:
        :attacker_2:
        :attacker_3:
        :attacker_4:
        :defender_1:
        :defender_2:
        :defender_3:
        :defender_4:
        :attacker_outcome:
        :battle_type:
        :major_death:
        :major_capture:
        :major_capture:
        :attacker_size:
        :defender_size:
        :attacker_commander:
        :defender_commander:
        :summer:
        :location:
        :region:
        :note:
        """
        file = 'battles.csv'
        get_file(self.uri, self.data_dir, file)
        return pd.read_csv(self.data_dir + file, sep=',', header=0)

    def deaths(self):
        """
        Parameters:

        Returns:
        :Name:
        :Allegiances:
        :Death Year:
        :Book of Death:
        :Death Chapter:
        :Book Intro Chapter:
        :Gender:
        :Nobility:
        :GoT:
        :CoK:
        :SoS:
        :FfC:
        :DwD:
        """
        return pd.read_csv(self.dir + 'character-deaths.csv', sep=',', header=0)
    
    def predictions(self):
        """
        Parameters:

        Returns:
        :S.No:
        :actual:
        :pred:
        :alive:
        :plod:
        :name:
        :title:
        :male:
        :culture:
        :dateOfBirth:
        :dateOfDeath:
        :mother:
        :father:
        :heir:
        :house:
        :spouse:
        :book1:
        :book2:
        :book3:
        :book4:
        :book5:
        :isAliveMother:
        :isAliveFather:
        :isAliveHeir:
        :isAliveSpouse:
        :isMarried:
        :isNoble:
        :age:
        :numDeadRelations:
        :boolDeadRelations:
        :isPopular:
        :popularity:
        :isAlive:
        """
        return pd.read_csv(self.dir + 'character-predictions.csv', sep=',', header=0)

class IMDB:

    def __init__(self):
        self.parentID = 'tt0944947'
        self.data_dir = '../data/'
        self.uri = 'https://datasets.imdbws.com/'

    def actor_basics(self, nconst):
        """
        Parameters:
        :nconst:            unique identifier

        Returns:
        :nconst:            unique identifier
        :primaryName:       name
        :birhtYear:         in YYYY format
        :deathYear:         in YYYY format
        :primaryProfession: top-3 professions of the person
        :knownForTitles:    titles the person is known for
        """
        file = 'name.basics.tsv.gz'
        get_file(self.uri, self.data_dir, file)
        df =  pd.read_table(self.data_dir + file, sep='\t', header=0)
        return df.loc[df['nconst'] == nconst].to_dict('records')[0]

    def title_akas(self):
        """
        Parmaters:

        Returns:
        :tconst:            unique identifier
        :ordering:          # to uniquely identify rows for a given tconst
        :title:             the localized title
        :region:            the region for this version of the title
        :language:          the language of the title
        :types:             {alternative, dvd, festival, tv, video, working, original, imdbDisplay}
        :attributes:        additional terms
        :isOriginalTitle:   boolean {0 not original, 1 original}
        """
        file = 'title.akas.tsv.gz'
        get_file(self.uri, self.data_dir, file)
        df = pd.read_table(self.data_dir + file, sep='\t', header=0)
        return df.loc[df['tconst'] == self.id].to_dict('records')

    def title_basics(self, EID):
        """
        Parameters:

        Returns:
        :tconst:            unique identifier
        :titleType:         {move, short, tvseries, tvepisode, video}
        :primaryTitle:      the more popular title 
        :originalTitle:     original title in original language
        :isAdult:           boolean {0 not adult, 1 adult}
        :startYear:         YYYY release
        :endYear:           YYYY TV series end year
        :runtimeMinutes:    primary runtime of the title in minutes
        :genres:            top-3 genres associated with the tile
        """
        file = 'title.basics.tsv.gz'
        get_file(self.uri, self.data_dir, file)
        df = pd.read_table(self.data_dir + file, sep='\t', header=0)
        return df.loc[df['tconst'] == EID].to_dict('records')[0]

    def crews(self, EID):
        """
        Parameters:
        :episode:           tconst unique identifier

        Returns:
        :tconst:            unique identifier
        :directors:         array of nconsts
        :writers:           writers of the given titles
        """
        file = 'title.crew.tsv.gz'
        get_file(self.uri, self.data_dir, file)
        df = pd.read_table(self.data_dir + file, sep='\t', header=0)
        return df.loc[df['tconst'] == EID].to_dict('records')

    def episodes(self, EID):
        """
        Parameters:
        :episode:           tconst unique identifier

        Returns:
        :tconst:            unique identifer
        :parentTconst:      unique identifier
        :seasonNumber:      season number the episode belongs to
        :episodeNumber:     episode number of the tconst in the TV series
        """
        file = 'title.episode.tsv.gz'
        get_file(self.uri, self.data_dir, file)
        df = pd.read_table(self.data_dir + file, sep='\t', header=0)
        return df.loc[df['tconst'] == EID].to_dict('records')[0]

    def principals(self, EID):
        """
        Parameters:
        :episode:           unique identifier

        Returns:
        :tconst:            unique identifier
        :principalCast:     array of nconst
        """
        file = 'title.principals.tsv.gz'
        get_file(self.uri, self.data_dir, file)
        df = pd.read_table(self.data_dir + file, sep='\t', header=0)
        return df.loc[df['tconst'] == EID].to_dict('records')

    def casts(self, EID):
        """
        Parameters:
        :episode:           unique identifier

        Returns:
        :tconst:            unique identifier
        :principalCast:     array of nconst
        """
        file = 'title.principals.tsv.gz'
        get_file(self.uri, self.data_dir, file)
        df = pd.read_table(self.data_dir + file, sep='\t', header=0)
        return df.loc[(df['tconst'] == EID) & df['category'].isin(('actor', 'actress'))].to_dict('records')

    def ratings(self, EID):
        """
        Parameters:
        :episode:           tconst unique identifier

        Returns:
        :tconst:            unique identifier
        :averageRating:     weighter average of all the individual user ratings
        :numVotes:          number of votes the title has received
        """
        file = 'title.ratings.tsv.gz'
        get_file(self.uri, self.data_dir, file)
        df = pd.read_table(self.data_dir + file, sep='\t', header=0)
        return df.loc[df['tconst'] == EID].to_dict('records')[0]

    def all_episodes(self):
        """
        Parameters:

        Returns:
        :tconst:           array of all GOT epidosdes
        """
        file = 'title.episode.tsv.gz'
        get_file(self.uri, self.data_dir, file)
        df = pd.read_table(self.data_dir + file, sep='\t', header=0)
        df = df.loc[df['parentTconst'] == self.parentID]
        return df['tconst'].tolist()

