-- MySQL dump 10.13  Distrib 5.5.22, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: w3a_scan
-- ------------------------------------------------------
-- Server version	5.5.22-0ubuntu1

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
-- Table structure for table `w3a_Scan_Lore`
--

DROP TABLE IF EXISTS `w3a_Scan_Lore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `w3a_Scan_Lore` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `v_name` varchar(100) NOT NULL,
  `v_type` int(2) NOT NULL,
  `v_risk` int(1) NOT NULL,
  `v_mode` int(1) NOT NULL,
  `v_info` text NOT NULL,
  `v_descp` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `w3a_Scan_Lore`
--

LOCK TABLES `w3a_Scan_Lore` WRITE;
/*!40000 ALTER TABLE `w3a_Scan_Lore` DISABLE KEYS */;
/*!40000 ALTER TABLE `w3a_Scan_Lore` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `w3a_Scan_Report`
--

DROP TABLE IF EXISTS `w3a_Scan_Report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `w3a_Scan_Report` (
  `rid` int(11) NOT NULL AUTO_INCREMENT,
  `r_type` int(1) NOT NULL,
  `r_high` int(11) NOT NULL,
  `r_warn` int(11) NOT NULL,
  `r_low` int(11) NOT NULL,
  `vid` char(32) NOT NULL,
  PRIMARY KEY (`rid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `w3a_Scan_Report`
--

LOCK TABLES `w3a_Scan_Report` WRITE;
/*!40000 ALTER TABLE `w3a_Scan_Report` DISABLE KEYS */;
INSERT INTO `w3a_Scan_Report` VALUES (1,1,0,0,0,'3ba0103356a155c2dfce65b04b56d8ed');
/*!40000 ALTER TABLE `w3a_Scan_Report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `w3a_Scan_Task`
--

DROP TABLE IF EXISTS `w3a_Scan_Task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `w3a_Scan_Task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `t_name` varchar(40) NOT NULL,
  `t_type` int(3) NOT NULL,
  `t_scan_temple` int(11) NOT NULL,
  `t_start_time` varchar(30) NOT NULL,
  `t_end_time` varchar(30) NOT NULL,
  `t_scan_task` text NOT NULL,
  `t_status` int(3) NOT NULL,
  `t_status_num` int(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `w3a_Scan_Task`
--

LOCK TABLES `w3a_Scan_Task` WRITE;
/*!40000 ALTER TABLE `w3a_Scan_Task` DISABLE KEYS */;
INSERT INTO `w3a_Scan_Task` VALUES (1,'测试任务[网关]',1,1,'2014-01-14 09:40:03','null','192.168.1.1',0,0);
/*!40000 ALTER TABLE `w3a_Scan_Task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `w3a_Scan_Task_Template`
--

DROP TABLE IF EXISTS `w3a_Scan_Task_Template`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `w3a_Scan_Task_Template` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tl_name` varchar(30) NOT NULL,
  `tl_mode` text NOT NULL,
  `tl_switch` int(1) NOT NULL,
  `tl_text` text NOT NULL,
  `tl_type` int(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `w3a_Scan_Task_Template`
--

LOCK TABLES `w3a_Scan_Task_Template` WRITE;
/*!40000 ALTER TABLE `w3a_Scan_Task_Template` DISABLE KEYS */;
/*!40000 ALTER TABLE `w3a_Scan_Task_Template` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `w3a_Scan_Task_Type`
--

DROP TABLE IF EXISTS `w3a_Scan_Task_Type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `w3a_Scan_Task_Type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ty_name` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `w3a_Scan_Task_Type`
--

LOCK TABLES `w3a_Scan_Task_Type` WRITE;
/*!40000 ALTER TABLE `w3a_Scan_Task_Type` DISABLE KEYS */;
INSERT INTO `w3a_Scan_Task_Type` VALUES (1,'Web应用扫描'),(2,'Sys系统扫描');
/*!40000 ALTER TABLE `w3a_Scan_Task_Type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `w3a_Scan_User`
--

DROP TABLE IF EXISTS `w3a_Scan_User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `w3a_Scan_User` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `password` char(32) NOT NULL,
  `gid` int(5) NOT NULL,
  `email` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `w3a_Scan_User`
--

LOCK TABLES `w3a_Scan_User` WRITE;
/*!40000 ALTER TABLE `w3a_Scan_User` DISABLE KEYS */;
INSERT INTO `w3a_Scan_User` VALUES (1,'admin','21232f297a57a5a743894a0e4a801fc3',1,'admin@163.com');
/*!40000 ALTER TABLE `w3a_Scan_User` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `w3a_scan_User_group`
--

DROP TABLE IF EXISTS `w3a_scan_User_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `w3a_scan_User_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `g_name` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `w3a_scan_User_group`
--

LOCK TABLES `w3a_scan_User_group` WRITE;
/*!40000 ALTER TABLE `w3a_scan_User_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `w3a_scan_User_group` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-01-23 16:48:13
