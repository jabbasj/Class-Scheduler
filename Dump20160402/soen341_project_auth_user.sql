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
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=10002036 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (10001011,'pbkdf2_sha256$24000$mVAZjZXnzIZO$JGTDZ1FlpGTUtr0CXh+fSNtL5aMhdUyr8pAGVc9JmCc=','2016-04-02 06:02:27.894146',0,'vLasalle@gmail.com','Vince','Lasalle','vLasalle@gmail.com',0,1,'2016-02-27 20:06:41.000000'),(10001110,'pbkdf2_sha256$24000$tDprz6PKT8mE$Z1lJBcWSwQhKdPEdlf1IpRFa9d/K5Fix04B614aCtY8=','2016-02-27 20:06:41.000000',0,'gGriswald@gmail.com','Gus','Griswald','gGriswald@gmail.com',0,1,'2016-02-27 20:06:41.000000'),(10001222,'pbkdf2_sha256$24000$7q4L3E3xigqv$08QQV7LrHTD/pARJ7GDIAokpQLM8pTUcq3BWPf8rusM=','2016-02-27 20:06:41.000000',0,'mBlumberg@gmail.com','Mikey','Blumberg','mBlumberg@gmail.com',0,1,'2016-02-27 20:06:41.000000'),(10001235,'pbkdf2_sha256$24000$Ly2GBVQWkHLR$t8hbLVM1O3IeGGIItrgrgJbKdaHWmCZLFIVKJKxqfJQ=','2016-02-27 20:06:41.000000',0,'TJDetweiller@gmail.com','T.J','Detweiler','TJDetweiller@gmail.com',0,1,'2016-02-27 20:06:41.000000'),(10001343,'pbkdf2_sha256$24000$VDAp2YLKr3D4$E7Va5nsrMHTP7nVGQkMHZGez4zYDxEe4UJ0jzTWsJc0=','2016-02-27 20:06:41.000000',0,'gGrundler@gmail.com','Gretchen','Grundler','gGrundler@gmail.com',0,1,'2016-02-27 20:06:41.000000'),(10002032,'pbkdf2_sha256$24000$v4WaFbZlzxJc$2U97hNaHrQkYkvOYZzyZHuN2WkxmPS32/szXc08wkbw=','2016-02-27 20:06:41.000000',0,'flashGordon4Life@gmail.com','Ashley','Spinelli','flashGordon4Life@gmail.com',0,1,'2016-02-27 20:06:41.000000'),(10002033,'pbkdf2_sha256$24000$VcRZjLgbsmXz$Kp3f8GsArWNTKny0chwDI/YGxOGauITtGOInQl7dDUQ=','2016-04-01 14:52:00.473429',1,'admin','','','admin@admin.com',1,1,'2016-02-27 20:06:40.568154'),(10002034,'pbkdf2_sha256$24000$Va1eECmiBJqO$FPhCwXfLxofglbyhRzjTXUa9Qu+IJ7bZhTDY+JVFrDI=','2016-02-27 20:09:32.975015',0,'test','test','test','test@test.com',0,1,'2016-02-27 20:08:19.000000'),(10002035,'pbkdf2_sha256$24000$kP8lJr9pLxsL$lqx4GIAqOAe+HoLoIBUvtvqV71gVy5nbjnC8JxqHUyw=','2016-03-30 23:01:49.566299',0,'new_user','','','',0,1,'2016-03-30 23:00:40.788365');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-04-02 15:13:07
