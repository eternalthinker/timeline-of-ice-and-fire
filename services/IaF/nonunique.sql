SELECT *
FROM characters c
JOIN
(
    SELECT slug
    FROM characters
    GROUP BY slug
    HAVING COUNT(*) > 1
) c2
ON c2.slug = c.slug