/*
 Navicat Premium Data Transfer

 Source Server         : root
 Source Server Type    : MySQL
 Source Server Version : 80019
 Source Host           : localhost:3306
 Source Schema         : auto_abstract

 Target Server Type    : MySQL
 Target Server Version : 80019
 File Encoding         : 65001

 Date: 07/03/2020 00:56:00
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auto_abstract_history
-- ----------------------------
DROP TABLE IF EXISTS `auto_abstract_history`;
CREATE TABLE `auto_abstract_history` (
  `history_id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `content` varchar(2040) DEFAULT NULL COMMENT '摘要内容',
  `timestamp` datetime(6) DEFAULT NULL COMMENT '操作时间',
  PRIMARY KEY (`history_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='自动摘要历史';

-- ----------------------------
-- Table structure for auto_abstract_model
-- ----------------------------
DROP TABLE IF EXISTS `auto_abstract_model`;
CREATE TABLE `auto_abstract_model` (
  `model_id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `parameters` varchar(255) DEFAULT NULL COMMENT '参数，json形式',
  `input` varchar(1020) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '输入值，词or句',
  `output` varchar(2040) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '输出值，SIF向量形式',
  `picture` blob COMMENT 'output生成词云图片',
  `timestamp` datetime(6) DEFAULT NULL COMMENT '操作时间',
  `commets` varchar(255) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`model_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='模型数据表';

SET FOREIGN_KEY_CHECKS = 1;
