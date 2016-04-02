CREATE DATABASE  IF NOT EXISTS `soen341_project` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `soen341_project`;
-- MySQL dump 10.13  Distrib 5.7.9, for Win32 (AMD64)
--
-- Host: localhost    Database: soen341_project
-- ------------------------------------------------------
-- Server version	5.7.11-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `registered`
--

DROP TABLE IF EXISTS `registered`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registered` (
  `studentId` int(11) NOT NULL,
  `cId` varchar(8) NOT NULL,
  `sectionId` varchar(8) NOT NULL,
  `semester` varchar(6) NOT NULL,
  `year` int(11) NOT NULL,
  `type` varchar(3) NOT NULL,
  `grade` varchar(4) DEFAULT NULL,
  `finished` tinyint(1) NOT NULL DEFAULT '0',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `studentId` (`studentId`),
  KEY `cId` (`cId`,`sectionId`,`semester`,`year`,`type`),
  CONSTRAINT `registered_ibfk_1` FOREIGN KEY (`studentId`) REFERENCES `students` (`sId`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registered`
--

LOCK TABLES `registered` WRITE;
/*!40000 ALTER TABLE `registered` DISABLE KEYS */;
INSERT INTO `registered` VALUES (10001011,'ENGR 201','EC','Fall',2017,'lec','',0,80),(10001011,'ENGR 201','ECEB','Fall',2017,'tut','',0,81),(10001011,'COMP 248','W','Fall',2017,'lec','',0,82),(10001011,'COMP 248','W WA','Fall',2017,'tut','',0,83),(10001011,'COMP 248','WI-X','Fall',2017,'lab','',0,84),(10001011,'ENGR 213','F','Summer',2016,'lec','',0,85),(10001011,'ENGR 213','F FB','Summer',2016,'tut','',0,86),(10001011,'ELEC 321','H','Fall',2017,'lec','',0,87),(10001011,'ELEC 321','H HA','Fall',2017,'tut','',0,88),(10001011,'ELEC 321','HI-X','Fall',2017,'lab','',0,89),(10001011,'ENCS 272','A','Winter',2017,'lec','',0,90);
/*!40000 ALTER TABLE `registered` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-04-02 15:13:06
