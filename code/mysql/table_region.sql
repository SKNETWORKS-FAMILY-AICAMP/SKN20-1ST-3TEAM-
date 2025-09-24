CREATE TABLE region (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sido VARCHAR(50) NOT NULL,
    sigungu VARCHAR(50) NOT NULL,
    
    UNIQUE KEY unique_sido_sigungu (sido, sigungu)
);

CREATE TABLE sknfirst.faq (
    faq_id INT AUTO_INCREMENT PRIMARY KEY,
    faq_company VARCHAR(50) NOT NULL,
    faq_major_category VARCHAR(50) NOT NULL,
    faq_sub_category VARCHAR(50) NOT NULL,
    faq_question TEXT NOT NULL,
    faq_answer TEXT NOT NULL);




CREATE TABLE `car_registeration` (
  `car_id` int NOT NULL AUTO_INCREMENT,
  `report_month` date NOT NULL,
  `region_id` int NOT NULL,
  `passenger_official` int DEFAULT '0',
  `passenger_private` int DEFAULT '0',
  `passenger_commercial` int DEFAULT '0',
  `passenger_subtotal` int DEFAULT '0',
  `van_official` int DEFAULT '0',
  `van_private` int DEFAULT '0',
  `van_commercial` int DEFAULT '0',
  `van_subtotal` int DEFAULT '0',
  `truck_official` int DEFAULT '0',
  `truck_private` int DEFAULT '0',
  `truck_commercial` int DEFAULT '0',
  `truck_subtotal` int DEFAULT '0',
  `special_official` int DEFAULT '0',
  `special_private` int DEFAULT '0',
  `special_commercial` int DEFAULT '0',
  `special_subtotal` int DEFAULT '0',
  `total_official` int DEFAULT '0',
  `total_private` int DEFAULT '0',
  `total_commercial` int DEFAULT '0',
  `total_subtotal` int DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`car_id`),
  UNIQUE KEY `unique_month_region` (`report_month`,`region_id`),
  KEY `idx_car_reg_month` (`report_month`),
  KEY `idx_car_reg_region` (`region_id`),
  KEY `idx_car_reg_month_region` (`report_month`,`region_id`),
  CONSTRAINT `car_registeration_ibfk_1` FOREIGN KEY (`region_id`) REFERENCES `region` (`region_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11938
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;
