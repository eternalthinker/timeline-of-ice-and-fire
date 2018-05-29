/* Globals */
let lastData = null;
let isFirstLoad = true;
let allEpisodes = null;

function getDiff(curData, prevData) {
  /* Convert data list to a map for quick lookup */
  const prevDataMap = prevData.reduce((acc, charInfo) => {
    acc[charInfo.slug] = charInfo;
    return acc;
  }, {});

  const curDataMap = curData.reduce((acc, charInfo) => {
    acc[charInfo.slug] = charInfo;
    return acc;
  }, {});

  let remove = [];
  let reuse = [];
  let deaths = [];
  let reverseDeaths = [];
  let add = [];

  curData.forEach((charInfo, i) => {
    const slug = charInfo.slug;
    if (slug in prevDataMap) {
      const isAlive = Boolean(charInfo.isAlive);
      const prevAlive = Boolean(prevDataMap[slug].isAlive);
      if (prevAlive && !isAlive) {
        deaths.push(charInfo);
      } else if (!prevAlive && isAlive) {
        reverseDeaths.push(charInfo);
      }
      reuse.push(charInfo);
    } else {
      add.push(charInfo);
    }
  });

  prevData.forEach((charInfo, i) => {
    const slug = charInfo.slug;
    if (!(slug in curDataMap)) {
      remove.push(charInfo);
    }
  });

  return {
    add,
    remove,
    reuse,
    deaths,
    reverseDeaths
  };
}

function getDiffFromService(curData, prevData) {
  return callApi({
    endpoint: `http://localhost:5001/diff`,
    method: 'POST',
    data: {
      'curr_data': curData,
      'prev_data': prevData
    }
  });
}


