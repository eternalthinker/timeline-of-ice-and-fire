select c.CID, name, actor, season_of_death, episode_of_death, means_of_death, episodeCount,
	CASE WHEN 
		cast(season_of_death as integer) == 5 and cast(episode_of_death as integer) == 1 
	THEN cast(0 as bit) ELSE cast(1 as bit) END as isAlive
from characters as c, episodes as e, episode_characters as ec,
	(select c1.CID, count(*) as episodeCount 
	 from episodes as e1, characters as c1, episode_characters as ec1
	 where 
		((cast(e1.seasonNumber as integer) < 5) or 
		 (cast(e1.seasonNumber as integer) == 5 and cast(e1.episodeNumber as integer) <= 1)) and 
		e1.EID == ec1.EID and
		c1.CID == ec1.CID
		group by c1.CID
	) as eCounts
where 
	seasonNumber='03' and 
	episodeNumber='04' and
	e.EID == ec.EID and
	c.CID == ec.CID and
	c.CID == eCounts.CID
;