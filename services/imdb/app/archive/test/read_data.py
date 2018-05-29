import sys
import numpy as np 
import requests

DATA_DIR = '../data'
DB_DIR = '../db'
sys.path.append(DATA_DIR)
sys.path.append(DB_DIR)

import imdb_got


# URI_KAGGLE = 'http://'
# URI_IMDB = 'https://datasets.imdbws.com/'

# r = requests.get(URI_IMDB + 'title.episode.tsv.gz')

# print(r.__dict__)


# kaggle = datasets.KAGGLE()
imdb = imdb_got.IMDB()

# episode = 'tt1480055' 
# cast = imdb.cast(episode)
# print(cast)

# ratings = imdb.ratings(episode)
# print(ratings)

# eps = imdb.episode(episode)
# print(eps[0])

# episodes = ['tt1480055', 'tt1668746', 'tt1829962', 'tt1829963', 'tt1829964', 'tt1837862',
#             'tt1837863', 'tt1837864', 'tt1851397', 'tt1851398', 'tt1971833', 'tt2069318',
#             'tt2069319', 'tt2070135', 'tt2074658', 'tt2084342', 'tt2085238', 'tt2085239',
#             'tt2085240', 'tt2112510', 'tt2178772', 'tt2178782', 'tt2178784', 'tt2178788',
#             'tt2178796', 'tt2178798', 'tt2178802', 'tt2178806', 'tt2178812', 'tt2178814',
#             'tt2816136', 'tt2832378', 'tt2972426', 'tt2972428', 'tt3060782', 'tt3060856',
#             'tt3060858', 'tt3060860', 'tt3060876', 'tt3060910', 'tt3658012', 'tt3658014',
#             'tt3846626', 'tt3866826', 'tt3866836', 'tt3866838', 'tt3866840', 'tt3866842',
#             'tt3866846', 'tt3866850', 'tt3866862', 'tt4077554', 'tt4131606', 'tt4283016',
#             'tt4283028', 'tt4283054', 'tt4283060', 'tt4283074', 'tt4283088', 'tt4283094',
#             'tt5654088', 'tt5655178', 'tt5775840', 'tt5775846', 'tt5775854', 'tt5775864',
#             'tt5775874', 'tt5924366', 'tt6027908', 'tt6027912', 'tt6027914', 'tt6027916',
#             'tt6027920']

EID = 'tt1480055'

# for ep in episodes:

#     data = {}

#     try:
#         eps = imdb.episode(ep)
#         data['tconst'] = ep
#         data['seasonNumber'] = eps[1]
#         data['episodeNumber'] = eps[2]
#     except:
#         pass

#     try:
#         rts = imdb.ratings(ep)
#         data['averageRating'] = rts[1]
#         data['numVotes'] = rts[2]
#     except:
#         pass

#     data['title'] = ''
#     data['duration'] = 60

#     print(data.keys())
#     print(tuple(data.values()))


# print(kaggle.battles())
print(imdb.rating(EID))