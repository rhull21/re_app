-- Active: 1661281381237@@127.0.0.1@3306@rivereyes

CREATE TABLE IF NOT EXISTS rivermile (
   rm DECIMAL (5,2) NOT NULL PRIMARY KEY UNIQUE,
   position POINT NOT NULL SRID 0,
   latlong POINT SRID 4326,
   SPATIAL INDEX(position)
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS observation (
   id INT NOT NULL AUTO_INCREMENT,
   fulcrum_id VARCHAR(38),
   rm DECIMAL (5,2),
   obstype ENUM('General',
               'Measured Flow Estimate (Ball and Tape)', 
               'GPS Extent of Drying',
               'Remnant Pool',
               'Visual Flow Estimate',
               'Metered Flow'
               ),
   datet DATETIME,
   note TEXT,
   PRIMARY KEY (id),
   INDEX par_ind (rm),
   FOREIGN KEY (rm)
     REFERENCES rivermile(rm)
     ON UPDATE CASCADE
     ON DELETE CASCADE
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS dryness (
   dryid INT NOT NULL,
   id INT NOT NULL,
   extent ENUM('Upstream',
               'Downstream'
               ),
   down_dryid INT,
   PRIMARY KEY (dryid),
   INDEX par_ind (dryid),
   FOREIGN KEY (id)
     REFERENCES observation(id)
     ON UPDATE CASCADE
     ON DELETE CASCADE
--   FOREIGN KEY (dryid)
--     REFERENCES dryness(down_dryid)
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS feature (
   fid INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
   feature TEXT,
   rm DECIMAL (5,2),
   featype ENUM('Gage'),
   INDEX par_ind (rm),
   FOREIGN KEY (rm)
     REFERENCES rivermile(rm)
     ON UPDATE CASCADE
     ON DELETE CASCADE
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS reach (
   reaid INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
   reach ENUM('Angostura',
              'Isleta',
              'San Acacia' 
               ),
   upstream_rm DECIMAL (5,2),
   downstream_rm DECIMAL (5,2),
   FOREIGN KEY (upstream_rm)
     REFERENCES rivermile(rm)
     ON UPDATE CASCADE
     ON DELETE CASCADE
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS remnant (
   remid INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
   id INT NOT NULL,
   approximate_area_sq_feet INT,
   FOREIGN KEY (id)
     REFERENCES observation(id)
     ON UPDATE CASCADE
     ON DELETE CASCADE
) ENGINE=INNODB;


CREATE TABLE IF NOT EXISTS photos (
   pid INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
   id INT NOT NULL,
   photos_gen_url VARCHAR(2083),
   FOREIGN KEY (id)
     REFERENCES observation(id)
     ON UPDATE CASCADE
     ON DELETE CASCADE
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS discharge_gsa (
   qid INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
   id INT NOT NULL,
   discharge_cfs MEDIUMINT,
   FOREIGN KEY (id)
     REFERENCES observation(id)
     ON UPDATE CASCADE
     ON DELETE CASCADE
) ENGINE=INNODB;
