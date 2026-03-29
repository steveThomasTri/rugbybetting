BEGIN TRANSACTION;
CREATE TABLE Players (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name TEXT,
                        BetsPlaced INTEGER,
                        SuccessRate REAL,
                        Bank REAL
                    );
INSERT INTO "Players" VALUES(1,'HAZ',0,0.0,50.0);
INSERT INTO "Players" VALUES(3,'HENKEL',0,0.0,50.0);
INSERT INTO "Players" VALUES(5,'BLAZE',0,0.0,50.0);
INSERT INTO "Players" VALUES(6,'ENZO',0,0.0,50.0);
INSERT INTO "Players" VALUES(7,'TRIF',0,0.0,50.0);
CREATE TABLE Transactions (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            PlayerID INTEGER,
                            Team TEXT,
                            BetType TEXT,
                            Description TEXT,
                            Odds INTEGER,
                            AmountBet REAL,
                            Status TEXT,
                            AmountWon REAL,
                            FOREIGN KEY(PlayerID) REFERENCES Players(ID)
                        );
INSERT INTO "Transactions" VALUES(1,1,'KNIGHTS','ML','KNIGHTS ML',184,10.0,'Pending',0);
INSERT INTO "Transactions" VALUES(2,1,'KNIGHTS','ATT','DOM YOUNG',-125,10.0,'Pending',0);
INSERT INTO "Transactions" VALUES(3,1,'KNIGHTS','DOZEN','KNIGHTS 1-12',310,10.0,'Pending',0);
INSERT INTO "Transactions" VALUES(4,1,'KNIGHTS','EXACT','KNIGHTS 2',1700,10.0,'Pending',0);
INSERT INTO "Transactions" VALUES(5,1,'KNIGHTS','LINE PARLAY','KNIGHTS +5.5 U 49.5',250,10.0,'Pending',0);

INSERT INTO "Transactions" VALUES(6,7,'COWBOYS','ML','COWBOYS ML',-154,10.0,'Pending',0);
INSERT INTO "Transactions" VALUES(7,7,'COWBOYS','ATT','JASON TAUMALOLO',500,10.0,'Pending',0);
INSERT INTO "Transactions" VALUES(8,7,'COWBOYS','DOZEN','COWBOYS 1-12',210,10.0,'Pending',0);
INSERT INTO "Transactions" VALUES(9,7,'COWBOYS','EXACT','COWBOYS 12',2000,10.0,'Pending',0);
INSERT INTO "Transactions" VALUES(10,7,'COWBOYS','LINE PARLAY','COWBOYS -2.5 U 58.5',220,10.0,'Pending',0);

INSERT INTO "Transactions" VALUES(11,3,'EELS','SPREAD','EELS -7.5',-110,10.0,'Pending',0);
INSERT INTO "Transactions" VALUES(12,3,'EELS','ATT','SEAN RUSSELL',100,10.0,'Pending',0);
INSERT INTO "Transactions" VALUES(13,3,'EELS','DOZEN','EELS 1-12',200,10.0,'Pending',0);
INSERT INTO "Transactions" VALUES(14,3,'EELS','EXACT','EELS 8',1700,10.0,'Pending',0);
INSERT INTO "Transactions" VALUES(15,3,'EELS','LINE PARLAY','EELS -5.5 O 50.5',170,10.0,'Pending',0);

INSERT INTO "Transactions" VALUES(16,5,'SHARKS','SPREAD','SHARKS -6.5',-110,10.0,'Pending',0);
INSERT INTO "Transactions" VALUES(17,5,'SHARKS','ATT','KL IRO',-115,10.0,'Pending',0);
INSERT INTO "Transactions" VALUES(18,5,'SHARKS','DOZEN','SHARKS 13+',150,10.0,'Pending',0);
INSERT INTO "Transactions" VALUES(19,5,'SHARKS','EXACT','SHARKS 18',2200,10.0,'Pending',0);
INSERT INTO "Transactions" VALUES(20,5,'SHARKS','LINE PARLAY','SHARKS -4.5 0 57.5',240,10.0,'Pending',0);

INSERT INTO "Transactions" VALUES(21,6,'TIGERS','ML','TIGERS ML',152,10.0,'Pending',0);
INSERT INTO "Transactions" VALUES(22,6,'TIGERS','ATT','SUNIA TURUVA',-105,10.0,'Pending',0);
INSERT INTO "Transactions" VALUES(23,6,'TIGERS','DOZEN','TIGERS 1-12',260,10.0,'Pending',0);
INSERT INTO "Transactions" VALUES(24,6,'TIGERS','EXACT','TIGERS 12',2700,10.0,'Pending',0);
INSERT INTO "Transactions" VALUES(25,6,'TIGERS','LINE PARLAY','TIGERS +6.5 U 55.5',185,10.0,'Pending',0);

DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('Players',5);
INSERT INTO "sqlite_sequence" VALUES('Transactions',25);
COMMIT;
