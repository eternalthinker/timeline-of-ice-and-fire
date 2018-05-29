import numpy as np 
import pandas as pd 
from os import path
import requests
import json


class IaF:

    def __init__(self):
        self.data_dir = '../data/iceandfire/'

    def get_file(self, file, uri):
        file_path = self.data_dir + file
        if not path.exists(file_path):
            r = requests.request('get', uri)
            with open(file_path, 'w') as out:
                json.dump(r.json(), out)
        return pd.read_json(self.data_dir + file)

    def houses(self):
        """
        Parameters:

        Returns:
        :url:
        :name:
        :region:
        :coatOfArms:
        :words:
        :titles:
        :seats:
        :currentLord:
        :heir:
        :overlord:
        :founded:
        :founder:
        :diedOut:
        :ancestralWeapons:
        :cadetBranches:
        :swornMembers:
        """
        uri = 'https://anapioficeandfire.com/api/houses/'
        file = 'houses.json'
        return self.get_file(file, uri)

    def book(self):
        """
        Parameters:

        Returns:
        :url:
        :name:
        :authors:
        :publisher:
        :country:
        :mediaType:
        :released:
        :characters:        A list of the uri for each character

        """
        file = 'book.json'
        uri = 'https://www.anapioficeandfire.com/api/books/1'
        return self.get_file(file, uri)

    def character(self, name):
        """
        Parameter:
        :CID:           String              

        Returns:
        :url:           String              The hypermedia URL of this resource
        :name:          String              The name of this character
        :gender:        String              The gender of this character
        :culture:       String              The culture that this character belongs to
        :born:          String              Textual representation of when and where this character was born
        :died:          String              Textual representation of when and where this character died
        :titles:        Array of Strings    The titles that this character goes by
        :alaiases:      Array of Strings    The aliases that this character goes by
        :father:        String              The character resource URL of this character's father
        :mother:        String              The character resource URL of this character's mother
        :spouse:        String              An array of character resource URLs that has had a POV-chapter in this book
        :allegiances:   Array of Strings    An array of House resource URLs that this character is loyal to
        :books:         Array of Strings    An array of Book resource URLs that this character has been in
        :povBooks:      Array of Strings    An array of Book resource URLs that this character has had a a POV-chapter in
        :tvSeries:      Array of Strings    An array of names of the seasons of Game of Thrones that this character has been in
        :playedBy:      Array of Strings    An array of actor names that has played this character in the TV show Game of Thrones
        """
        file = string(name) + '.json'
        uri = 'https://www.anapioficeandfire.com/api/characters/?name=<name>'
        return self.get_file(file, uri)
