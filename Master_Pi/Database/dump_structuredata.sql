-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: 35.197.185.32    Database: car_share
-- ------------------------------------------------------
-- Server version	5.7.25-google-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'afa936ce-8c41-11ea-a703-42010a98002e:1-315623';

--
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking` (
  `car_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `start_datetime` datetime NOT NULL,
  `end_datetime` datetime NOT NULL,
  `status` varchar(45) NOT NULL,
  `calendar_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`car_id`,`user_id`,`start_datetime`),
  KEY `fk_booking_user1_idx` (`user_id`),
  CONSTRAINT `car_id` FOREIGN KEY (`car_id`) REFERENCES `car` (`car_id`),
  CONSTRAINT `fk_booking_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking`
--

LOCK TABLES `booking` WRITE;
/*!40000 ALTER TABLE `booking` DISABLE KEYS */;
INSERT INTO `booking` VALUES (1,0,'2020-05-24 17:00:00','2020-05-24 18:00:00','complete',NULL),(2,0,'2020-05-26 16:00:00','2020-05-26 17:00:00','complete',NULL),(2,0,'2020-05-29 16:00:00','2020-05-29 17:00:00','cancelled','e0clho7hr30p6o51p2ot5nahn4'),(3,0,'2020-05-24 09:00:00','2020-05-24 17:30:00','complete',NULL),(4,0,'2020-05-01 19:00:00','2020-05-02 13:30:00','complete',NULL),(5,0,'2020-04-03 17:00:00','2020-04-10 17:00:00','cancelled',NULL),(5,0,'2020-05-26 06:59:00','2020-05-26 08:01:00','cancelled','6u1fej6196hgh4fimusuaef47s'),(5,0,'2020-05-27 17:29:00','2020-05-27 20:29:00','cancelled','toti2ubsbrs18hjrl79mg4tpn0'),(5,0,'2020-05-28 20:48:00','2020-05-29 08:49:00','complete','k0rvr293t20r075v74bt3a6hro'),(6,0,'2020-05-24 17:33:00','2020-05-24 19:33:00','cancelled','9m9v5dm1udf89imo1344gj7hvc'),(6,0,'2020-05-27 18:14:00','2020-05-27 21:14:00','cancelled','5b49tdvjl5kl80kvh5n27vrd80'),(9,0,'2020-05-28 15:07:00','2020-05-29 15:07:00','complete','3j6etg7eqiqqvfvlij74se5l8s'),(10,0,'2020-05-28 14:50:00','2020-05-29 14:50:00','cancelled','703jioqsdbmg8f2801h4j22mno');
/*!40000 ALTER TABLE `booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `car`
--

