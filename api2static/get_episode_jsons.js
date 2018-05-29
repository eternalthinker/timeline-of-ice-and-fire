const fetch = require('node-fetch');
const fs = require('fs');

function callApi({endpoint, method, data}) {
  let params = {};
  if (method === 'POST') {
    params = {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      }
    };
  }
  return fetch(endpoint, params)
    .then(res => res.json())
    .then(json => json);
}

function getEID(seasonNumber, episodeNumber) {
  return `s${("0" + seasonNumber).slice(-2)}e${("0" + episodeNumber).slice(-2)}`;
}

function mashUp(episodeCharacters, characterQuotes, charactersIaF, characterImages) {
  const episodeCharactersMap = episodeCharacters.reduce((acc, charInfo) => {
    acc[charInfo.CID] = charInfo;
    return acc;
  }, {});
  
  const characterQuotesMap = characterQuotes.reduce((acc, quote) => {
    const slug = quote.CID;
    if (!acc.hasOwnProperty(slug)) {
      acc[slug] = [];
    }
    acc[slug].push(quote.quote_text);
    return acc;
  }, {});

  const charactersIaFMap = charactersIaF.reduce((acc, charInfo) => {
    acc[charInfo.slug] = charInfo;
    return acc;
  }, {});

  const characters = charactersIaF.map(charInfo => {
    const slug = charInfo.slug;
    return {
      ...charInfo,
      ...episodeCharactersMap[slug],
      quotes: characterQuotesMap[slug],
      image: characterImages[slug]
    }
  });

  /*const characters = episodeCharacters.map(charInfo => {
    const slug = charInfo.CID;
    return {
      ...charInfo,
      ...charactersIaFMap[slug],
      quotes: characterQuotesMap[slug]
    }
  });*/

  return characters;
}

function writeToFile(seasonNumber, episodeNumber, data) {
  const jsonStr = JSON.stringify(data, null, 2);
  const eid = getEID(seasonNumber, episodeNumber);
  const fileName = `../data/${eid}.json`;
  fs.writeFile(fileName, jsonStr, function (err) {
    if (err) throw err;
    console.log(`Saved ${fileName}`);
  });
}


function loadEpisode(seasonNumber, episodeNumber) {
  callApi({
    endpoint: `http://localhost:5000/season/${seasonNumber}/episode/${episodeNumber}/characters`,
    method: 'GET'
  })
  .then(episodeCharacters => {
    callApi({
      endpoint: `http://localhost:5000/season/${seasonNumber}/episode/${episodeNumber}/quotes`,
      method: 'GET'
    })
    .then(characterQuotes => {
      const characterList = episodeCharacters.map(charInfo => charInfo.CID);
      callApi({
        endpoint: `http://localhost:7000/characters`,
        method: 'POST',
        data: characterList
      })
      .then(charactersIaF => {
        callApi({
          endpoint: `http://localhost:1337/images`,
          method: 'POST',
          data: characterList
        }).then(characterImages => {
          const characters = mashUp(
            episodeCharacters, 
            characterQuotes, 
            charactersIaF, 
            characterImages
          );
          if (characters.length > 0) {
            writeToFile(seasonNumber, episodeNumber, characters);
          }
        }); // Img service 
      }); // IaF - characters
    }); // IMDB - quotes
  }) // IMDB - episode chars
  .catch(err => {
    console.log(`Couldn't fetch season ${seasonNumber}, episode ${episodeNumber}`);
  });
}

for (let s = 1; s <= 7; ++s) {
  for (let e = 1; e <= 10; ++e) {
    loadEpisode(s, e);
  }
}
