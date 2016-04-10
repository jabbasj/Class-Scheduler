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
INSERT INTO `sequence` VALUES ('BIOL 206','cegep',-1),('BIOL 261','cegep',-1),('CHEM 221','cegep',-1),('COEN 346','Winter',1),('COMP 232','Fall',0),('COMP 248','Fall',0),('COMP 249','Winter',0),('COMP 335','Summer',2),('COMP 345','Winter',0),('COMP 346','Fall',2),('COMP 348','Fall',1),('COMP 352','Winter',1),('COMP 353','Fall',1),('COMP 371','Winter',1),('COMP 426','Summer',1),('COMP 428','Fall',2),('COMP 442','Fall',3),('COMP 445','Winter',3),('ELEC 273','Winter',1),('ELEC 275','Fall',2),('ELEC 321','Summer',1),('ENCS 272','Fall',-1),('ENCS 282','Summer',1),('ENGR 201','Fall',0),('ENGR 202','Summer',0),('ENGR 213','Fall',0),('ENGR 233','Summer',0),('ENGR 242','Fall',1),('ENGR 243','Fall',1),('ENGR 251','Fall',1),('ENGR 301','Summer',3),('ENGR 361','Winter',1),('ENGR 371','Fall',2),('ENGR 391','Winter',2),('ENGR 392','Winter',3),('MECH 221','Winter',0),('PHYS 252','cegep',-1),('SOEN 228','Winter',0),('SOEN 287','Winter',0),('SOEN 321','Summer',3),('SOEN 331','Fall',2),('SOEN 341','Summer',2),('SOEN 342','Winter',2),('SOEN 343','Winter',2),('SOEN 344','Fall',3),('SOEN 345','Fall',3),('SOEN 357','Fall',3),('SOEN 384','Winter',2),('SOEN 385','Winter',3),('SOEN 390','Fall',3);
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

-- Dump completed on 2016-04-10 14:07:51
