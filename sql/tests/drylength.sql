-- Active: 1661281381237@@127.0.0.1@3306@rivereyes

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