-- Active: 1661281381237@@127.0.0.1@3306@rivereyes

CREATE OR REPLACE VIEW rivereyes.dry_length AS
SELECT a.rm_up, b.rm_down, (a.rm_up-b.rm_down) as dry_length, a.dat
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
ORDER BY dat ASC;

CREATE OR REPLACE VIEW rivereyes.isleta_len AS
SELECT dat, SUM(dry_length) AS sum_len, 
  ROUND(SUM(dry_length)/(SELECT reachcalc('Isleta')),2) AS frac_len
FROM dry_length
WHERE 
(rm_up > (SELECT downreachcalc('Isleta')) 
AND rm_up < (SELECT upreachcalc('Isleta')))
GROUP BY dat
ORDER BY dat ASC; 

CREATE OR REPLACE VIEW rivereyes.acacia_len AS
SELECT dat, SUM(dry_length) AS sum_len, 
  ROUND(SUM(dry_length)/(SELECT reachcalc('San Acacia')),2) AS frac_len
FROM dry_length
WHERE 
(rm_up > (SELECT downreachcalc('San Acacia')) 
AND rm_up < (SELECT upreachcalc('San Acacia')))
GROUP BY dat
ORDER BY dat ASC; 

CREATE OR REPLACE VIEW rivereyes.all_len AS
SELECT DATE(a.datet) AS thedate, 
  b.sum_len AS isleta_sum_len, b.frac_len AS isleta_frac_len, 
  c.sum_len AS acacia_sum_len, c.frac_len AS acacia_frac_len, 
  (b.sum_len + c.sum_len) AS combined_sum_len,
  ROUND((b.sum_len + c.sum_len)/((SELECT reachcalc('San Acacia')) + 
                                    (SELECT reachcalc('Isleta'))),2) AS combined_frac_len
FROM (observation a 
  LEFT JOIN isleta_len b 
    ON DATE(a.datet) = b.dat)
  LEFT JOIN acacia_len c 
    ON c.dat = DATE(a.datet)
GROUP BY DATE(a.datet)
ORDER BY DATE(a.datet);

CREATE OR REPLACE VIEW rivereyes.feature_rm AS
SELECT
	round(floor(rivermile.rm* 2  + 0.5) / 2,1) AS `rm-rounded`, MIN(feature.feature) AS `feature`
FROM
	feature
	RIGHT JOIN
	rivermile
	ON 
		feature.rm = rivermile.rm
WHERE (rivermile.rm > 53.5 AND rivermile.rm < 164)
GROUP BY
	floor(rivermile.rm* 2  + 0.5) / 2