function episodeChart() {
  const width = 1100;
  const height = 550;

  const tooltip = floatingTooltip('character_tooltip', 180);
  const center = {
    x: width / 2,
    y: height /2
  };  

  const forceStrength = 0.05;

  let svg = null;
  let bubbles = null;
  let nodes = [];
  let houseCenters = {};

  function charge(d) {
    return -Math.pow(d.radius, 2.1) * forceStrength;
  }

  let simulation = d3.forceSimulation()
    .velocityDecay(0.2)
    .force('x', d3.forceX().strength(forceStrength).x(center.x))
    .force('y', d3.forceY().strength(forceStrength).y(center.y))
    .force('charge', d3.forceManyBody().strength(charge))
    //.force('link', d3.forceLink().id(function(d) { return d.index; }))
    //.force('collide', d3.forceCollide(d => d.r + 2).iterations(24))
    .on('tick', ticked);

  simulation.stop();

  const strokeColor = d3.scaleOrdinal()
    .domain(['alive', 'dead'])
    .range(['#ffffff', '#000000']);

  const houseColorMappings = {
    'targaryen': '#f73859',
    'lannister': '#ffc300',
    'tully': '#add3fb',
    'baratheon': '#feda95',
    'tyrell': '#88d3d1',
    'nymeros': '#fcba86',
    'stark': '#93deff', //#6f6f6f',
    'arryn': '#506c86',
    'greyjoy': '#d8c5ad',
    'other': '#d8d8d8',

    'clegane': '#f8b195',
    'reed': '#a40a3c',
    'cassel': '#ec610a',
    'mormont': '#c26271',
    'baelish': '#fc94aa',
    'selmy': '#404b69',
    'payne': '#00818a',
    'tarly': '#6db193',
    'stokeworth': '#e7759a',
    'bolton': '#ba78cd',
    'frey': '#409d9b'
  };

  /*let houseDomains = Object.keys(houseColorMappings);
  let houseColorRange = [];
  for (let key of houseDomains) {
    houseColorRange.push(houseColorMappings[key]);
  }*/

  /*const fillColor = d3.scaleOrdinal()
    .domain(houseDomains)
    .range([...houseColorRange]);*/
    /*, 
      '#6b0848', '#a40a3c', '#ec610a', '#ffc300', 
      '#f73859', '#404b69', '#00818a', '#658525', '#e7759a']);*/

  const fillColor = (house) => {
    house = house.toLowerCase();
    if (!houseColorMappings.hasOwnProperty(house)) {
      house = 'other';
    } 
    return houseColorMappings[house];
  };

  function getHouse(allegiances) {
    if (allegiances == 'NULL') {
      return 'Other';
    }
    const houseTitle = allegiances.split(',')[0];
    const house = houseTitle.split(' ')[1];
    return house;
  }

  function createNodes(rawData, prevDataMap) {
    const maxEpisodes = 45; //d3.max(rawData, (d) => +d.episodeCount);
    const radiusScale = d3.scalePow()
      .exponent(0.5)
      .range([5, 40])
      .domain([0, maxEpisodes]);

    const myNodes = rawData.map((d) => {
      let node = {
        ...d,
        slug: d.slug,
        name: d.name,
        actor: d.actor,
        house: getHouse(d.allegiances),
        value: d.episodeCount,
        id: d.CID,
        isAlive: Boolean(d.isAlive),
        radius: radiusScale(+d.episodeCount),
        r: radiusScale(+d.episodeCount)
      };

      const slug = d.slug;
      if (prevDataMap && (slug in prevDataMap)) {
        const prevNode = prevDataMap[slug];
        node.x = prevNode.x;
        node.y = prevNode.y;
      } else {
        node.x = Math.random() * width;
        node.y = Math.random() * height;
      }

      return node;
    });

    myNodes.sort(function (a, b) { return b.value - a.value; });

    return myNodes;
  }

  // Create chart
  const chart = async function chart(selector, rawData) {
    let diff = null;
    if (lastData) {
      isFirstLoad = false;
      diff = await getDiff(rawData, lastData);
    }

    // lastData = rawData;
    let lastDataMap = null;
    if (lastData) {
      lastDataMap = lastData.reduce((acc, charInfo) => {
        acc[charInfo.slug] = charInfo;
        return acc;
      }, {});
    }
    nodes = createNodes(rawData, lastDataMap);
    lastData = nodes;

    const housesMap = nodes.reduce((acc, charInfo) => {
      acc[charInfo.house] = true;
      return acc;
    }, {});
    const houses = Object.keys(housesMap);
    const numHouses = houses.length;
    const centersGap = (width - 150) / (numHouses + 1);
    houseCenters = houses.reduce((acc, house, i) => {
      console.log(centersGap ,100 + centersGap*(i+1));
      acc[house] = {
        x: 100 + centersGap*(i+1),
        y: height / 2
      };
      return acc;
    }, {});

    /*if (svg) {
      d3.selectAll("svg").remove();
    } */
    if (!svg) {
      svg = d3.select(selector)
        .append('svg')
        .attr('width', width)
        .attr('height', height);
    }

    bubbles = svg.selectAll('.bubble')
      .data(nodes, (d) => d.CID);

    function aliveStatus(isAlive) {
      if (isAlive) {
        return "alive";
      } else {
        return "dead";
      }
    }

    function dragstarted(d) {
      if (!d3.event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }
    
    function dragged(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    }
    
    function dragended(d) {
      if (!d3.event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    } 

    const bubblesE = bubbles.enter()
      .append('circle')
        .classed('bubble', true)
        .attr('id', d => d.slug)
        .attr('r', 0)
        .attr('fill', function (d) { return fillColor(d.house); })
        .attr('stroke', function (d) { return d3.rgb(fillColor(d.house)).darker(); })
        .attr('stroke-width', 2)
        .attr('stroke-dasharray', (d) => d.isAlive? "": "5")
        .on('mouseover', showDetail)
        .on('mouseout', hideDetail)
        //.attr("r", function(d){  return d.r })
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended))
      ;

    bubbles = bubbles.merge(bubblesE);

    bubbles.transition()
      .duration(2000)
      .attr('transform', 'translate(0)')
      .attr('r', function (d) { return d.radius; })
      ;

    simulation.nodes(nodes);

    groupBubbles();
    //splitBubbles();

    if (diff) {
      diff.remove.forEach((charInfo) => {
        d3.select(`#${charInfo.slug}`).transition()
          .duration(2000)
          .attr('transform', 'translate(0)')
          .attr('r', 0)
          .remove()
          ;
      });

      diff.deaths.forEach((charInfo) => {
        d3.select(`#${charInfo.slug}`).transition()
          .duration(2000)
          .attr('stroke-dasharray', '5')
          ;
      });

      diff.reverseDeaths.forEach((charInfo) => {
        d3.select(`#${charInfo.slug}`).transition()
          .duration(2000)
          .attr('stroke-dasharray', '')
          ;
      });
    }

  };

  function nodeHousePos(d) {
    return houseCenters[d.house].x;
  }

  function ticked() {
    bubbles
      .attr('cx', function (d) { return d.x; })
      .attr('cy', function (d) { return d.y; });
  }

  function groupBubbles() {
    simulation.force('x', d3.forceX().strength(forceStrength).x(center.x));
    simulation.alpha(1).restart();
  }

  function splitBubbles() {
    simulation.force('x', d3.forceX().strength(forceStrength).x(nodeHousePos));
    simulation.alpha(1).restart();
  }

  function showCharacter(d) {
    $('.character-name').text(d.name);
    $('.character-house').text(d.house === 'Other' ? '' : `House ${d.house}` || '');
    $('.character-episodeCount').text(`in ${d.episodeCount} episode${d.episodeCount > 1 ? 's' : ''}`);
    $('.character-image').attr('src', d.image || '');
    $('.character-quote').html(d.quotes ? d.quotes[Math.floor(Math.random() * d.quotes.length)] : '');
    if (d.isAlive) {
      $('.character-death').hide();
      $('.character-is-dead').hide();
    } else {
      $('.character-death').text(d.means_of_death);
      $('.character-death').show();
      $('.character-is-dead').show();
    }
    $('.character').show();
  }

  function hideCharacter(d) {
    $('.character').hide(); 
  }

  function showDetail(d) {
    d3.select(this).attr('stroke', 'black');

    var content = '<span class="name">Name: </span><span class="value">' +
                  d.name +
                  '</span><br/>' +
                  '<span class="name">House: </span><span class="value">' +
                  d.house +
                  '</span><br/>' +
                  '<span class="name">Actor: </span><span class="value">' +
                  d.actor +
                  '</span>';
    tooltip.showTooltip(content, d3.event);
    showCharacter(d);
  }

  function hideDetail(d) {
    d3.select(this)
      .attr('stroke', d3.rgb(fillColor(d.house)).darker());

    tooltip.hideTooltip();
    hideCharacter(d);
  }

  chart.toggleDisplay = function (displayName) {
    if (displayName === 'split-bubbles') {
      splitBubbles();
    } else {
      groupBubbles();
    }
  };

  return chart;
}