DROP TABLE IF EXISTS `car`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `car` (
  `car_id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(11) NOT NULL,
  `make` varchar(45) NOT NULL,
  `model` varchar(45) NOT NULL,
  `body_type` varchar(45) NOT NULL,
  `colour` varchar(45) NOT NULL,
  `seats` int(11) NOT NULL,
  `location` varchar(45) NOT NULL,
  `cost_per_hour` double NOT NULL,
  PRIMARY KEY (`car_id`),
  UNIQUE KEY `car_id_UNIQUE` (`car_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car`
--

LOCK TABLES `car` WRITE;
/*!40000 ALTER TABLE `car` DISABLE KEYS */;
INSERT INTO `car` VALUES (1,'unavailable','Volkswagen','Passat','sedan','grey',5,'-37.766720,145.137650',60),(2,'available','Subaru','Impreza WRX STI','sedan','blue',5,'-37.781078,145.100199',55),(3,'available','Ford','Fiesta','hatchback','silver',5,'-37.766720,145.137650',35),(4,'unavailable','Volkswagen','Tiguan','SUV','white',7,'-37.709227,145.109037',65),(5,'available','Ferrari','488','coupe','red',2,'34.625479,-97.212649',150),(6,'unavailable','Nissan','Skyline GTR','sedan','black',5,'34.625479,-97.212649',45),(7,'available','Honda','Civic Type R','hatchback','red',5,'34.625479,-97.212649',40),(8,'unavailable','Toyota','Supra','coupe','silver',2,'34.625479,-97.212649',35),(9,'available','Honda','Integra Type R','coupe','yellow',4,'-37.766720,145.137650',35),(10,'available','Nissan','Silvia','coupe','silver',5,'-37.781078,145.100199',45),(11,'available','Mazda','RX7 FD','coupe','yellow',2,'34.625479,-97.212649',50);
/*!40000 ALTER TABLE `car` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `engineer_mac`
--

DROP TABLE IF EXISTS `engineer_mac`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `engineer_mac` (
  `mac_address` varchar(45) NOT NULL,
  `engineer_id` int(11) NOT NULL,
  PRIMARY KEY (`mac_address`),
  KEY `fk_engineer_mac_user1_idx` (`engineer_id`),
  CONSTRAINT `fk_engineer_mac_user1` FOREIGN KEY (`engineer_id`) REFERENCES `user` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `engineer_mac`
--

LOCK TABLES `engineer_mac` WRITE;
/*!40000 ALTER TABLE `engineer_mac` DISABLE KEYS */;
/*!40000 ALTER TABLE `engineer_mac` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `issue`
--

DROP TABLE IF EXISTS `issue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `issue` (
  `issue_id` varchar(45) NOT NULL,
  `description` mediumtext NOT NULL,
  `date_reported` datetime NOT NULL,
  `status` varchar(45) NOT NULL,
  `engineer_id` int(11) NOT NULL,
  `car_id` int(11) NOT NULL,
  PRIMARY KEY (`issue_id`),
  KEY `fk_issue_user1_idx` (`engineer_id`),
  KEY `fk_issue_car1_idx` (`car_id`),
  CONSTRAINT `fk_issue_car1` FOREIGN KEY (`car_id`) REFERENCES `car` (`car_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_issue_user1` FOREIGN KEY (`engineer_id`) REFERENCES `user` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `issue`
--

LOCK TABLES `issue` WRITE;
/*!40000 ALTER TABLE `issue` DISABLE KEYS */;
INSERT INTO `issue` VALUES ('1','Dead battery requires replacement','2020-06-05 13:00:00','unresolved',0,0),('2','Flat tyre at rear left of car requiring replacement','2020-06-06 13:00:00','unresolved',0,0),('3','Worn break pads require replacement','2020-06-07 13:00:00','resolved',0,0),('4','Alternator failure','2020-06-08 13:00:00','resolved',0,0),('5','Oil change overdue','2020-06-09 13:00:00','unresolved',0,0),('6','Service due at 100,000km','2020-06-05 13:00:00','resolved',0,0);
/*!40000 ALTER TABLE `issue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `username` varchar(45) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `type` varchar(45) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `customer_id_UNIQUE` (`user_id`),
  UNIQUE KEY `username_UNIQUE` (`username`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Luke','Davoli','l_davoli','$5$rounds=1000$W91C2LluaaNPBuag$RZZqKD.LpO6acV6dEx1yiCmjNJ6qtz4aBHs3ro.DdxA','s3782747@student.rmit.edu.au','admin'),(2,'Matthies','Abera','big_bear_gaming','$5$rounds=1000$W91C2LluaaNPBuag$RZZqKD.LpO6acV6dEx1yiCmjNJ6qtz4aBHs3ro.DdxA','s3779748@student.rmit.edu.au','manager'),(4,'Hollie','Steinman','god_on_earth','$5$rounds=1000$W91C2LluaaNPBuag$RZZqKD.LpO6acV6dEx1yiCmjNJ6qtz4aBHs3ro.DdxA','S3784783@student.rmit.edu.au','admin'),(5,'Michael','Sartorel','moose','$5$rounds=1000$RtVE6dBxUXteWds0$OQFrAWX12FiaqNNKdeoczBTiofkxTStupLpKDL39unD','moose10141@gmail.com','engineer'),(7,'John','Smith','jsmith10','$5$rounds=1000$mJAW0nSq.GVKOPQK$Ycs92PSl4ZViegUv3G7sTcVQe7MkVrdtSjduYUuwVl3','jsmith10@gmail.com','customer'),(8,'Ben','Zannoni','bz_flog','$RZZqKD.LpO6acV6dEx1yiCmjNJ6qtz4aBHs3ro.DdxA','bzannoni@gmail.com','customer'),(9,'Luca','Diavolo','il_diavolo','$RZZqKD.LpO6acV6dEx1yiCmjNJ6qtz4aBHs3ro.DdxA','ldavoli33@gmail.com','engineer'),(10,'Kali','Uchis','kalietta','$RZZqKD.LpO6acV6dEx1yiCmjNJ6qtz4aBHs3ro.DdxA','kuchis@gmail.com','customer'),(11,'Maria','Campana','mmm_campana','$RZZqKD.LpO6acV6dEx1yiCmjNJ6qtz4aBHs3ro.DdxA','campanamaria@gmail.com','customer'),(12,'Frank','Ocean','blonded','$RZZqKD.LpO6acV6dEx1yiCmjNJ6qtz4aBHs3ro.DdxA','frank@blondedradio.com','customer'),(13,'Kacy','Hill','kc90210','$RZZqKD.LpO6acV6dEx1yiCmjNJ6qtz4aBHs3ro.DdxA','kc.rodeo@gmail.com','engineer'),(14,'Don','Toliver','don_t','$RZZqKD.LpO6acV6dEx1yiCmjNJ6qtz4aBHs3ro.DdxA','don@jackboys.com','engineer');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-06-10 15:48:10
