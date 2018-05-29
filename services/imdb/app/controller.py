from flask import jsonify

from app import app
from app.models import *
from app.database import engine, db_session


def seid(sid, eid):
    eid = eid if len(eid) == 2 else '0' + eid
    sid = sid if len(sid) == 2 else '0' + sid
    return sid + eid


@app.route('/episodes', methods=['GET'])
def all_episodes():
    eps = Episode.query.all()
    episodes = []
    for e in eps:
        e = dict(e.__dict__)
        e.pop('_sa_instance_state')
        e['averageRating'] = str(e['averageRating'])[:3]
        episodes.append(e)
    return jsonify(episodes), 200


@app.route('/season/<season>/episode/<episode>/characters', methods=['GET'])
def test(season, episode):
    cs = engine.execute('''
        select c.CID, name, actor, season_of_death, episode_of_death, means_of_death, episodeCount,
            CASE WHEN 
                cast(season_of_death as integer) == {} and cast(episode_of_death as integer) == {} 
            THEN cast(0 as bit) ELSE cast(1 as bit) END as isAlive
        from characters as c, episodes as e, episode_characters as ec,
            (select c1.CID, count(*) as episodeCount 
             from episodes as e1, characters as c1, episode_characters as ec1
             where 
                ((cast(e1.seasonNumber as integer) < {}) or 
                 (cast(e1.seasonNumber as integer) == {} and cast(e1.episodeNumber as integer) <= {})) and 
                e1.EID == ec1.EID and
                c1.CID == ec1.CID
                group by c1.CID
            ) as eCounts
        where 
            cast(seasonNumber as integer) == {} and 
            cast(episodeNumber as integer) == {} and
            e.EID == ec.EID and
            c.CID == ec.CID and
            c.CID == eCounts.CID
        ;
        '''.format(season, episode, season, season, episode, season, episode)
    )
    characters = []
    for character in cs:
        character_dict = {}
        for pair in character.items():
            character_dict[pair[0]] = pair[1]
        characters.append(character_dict)
    return jsonify(characters), 200


@app.route('/season/<sid>/episode/<eid>', methods=['GET'])
def episode(sid, eid):
    e = Episode.query.filter(Episode.EID == seid(sid, eid))[0]
    if e:
        e = dict(e.__dict__)
        e.pop('_sa_instance_state')
        e['averageRating'] = str(e['averageRating'])[:3]
        return jsonify(e), 200
    return "Episode Not Found", 404


@app.route('/character/<cid>', methods=['GET'])
def character(cid):
    c = Character.query.filter(Character.CID == cid)[0]
    if c:
        c = dict(c.__dict__)
        c.pop('_sa_instance_state')
        return jsonify(c), 200
    return "Character Not Found", 404


@app.route('/season/<sid>/episode/<eid>/characters_old', methods=['GET'])
def episode_characters(sid, eid):
    ceid = seid(sid, eid)
    cs = Character.query.outerjoin(EpisodeCharacters).filter(EpisodeCharacters.EID == ceid)
    if cs:
        ep_characters = []
        for c in cs:
            c = dict(c.__dict__)
            c.pop('_sa_instance_state')
            ep_characters.append(c)
        return jsonify(ep_characters), 200
    return "Complete and Catastrophic Character Failure"


@app.route('/season/<sid>/episode/<eid>/quotes', methods=['GET'])
def episode_quotes(sid, eid):
    qeid = seid(sid, eid)
    #qs = Quote.query.outerjoin(CharacterQuotes).filter(Quote.EID == qeid)
    #qs = CharacterQuotes.query.outerjoin(Quote).filter(Quote.EID == qeid)
    qs = db_session.query(CharacterQuotes.CID, Quote.QID, Quote.quote_text).outerjoin(Quote).filter(Quote.EID == qeid)
    if qs:
        ep_quotes = []
        for q in qs:
            CID, QID, quote_text = q
            q_dict = {
                "CID": CID,
                "QID": QID,
                "quote_text": quote_text
            }
            ep_quotes.append(q_dict)
        return jsonify(ep_quotes), 200
    return "Complete and Catastrophic Quote Failure"


@app.route('/character/<cid>/quotes', methods=['GET'])
def characters_quotes(cid):
    cs = Quote.query.outerjoin(CharacterQuotes).filter(CharacterQuotes.CID == cid)
    if cs:
        character_quote = []
        for c in cs:
            c = dict(c.__dict__)
            c.pop('_sa_instance_state')
            character_quote.append(c)
        return jsonify(character_quote), 200
    return "Complete and Catastrophic Character Failure"


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = "Content-Type, x-access-token, Accept"
    header['Access-Control-Allow-Methods'] = "GET, POST, DELETE"
    return response