const gotChart = episodeChart();

function display(data) {
  gotChart('#vis', data);
}

function setupButtons() {
  d3.selectAll('.btn')
    .on('click', function () {
      var button = d3.select(this);
      var buttonId = button.attr('id');
      gotChart.toggleDisplay(buttonId);
    });
}

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

function loadEpisode(seasonNumber, episodeNumber) {
  callApi({
    endpoint: getDataFile(seasonNumber, episodeNumber),
    method: 'GET'
  })
  .then(characters => {
    display(characters);
  })
  ;
}

function loadEpisodeServices(seasonNumber, episodeNumber) {
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
          //console.log(characters);
          // console.log(JSON.stringify(characters, null, 2));
          display(characters);
        }); // Img service 
      }); // IaF - characters
    }); // IMDB - quotes
  }); // IMDB - episode chars
}

function getEID(seasonNumber, episodeNumber) {
  return `${("0" + seasonNumber).slice(-2)}${("0" + episodeNumber).slice(-2)}`;
}

function getDataFile(seasonNumber, episodeNumber) {
  return `./data/s${("0" + seasonNumber).slice(-2)}e${("0" + episodeNumber).slice(-2)}.json`;
}

function showTimelineProgress(seasonNumber, episodeNumber) {
  $('.episode-step').removeClass('form-steps__item--active');
  Array.from(Array(seasonNumber-1).keys()).forEach((s) => {
    Array.from(Array(10).keys()).forEach((e) => {
      const eid = getEID(s+1, e+1);
      const stepEl = $(`#episode-step-${eid}`)
      if (stepEl) {
        stepEl.addClass('form-steps__item--active');
      }
    });
  });
  Array.from(Array(episodeNumber).keys()).forEach((e) => {
    const eid = getEID(seasonNumber, e+1);
    $(`#episode-step-${eid}`).addClass('form-steps__item--active');
  });
}

