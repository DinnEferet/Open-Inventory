-- MySQL dump 10.13  Distrib 8.0.12, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: open_inventory_desktop
-- ------------------------------------------------------
-- Server version	8.0.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `a_items`
--

DROP TABLE IF EXISTS `a_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `a_items` (
  `item_name` varchar(33) NOT NULL,
  `quantity` int(11) DEFAULT NULL,
  `price` float DEFAULT NULL,
  PRIMARY KEY (`item_name`),
  UNIQUE KEY `item_name` (`item_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `a_items`
--

LOCK TABLES `a_items` WRITE;
/*!40000 ALTER TABLE `a_items` DISABLE KEYS */;
INSERT INTO `a_items` VALUES ('Cardboard',266,150);
/*!40000 ALTER TABLE `a_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `a_sales`
--

DROP TABLE IF EXISTS `a_sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `a_sales` (
  `item_name` varchar(33) NOT NULL,
  `quantity_bought` int(11) DEFAULT NULL,
  `amount_paid` float DEFAULT NULL,
  `date_of_sale` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `a_sales`
--

LOCK TABLES `a_sales` WRITE;
/*!40000 ALTER TABLE `a_sales` DISABLE KEYS */;
INSERT INTO `a_sales` VALUES ('Monster',23,52900,'2018-11-04'),('Cardboard',34,5100,'2018-11-04');
/*!40000 ALTER TABLE `a_sales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eferet_items`
--

DROP TABLE IF EXISTS `eferet_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `eferet_items` (
  `item_name` varchar(33) NOT NULL,
  `quantity` int(11) DEFAULT NULL,
  `price` float DEFAULT NULL,
  PRIMARY KEY (`item_name`),
  UNIQUE KEY `item_name` (`item_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eferet_items`
--

LOCK TABLES `eferet_items` WRITE;
/*!40000 ALTER TABLE `eferet_items` DISABLE KEYS */;
INSERT INTO `eferet_items` VALUES ('Faro Water',89,100),('Galaxy Chocolate Large',39,1000),('HB Pencil',280,25),('HP Notebook 15 PC',17,105000),('Indomie Carton',33,1900),('Monster',609,300),('Orbit Gum',463,350),('Pepsi Medium',314,120),('Snickers',232,300),('Twix',300,300);
/*!40000 ALTER TABLE `eferet_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eferet_sales`
--

DROP TABLE IF EXISTS `eferet_sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `eferet_sales` (
  `item_name` varchar(33) NOT NULL,
  `quantity_bought` int(11) DEFAULT NULL,
  `amount_paid` float DEFAULT NULL,
  `date_of_sale` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eferet_sales`
--

LOCK TABLES `eferet_sales` WRITE;
/*!40000 ALTER TABLE `eferet_sales` DISABLE KEYS */;
INSERT INTO `eferet_sales` VALUES ('Monster',34,10200,'2018-10-31'),('Monster',23,6900,'2018-10-31'),('HP Notebook 15 PC',300,31500000,'2018-10-31'),('Pepsi Medium',40,4800,'2018-10-31'),('5 Alive Large',45,15750,'2018-10-31'),('Orbit Gum',34,11900,'2018-10-31'),('HP Notebook 15 PC',5,525000,'2018-10-31'),('Indomie Carton',50,95000,'2018-10-31'),('5 Alive Large',3,1050,'2018-10-31'),('Faro Water',45,4500,'2018-11-03'),('HP Notebook 15 PC',3,315000,'2018-11-03'),('HB Pencil',20,500,'2018-11-04'),('Faro Water',2,200,'2018-11-04'),('Galaxy Chocolate Large',3,3000,'2018-11-04'),('Snickers',34,10200,'2018-11-04'),('Orbit Gum',3,1050,'2018-11-04'),('Pepsi Medium',23,2760,'2018-11-04'),('Faro Water',3,300,'2018-11-04'),('Galaxy Chocolate Large',3,3000,'2018-11-04'),('Snickers',34,10200,'2018-11-04'),('Faro Water',2,200,'2018-11-04'),('Faro Water',2,200,'2018-11-04'),('Faro Water',3,300,'2018-11-04'),('Faro Water',34,3400,'2018-11-04'),('Galaxy Chocolate Large',2,2000,'2018-11-04'),('Faro Water',3,300,'2018-11-04'),('HP Notebook 15 PC',2,210000,'2018-11-05'),('Faro Water',12,1200,'2018-11-05'),('Galaxy Chocolate Large',3,3000,'2018-11-05'),('Faro Water',3,300,'2018-11-05'),('HP Notebook 15 PC',3,315000,'2018-11-05'),('Faro Water',2,200,'2018-11-05'),('Pepsi Medium',23,2760,'2018-11-05');
/*!40000 ALTER TABLE `eferet_sales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_accounts`
--

DROP TABLE IF EXISTS `user_accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user_accounts` (
  `bname` varchar(100) NOT NULL,
  `uname` varchar(100) NOT NULL,
  `pword` varchar(100) NOT NULL,
  `date_created` date NOT NULL,
  PRIMARY KEY (`uname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_accounts`
--

LOCK TABLES `user_accounts` WRITE;
/*!40000 ALTER TABLE `user_accounts` DISABLE KEYS */;
INSERT INTO `user_accounts` VALUES ('Testing','a','a','2018-11-03'),('Eferet Technologies','eferet','eferet','2018-10-31');
/*!40000 ALTER TABLE `user_accounts` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-11-05  8:55:21
