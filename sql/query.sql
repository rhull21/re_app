-- Active: 1661281381237@@127.0.0.1@3306@rivereyes

SELECT 
  a.rm
FROM 
    rivermile a
WHERE 
    a.rm BETWEEN 50 AND 65.3
ORDER BY
  a.rm
;

Select max(rm), min(rm) FROM rivermile;

SELECT a.*,b.datet 
FROM dryness a 
INNER JOIN observation b 
    ON a.id = b.id  
WHERE a.id=1292;

SELECT 
  a.rm, b.datet
FROM rivermile a
INNER JOIN 
  observation b
ON 
  a.rm = b.rm
ORDER BY 
  a.rm; 

SELECT 
  a.rm, Count(a.rm)
FROM rivermile a
INNER JOIN 
  observation b
ON 
  a.rm = b.rm
GROUP BY
  a.rm
ORDER BY 
  a.rm; 

SELECT 
  b.obstype, count(b.obstype) 
FROM rivermile a
LEFT JOIN 
  observation b
ON 
  a.rm = b.rm
GROUP BY
  b.obstype
ORDER BY
  a.rm
;

SELECT 
  a.rm, b.datet, b.obstype, c.extent
FROM (rivermile a
    INNER JOIN 
    observation b ON a.rm = b.rm) 
    INNER JOIN dryness c 
      ON b.id = c.id
ORDER BY
  b.datet
;

SELECT 
    a.id, a.dryid, b.dryid as dryidb
FROM
    dryness a
INNER JOIN dryness b ON 
    b.dryid = a.down_dryid
ORDER BY 
    a.id; 


SELECT d.id_up, d.id_down, c.datet as date_up, c.rm as rm_up
FROM observation c
INNER JOIN
    (SELECT 
        a.id as id_up, b.id as id_down
    FROM
        dryness a
    INNER JOIN dryness b ON 
        b.dryid = a.down_dryid
    ) d ON
    c.id = d.id_up
ORDER BY
    c.rm; 

SELECT 
    observation.rm as rm_up, 
    observation.id as id_up, 
    DATE(datet) as dat, 
    dryness.dryid as dryid_up, 
    dryness.down_dryid as dryid_down 
FROM observation 
INNER JOIN
    dryness ON
    observation.id = dryness.id
WHERE 
    dryness.down_dryid IS NOT NULL
ORDER BY
    observation.rm; 

SELECT 
    observation.rm as rm_down, 
    observation.id as id_down,  
    dryness.dryid as dryid_down 
FROM observation 
INNER JOIN
    dryness ON
    observation.id = dryness.id
WHERE 
    dryness.extent = 'Downstream'
ORDER BY
    observation.rm; 

SELECT a.id_up, b.id_down, a.rm_up, b.rm_down, a.dat
FROM (SELECT 
        observation.rm as rm_up, 
        observation.id as id_up, 
        DATE(datet) as dat, 
        dryness.dryid as dryid_up, 
        dryness.down_dryid as dryid_down 
    FROM observation 
    INNER JOIN
        dryness ON
        observation.id = dryness.id
    WHERE 
        dryness.down_dryid IS NOT NULL) a
INNER JOIN (SELECT 
    observation.rm as rm_down, 
    observation.id as id_down,  
    dryness.dryid as dryid_down 
FROM observation 
INNER JOIN
    dryness ON
    observation.id = dryness.id
WHERE 
    dryness.extent = 'Downstream') b 
ON a.dryid_down = b.dryid_down
ORDER BY a.dat, a.rm_up;

SELECT a.rm_up, (a.rm_up-b.rm_down) as dry_length, a.dat
FROM (SELECT 
        observation.rm as rm_up, 
        observation.id as id_up, 
        DATE(datet) as dat, 
        dryness.dryid as dryid_up, 
        dryness.down_dryid as dryid_down 
    FROM observation 
    INNER JOIN
        dryness ON
        observation.id = dryness.id
    WHERE 
        dryness.down_dryid IS NOT NULL) a
INNER JOIN (SELECT 
    observation.rm as rm_down, 
    observation.id as id_down,  
    dryness.dryid as dryid_down 
FROM observation 
INNER JOIN
    dryness ON
    observation.id = dryness.id
WHERE 
    dryness.extent = 'Downstream') b 
ON a.dryid_down = b.dryid_down
ORDER BY dry_length DESC LIMIT 10;

SELECT MONTH(thedate) as themonth, 
  MAX(acacia_sum_len) AS acacia_miles, 
  MAX(acacia_frac_len)*100 AS acacia_percent,
  MAX(isleta_sum_len) AS isleta_miles, 
  MAX(isleta_frac_len)*100 AS isleta_percent,
  MAX(combined_sum_len) AS combined_miles,
  MAX(combined_frac_len)*100 AS combined_percent
FROM all_len 
GROUP BY MONTH(thedate); 