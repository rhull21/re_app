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

* moved to project -> issues

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


### Github Flow

1.	Create a branch for some specific part of the website
    a.	`git checkout -b <name>`
2.	Do some work locally on the branch 
    a.	i.e. make changes to `plotpy.html`
3.	Add, Commit, and Push branch to remote (can also use GUI)
    a.	`git add plotpy.html` (or whatever)
    b.	`git commit -m ‘changes to plotpy heatmap that does xyz’`
    c.	`git push -u origin <name>`, will see text like 
        ```
    remote: Create a pull request for 'rmupdate' oo GitHub by visiting:     
    remote:      https://github.com/rhull21/re_app/pull/new/rmupdate 

        ```
4.	On github, do a Pull Request, Merge branch and Delete branch when done
    a. Use Githhub remote; this can also be down using the CLI but maybe more commands than are needed

