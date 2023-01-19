CREATE DATABASE IF NOT EXISTS `rivereyes`;
USE `rivereyes`;

/*
 Navicat MySQL Data Transfer

 Source Server         : root_dir
 Source Server Type    : MySQL
 Source Server Version : 80031 (8.0.31)
 Source Host           : localhost:3306
 Source Schema         : rivereyes

 Target Server Type    : MySQL
 Target Server Version : 80031 (8.0.31)
 File Encoding         : 65001

 Date: 18/01/2023 16:00:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id` ASC, `codename` ASC) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 89 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id` ASC, `group_id` ASC) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id` ASC) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for databasechangelog
-- ----------------------------
DROP TABLE IF EXISTS `databasechangelog`;
CREATE TABLE `databasechangelog`  (
  `ID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `AUTHOR` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `FILENAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DATEEXECUTED` datetime NOT NULL,
  `ORDEREXECUTED` int NOT NULL,
  `EXECTYPE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `MD5SUM` varchar(35) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `DESCRIPTION` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `COMMENTS` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `TAG` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `LIQUIBASE` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `CONTEXTS` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `LABELS` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `DEPLOYMENT_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for databasechangeloglock
-- ----------------------------
DROP TABLE IF EXISTS `databasechangeloglock`;
CREATE TABLE `databasechangeloglock`  (
  `ID` int NOT NULL,
  `LOCKED` bit(1) NOT NULL,
  `LOCKGRANTED` datetime NULL DEFAULT NULL,
  `LOCKEDBY` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for discharge_ball_tape
-- ----------------------------
DROP TABLE IF EXISTS `discharge_ball_tape`;
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
) ENGINE = InnoDB AUTO_INCREMENT = 49 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for discharge_gsa
-- ----------------------------
DROP TABLE IF EXISTS `discharge_gsa`;
CREATE TABLE `discharge_gsa`  (
  `qid` int NOT NULL AUTO_INCREMENT,
  `id` int NOT NULL,
  `discharge_cfs` mediumint NULL DEFAULT NULL,
  PRIMARY KEY (`qid`) USING BTREE,
  INDEX `id`(`id` ASC) USING BTREE,
  CONSTRAINT `discharge_gsa_ibfk_1` FOREIGN KEY (`id`) REFERENCES `observation` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 76 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for discharge_visual
-- ----------------------------
DROP TABLE IF EXISTS `discharge_visual`;
CREATE TABLE `discharge_visual`  (
  `dvid` int NOT NULL AUTO_INCREMENT,
  `qid` int NOT NULL,
  `minimum_estimated_discharge_cfs` mediumint NULL DEFAULT NULL,
  `maximum_estimated_discharge_cfs` mediumint NULL DEFAULT NULL,
  PRIMARY KEY (`dvid`) USING BTREE,
  INDEX `qid`(`qid` ASC) USING BTREE,
  CONSTRAINT `discharge_visual_ibfk_1` FOREIGN KEY (`qid`) REFERENCES `discharge_gsa` (`qid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 249 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content_type_id` int NULL DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id` ASC) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_chk_1` CHECK (`action_flag` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label` ASC, `model` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 23 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for django_plotly_dash_dashapp
-- ----------------------------
DROP TABLE IF EXISTS `django_plotly_dash_dashapp`;
CREATE TABLE `django_plotly_dash_dashapp`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `instance_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `slug` varchar(110) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `base_state` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `creation` datetime(6) NOT NULL,
  `update` datetime(6) NOT NULL,
  `save_on_change` tinyint(1) NOT NULL,
  `stateless_app_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `instance_name`(`instance_name` ASC) USING BTREE,
  UNIQUE INDEX `slug`(`slug` ASC) USING BTREE,
  INDEX `django_plotly_dash_d_stateless_app_id_220444de_fk_django_pl`(`stateless_app_id` ASC) USING BTREE,
  CONSTRAINT `django_plotly_dash_d_stateless_app_id_220444de_fk_django_pl` FOREIGN KEY (`stateless_app_id`) REFERENCES `django_plotly_dash_statelessapp` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for django_plotly_dash_statelessapp
-- ----------------------------
DROP TABLE IF EXISTS `django_plotly_dash_statelessapp`;
CREATE TABLE `django_plotly_dash_statelessapp`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `slug` varchar(110) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `app_name`(`app_name` ASC) USING BTREE,
  UNIQUE INDEX `slug`(`slug` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for dryness
-- ----------------------------
DROP TABLE IF EXISTS `dryness`;
CREATE TABLE `dryness`  (
  `dryid` int NOT NULL,
  `id` int NOT NULL,
  `extent` enum('Upstream','Downstream') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `down_dryid` int NULL DEFAULT NULL,
  PRIMARY KEY (`dryid`) USING BTREE,
  INDEX `par_ind`(`dryid` ASC) USING BTREE,
  INDEX `id`(`id` ASC) USING BTREE,
  CONSTRAINT `dryness_ibfk_1` FOREIGN KEY (`id`) REFERENCES `observation` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for feature
-- ----------------------------
DROP TABLE IF EXISTS `feature`;
CREATE TABLE `feature`  (
  `fid` int NOT NULL AUTO_INCREMENT,
  `feature` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `rm` decimal(5, 2) NULL DEFAULT NULL,
  PRIMARY KEY (`fid`) USING BTREE,
  INDEX `par_ind`(`rm` ASC) USING BTREE,
  CONSTRAINT `feature_ibfk_1` FOREIGN KEY (`rm`) REFERENCES `rivermile` (`rm`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 90 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for observation
-- ----------------------------
DROP TABLE IF EXISTS `observation`;
CREATE TABLE `observation`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `fulcrum_id` varchar(38) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `rm` decimal(5, 2) NULL DEFAULT NULL,
  `obstype` enum('General','Measured Flow Estimate (Ball and Tape)','GPS Extent of Drying','Remnant Pool','Visual Flow Estimate','Metered Flow') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `datet` datetime NULL DEFAULT NULL,
  `note` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `par_ind`(`rm` ASC) USING BTREE,
  CONSTRAINT `observation_ibfk_1` FOREIGN KEY (`rm`) REFERENCES `rivermile` (`rm`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 6152 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for observation_observer
-- ----------------------------
DROP TABLE IF EXISTS `observation_observer`;
CREATE TABLE `observation_observer`  (
  `ooid` int NOT NULL AUTO_INCREMENT,
  `id` int NOT NULL,
  `oid` int NOT NULL,
  PRIMARY KEY (`ooid`) USING BTREE,
  INDEX `id`(`id` ASC) USING BTREE,
  INDEX `oid_ibfk_1`(`oid` ASC) USING BTREE,
  CONSTRAINT `observation_observer_ibfk_1` FOREIGN KEY (`id`) REFERENCES `observation` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `oid_ibfk_1` FOREIGN KEY (`oid`) REFERENCES `observer` (`oid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6277 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for observer
-- ----------------------------
DROP TABLE IF EXISTS `observer`;
CREATE TABLE `observer`  (
  `oid` int NOT NULL AUTO_INCREMENT,
  `observer_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`oid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for photos
-- ----------------------------
DROP TABLE IF EXISTS `photos`;
CREATE TABLE `photos`  (
  `pid` int NOT NULL AUTO_INCREMENT,
  `id` int NOT NULL,
  `photos_gen_url` varchar(2083) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`pid`) USING BTREE,
  INDEX `id`(`id` ASC) USING BTREE,
  CONSTRAINT `photos_ibfk_1` FOREIGN KEY (`id`) REFERENCES `observation` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 1392 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for reach
-- ----------------------------
DROP TABLE IF EXISTS `reach`;
CREATE TABLE `reach`  (
  `reaid` int NOT NULL AUTO_INCREMENT,
  `reach` enum('Angostura','Isleta','San Acacia') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `upstream_rm` decimal(5, 2) NULL DEFAULT NULL,
  `downstream_rm` decimal(5, 2) NULL DEFAULT NULL,
  PRIMARY KEY (`reaid`) USING BTREE,
  INDEX `upstream_rm`(`upstream_rm` ASC) USING BTREE,
  CONSTRAINT `reach_ibfk_1` FOREIGN KEY (`upstream_rm`) REFERENCES `rivermile` (`rm`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for remnant
-- ----------------------------
DROP TABLE IF EXISTS `remnant`;
CREATE TABLE `remnant`  (
  `remid` int NOT NULL AUTO_INCREMENT,
  `id` int NOT NULL,
  `approximate_width_ft` int NULL DEFAULT NULL,
  `approximate_length_ft` int NULL DEFAULT NULL,
  `approximate_area_sq_feet` int NULL DEFAULT NULL,
  PRIMARY KEY (`remid`) USING BTREE,
  INDEX `id`(`id` ASC) USING BTREE,
  CONSTRAINT `remnant_ibfk_1` FOREIGN KEY (`id`) REFERENCES `observation` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 108 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for rivermile
-- ----------------------------
DROP TABLE IF EXISTS `rivermile`;
CREATE TABLE `rivermile`  (
  `rm` decimal(5, 2) NOT NULL,
  `position` point NOT NULL,
  `latlong` point NULL,
  PRIMARY KEY (`rm`) USING BTREE,
  UNIQUE INDEX `rm`(`rm` ASC) USING BTREE,
  SPATIAL INDEX `position`(`position`)
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for subreach
-- ----------------------------
DROP TABLE IF EXISTS `subreach`;
CREATE TABLE `subreach`  (
  `sid` int NOT NULL AUTO_INCREMENT,
  `subreach` enum('') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `upstream_rm` decimal(5, 2) NULL DEFAULT NULL,
  `downstream_rm` decimal(5, 2) NULL DEFAULT NULL,
  PRIMARY KEY (`sid`) USING BTREE,
  INDEX `upstream_rm`(`upstream_rm` ASC) USING BTREE,
  CONSTRAINT `subreach_ibfk_1` FOREIGN KEY (`upstream_rm`) REFERENCES `rivermile` (`rm`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for usgs_data
-- ----------------------------
DROP TABLE IF EXISTS `usgs_data`;
CREATE TABLE `usgs_data`  (
  `uoid` int NOT NULL AUTO_INCREMENT,
  `usgs_id` int NOT NULL,
  `date` datetime NULL DEFAULT NULL,
  `flow_cfs` float NULL DEFAULT NULL,
  `prov_flag` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`uoid`) USING BTREE,
  INDEX `usgs_id_ibfk_1`(`usgs_id` ASC) USING BTREE,
  CONSTRAINT `usgs_id_ibfk_1` FOREIGN KEY (`usgs_id`) REFERENCES `usgs_gages` (`usgs_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 47457 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for usgs_gages
-- ----------------------------
DROP TABLE IF EXISTS `usgs_gages`;
CREATE TABLE `usgs_gages`  (
  `usgs_id` int NOT NULL AUTO_INCREMENT,
  `fid` int NOT NULL,
  `usgs_station_name` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `usgs_feature_short_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`usgs_id`) USING BTREE,
  INDEX `feature_id_ibfk_1`(`fid` ASC) USING BTREE,
  CONSTRAINT `feature_id_ibfk_1` FOREIGN KEY (`fid`) REFERENCES `feature` (`fid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Function structure for downreachcalc
-- ----------------------------
DROP FUNCTION IF EXISTS `downreachcalc`;
delimiter ;;
CREATE FUNCTION `downreachcalc`(reachnm TEXT)
 RETURNS decimal(5,2)
  DETERMINISTIC
return (SELECT downstream_rm FROM reach WHERE reach=reachnm)
;;
delimiter ;

-- ----------------------------
-- Function structure for hello
-- ----------------------------
DROP FUNCTION IF EXISTS `hello`;
delimiter ;;
CREATE FUNCTION `hello`(s CHAR(20))
 RETURNS char(50) CHARSET utf8mb4
  DETERMINISTIC
RETURN CONCAT('Hello, ', s)
;;
delimiter ;

-- ----------------------------
-- Function structure for maxrmdrycalc
-- ----------------------------
DROP FUNCTION IF EXISTS `maxrmdrycalc`;
delimiter ;;
CREATE FUNCTION `maxrmdrycalc`()
 RETURNS decimal(5,2)
  DETERMINISTIC
return (SELECT MAX(rm) from observation where obstype='GPS Extent of Drying')
;;
delimiter ;

-- ----------------------------
-- Function structure for minrmdrycalc
-- ----------------------------
DROP FUNCTION IF EXISTS `minrmdrycalc`;
delimiter ;;
CREATE FUNCTION `minrmdrycalc`()
 RETURNS decimal(5,2)
  DETERMINISTIC
return (SELECT MIN(rm) from observation where obstype='GPS Extent of Drying')
;;
delimiter ;

-- ----------------------------
-- Procedure structure for proc_delta_dry
-- ----------------------------
DROP PROCEDURE IF EXISTS `proc_delta_dry`;
delimiter ;;
CREATE PROCEDURE `proc_delta_dry`(grp_type CHAR(20))
BEGIN
	# read in grouping type (Month, Year, None) to generate a query that calculates the change between previous time steps
	
	SET @win_vals = 'max(`sum_len` ) AS `len`, (max(`sum_len` ) - lag(max(`sum_len` )) OVER `w`) AS `diff`, ';

	SET @win  = 'WINDOW `w` AS ( ORDER BY `dat` )';
 
	IF grp_type = 'MONTH' THEN
		SET @grp_vals = ' YEAR(`dat`) , MONTH(`dat`) ';
	ELSEIF grp_type = 'YEAR' THEN
		SET @grp_vals = ' YEAR(`dat`) ';
	ELSE
		SET @grp_vals = ' `dat` ';
	END IF;

	SET @s = CONCAT('SELECT ', @win_vals, ' \'acacia\' AS `domain`, ', @grp_vals, 'FROM `acacia_len` ', 'GROUP BY ', @grp_vals, @win, ' UNION ALL '
									'SELECT ', @win_vals, ' \'isleta\' AS `domain`, ', @grp_vals, 'FROM `isleta_len` ', 'GROUP BY ', @grp_vals, @win);
	
-- 	SELECT @s AS ''; 
	PREPARE stmt FROM @s;
  EXECUTE stmt;
  DEALLOCATE PREPARE stmt;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for reachcalc
-- ----------------------------
DROP FUNCTION IF EXISTS `reachcalc`;
delimiter ;;
CREATE FUNCTION `reachcalc`(reachnm TEXT)
 RETURNS decimal(5,2)
  DETERMINISTIC
return (SELECT (upstream_rm-downstream_rm) FROM reach WHERE reach=reachnm)
;;
delimiter ;

-- ----------------------------
-- Function structure for upreachcalc
-- ----------------------------
DROP FUNCTION IF EXISTS `upreachcalc`;
delimiter ;;
CREATE FUNCTION `upreachcalc`(reachnm TEXT)
 RETURNS decimal(5,2)
  DETERMINISTIC
return (SELECT upstream_rm FROM reach WHERE reach=reachnm)
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;


-- ----------------------------
-- View structure for dry_length
-- ----------------------------
DROP VIEW IF EXISTS `dry_length`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `dry_length` AS select `a`.`rm_up` AS `rm_up`,`b`.`rm_down` AS `rm_down`,(`a`.`rm_up` - `b`.`rm_down`) AS `dry_length`,`a`.`dat` AS `dat` from ((select `observation`.`rm` AS `rm_up`,`observation`.`id` AS `id_up`,cast(`observation`.`datet` as date) AS `dat`,`dryness`.`dryid` AS `dryid_up`,`dryness`.`down_dryid` AS `dryid_down` from (`observation` join `dryness` on((`observation`.`id` = `dryness`.`id`))) where (`dryness`.`down_dryid` is not null)) `a` join (select `observation`.`rm` AS `rm_down`,`observation`.`id` AS `id_down`,`dryness`.`dryid` AS `dryid_down` from (`observation` join `dryness` on((`observation`.`id` = `dryness`.`id`))) where (`dryness`.`extent` = 'Downstream')) `b` on((`a`.`dryid_down` = `b`.`dryid_down`))) order by `a`.`dat`;

-- ----------------------------
-- View structure for acacia_len
-- ----------------------------
DROP VIEW IF EXISTS `acacia_len`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `acacia_len` AS select `dry_length`.`dat` AS `dat`,sum(`dry_length`.`dry_length`) AS `sum_len`,round((sum(`dry_length`.`dry_length`) / (select `reachcalc`('San Acacia'))),2) AS `frac_len` from `dry_length` where ((`dry_length`.`rm_up` > (select `downreachcalc`('San Acacia'))) and (`dry_length`.`rm_up` < (select `upreachcalc`('San Acacia')))) group by `dry_length`.`dat` order by `dry_length`.`dat`;

-- ----------------------------
-- View structure for isleta_len
-- ----------------------------
DROP VIEW IF EXISTS `isleta_len`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `isleta_len` AS select `dry_length`.`dat` AS `dat`,sum(`dry_length`.`dry_length`) AS `sum_len`,round((sum(`dry_length`.`dry_length`) / (select `reachcalc`('Isleta'))),2) AS `frac_len` from `dry_length` where ((`dry_length`.`rm_up` > (select `downreachcalc`('Isleta'))) and (`dry_length`.`rm_up` < (select `upreachcalc`('Isleta')))) group by `dry_length`.`dat` order by `dry_length`.`dat`;


-- ----------------------------
-- View structure for all_len
-- ----------------------------
DROP VIEW IF EXISTS `all_len`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `all_len` AS select cast(`a`.`datet` as date) AS `thedate`,`b`.`sum_len` AS `isleta_sum_len`,`b`.`frac_len` AS `isleta_frac_len`,`c`.`sum_len` AS `acacia_sum_len`,`c`.`frac_len` AS `acacia_frac_len`,(`b`.`sum_len` + `c`.`sum_len`) AS `combined_sum_len`,round(((`b`.`sum_len` + `c`.`sum_len`) / ((select `reachcalc`('San Acacia')) + (select `reachcalc`('Isleta')))),2) AS `combined_frac_len` from ((`observation` `a` left join `isleta_len` `b` on((cast(`a`.`datet` as date) = `b`.`dat`))) left join `acacia_len` `c` on((`c`.`dat` = cast(`a`.`datet` as date)))) group by cast(`a`.`datet` as date) order by cast(`a`.`datet` as date);

-- ----------------------------
-- View structure for dry_length_agg
-- ----------------------------
DROP VIEW IF EXISTS `dry_length_agg`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `dry_length_agg` AS select `dry_length`.`rm_up` AS `rm_up`,`dry_length`.`rm_down` AS `rm_down`,`dry_length`.`dry_length` AS `dry_length`,`dry_length`.`dat` AS `dat`,round((floor(((`dry_length`.`rm_down` * 2) + 0.5)) / 2),1) AS `rm_down_rd`,round((floor(((`dry_length`.`rm_up` * 2) + 0.5)) / 2),1) AS `rm_up_rd` from `dry_length`;

-- ----------------------------
-- View structure for feature_rm
-- ----------------------------
DROP VIEW IF EXISTS `feature_rm`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `feature_rm` AS select round((floor(((`rivermile`.`rm` * 2) + 0.5)) / 2),1) AS `rm_rounded`,min(`feature`.`feature`) AS `feature`,st_x(`rivermile`.`latlong`) AS `latitude_rounded`,st_y(`rivermile`.`latlong`) AS `longitude_rounded`,`rivermile`.`latlong` AS `latlong` from (`rivermile` left join `feature` on((`feature`.`rm` = `rivermile`.`rm`))) where ((`rivermile`.`rm` > (select `minrmdrycalc`())) and (`rivermile`.`rm` < (select `maxrmdrycalc`()))) group by (floor(((`rivermile`.`rm` * 2) + 0.5)) / 2);

-- ----------------------------
-- View structure for flat_table
-- ----------------------------
DROP VIEW IF EXISTS `flat_table`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `flat_table` AS select `observation`.`rm` AS `rm`,`observation`.`id` AS `id`,`discharge_gsa`.`qid` AS `qid`,`observation`.`fulcrum_id` AS `fulcrum_id`,`observation`.`obstype` AS `obstype`,`observation`.`datet` AS `datet`,`observation`.`note` AS `note`,`c`.`observer_name_joined` AS `observer_name_joined`,`c`.`oid_joined` AS `oid_joined`,`remnant`.`remid` AS `remid`,`remnant`.`approximate_width_ft` AS `approximate_width_ft`,`remnant`.`approximate_length_ft` AS `approximate_length_ft`,`remnant`.`approximate_area_sq_feet` AS `approximate_area_sq_feet`,`discharge_gsa`.`discharge_cfs` AS `discharge_cfs`,`discharge_visual`.`dvid` AS `dvid`,`discharge_visual`.`minimum_estimated_discharge_cfs` AS `minimum_estimated_discharge_cfs`,`discharge_visual`.`maximum_estimated_discharge_cfs` AS `maximum_estimated_discharge_cfs`,`discharge_ball_tape`.`dbid` AS `dbid`,`discharge_ball_tape`.`channel_width_ft` AS `channel_width_ft`,`discharge_ball_tape`.`depth_measurement_1_ft` AS `depth_measurement_1_ft`,`discharge_ball_tape`.`depth_measurement_2_ft` AS `depth_measurement_2_ft`,`discharge_ball_tape`.`depth_measurement_3_ft` AS `depth_measurement_3_ft`,`discharge_ball_tape`.`depth_measurement_4_ft` AS `depth_measurement_4_ft`,`discharge_ball_tape`.`average_depth_ft` AS `average_depth_ft`,`discharge_ball_tape`.`cross_section_area_sq_ft` AS `cross_section_area_sq_ft`,`discharge_ball_tape`.`seconds_to_travel_length_recorded_below_typically_20_ft` AS `seconds_to_travel_length_recorded_below_typically_20_ft`,`discharge_ball_tape`.`timed_length_ft_leave_at_20_unless_a_different_distance_was_used` AS `timed_length_ft_leave_at_20_unless_a_different_distance_was_used`,`discharge_ball_tape`.`correction_factor_coefficient_typically_leave_at_09` AS `correction_factor_coefficient_typically_leave_at_09`,`photos`.`pid` AS `pid`,`photos`.`photos_gen_url` AS `photos_gen_url`,`dryness`.`dryid` AS `dryid`,`dryness`.`extent` AS `extent`,`dryness`.`down_dryid` AS `down_dryid`,`rivermile`.`position` AS `position`,`rivermile`.`latlong` AS `latlong` from ((((((((`observation` left join (select `a`.`id` AS `id`,if((count(`b`.`observer_name`) > 1),concat(max(`b`.`observer_name`),' | ',min(`b`.`observer_name`)),`b`.`observer_name`) AS `observer_name_joined`,if((count(`a`.`oid`) > 1),concat(max(`a`.`oid`),' | ',min(`a`.`oid`)),`a`.`oid`) AS `oid_joined` from (`observation_observer` `a` left join `observer` `b` on((`a`.`oid` = `b`.`oid`))) group by `a`.`id`) `c` on((`observation`.`id` = `c`.`id`))) left join `remnant` on((`observation`.`id` = `remnant`.`id`))) left join `discharge_gsa` on((`observation`.`id` = `discharge_gsa`.`id`))) left join `discharge_visual` on((`discharge_gsa`.`qid` = `discharge_visual`.`qid`))) left join `discharge_ball_tape` on((`discharge_gsa`.`qid` = `discharge_ball_tape`.`qid`))) left join `photos` on((`observation`.`id` = `photos`.`id`))) left join `dryness` on((`observation`.`id` = `dryness`.`id`))) left join `rivermile` on((`observation`.`rm` = `rivermile`.`rm`))) group by `observation`.`id`;


-- ----------------------------
-- View structure for usgs_feature_data
-- ----------------------------
DROP VIEW IF EXISTS `usgs_feature_data`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `usgs_feature_data` AS select `usgs_data`.`uoid` AS `uoid`,`feature`.`rm` AS `rm`,`usgs_gages`.`usgs_feature_short_name` AS `usgs_feature_short_name`,`usgs_gages`.`usgs_station_name` AS `usgs_station_name`,`usgs_data`.`date` AS `date`,`usgs_data`.`flow_cfs` AS `flow_cfs` from ((`usgs_data` join `usgs_gages` on((`usgs_data`.`usgs_id` = `usgs_gages`.`usgs_id`))) join `feature` on((`usgs_gages`.`fid` = `feature`.`fid`))) where (`usgs_data`.`prov_flag` = 'A');
