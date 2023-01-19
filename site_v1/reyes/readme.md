## This the readme for the Rivereyes Database Dev Team

### Resources for deploying development container of applictaion on docker 

#### Docker Playground URL 

* https://labs.play-with-docker.com/

#### Github Repo 

* https://github.com/rhull21/re_app

#### video Walkthrough

* https://geosystemsanalysis-my.sharepoint.com/:v:/g/personal/rhull_gsanalysis_com/EURrDtkQk75Evx1Lf6KxiicBG7f9F5J9L0wsx6bkOdveng?e=Kh9bDW

#### Code for Docker Playgrround

        ```
        $ git clone https://github.com/rhull21/re_app.git
        $ cd re_app/site_v1/reyes/
        $ docker compose up -d

        PORT 8000/rivereyes
        ```


### some todos before production: 

#### page-by-page feedback CM, JT

##### riogrande

* *''*

##### geospatial

* *'map'*

##### dryness

* *'dry'*
* *'dry/deltadry'*
* *'dry/drysegs'*
* *'dry/drysegs/filtereddrysegs'*
* *'dry/drysegs/filteredfeatures'*
* *'dry/drylen'*
* *'dry/comp'*
* *'dry/days'*
* *'dry/events'*

##### flow / discharge

* *'flow'*
* *'flow/summary'*
* *'flow/series'*

##### dashboards

* *'dashboard/'*
* *'dashboard/dryevents'*
* *'dashboard/drysegs'*


#### front-end

0. Identify realistic priorities given time constraints
1. create `dry/comp` view
2. create `dry/days` view
3. create `dry/events` view
4. create `dashboard/drysegs` view
5. create `dashboard/dryevents` view
6. spiff up front-end stylistically
7. create better descriptions of page content
8. create metadata (units, origin) for data, as view. Following conventions of USGS
9. Add better mapping functionality, either as a dynamic mapping between query outputs and pages, or as an embedded AGOL presence
10. For date and rm ranges add sliders to all tables
12. User Authentication (log in)

#### back-end

0. Identify realistic priorities given time constraints
1. create `dry_comp` queries
2. create `dry_days` queries
3. create `dry_events` queries
4. create `dash_dry_segs` queries
5. create `dash_dry_events` queries
6. figure out a permanent
7. Fix weird redudant records from the 2002-2018 dataset, where there might be multiple dry records of different length in the `rivereyes.dryness`
8. create metadata (units, origin) for data, as queries
9. re-render 2021 dryness data as scrubbed, as well as some missing fulcrum data from 2019, 2020
10. Error Handling (make for more graceful handling of app malfunctions)
11. Security 
    - careful of SQL injection
    - secrets


#### docker / deployment

1. cache user / pwd information in 'secrets'; with a virtual environment?
2. ~In dockerfile find out redundancies in apk loading that could be removed and speed up build (it takes several minutes now)~
3. should set db.healthcheck.interval to something smaller, but extra period is needed for boot up
4. deployment options:
    * app: AWS ECS? db: jade? 

### Toggle between local and docker

1. ensure that ./db is updated with the latest data
    * trigger update:
        ```
        CREATE DATABASE IF NOT EXISTS `rivereyes`;
        USE `rivereyes`;
        ```
    * reorganize the functions and views (at bottom) in the order of their appearance / use. See
        ```
        rivereyes_dump_011820223_structure_model.sql
        ``` 
    * ~at end of file do this to allow for some group by queries used herein~ (not needed as of 01192023)
        ```
        SET GLOBAL sql_mode='';
        ```
        * if this doesn't work, then go into docker terminal (`mysql -u <user> -p`) and enter this
2. comment on/off between django db in settings.py