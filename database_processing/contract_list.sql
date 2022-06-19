/*
 Navicat Premium Data Transfer

 Source Server         : quantworld_internal
 Source Server Type    : MySQL
 Source Server Version : 50736
 Source Host           : 192.168.0.103:16666
 Source Schema         : high_frequency_futures

 Target Server Type    : MySQL
 Target Server Version : 50736
 File Encoding         : 65001

 Date: 15/06/2022 22:59:05
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for contract_list
-- ----------------------------
DROP TABLE IF EXISTS `contract_list`;
CREATE TABLE `contract_list`  (
  `ContractId` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `UpdDate` date NOT NULL COMMENT 'Record the insert date of this row for rolling update',
  `IsAvailable` tinyint(1) NOT NULL COMMENT 'Whether data of this contract is available now. ! for available. If 0, the data of this contract has been deleted',
  PRIMARY KEY (`ContractId`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