function showEpisodeInfo(episode) {
  //$('.episode-title').text(episode.title);
  $(".episode-title").fadeOut(function() {
    $(this).text(episode.title);
  }).fadeIn();
  $('.episode-order').text(`Season ${+episode.seasonNumber}, Episode ${+episode.episodeNumber}`);
  $('.episode-duration').text(`${episode.duration} minutes`);
  $('.episode-rating').text(episode.averageRating);
  $('.episode-votes').text(episode.numVotes);
}

function displayEpisodeTimeline(episodes) {
  episodes = episodes.sort((e1, e2) => {
    if (e1.seasonNumber === e2.seasonNumber) {
      return +e1.episodeNumber - +e2.episodeNumber;
    }
    return +e1.seasonNumber - +e2.seasonNumber;
  });

  $episodeTimeline = $("#episode-timeline");

  episodes.forEach((episode, i) => {
    const episodeNumber = +episode.episodeNumber;
    const seasonNumber = +episode.seasonNumber;
    let seasonText = '.';
    if (episodeNumber === 1) {
      seasonText = `S${+episode.seasonNumber}`;
    }
    $episodeStep = $(`
      <div id="episode-step-${episode.EID}" 
        class="episode-step form-steps__item"
        data-toggle="tooltip" 
        data-placement="top" 
        data-html="true"
        title="Season ${seasonNumber}, Episode ${episodeNumber}<br/><b>${episode.title}</b>"
      >
        <div class="form-steps__item-content">
          <span class="form-steps__item-icon">${episodeNumber}</span>
          <span class="form-steps__item-line"></span>
          <span class="form-steps__item-text">${seasonText}</span>
        </div>
      </div>`
    );
    if (i === 0) {
      $episodeStep.addClass('form-steps__item--active');
      $episodeStep.addClass('first-episode-step');
      $episodeStep.find('.form-steps__item-line').remove();
    }
    if (episodeNumber === 1) {
      $episodeStep.find('.form-steps__item-text').addClass('first-episode');
    }

    $episodeStep.click(event => {
      loadEpisode(seasonNumber, episodeNumber);
      showTimelineProgress(seasonNumber, episodeNumber);
      showEpisodeInfo(episode);
    });

    $episodeTimeline.append($episodeStep)
  });
}



$(document).ready(function () {

  $(".button").click(function (event) {
    event.preventDefault();
    $(this).toggleClass('active').siblings().removeClass('active');
    const buttonId = $(this).attr('id');
    fetch(`data/data-${buttonId}.json`)
      .then(res => res.json())
      .then(json => display(json));
  });

  fetch(`./data/episodes.json`)
    .then(res => res.json())
    .then(json => {
      allEpisodes = json;
      displayEpisodeTimeline(json);
      showEpisodeInfo(json[0]);
      $(function () {
        $('[data-toggle="tooltip"]').tooltip()
      })
    });

  loadEpisode(1, 1);
  setupButtons();

  /*fetch(`data/data-s01e01.json`)
    .then(res => res.json())
    .then(json => display(json));*/

});
