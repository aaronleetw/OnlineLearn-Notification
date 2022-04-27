create database online_notif;
use online_notif;

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id),
    email TEXT,
    epoint TEXT,
    password TEXT
);

CREATE TABLE schedule (
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id),
    user_id INT,
    dow INT,
    period CHAR,
    subject TEXT,
    url TEXT
);
