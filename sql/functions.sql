-- Active: 1661291781688@@127.0.0.1@3306@rivereyes

CREATE FUNCTION IF NOT EXISTS hello(s CHAR(20)) RETURNS CHAR(50) DETERMINISTIC
-- simple hello world test function
    RETURN CONCAT('Hello, ', s);

CREATE FUNCTION IF NOT EXISTS reachcalc(reachnm TEXT) RETURNS DECIMAL(5,2) DETERMINISTIC
-- Passes the name of a reach ('San Acacia', 'Isleta', 'Angostura'), calculates length
    return (SELECT (upstream_rm-downstream_rm) FROM reach WHERE reach=reachnm);

CREATE FUNCTION IF NOT EXISTS downreachcalc(reachnm TEXT) RETURNS DECIMAL(5,2) DETERMINISTIC
-- Passes the name of a reach ('San Acacia', 'Isleta', 'Angostura'), calculates downstream
    return (SELECT downstream_rm FROM reach WHERE reach=reachnm);

CREATE FUNCTION IF NOT EXISTS upreachcalc(reachnm TEXT) RETURNS DECIMAL(5,2) DETERMINISTIC
-- Passes the name of a reach ('San Acacia', 'Isleta', 'Angostura'), calculates upstream
    return (SELECT upstream_rm FROM reach WHERE reach=reachnm);





