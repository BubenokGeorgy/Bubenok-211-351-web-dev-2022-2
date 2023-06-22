-- MySQL dump 10.13  Distrib 8.0.33, for Linux (x86_64)
--
-- Host: 45.138.74.69    Database: std_2196_exam
-- ------------------------------------------------------
-- Server version	8.0.33-0ubuntu0.22.04.2

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
-- Table structure for table `book`
--

DROP TABLE IF EXISTS `book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(45) NOT NULL,
  `description` text NOT NULL,
  `year` int NOT NULL,
  `publisher` varchar(45) NOT NULL,
  `author` varchar(45) NOT NULL,
  `size` int NOT NULL,
  `covers_id` int NOT NULL,
  PRIMARY KEY (`id`,`covers_id`),
  KEY `fk_book_covers1_idx` (`covers_id`),
  CONSTRAINT `fk_book_covers1` FOREIGN KEY (`covers_id`) REFERENCES `covers` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book`
--

LOCK TABLES `book` WRITE;
/*!40000 ALTER TABLE `book` DISABLE KEYS */;
INSERT INTO `book` VALUES (1,'Капитанская дочка','Это исторический роман, в котором на фоне событий восстания Емельяна Пугачева рассказана история любви, преданности и верности главных героев — Петра Гринева и капитанской дочери Маши. Параллельно подняты вопросы социального неравенства, чести, дружбы, верности, сложности выбора. Повествование ведется от имени Гринева.',1836,'Азбука','Александр Сергеевич Пушкин',480,1),(2,'Преступление и наказание','Нищий и болезненно гордый студент Родион Романович Раскольников решает проверить, способен ли он на поступок, возвышающий его над «обычными» людьми. Для этого он убивает жалкую старую ростовщицу — а затем и её сестру, случайно оказавшуюся на месте преступления.',1866,'АСТ','Достоевский Федор Михайлович',672,2),(3,'Война и мир','Роман Толстого «Войн и мир» рассказывает о военных и довоенных, а также, послевоенных событиях девятнадцатого века. Главные исторические события – война Наполеона Бонапарта с Россией. Кроме этого, главнее персонажи – Андрей Болконский, Наташа Ростова и Пьер Безухов. Между этими героями на всем протяжении романа происходит любовный треугольник. Между этими событиями также существуют остальные, как события, так и персонажи.',1867,'Азбука','Толстой Лев Николаевич',1472,3),(4,'Герой нашего времени','Смысл «Героя нашего времени» - это отражение эпохи, предостережение будущему поколению. Это яркий пример того, как можно быть умным, образованным человеком, но потерять себя, суть своего существования.',1840,'Азбука','Лермонтов Михаил Юрьевич',416,4),(5,'Идиот','Достоевский намеревался показать идеального человека, похожего на Христа; мир, в котором ему приходится существовать, берёт верх над добродетелью, изменить его не удаётся. Роман, плохо встреченный современниками, потомки оценили как одно из самых мощных высказываний Достоевского.',1868,'АСТ','Достоевский Федор Михайлович',640,5),(6,'Евгений Онегин','«„Онегина“ можно назвать энциклопедией русской жизни и в высшей степени народным произведением». Из романа, как и из энциклопедии, можно узнать практически всё об эпохе: о том, как одевались, и что было в моде, что люди ценили больше всего, о чём они разговаривали, какими интересами они жили.',1833,'Азбука','Александр Сергеевич Пушкин',448,6),(7,'Обломов','Сюжет произведения Гончарова поднимает множество социальных тем и проблем, присущих обществу.',1859,'Аст','Гончаров Иван Александрович',640,7),(8,'Горе от ума','ли в двух словах, то комедия «Горе от ума» была написана как яркая сатира на аристократическое московское общество с его преклонением перед вышестоящими чинами, невежеством, лицемерием и фальшью. Пьеса была так богата на афоризмы и точные высказывания, что моментально разошлась на цитаты. Некоторые из них можно встретить в речи до сих пор – наверняка вы слышали выражение «и дым Отечества нам сладок и приятен» (например, его употребляет герой «Служебного романа» Новосельцев, кашляя после затяжки крепкой сигаретой).',1825,'Азбука','Александр Сергеевич Грибоедов',352,8),(9,'Мертвые души','Тема — жизнь и нравы помещиков России в 1830-х годах. Идея заложена в символическом названии поэмы — показать порочность той жизни, вытащить на поверхность проблемы общества. Мертвые души — это не только умершие крестьяне, которых скупал Чичиков. Автор считал всех своих персонажей духовно мертвыми.',1842,'Азбука','Николай Васильевич Гоголь',352,9),(10,'Ревизор','Темой этой комедии социально-сатирической направленности являются пороки общества, чиновничество и его бездеятельность, лицемерие, духовная бедность, общечеловеческая глупость.',1836,'АСТ','Николай Васильевич Гоголь',224,10),(11,'Тарас Бульба','Если описывать «Тараса Бульбу» кратко, то это повесть о старом казацком полковнике, который встречает двух вернувшихся из киевской академии молодых сыновей, Остапа и Андрия. Бульба решает, что нет лучше ученья, чем настоящий бой, и посылает сыновей в Запорожскую Сечь.',1835,'АСТ','Николай Васильевич Гоголь',320,11);
/*!40000 ALTER TABLE `book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_has_genres`
--

DROP TABLE IF EXISTS `book_has_genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_has_genres` (
  `book_id` int NOT NULL,
  `genres_id` int NOT NULL,
  PRIMARY KEY (`book_id`,`genres_id`),
  KEY `fk_book_has_genres_genres1_idx` (`genres_id`),
  KEY `fk_book_has_genres_book_idx` (`book_id`),
  CONSTRAINT `fk_book_has_genres_book` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_book_has_genres_genres1` FOREIGN KEY (`genres_id`) REFERENCES `genres` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_has_genres`
--

LOCK TABLES `book_has_genres` WRITE;
/*!40000 ALTER TABLE `book_has_genres` DISABLE KEYS */;
INSERT INTO `book_has_genres` VALUES (1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(9,1),(1,2),(3,2),(11,2),(2,3),(3,3),(2,4),(2,5),(2,6),(4,6),(3,8),(11,8),(3,9),(3,10),(11,10),(4,11),(7,12),(7,13),(9,13),(8,16),(10,16),(9,17),(11,18);
/*!40000 ALTER TABLE `book_has_genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `covers`
--

DROP TABLE IF EXISTS `covers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `covers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `file_name` varchar(45) NOT NULL,
  `MIME_type` varchar(45) NOT NULL,
  `MD5_hash` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `file_name_UNIQUE` (`file_name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `covers`
--

LOCK TABLES `covers` WRITE;
/*!40000 ALTER TABLE `covers` DISABLE KEYS */;
INSERT INTO `covers` VALUES (1,'kapitanskaya dochka.jpg','image/jpg','1c21ffb75531a96dfe5272874f403f1d'),(2,'prestuplenie i nakazanie.jpg','image/jpg','94a274a2dfbc3885b8f17235a01ea83f'),(3,'voina i mir.jpg','image/jpg','6687ae39c2c09133f10b99f7b7d5bee4'),(4,'geroy nashego vremeni.jpg','image/jpg','c75c918e60973d9482df6a8629fda5d2'),(5,'idiot.jpg','image/jpg','c75c918e60973d9482df6a8629fda5d2'),(6,'evgeniy onegin.jpg','image/jpg','72cf46984d9386caa58340a55c1e8fd5'),(7,'oblomov.jpg','image/jpg','dc008a9866c2541c3e00a5d46262964d'),(8,'gore ot uma.jpg','image/jpg','ea233f545829117d544e216a2fe8c56f'),(9,'mertvye dushi.jpg','image/jpg','3ecc6a4ca06700af0c436467f613bd85'),(10,'revizor.jpg','image/jpg','bf0ffe6e001274816a5e8ddbfb7d97b0'),(11,'taras bulba.jpg','image/jpg','3977257dc73a0c6d2dc4aa3b3ec38c7f'),(12,'dsad.jpg','sadsd','sadsad');
/*!40000 ALTER TABLE `covers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genres`
--

DROP TABLE IF EXISTS `genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genres` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genres`
--

LOCK TABLES `genres` WRITE;
/*!40000 ALTER TABLE `genres` DISABLE KEYS */;
INSERT INTO `genres` VALUES (9,'Военная проза'),(10,'Историческая проза'),(2,'Исторический жанр'),(16,'Комедия'),(4,'Криминальный жанр'),(8,'Любовный роман'),(5,'Мистерия'),(18,'Новелла'),(17,'Пикареска'),(6,'Психологический реализм'),(1,'Роман'),(11,'Романтизм'),(13,'Сатира'),(12,'Фикшн'),(3,'Философский роман');
/*!40000 ALTER TABLE `genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id` int NOT NULL AUTO_INCREMENT,
  `grade` int NOT NULL,
  `text` text NOT NULL,
  `created_At` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `book_id` int NOT NULL,
  `users_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_reviews_book1_idx` (`book_id`),
  KEY `fk_reviews_users1_idx` (`users_id`),
  CONSTRAINT `fk_reviews_book1` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_reviews_users1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (1,5,'Отличная книга','2023-06-21 01:46:44',1,1),(2,3,'Сойдет','2023-06-21 14:44:49',1,2),(5,4,'Почитать можно','2023-06-22 02:14:25',5,1);
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'администратор','суперпользователь, имеет полный доступ к системе, в том числе к созданию и удалению книг'),(2,'модератор','может редактировать данные книг и производить модерацию рецензий'),(3,'пользователь','может оставлять рецензии');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `login` varchar(45) NOT NULL,
  `password_hash` varchar(64) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `first_name` varchar(45) NOT NULL,
  `middle_name` varchar(45) DEFAULT NULL,
  `roles_id` int NOT NULL,
  PRIMARY KEY (`id`,`roles_id`),
  UNIQUE KEY `login_UNIQUE` (`login`),
  KEY `fk_users_roles1_idx` (`roles_id`),
  CONSTRAINT `fk_users_roles1` FOREIGN KEY (`roles_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918','Бубенок','Георгий','Владимирович',1),(2,'moder','b465361ffa25886d97c693b209bd347e600d1b14d397a8e42b7b7c408f32f0a9','Иванов','Иван','Иванович',2);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-22 19:12:57
