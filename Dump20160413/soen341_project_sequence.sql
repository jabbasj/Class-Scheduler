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
-- Table structure for table `sequence`
--

DROP TABLE IF EXISTS `sequence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sequence` (
  `cId` varchar(8) NOT NULL,
  `semester` varchar(6) NOT NULL,
  `year` int(11) NOT NULL,
  PRIMARY KEY (`cId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sequence`
--

LOCK TABLES `sequence` WRITE;
/*!40000 ALTER TABLE `sequence` DISABLE KEYS */;
INSERT INTO `sequence` VALUES ('COEN 346','Winter',100),('COMP 232','Fall',0),('COMP 248','Fall',0),('COMP 249','Winter',1),('COMP 335','Fall',2),('COMP 346','Winter',2),('COMP 348','Fall',1),('COMP 352','Fall',1),('COMP 353','Fall',100),('COMP 428','Fall',100),('COMP 442','Fall',100),('COMP 445','Winter',100),('ELEC 275','Winter',2),('ENCS 282','Fall',1),('ENGR 201','Fall',0),('ENGR 202','Fall',1),('ENGR 213','Fall',0),('ENGR 233','Winter',1),('ENGR 242','Fall',100),('ENGR 243','Fall',100),('ENGR 251','Fall',100),('ENGR 301','Fall',3),('ENGR 371','Winter',2),('ENGR 391','Fall',2),('ENGR 392','Winter',3),('SOEN 228','Winter',1),('SOEN 287','Winter',1),('SOEN 321','Fall',3),('SOEN 331','Winter',2),('SOEN 341','Winter',2),('SOEN 342','Fall',2),('SOEN 343','Fall',2),('SOEN 344','Fall',3),('SOEN 345','Fall',3),('SOEN 357','Fall',3),('SOEN 384','Fall',2),('SOEN 385','Winter',3),('SOEN 390','Fall',3);
/*!40000 ALTER TABLE `sequence` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-04-13  0:24:37
