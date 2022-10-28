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