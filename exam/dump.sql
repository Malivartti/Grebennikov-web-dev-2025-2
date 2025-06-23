-- MySQL dump 10.13  Distrib 9.3.0, for macos15.4 (arm64)
--
-- Host: 127.0.0.1    Database: wad-exam
-- ------------------------------------------------------
-- Server version	9.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `adoption`
--

DROP TABLE IF EXISTS `adoption`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adoption` (
  `id` int NOT NULL AUTO_INCREMENT,
  `animal_id` int NOT NULL,
  `user_id` int NOT NULL,
  `submission_date` date NOT NULL,
  `status` enum('pending','accepted','rejected','rejected_adopted') DEFAULT NULL,
  `contact` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_adoption_user_id_user` (`user_id`),
  KEY `fk_adoption_animal_id_animal` (`animal_id`),
  CONSTRAINT `fk_adoption_animal_id_animal` FOREIGN KEY (`animal_id`) REFERENCES `animal` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_adoption_user_id_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adoption`
--

LOCK TABLES `adoption` WRITE;
/*!40000 ALTER TABLE `adoption` DISABLE KEYS */;
INSERT INTO `adoption` VALUES (10,42,4,'2025-06-24','rejected','111'),(11,40,4,'2025-06-24','pending','111'),(12,33,4,'2025-06-24','pending','111'),(13,32,4,'2025-06-24','pending','111'),(14,31,4,'2025-06-24','rejected','111'),(15,34,5,'2025-06-24','rejected','222'),(16,33,5,'2025-06-24','pending','222'),(17,38,5,'2025-06-24','accepted','222'),(18,40,5,'2025-06-24','pending','222'),(19,42,5,'2025-06-24','rejected','222'),(20,42,6,'2025-06-24','accepted','333'),(21,33,6,'2025-06-24','pending','333'),(22,38,6,'2025-06-24','rejected_adopted','222'),(23,31,6,'2025-06-24','accepted','333'),(24,42,7,'2025-06-24','rejected_adopted','444'),(25,35,7,'2025-06-24','pending','444'),(26,32,7,'2025-06-24','pending','444'),(27,40,8,'2025-06-24','pending','555'),(28,33,8,'2025-06-24','pending','555'),(29,35,8,'2025-06-24','pending','555'),(30,42,8,'2025-06-24','rejected_adopted','555'),(31,38,8,'2025-06-24','rejected_adopted','555'),(32,40,9,'2025-06-24','pending','666'),(33,33,9,'2025-06-24','pending','666'),(34,35,10,'2025-06-24','pending','777'),(35,34,10,'2025-06-24','rejected','777');
/*!40000 ALTER TABLE `adoption` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('70a53032e057');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `animal`
--

DROP TABLE IF EXISTS `animal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `animal` (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` text NOT NULL,
  `age_months` int NOT NULL,
  `breed` varchar(100) NOT NULL,
  `sex` enum('male','female') DEFAULT NULL,
  `status` enum('available','adoption','adopted') DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `animal`
--

LOCK TABLES `animal` WRITE;
/*!40000 ALTER TABLE `animal` DISABLE KEYS */;
INSERT INTO `animal` VALUES (31,'## Описание \r\nХорошая собака\r\nПреимущества\r\n* Один\r\n* Два\r\n* Три',4,'Maltese','male','adopted','Майк'),(32,'## Заголовок\r\nСписок\r\n1. Три\r\n2. Четыре',5,'Weimaraner','female','adoption','Кот'),(33,'**Жирный**\r\n*Курсив*\r\n[Ссылка](https://google.com)',2,'Yorkie','male','adoption','Чарли'),(34,'Описание',5,'Canine','female','available','Мило'),(35,'# аааа\r\n## оооо\r\n*как-то так*',4,'Eurasier','male','adoption','Лео'),(36,'* ааа\r\n* ааа\r\n\r\nаа*аа*',7,'corgi','male','available','Макс'),(37,'фф',12,'Dalmatiner','male','available','Тоби'),(38,'123',6,'Labrador','male','adopted','Феликс'),(39,'рр',12,'Cavalier','female','available','Рита'),(40,'ррр',15,'Mammal','male','adoption','Диего'),(41,'# уууу\r\n*возьмите*',6,'Australian Shepherd','female','available','Нора'),(42,'1. рр\r\n2. р\r\n3. рр\r\n\r\n\r\n## ррр\r\n*оооо*',6,'Bulldog','male','adopted','Зак');
/*!40000 ALTER TABLE `animal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `image`
--

DROP TABLE IF EXISTS `image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `image` (
  `id` int NOT NULL AUTO_INCREMENT,
  `filename` varchar(100) NOT NULL,
  `mime_type` varchar(50) NOT NULL,
  `animal_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_image_animal_id_animal` (`animal_id`),
  CONSTRAINT `fk_image_animal_id_animal` FOREIGN KEY (`animal_id`) REFERENCES `animal` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image`
--

LOCK TABLES `image` WRITE;
/*!40000 ALTER TABLE `image` DISABLE KEYS */;
INSERT INTO `image` VALUES (24,'7adac8fa69dc4c709f11b404608624ae.jpg','image/jpeg',31),(25,'8124bc20ee784b67996d15521ea31980.jpg','image/jpeg',31),(26,'854a3a36d633426abe3eb9ddfd532669.jpg','image/jpeg',31),(27,'87c2d99e7fab4712a2bfdee2f53afdf6.jpg','image/jpeg',32),(28,'bc4212785ec84d119e1ea09b99135aab.jpg','image/jpeg',32),(29,'fa8bfaf503d94fd3a652b7259fd3e558.jpg','image/jpeg',33),(30,'35455d16bb77429a8762c0d295253a55.jpg','image/jpeg',33),(31,'53386a9cf8074a6db276a4e62fbb55b5.jpg','image/jpeg',34),(32,'4f26bd5da1dc45d387f8af16250bb9cd.jpg','image/jpeg',35),(33,'e392fe62e5f64fc197a257b16dd75e4d.jpg','image/jpeg',36),(34,'1a499fd101d943318db88437203f57c4.jpg','image/jpeg',37),(35,'bd4eb7a601f041938cd22a9142c45d31.png','image/png',37),(36,'1ea5644ca65440efa972f6bc55a9c3e3.jpg','image/jpeg',38),(37,'794d0fa734a040118e52cc1dff6eda83.jpg','image/jpeg',38),(38,'48a444a57093421c8b2f7e4a3c10af02.jpg','image/jpeg',39),(39,'35d8a57e86194157af7c1e1ea9fe0ca4.jpg','image/jpeg',39),(40,'4ea8d069eb8b4eb583e982fcc9ecba67.jpg','image/jpeg',40),(41,'4622ead8d0724bb7bc51f2c6c174fa55.jpg','image/jpeg',41),(42,'ea7a8f78c86c48e2ba2c8f62ff2ea213.jpg','image/jpeg',41),(43,'870f5827b9ad42ce9fbcb6535f7f5631.jpg','image/jpeg',42),(44,'863d33a654c24ee59f68fe78b7f83ecc.jpg','image/jpeg',42);
/*!40000 ALTER TABLE `image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_role_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'администратор','суперпользователь, имеет полный доступ к системе, в том числе к созданию и удалению животных'),(2,'модератор','может редактировать данные животных и производить модерацию запросов на усыновление'),(3,'пользователь','может инициировать процесс усыновления');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `login` varchar(100) NOT NULL,
  `hashed_password` varchar(255) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_user_login` (`login`),
  KEY `fk_user_role_id_role` (`role_id`),
  CONSTRAINT `fk_user_role_id_role` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'user','scrypt:32768:8:1$wWpjJkRtbVBnchiE$ba3cab28609897d4feb9b88cc76f66911c992ff3649b893872da3843634c078114048aac94f775bfc155f03ffd70d1e110465f50975fd64707ea017013a8b251','user','user','',3),(2,'admin','scrypt:32768:8:1$8iategWOqh7k8Fc8$a2d0ca8d0c2e30526ad4dd9e2276e80133d323539a4c7218ed34f6fab2b44a2ff9728c632e2daba7107e728718e4b1b2810275408c5a9150affc795f0addc013','Admin','Admin','',1),(3,'moder','scrypt:32768:8:1$jyRHK8t1Z0kE7oXL$9f112b73777f4ee20953cca8d4ad7adf4a715a074db8c102e27716765b79499d007405bc8b6e3534e573f1471ffd6301be8b4b6138cf5d57d83ee48391fdf415','Moder','Moder','',2),(4,'user-1','scrypt:32768:8:1$F6EVbtq76Jaem97x$98196a8b10c0d934eb63f2ecb7322e62d6176ff47e05da7919570da12d249756102dc38d1b9364eae8dcbbbe5f4dea1810c6d7c98d010c4b2b0d710bd20866a9','1','User','',3),(5,'user-2','scrypt:32768:8:1$fWe0RXQvlYTptfAd$b6f397f0ce36fecb0ae29d60d8e08f77c0a21c43a72a4cd4f4ffb2c81afee8b261bc65febb78d52614b4d7b10f59a1ce323ba9d301a83c5db6dd6af50f6d3bd1','2','User','',3),(6,'user-3','scrypt:32768:8:1$XqYAyF8Y7ywDWU24$1c8992da36530ee2c185714dad4f9cfa346958bb0f86a1dbe0ccc6985f4db6e297b0a240cfb94f239bb7c97618a808dadcfb461f17ce901fefb11b78b7b8c631','3','User','',3),(7,'user-4','scrypt:32768:8:1$agiX17r52F46ODwo$7f9236f28c6ad8075682c573f34bf77f16895c717f12b4d7c7f33e8a0a6bd40771962e44b1ec7f26b1705da081425982432aae2c690e2a39e44658372da5e6f6','4','User','',3),(8,'user-5','scrypt:32768:8:1$AM0FXs9Cm1fhbw8Q$8bd44c70e379ee9e21586bd14969bbdbbc45c65a9c3e47c79fa30f98b8cf5612721529fb6a148fc39a2912286b7b50c52ca01bdb144d91a543a87443bab085ea','5','User','',3),(9,'user-6','scrypt:32768:8:1$Zsaxeg8kXxAqy25c$061c151d8b0d1855a33a630775ed7ed99c0d473371fdff1666bccc50c8eb250df4b8b6f5177bc3f842b85d82178ca6b155a4b61eac5e6fb10469cf62dfade992','6','User','',3),(10,'user-7','scrypt:32768:8:1$Zsaxeg8kXxAqy25c$061c151d8b0d1855a33a630775ed7ed99c0d473371fdff1666bccc50c8eb250df4b8b6f5177bc3f842b85d82178ca6b155a4b61eac5e6fb10469cf62dfade992','7','User',NULL,3),(11,'user-8','scrypt:32768:8:1$Zsaxeg8kXxAqy25c$061c151d8b0d1855a33a630775ed7ed99c0d473371fdff1666bccc50c8eb250df4b8b6f5177bc3f842b85d82178ca6b155a4b61eac5e6fb10469cf62dfade992','8','User',NULL,3),(12,'user-9','scrypt:32768:8:1$Zsaxeg8kXxAqy25c$061c151d8b0d1855a33a630775ed7ed99c0d473371fdff1666bccc50c8eb250df4b8b6f5177bc3f842b85d82178ca6b155a4b61eac5e6fb10469cf62dfade992','9','User',NULL,3),(13,'user-10','scrypt:32768:8:1$Zsaxeg8kXxAqy25c$061c151d8b0d1855a33a630775ed7ed99c0d473371fdff1666bccc50c8eb250df4b8b6f5177bc3f842b85d82178ca6b155a4b61eac5e6fb10469cf62dfade992','10','User',NULL,3);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-24  3:30:58
