-- MySQL dump 10.13  Distrib 5.7.19, for macos10.12 (x86_64)
--
-- Host: localhost    Database: PhotoShare
-- ------------------------------------------------------
-- Server version	5.7.19

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
-- Table structure for table `Album`
--

DROP TABLE IF EXISTS `Album`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Album` (
  `aid` int(10) NOT NULL AUTO_INCREMENT,
  `uid` int(10) NOT NULL,
  `name` varchar(20) NOT NULL,
  `DOCreation` date NOT NULL,
  PRIMARY KEY (`aid`),
  KEY `uid` (`uid`),
  CONSTRAINT `album_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `User` (`uid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Album`
--

LOCK TABLES `Album` WRITE;
/*!40000 ALTER TABLE `Album` DISABLE KEYS */;
INSERT INTO `Album` VALUES (1,1,'Football Team','2017-10-30'),(8,1,'Random','2017-10-30'),(9,7,'Death Note','2017-10-30'),(10,7,'Barcelona','2017-10-30'),(11,6,'Dhoni','2017-10-30');
/*!40000 ALTER TABLE `Album` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Comments`
--

DROP TABLE IF EXISTS `Comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Comments` (
  `cid` int(10) NOT NULL AUTO_INCREMENT,
  `pid` int(10) NOT NULL,
  `uid` int(10) NOT NULL,
  `comment` varchar(150) NOT NULL,
  `date_comm` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`cid`),
  KEY `pid` (`pid`),
  KEY `uid` (`uid`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`pid`) REFERENCES `Photos` (`pid`) ON DELETE CASCADE,
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`uid`) REFERENCES `User` (`uid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Comments`
--

LOCK TABLES `Comments` WRITE;
/*!40000 ALTER TABLE `Comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `Comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Photos`
--

DROP TABLE IF EXISTS `Photos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Photos` (
  `pid` int(10) NOT NULL AUTO_INCREMENT,
  `aid` int(10) NOT NULL,
  `caption` varchar(50) NOT NULL,
  `data` text NOT NULL,
  PRIMARY KEY (`pid`),
  KEY `aid` (`aid`),
  CONSTRAINT `photos_ibfk_1` FOREIGN KEY (`aid`) REFERENCES `Album` (`aid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Photos`
--

LOCK TABLES `Photos` WRITE;
/*!40000 ALTER TABLE `Photos` DISABLE KEYS */;
INSERT INTO `Photos` VALUES (1,1,'Football Team 2016-2017','uploads/1/1.jpeg'),(16,1,'Coep Winners','uploads/1/2.jpg'),(17,1,'Ground','uploads/1/17.jpg'),(18,1,'skream trophies','uploads/1/18.jpg'),(19,8,'Naruto','uploads/8/19.jpg'),(20,9,'death poster','uploads/9/20.jpg'),(21,9,'Lit','uploads/9/21.jpg'),(22,9,'poster','uploads/9/22.jpg'),(23,9,'L vs Light','uploads/9/23.jpg'),(24,9,'Ryuk','uploads/9/24.jpg'),(25,10,'Mes que un club','uploads/10/25.jpg'),(26,10,'G.O.A.T','uploads/10/26.jpg'),(27,10,'Don Andres','uploads/10/27.jpg'),(28,10,'Midfield maestro','uploads/10/28.jpg'),(29,10,'The Wall','uploads/10/29.jpg'),(30,11,'Dhoni ','uploads/11/30.jpg'),(31,11,'test series vs australia','uploads/11/31.jpg');
/*!40000 ALTER TABLE `Photos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Tags`
--

DROP TABLE IF EXISTS `Tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Tags` (
  `tid` int(10) NOT NULL AUTO_INCREMENT,
  `tag_name` varchar(15) NOT NULL,
  PRIMARY KEY (`tid`),
  UNIQUE KEY `tag_name` (`tag_name`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Tags`
--

LOCK TABLES `Tags` WRITE;
/*!40000 ALTER TABLE `Tags` DISABLE KEYS */;
INSERT INTO `Tags` VALUES (17,''),(31,'100'),(7,'2017'),(23,'Barcelona'),(26,'Best'),(11,'Bombay'),(13,'Coep'),(24,'Crest'),(18,'deathnote'),(32,'dhoni'),(34,'four'),(27,'Greatest'),(15,'Ground'),(6,'hai'),(3,'hi'),(10,'IIt'),(33,'India'),(28,'Iniesta'),(2,'likes'),(25,'Messi'),(20,'movie'),(19,'poster'),(30,'Puyol'),(22,'shinigami'),(12,'shoni'),(21,'showdown'),(8,'Skream'),(14,'Somaiya'),(1,'test'),(5,'toh'),(16,'trophies'),(9,'Winners'),(29,'Xavi'),(4,'ye');
/*!40000 ALTER TABLE `Tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User` (
  `uid` int(10) NOT NULL AUTO_INCREMENT,
  `fname` text NOT NULL,
  `name` text NOT NULL,
  `DOB` date NOT NULL,
  `gender` text NOT NULL,
  `email` varchar(30) NOT NULL,
  `hometown` text NOT NULL,
  `password` varchar(20) NOT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES (1,'Pranav','Raikundalia','1995-12-16','male','pranavpr@bu.edu','Mumbai','abc123'),(5,'anonymous','user','2017-10-10','male','anonymous@user.com','unknown','anonymous@user'),(6,'Vaibhav ','Sharma','1995-08-12','male','vaibhavs@bu.edu','Delhi','vaibhav123'),(7,'Dishant','Pandya','1995-10-08','male','pdishant95@gmail.com','Mumbai','dishant123'),(8,'Hardik','Shah','1995-09-25','male','shardik95@gmail.com','Mumbai','hardik123');
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consists_of`
--

DROP TABLE IF EXISTS `consists_of`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `consists_of` (
  `tid` int(10) NOT NULL,
  `pid` int(10) NOT NULL,
  PRIMARY KEY (`tid`,`pid`),
  KEY `pid` (`pid`),
  CONSTRAINT `consists_of_ibfk_1` FOREIGN KEY (`tid`) REFERENCES `Tags` (`tid`),
  CONSTRAINT `consists_of_ibfk_2` FOREIGN KEY (`pid`) REFERENCES `Photos` (`pid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consists_of`
--

LOCK TABLES `consists_of` WRITE;
/*!40000 ALTER TABLE `consists_of` DISABLE KEYS */;
INSERT INTO `consists_of` VALUES (7,1),(8,1),(9,1),(11,1),(7,16),(9,16),(13,16),(14,17),(15,17),(8,18),(9,18),(14,18),(16,18),(9,19),(17,19),(9,20),(18,20),(18,21),(19,21),(18,22),(20,22),(18,23),(21,23),(18,24),(22,24),(23,25),(24,25),(23,26),(25,26),(26,26),(27,26),(23,27),(28,27),(23,28),(29,28),(23,29),(30,29),(31,30),(32,30),(1,31),(32,31),(33,31),(34,31);
/*!40000 ALTER TABLE `consists_of` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `friends_with`
--

DROP TABLE IF EXISTS `friends_with`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `friends_with` (
  `uid1` int(10) NOT NULL,
  `uid2` int(10) NOT NULL,
  PRIMARY KEY (`uid1`,`uid2`),
  KEY `uid2` (`uid2`),
  CONSTRAINT `friends_with_ibfk_1` FOREIGN KEY (`uid1`) REFERENCES `User` (`uid`) ON DELETE CASCADE,
  CONSTRAINT `friends_with_ibfk_2` FOREIGN KEY (`uid2`) REFERENCES `User` (`uid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `friends_with`
--

LOCK TABLES `friends_with` WRITE;
/*!40000 ALTER TABLE `friends_with` DISABLE KEYS */;
INSERT INTO `friends_with` VALUES (6,1),(1,7),(1,8);
/*!40000 ALTER TABLE `friends_with` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `likes` (
  `uid` int(10) NOT NULL,
  `pid` int(10) NOT NULL,
  PRIMARY KEY (`uid`,`pid`),
  KEY `pid` (`pid`),
  CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `User` (`uid`),
  CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`pid`) REFERENCES `Photos` (`pid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
INSERT INTO `likes` VALUES (6,26);
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-10-30 16:06:08
