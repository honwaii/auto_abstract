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

 Date: 27/02/2020 18:02:24
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(10) DEFAULT '',
  `sex` varchar(10) DEFAULT '',
  `age` int DEFAULT '0',
  `email` varchar(128) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='user table';

-- ----------------------------
-- Records of user
-- ----------------------------
BEGIN;
INSERT INTO `user` VALUES (1, 'xiaoming', 'man', 21, 'xiaoming@qq.com');
INSERT INTO `user` VALUES (2, 'xiaohong', 'women', 22, 'xiaohong@qq.com');
INSERT INTO `user` VALUES (3, '小恒', 'man', 21, 'xiaoheng@qq.com');
INSERT INTO `user` VALUES (4, '小嫣', 'women', 22, 'xiaoyan@qq.com');
INSERT INTO `user` VALUES (5, '小勇', 'man', 21, 'xiaoyong@qq.com');
INSERT INTO `user` VALUES (6, '小雯', 'women', 22, 'xiaowen@qq.com');
INSERT INTO `user` VALUES (7, 'John', 'man', 30, 'John@gmail.com');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
