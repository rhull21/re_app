* Toggle between local and docker
    1. ensure that ./db is updated with the latest data
        * trigger update:
            ```
            CREATE DATABASE IF NOT EXISTS `rivereyes`;
            USE `rivereyes`;
            ```
    2. comment on/off between 



* some todos before production: 
    1. cache user / pwd information in 'secrets'; with a virtual environment?
    2. In dockerfile find out redundancies in apk loading that could be removed and speed up build (it takes several minutes now)
    3. 