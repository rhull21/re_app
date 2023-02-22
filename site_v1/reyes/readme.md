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

#### global comments

- page headers and descriptions higher up on the page
- have title tags for each page (now it says Rio Grande Dryness... for all of them)
- might be too much for right now, but what about having a terminal kind of thing for people to query the database directly?
- include some space between the header and the start of the pages
- Let’s change “dryness” to “drying”
- Reach names: san acacia, isleta, angostura
- Note that the angostura reach includes the city of Albuquerque, which dried during 2022 for the first time in 40 years, so no data until we get 2022 ingested
- Wanted to confirm that for years 2017 and later, we are no longer relying on Fulcrum data; using the summary tables instead
- Appears data from 2002 through 2021 have been ingested into the database?
- We should add some context and instructions for use on most of the pages. I can help with that.


#### page-by-page feedback CM, JT

##### riogrande

* *''*
* 

##### geospatial

* *'map'*

##### dryness

* *'dry'*
* *'dry/deltadry'*
  * Date column first would make this more intuitive for me
  * typo in Previous Dry Length column header
  * can this table be longer? clicking on page numbers gets tedious. maybe not infinitely scrolling but at least a few hundred records
  * group selection isn't working for me
  * include option to group by reach?
  * have "Submit" button to the right of Group Selection options, so it's clear that they're related
  * Correct column header spelling to “Previous”
  * Add upstream RM, and downstream RM
  * Can we add more rows to each page?
  * Let’s discuss how to best optimize the view without needing to scroll through too many pages

* *'dry/drysegs'*
  * having the animation running by default was a little intense (either have it paused by default, or just slower)
  * have reaches delineated by thicker horizontal lines
  * took me a minute to realize that having the mouse cursor just to the left or right of the plot would show landmarks + RM
  * having all the landmark horizontal lines turned on by default feels a little cluttered to me. Maybe just starting with a few significant ones (e.g. reaches, Peralta Wasteway, etc). Or at least have an easier way to turn them off (I was only able to do it by double clicking on one to isolate it, then clicking again to turn it off)
  * I think some vertical grid lines could help - like thicker lines on the 1st of the month and thinner on the 10th and 20th (or 15th)
  * going to different numbered pages in the tables reloads the whole page - maybe there's a way it could only reload the table?
  * should we filter the Features table to only include rows that have a feature? Is the purpose of that table for folks to look up the location of various features? 
  * regarding that same table, do the coordinates refer to the actual location of the feature or to the location of the RM associated with that feature?
  * the two tables are kind of hidden below the plot, and people might not find them if they don't scroll down
  * links to Feature filtering and Dry Segments filtering both have the same text 
  * This is going to be a really freaking cool tool.
  * Please pivot the RM on the Y axis, so they are listed in descending order --- this better aligns to geographic context, RMs start with zero on the south end and then increase moving north
  * Lets discuss the best way to plot landmarks, wondering if we should group major and minor landmarks, for example

* *'dry/drysegs/filtereddrysegs'*
  * wonder if these tables should be nested under dry/ instead of dry/drysegs - my first impression of the dry/drysegs page is that it was just about the visualization, so I wasn't expecting the tables to be nested inside. i didn't notice these pages until after writing comments for /drysegs, so some of those might apply here
  * for filters, saying "Start Date" and "End Date" and "Min dry length" and "max dry length"
  * maybe have a column for reach? having multiple dry lengths for the same date might be confusing for folks that are less familiar with drying patterns in the MRG
  * for me, it's a little more intuitive to have the columns ordered with downstream RM first then upstream. Not sure exactly why. i think that's how we have it on the daily reports, and my impression is that dry segments tends to expand in the upstream direction (but maybe that's an Angostura reach bias)
  * If possible I think that having some quick way to filter by year and reach would improve functionality. Like a dropdown menu, or buttons. Typing in start and end dates could be tedious if you wanted to be exploring differences
  * seems like for filtering by RM, the entire dry segment has to be within the bounds. Wonder if there's a way to make that clear to users. I'm thinking of people that might want to search for any dry segments that include a specific RM, for example. 
  * when typing RMs into the filter boxes, you can no longer see which box is for upstream and which is for downstream. That tripped me up because they're in the opposite order as in the table columns.
* *'dry/drysegs/filteredfeatures'*
  * I wonder about having a short (~ 1 sentence) description of each feature as an additional column
  * "Feature Contains" might not be obvious for some that it's for filtering by name. Maybe "Feature Name" or "Feature Name Contains"?
  * have a "clear filter" button - this could apply to any table on the site
  * think I mentioned this earlier, but I think unless people are going to be looking up the coordinates for specific RMs, there's no need to include RMs that don't have a feature
  * For filtering by lat/long, it looks like you'd have to enter the exact coordinate down to the same # of digits after the decimal. I think the only way someone would be able to do that is if they already had a copy of the table. Could we make it so that it would filter down to something like hundredths place (not exactly sure which would work best here)? 
  * Just speculating on how people might use this page, what about having another column for "Feature Type" - like gages, bridges, etc. I can imagine someone wanting to look up the associated RM for all the USGS, for example. 
* *'dry/drylen'*
  * should it say "Middle Rio Grande" instead of "Rio Grande"?
  * are we delineating between Abeytas and Peralta segments in the database? If so, that could be good to include here as additional columns
  * filtering would be easier to navigate if the filter boxes for each reach were in their own column. so one column would be Isleta sum and Isleta percent dry, the next column would be San Acacia sum and percent dry, then Rio Grande sum and percent dry. 
* *'dry/comp'*
* *'dry/days'*
* *'dry/events'*

##### flow / discharge

* *'flow'*
  * don't really need a link to "Flow Home" on the nav page, but it would be useful to have that link on the nested pages below
* *'flow/summary'*
  * can't think of much to change here - everything looks pretty good. maybe just making it easier to filter by station for people who don't know the numerical ID for the gages
* *'flow/series'*
  * default view of the plot is a bit confusing to look at. The layer drawn on top kind of covers up everything else. Curious how a line chart would look, with a relatively thin line weight. Or just having either a single year or single gage displayed by default
  * I know there's a zoom function, but would it be possible to interactively narrow the date range?
  * Maybe not necessary to have an X-axis title in this case
  * including the "common names" of the gages would be helpful

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
13. Embed web map application

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
12. How to deal with floor RMs?
13. Metadata


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
