/*
 Navicat Premium Data Transfer

 Source Server         : root
 Source Server Type    : MySQL
 Source Server Version : 80019
 Source Host           : localhost:3306
 Source Schema         : python_mysql

 Target Server Type    : MySQL
 Target Server Version : 80019
 File Encoding         : 65001

 Date: 03/03/2020 01:05:21
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for pvuv
-- ----------------------------
DROP TABLE IF EXISTS `pvuv`;
CREATE TABLE `pvuv` (
  `pdate` varchar(30) DEFAULT NULL,
  `pv` int DEFAULT NULL,
  `uv` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of pvuv
-- ----------------------------
BEGIN;
INSERT INTO `pvuv` VALUES ('2019-07-15', 15000, 150);
INSERT INTO `pvuv` VALUES ('2019-07-14', 14000, 140);
INSERT INTO `pvuv` VALUES ('2019-07-13', 13000, 130);
INSERT INTO `pvuv` VALUES ('2019-07-12', 12000, 120);
INSERT INTO `pvuv` VALUES ('2019-07-11', 11000, 110);
INSERT INTO `pvuv` VALUES ('2019-07-10', 10000, 100);
INSERT INTO `pvuv` VALUES ('2019-07-9', 9000, 90);
INSERT INTO `pvuv` VALUES ('2019-07-8', 8000, 80);
INSERT INTO `pvuv` VALUES ('2019-07-7', 7000, 70);
INSERT INTO `pvuv` VALUES ('2019-07-6', 6000, 60);
INSERT INTO `pvuv` VALUES ('2019-07-5', 5000, 50);
INSERT INTO `pvuv` VALUES ('2019-07-4', 4000, 40);
INSERT INTO `pvuv` VALUES ('2019-07-3', 3000, 30);
INSERT INTO `pvuv` VALUES ('2019-07-2', 2000, 20);
INSERT INTO `pvuv` VALUES ('2019-07-1', 1000, 10);
INSERT INTO `pvuv` VALUES ('2019-07-15', 15000, 150);
INSERT INTO `pvuv` VALUES ('2019-07-14', 14000, 140);
INSERT INTO `pvuv` VALUES ('2019-07-13', 13000, 130);
INSERT INTO `pvuv` VALUES ('2019-07-12', 12000, 120);
INSERT INTO `pvuv` VALUES ('2019-07-11', 11000, 110);
INSERT INTO `pvuv` VALUES ('2019-07-10', 10000, 100);
INSERT INTO `pvuv` VALUES ('2019-07-9', 9000, 90);
INSERT INTO `pvuv` VALUES ('2019-07-8', 8000, 80);
INSERT INTO `pvuv` VALUES ('2019-07-7', 7000, 70);
INSERT INTO `pvuv` VALUES ('2019-07-6', 6000, 60);
INSERT INTO `pvuv` VALUES ('2019-07-5', 5000, 50);
INSERT INTO `pvuv` VALUES ('2019-07-4', 4000, 40);
INSERT INTO `pvuv` VALUES ('2019-07-3', 3000, 30);
INSERT INTO `pvuv` VALUES ('2019-07-2', 2000, 20);
INSERT INTO `pvuv` VALUES ('2019-07-1', 1000, 10);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
