import unittest
import sys

DATA_DIR = '../data'
DB_DIR = '../db'
sys.path.append(DATA_DIR)
sys.path.append(DB_DIR)

import imdb_got

class TestIMDB(unittest.TestCase):

    def test_title_basics(self, EID='tt1480055'):
        imdb = imdb_got.IMDB()
        title = {'tconst': 'tt1480055', 'titleType': 'tvEpisode', 'primaryTitle': 'Winter Is Coming', 'originalTitle': 'Winter Is Coming', 'isAdult': 0, 'startYear': '2011', 'endYear': '\\N', 'runtimeMinutes': '62', 'genres': 'Action,Adventure,Drama'}
        self.assertEqual(imdb.title_basic(EID), title)

    def test_episode(self, EID='tt1480055'):
        imdb = imdb_got.IMDB()
        episode = {'tconst': 'tt1480055', 'parentTconst': 'tt0944947', 'seasonNumber': '1', 'episodeNumber': '1'}
        self.assertEqual(imdb.episode(EID), episode)

    def test_rating(self, EID='tt1480055'):
        imdb = imdb_got.IMDB()
        rating = {'tconst': 'tt1480055', 'averageRating': 9.0, 'numVotes': 25381}
        self.assertEqual(imdb.rating(EID), rating)

    def test_all_episodes(self):
        imdb = imdb_got.IMDB()
        all_episodes = ['tt1480055', 'tt1668746', 'tt1829962', 'tt1829963', 'tt1829964', 'tt1837862', 'tt1837863', 'tt1837864', 'tt1851397', 'tt1851398', 'tt1971833', 'tt2069318', 'tt2069319', 'tt2070135', 'tt2074658', 'tt2084342', 'tt2085238', 'tt2085239', 'tt2085240', 'tt2112510', 'tt2178772', 'tt2178782', 'tt2178784', 'tt2178788', 'tt2178796', 'tt2178798', 'tt2178802', 'tt2178806', 'tt2178812', 'tt2178814', 'tt2816136', 'tt2832378', 'tt2972426', 'tt2972428', 'tt3060782', 'tt3060856', 'tt3060858', 'tt3060860', 'tt3060876', 'tt3060910', 'tt3658012', 'tt3658014', 'tt3846626', 'tt3866826', 'tt3866836', 'tt3866838', 'tt3866840', 'tt3866842', 'tt3866846', 'tt3866850', 'tt3866862', 'tt4077554', 'tt4131606', 'tt4283016', 'tt4283028', 'tt4283054', 'tt4283060', 'tt4283074', 'tt4283088', 'tt4283094', 'tt5654088', 'tt5655178', 'tt5775840', 'tt5775846', 'tt5775854', 'tt5775864', 'tt5775874', 'tt5924366', 'tt6027908', 'tt6027912', 'tt6027914', 'tt6027916', 'tt6027920']
        self.assertEqual(imdb.all_episodes(), all_episodes)

if __name__ == '__main__':
    unittest.main()