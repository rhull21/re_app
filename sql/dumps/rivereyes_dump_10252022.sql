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

 Date: 25/10/2022 09:20:07
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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB AUTO_INCREMENT = 81 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB AUTO_INCREMENT = 76 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for feature
-- ----------------------------
DROP TABLE IF EXISTS `feature`;
CREATE TABLE `feature`  (
  `fid` int NOT NULL AUTO_INCREMENT,
  `feature` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `rm` decimal(5, 2) NULL DEFAULT NULL,
  `featype` enum('Gage') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`fid`) USING BTREE,
  INDEX `par_ind`(`rm` ASC) USING BTREE,
  CONSTRAINT `feature_ibfk_1` FOREIGN KEY (`rm`) REFERENCES `rivermile` (`rm`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 90 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB AUTO_INCREMENT = 1414 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB AUTO_INCREMENT = 1392 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for remnant
-- ----------------------------
DROP TABLE IF EXISTS `remnant`;
CREATE TABLE `remnant`  (
  `remid` int NOT NULL AUTO_INCREMENT,
  `id` int NOT NULL,
  `approximate_area_sq_feet` int NULL DEFAULT NULL,
  PRIMARY KEY (`remid`) USING BTREE,
  INDEX `id`(`id` ASC) USING BTREE,
  CONSTRAINT `remnant_ibfk_1` FOREIGN KEY (`id`) REFERENCES `observation` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 108 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for usgs
-- ----------------------------
DROP TABLE IF EXISTS `usgs`;
CREATE TABLE `usgs`  (
  `usgs_id` int NOT NULL,
  `date` datetime NOT NULL,
  `flow_cfs` float NULL DEFAULT NULL,
  `prov_flag` tinyint(1) NULL DEFAULT NULL,
  `rm` decimal(10, 2) NOT NULL,
  PRIMARY KEY (`date`) USING BTREE,
  INDEX `rm`(`rm` ASC) USING BTREE,
  CONSTRAINT `rm` FOREIGN KEY (`rm`) REFERENCES `rivermile` (`rm`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- View structure for acacia_len
-- ----------------------------
DROP VIEW IF EXISTS `acacia_len`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `acacia_len` AS select `dry_length`.`dat` AS `dat`,sum(`dry_length`.`dry_length`) AS `sum_len`,round((sum(`dry_length`.`dry_length`) / (select `reachcalc`('San Acacia'))),2) AS `frac_len` from `dry_length` where ((`dry_length`.`rm_up` > (select `downreachcalc`('San Acacia'))) and (`dry_length`.`rm_up` < (select `upreachcalc`('San Acacia')))) group by `dry_length`.`dat` order by `dry_length`.`dat`;

-- ----------------------------
-- View structure for all_len
-- ----------------------------
DROP VIEW IF EXISTS `all_len`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `all_len` AS select cast(`a`.`datet` as date) AS `thedate`,`b`.`sum_len` AS `isleta_sum_len`,`b`.`frac_len` AS `isleta_frac_len`,`c`.`sum_len` AS `acacia_sum_len`,`c`.`frac_len` AS `acacia_frac_len`,(`b`.`sum_len` + `c`.`sum_len`) AS `combined_sum_len`,round(((`b`.`sum_len` + `c`.`sum_len`) / ((select `reachcalc`('San Acacia')) + (select `reachcalc`('Isleta')))),2) AS `combined_frac_len` from ((`observation` `a` left join `isleta_len` `b` on((cast(`a`.`datet` as date) = `b`.`dat`))) left join `acacia_len` `c` on((`c`.`dat` = cast(`a`.`datet` as date)))) group by cast(`a`.`datet` as date) order by cast(`a`.`datet` as date);

-- ----------------------------
-- View structure for dry_length
-- ----------------------------
DROP VIEW IF EXISTS `dry_length`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `dry_length` AS select `a`.`rm_up` AS `rm_up`,`b`.`rm_down` AS `rm_down`,(`a`.`rm_up` - `b`.`rm_down`) AS `dry_length`,`a`.`dat` AS `dat` from ((select `observation`.`rm` AS `rm_up`,`observation`.`id` AS `id_up`,cast(`observation`.`datet` as date) AS `dat`,`dryness`.`dryid` AS `dryid_up`,`dryness`.`down_dryid` AS `dryid_down` from (`observation` join `dryness` on((`observation`.`id` = `dryness`.`id`))) where (`dryness`.`down_dryid` is not null)) `a` join (select `observation`.`rm` AS `rm_down`,`observation`.`id` AS `id_down`,`dryness`.`dryid` AS `dryid_down` from (`observation` join `dryness` on((`observation`.`id` = `dryness`.`id`))) where (`dryness`.`extent` = 'Downstream')) `b` on((`a`.`dryid_down` = `b`.`dryid_down`))) order by `a`.`dat`;

-- ----------------------------
-- View structure for dry_length_agg
-- ----------------------------
DROP VIEW IF EXISTS `dry_length_agg`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `dry_length_agg` AS select `dry_length`.`rm_up` AS `rm_up`,`dry_length`.`rm_down` AS `rm_down`,`dry_length`.`dry_length` AS `dry_length`,`dry_length`.`dat` AS `dat`,round((floor(((`dry_length`.`rm_down` * 2) + 0.5)) / 2),1) AS `rm_down_rd`,round((floor(((`dry_length`.`rm_up` * 2) + 0.5)) / 2),1) AS `rm_up_rd` from `dry_length`;

-- ----------------------------
-- View structure for feature_rm
-- ----------------------------
DROP VIEW IF EXISTS `feature_rm`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `feature_rm` AS select round((floor(((`rivermile`.`rm` * 2) + 0.5)) / 2),1) AS `rm-rounded`,min(`feature`.`feature`) AS `feature` from (`rivermile` left join `feature` on((`feature`.`rm` = `rivermile`.`rm`))) where ((`rivermile`.`rm` > 53.5) and (`rivermile`.`rm` < 164)) group by (floor(((`rivermile`.`rm` * 2) + 0.5)) / 2);

-- ----------------------------
-- View structure for isleta_len
-- ----------------------------
DROP VIEW IF EXISTS `isleta_len`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `isleta_len` AS select `dry_length`.`dat` AS `dat`,sum(`dry_length`.`dry_length`) AS `sum_len`,round((sum(`dry_length`.`dry_length`) / (select `reachcalc`('Isleta'))),2) AS `frac_len` from `dry_length` where ((`dry_length`.`rm_up` > (select `downreachcalc`('Isleta'))) and (`dry_length`.`rm_up` < (select `upreachcalc`('Isleta')))) group by `dry_length`.`dat` order by `dry_length`.`dat`;

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
