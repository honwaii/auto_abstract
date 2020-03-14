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

 Date: 09/03/2020 00:26:57
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auto_abstract_history
-- ----------------------------
SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for auto_abstract_history
-- ----------------------------
DROP TABLE IF EXISTS `auto_abstract_history`;
CREATE TABLE `auto_abstract_history` (
  `history_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL COMMENT '标题',
  `abstract` text NOT NULL COMMENT '摘要内容',
  `similarity` varchar(255) DEFAULT NULL COMMENT '最相似的句子，json形式 {"sentence": "similarity"} ',
  `model_id` int(11) DEFAULT NULL COMMENT '对应的模型id',
  `timestamp` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp(),
  `top_sentences` blob DEFAULT NULL,
  `content` text DEFAULT NULL,
  PRIMARY KEY (`history_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for auto_abstract_model
-- ----------------------------
DROP TABLE IF EXISTS `auto_abstract_model`;
CREATE TABLE `auto_abstract_model` (
  `model_id` int(11) NOT NULL AUTO_INCREMENT,
  `word_embedding_feature` int(11) NOT NULL COMMENT '词向量模型的维度',
  `coefficients` float(6,3) DEFAULT NULL COMMENT '标题和文章之间的相关系数 (0~1)',
  `exceptions` float(6,3) DEFAULT NULL COMMENT '该模型得到的所有摘要相关性的期望',
  `variances` float(6,3) DEFAULT NULL COMMENT '该模型得到的所有摘要相关性的方差',
  `comments` varchar(255) DEFAULT '' COMMENT '备注',
  `timestamp` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `top_num` int(11) DEFAULT NULL,
  PRIMARY KEY (`model_id`)
) ENGINE=InnoDB AUTO_INCREMENT=397 DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;
