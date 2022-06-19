/*
 Navicat Premium Data Transfer

 Source Server         : quantworld_internal
 Source Server Type    : MySQL
 Source Server Version : 50736
 Source Host           : 192.168.0.103:16666
 Source Schema         : multi_factor

 Target Server Type    : MySQL
 Target Server Version : 50736
 File Encoding         : 65001

 Date: 15/06/2022 22:24:10
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for high_freq_trading
-- ----------------------------
DROP TABLE IF EXISTS `high_freq_trading`;
CREATE TABLE `high_freq_trading`  (
  `ContractId` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `TimeIndex` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `LastPrice` decimal(10, 2) NULL DEFAULT 0.00,
  `Volume` int(10) UNSIGNED ZEROFILL NULL DEFAULT NULL COMMENT 'Cumulative volume dealed',
  `CumulTurnover` bigint(20) UNSIGNED ZEROFILL NULL DEFAULT NULL COMMENT 'Cumulative turnover money value',
  `OpenInt` int(10) UNSIGNED ZEROFILL NULL DEFAULT NULL,
  `BidPrice_1` decimal(10, 2) NULL DEFAULT 0.00,
  `BidPrice_2` decimal(10, 2) NULL DEFAULT 0.00,
  `BidPrice_3` decimal(10, 2) NULL DEFAULT 0.00,
  `BidPrice_4` decimal(10, 2) NULL DEFAULT 0.00,
  `BidPrice_5` decimal(10, 2) NULL DEFAULT 0.00,
  `AskPrice_1` decimal(10, 2) NULL DEFAULT 0.00,
  `AskPrice_2` decimal(10, 2) NULL DEFAULT 0.00,
  `AskPrice_3` decimal(10, 2) NULL DEFAULT 0.00,
  `AskPrice_4` decimal(10, 2) NULL DEFAULT 0.00,
  `AskPrice_5` decimal(10, 2) NULL DEFAULT 0.00,
  `BidVolume_1` int(8) UNSIGNED ZEROFILL NULL DEFAULT NULL,
  `BidVolume_2` int(8) UNSIGNED ZEROFILL NULL DEFAULT NULL,
  `BidVolume_3` int(8) UNSIGNED ZEROFILL NULL DEFAULT NULL,
  `BidVolume_4` int(8) UNSIGNED ZEROFILL NULL DEFAULT NULL,
  `BidVolume_5` int(8) UNSIGNED ZEROFILL NULL DEFAULT NULL,
  `AskVolume_1` int(8) UNSIGNED ZEROFILL NULL DEFAULT NULL,
  `AskVolume_2` int(8) UNSIGNED ZEROFILL NULL DEFAULT NULL,
  `AskVolume_3` int(8) UNSIGNED ZEROFILL NULL DEFAULT NULL,
  `AskVolume_4` int(8) UNSIGNED ZEROFILL NULL DEFAULT NULL,
  `AskVolume_5` int(8) UNSIGNED ZEROFILL NULL DEFAULT NULL,
  PRIMARY KEY (`ContractId`, `TimeIndex`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
