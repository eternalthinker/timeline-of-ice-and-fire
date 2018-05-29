from flask import Flask, redirect, render_template, request, url_for, jsonify, Response, make_response
from flask_restful import reqparse
from episode import *
from quoteslist import *
import sys

sys.path.insert(0, '../db')

from read_data import * #just checking I can get things from the db folder

app = Flask(__name__)


@app.route('/episodes', methods=['GET'])
def get_episode():

				# Parse request
				parser = reqparse.RequestParser()
				parser.add_argument('season', type=str)
				parser.add_argument('episode', type=str)
				args = parser.parse_args()
				season_num = args.get("season")
				episode_num = args.get("episode")

				episode = create_episode(season_num, episode_num)

				return jsonify([episode.__dict__])

@app.route('/quotes', methods=['GET'])
def get_quotes_by_episode():

				# Parse request
				parser = reqparse.RequestParser()
				parser.add_argument('season', type=str)
				parser.add_argument('episode', type=str)
				args = parser.parse_args()
				season_num = args.get("season")
				episode_num = args.get("episode")

				quotes = get_quotes(season_num, episode_num)

				return jsonify([quotes.__dict__])



def create_episode(season_num, episode_num):
				e = Episode(season_num, episode_num)
				return e

def get_quotes(season_num, episode_num):
				q = QuotesList(season_num, episode_num)
				return q
