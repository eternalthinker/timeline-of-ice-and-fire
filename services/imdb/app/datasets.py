import numpy as np 
import pandas as pd 
from os import path
import requests
import json


class IMDB:

    def __init__(self):
        self.data_dir = '../data/imdb/'
        self.uri = 'https://datasets.imdbws.com/'

    def get_file(self, file):
        file_path = self.data_dir + file
        if not path.exists(file_path):
            r = requests.request('get', self.uri + file, allow_redirects=True)
            open(file_path, 'wb').write(r.content)
        return pd.read_table(self.data_dir + file, sep='\t', header=0)

    def actor_basics(self):
        """
        Parameters:

        Returns:
        :nconst:            unique identifier
        :primaryName:       name
        :birhtYear:         in YYYY format
        :deathYear:         in YYYY format
        :primaryProfession: top-3 professions of the person
        :knownForTitles:    titles the person is known for
        """
        file = 'name.basics.tsv.gz'
        return self.get_file(file)

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
        return self.get_file(file)

    def title_basics(self):
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
        return self.get_file(file)

    def crews(self):
        """
        Parameters:

        Returns:
        :tconst:            unique identifier
        :directors:         array of nconsts
        :writers:           writers of the given titles
        """
        file = 'title.crew.tsv.gz'
        return self.get_file(file)

    def episodes(self):
        """
        Parameters:

        Returns:
        :tconst:            unique identifer
        :parentTconst:      unique identifier parent
        :seasonNumber:      season number the episode belongs to
        :episodeNumber:     episode number of the tconst in the TV series
        """
        file = 'title.episode.tsv.gz'
        return self.get_file(file)

    def principals(self):
        """
        Parameters:

        Returns:
        :tconst:            unique identifier
        :principalCast:     array of nconst
        """
        file = 'title.principals.tsv.gz'
        return self.get_file(file)

    def casts(self):
        """
        Parameters:

        Returns:
        :tconst:            unique identifier
        :principalCast:     array of nconst
        """
        file = 'title.principals.tsv.gz'
        return self.get_file(file)

    def ratings(self):
        """
        Parameters:

        Returns:
        :tconst:            unique identifier
        :averageRating:     weighter average of all the individual user ratings
        :numVotes:          number of votes the title has received
        """
        file = 'title.ratings.tsv.gz'
        return self.get_file(file)
