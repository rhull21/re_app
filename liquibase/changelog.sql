-- liquibase formatted sql changeLogId:283c58d3-46e9-42ba-86ff-2427ec686e11

-- changeset liquibase:1
CREATE TABLE test_table (test_id INT, test_column VARCHAR(256), PRIMARY KEY (test_id))

-- changeset liquibase:2
DROP TABLE test_table

-- changeset liquibase:3
CREATE TABLE `discharge_ball_tape`  (
  `dbid` int NOT NULL AUTO_INCREMENT,
  `qid` int NOT NULL,
  `channel_width_ft` mediumint NULL DEFAULT NULL,
  `depth_measurement_1_ft` mediumint NULL DEFAULT NULL,
  `depth_measurement_2_ft` mediumint NULL DEFAULT NULL,
  `depth_measurement_3_ft` mediumint NULL DEFAULT NULL,
  `depth_measurement_4_ft` mediumint NULL DEFAULT NULL,
  `average_depth_ft` mediumint NULL DEFAULT NULL,
  `cross_section_area_sq_ft` mediumint NULL DEFAULT NULL,
  `seconds_to_travel_length_recorded_below_typically_20_ft` mediumint NULL DEFAULT NULL,
  `timed_length_ft_leave_at_20_unless_a_different_distance_was_used` mediumint NULL DEFAULT NULL,
  `correction_factor_coefficient_typically_leave_at_09` mediumint NULL DEFAULT NULL,
  PRIMARY KEY (`dbid`) USING BTREE,
  INDEX `qid`(`qid` ASC) USING BTREE,
  CONSTRAINT `discharge_ball_tape_ibfk_1` FOREIGN KEY (`qid`) REFERENCES `discharge_gsa` (`qid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

-- changeset liquibase:4
CREATE TABLE `discharge_visual`  (
  `dvid` int NOT NULL AUTO_INCREMENT,
  `qid` int NOT NULL,
  `minimum_estimated_discharge_cfs` mediumint NULL DEFAULT NULL,
  `maximum_estimated_discharge_cfs` mediumint NULL DEFAULT NULL,
  PRIMARY KEY (`dvid`) USING BTREE,
  INDEX `qid`(`qid` ASC) USING BTREE,
  CONSTRAINT `discharge_visual_ibfk_1` FOREIGN KEY (`qid`) REFERENCES `discharge_gsa` (`qid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

-- changeset liquibase:5
CREATE TABLE `subreach`  (
  `sid` int NOT NULL AUTO_INCREMENT,
  `subreach` enum('') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `upstream_rm` decimal(5, 2) NULL DEFAULT NULL,
  `downstream_rm` decimal(5, 2) NULL DEFAULT NULL,
  PRIMARY KEY (`sid`) USING BTREE,
  INDEX `upstream_rm`(`upstream_rm` ASC) USING BTREE,
  CONSTRAINT `subreach_ibfk_1` FOREIGN KEY (`upstream_rm`) REFERENCES `rivermile` (`rm`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

-- changeset liquibase:6
CREATE TABLE `observer` (
  `oid` int NOT NULL AUTO_INCREMENT,
  `observer_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`oid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- changeset liquibase:7
ALTER TABLE `observation` 
	ADD COLUMN `oid` INT AFTER `rm`;
  
-- changeset liquibase:8
ALTER TABLE `remnant`
	ADD COLUMN `approximate_length_ft` INT AFTER `id`, 
	ADD COLUMN `approximate_width_ft` INT AFTER `id`;

-- changeset liquibase:9
ALTER TABLE `observation` 
	DROP COLUMN `oid`;

-- changeset liquibase:10
CREATE TABLE `observation_observer`  (
  `ooid` int NOT NULL AUTO_INCREMENT,
  `id` int NOT NULL,
  `oid` int NOT NULL,
  PRIMARY KEY (`ooid`) USING BTREE,
  INDEX `id`(`id` ASC) USING BTREE,
  CONSTRAINT `observation_observer_ibfk_1` FOREIGN KEY (`id`) REFERENCES `observation` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

-- changeset liquibase:11
ALTER TABLE `observation_observer` 
	ADD CONSTRAINT `oid_ibfk_1` FOREIGN KEY (`oid`) REFERENCES `observer` (`oid`);

 -- changeset liquibase:12
 ALTER TABLE `feature` 
	DROP COLUMN featype; 

-- changeset liquibase:13
CREATE TABLE `usgs_gages` (
  `usgs_id` int NOT NULL AUTO_INCREMENT,
  `fid` int NOT NULL,
  `usgs_station_name` varchar(8) NOT NULL,
  `usgs_feature_short_name` varchar(150), 
  PRIMARY KEY (`usgs_id`) USING BTREE,
  CONSTRAINT `feature_id_ibfk_1` FOREIGN KEY (`fid`) REFERENCES `feature` (`fid`));

-- changeset liquibase:14
INSERT INTO `usgs_gages`
  (`fid`, `usgs_station_name`, `usgs_feature_short_name`)
    VALUES
(89, '08358400', 'FLOODWAY AT SAN MARCIAL'),
(83, '08331160', 'NEAR BOSQUE FARMS'),
(84, '08331510', 'AT STATE HWY 346 NEAR BOSQUE'),
(85, '08332010', 'FLOODWAY NEAR BERNARDO'),
(86, '08354900', 'FLOODWAY AT SAN ACACIA'),
(87, '08355050', 'AT BRIDGE NEAR ESCONDIDA'),
(88, '08355490', 'ABOVE US HWY 380 NR SAN ANTONIO');


-- changeset liquibase:15 
ALTER TABLE `usgs`
  ADD COLUMN `uoid` int NOT NULL AUTO_INCREMENT FIRST,
  DROP CONSTRAINT  `rm`,
  DROP COLUMN `rm`,
  DROP PRIMARY KEY,
  ADD PRIMARY KEY (`uoid`) USING BTREE, 
  ADD CONSTRAINT `usgs_id_ibfk_1` FOREIGN KEY (`usgs_id`) REFERENCES `usgs_gages` (`usgs_id`) ON DELETE CASCADE ON UPDATE CASCADE;

-- changeset liquibase:16
ALTER TABLE `usgs` 
	RENAME TO `usgs_data`;

-- changeset liquibase:18
CREATE VIEW `flat_table` AS 
SELECT
	*
FROM
	observation
	LEFT JOIN 
	(Select id, IF(COUNT(b.observer_name)>1, CONCAT(MAX(b.observer_name), " | ", MIN(b.observer_name)), b.observer_name) AS observer_name_joined, IF(COUNT(a.oid)>1, 		CONCAT(MAX(a.oid), " | ", MIN(a.oid)), a.oid) AS oid_joined FROM observation_observer a LEFT JOIN observer b using(oid) GROUP BY a.id) c
		using(id)
	LEFT JOIN
	remnant
		using(id)
	LEFT JOIN
	discharge_gsa
		using(id)
	LEFT JOIN
	discharge_visual
		using(qid)
	LEFT JOIN
	discharge_ball_tape
		using(qid)
	LEFT JOIN
	photos
		using(id)
	LEFT JOIN
	dryness
		using(id)
	LEFT JOIN
	rivermile
		using(rm)
	GROUP BY 
		observation.id  

-- above changes migrated into Django Applciation Model.py 11022022