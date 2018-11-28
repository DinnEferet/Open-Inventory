-- MySQL dump 10.13  Distrib 8.0.12, for Win64 (x86_64)
--
-- Host: localhost    Database: open_inventory_desktop
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
-- Table structure for table `q_items`
--

DROP TABLE IF EXISTS `q_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `q_items` (
  `item_name` varchar(33) NOT NULL,
  `quantity` int(11) DEFAULT NULL,
  `price` float DEFAULT NULL,
  PRIMARY KEY (`item_name`),
  UNIQUE KEY `item_name` (`item_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `q_items`
--

LOCK TABLES `q_items` WRITE;
/*!40000 ALTER TABLE `q_items` DISABLE KEYS */;
INSERT INTO `q_items` VALUES ('Beast',592,300),('Eva Water',174,100),('Faro Water',44,100),('Galaxy Chocolate',105,1000),('Heinz Ketchup',50,750),('HP Notebook 15 PC',34,105000),('Milo Sachet',500,40),('Monster',3,300),('Motorola G5',36,98000),('Orijin',50,250),('Peak Milk Tin',20,800),('Peak Sachet',500,40),('Pepsi Medium',9,120),('Samsung Smartphone',20,100000),('Smirnoff Ice',277,150),('Snickers',8,300),('Tisue Pack',200,150),('Twix',600,300);
/*!40000 ALTER TABLE `q_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `q_sales`
--

DROP TABLE IF EXISTS `q_sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `q_sales` (
  `item_name` varchar(33) NOT NULL,
  `quantity_bought` int(11) DEFAULT NULL,
  `amount_paid` float DEFAULT NULL,
  `date_of_sale` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `q_sales`
--

LOCK TABLES `q_sales` WRITE;
/*!40000 ALTER TABLE `q_sales` DISABLE KEYS */;
INSERT INTO `q_sales` VALUES ('Monster',34,10200,'2018-10-31'),('Monster',23,6900,'2018-10-31'),('HP Notebook 15 PC',300,31500000,'2018-10-31'),('Pepsi Medium',40,4800,'2018-10-31'),('5 Alive Large',45,15750,'2018-10-31'),('Orbit Gum',34,11900,'2018-10-31'),('HP Notebook 15 PC',5,525000,'2018-10-31'),('5 Alive Large',3,1050,'2018-10-31'),('Faro Water',45,4500,'2018-11-03'),('HP Notebook 15 PC',3,315000,'2018-11-03'),('Faro Water',2,200,'2018-11-04'),('Galaxy Chocolate Large',3,3000,'2018-11-04'),('Snickers',34,10200,'2018-11-04'),('Orbit Gum',3,1050,'2018-11-04'),('Pepsi Medium',23,2760,'2018-11-04'),('Faro Water',3,300,'2018-11-04'),('Galaxy Chocolate Large',3,3000,'2018-11-04'),('Snickers',34,10200,'2018-11-04'),('Faro Water',2,200,'2018-11-04'),('Faro Water',2,200,'2018-11-04'),('Faro Water',3,300,'2018-11-04'),('Faro Water',34,3400,'2018-11-04'),('Galaxy Chocolate Large',2,2000,'2018-11-04'),('Faro Water',3,300,'2018-11-04'),('HP Notebook 15 PC',2,210000,'2018-11-05'),('Faro Water',12,1200,'2018-11-05'),('Galaxy Chocolate Large',3,3000,'2018-11-05'),('Faro Water',3,300,'2018-11-05'),('HP Notebook 15 PC',3,315000,'2018-11-05'),('Faro Water',2,200,'2018-11-05'),('Pepsi Medium',23,2760,'2018-11-05'),('HP Notebook 15 PC',3,315000,'2018-11-05'),('Cabin Biscuit',299,89700,'2018-11-05'),('Faro Water',23,2300,'2018-11-05'),('Galaxy Chocolate Large',3,3000,'2018-11-06'),('Pepsi Medium',2,240,'2018-11-08'),('Galaxy Chocolate Large',2,2000,'2018-11-08'),('Galaxy Chocolate Large',23,23000,'2018-11-12'),('Faro Water',60,6000,'2018-11-12'),('Faro Water',2,200,'2018-11-12'),('Pepsi Medium',3,360,'2018-11-12'),('Faro Juice Orange',89,22250,'2018-11-12'),('Faro Juice Orange',8,2000,'2018-11-12'),('Cabin Biscuit',23,6900,'2018-11-13'),('Cabin Biscuit',2,600,'2018-11-13'),('Cabin Biscuit',2,600,'2018-11-13'),('Cabin Biscuit',3,900,'2018-11-13'),('Twix',23,6900,'2018-11-13'),('Pepsi Medium',300,36000,'2018-11-13'),('HP Notebook 15 PC',10,1050000,'2018-11-13'),('Monster',6,1800,'2018-11-14'),('Monster',6,1800,'2018-11-14'),('Twix',270,81000,'2018-11-14'),('Snickers',292,87600,'2018-11-14'),('Monster',600,180000,'2018-11-14'),('Motorola G5',2,196000,'2018-11-14'),('Eva Water',34,3400,'2018-11-15'),('Eva Water',4,400,'2018-11-20'),('Eva Water',10,1000,'2018-11-23'),('Galaxy Chocolate',6,6000,'2018-11-23'),('Eva Water',5,500,'2018-11-27'),('Faro Water',23,2300,'2018-11-27'),('Eva Water',100,10000,'2018-11-27'),('Eva Water',23,2300,'2018-11-27'),('Faro Water',33,3300,'2018-11-28'),('Beast',90,27000,'2018-11-28'),('Beast',40,12000,'2018-11-28'),('Beast',34,10200,'2018-11-28'),('Smirnoff Ice',23,3450,'2018-11-28'),('Motorola G5',2,196000,'2018-11-28');
/*!40000 ALTER TABLE `q_sales` ENABLE KEYS */;
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
INSERT INTO `user_accounts` VALUES ('Eferet Inc.','q','q','2018-10-31');
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

-- Dump completed on 2018-11-29  0:02:22