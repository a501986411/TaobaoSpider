/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50726
Source Host           : localhost:3306
Source Database       : easy_taobao

Target Server Type    : MYSQL
Target Server Version : 50726
File Encoding         : 65001

Date: 2019-10-09 13:32:13
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for etb_goods_log
-- ----------------------------
DROP TABLE IF EXISTS `etb_goods_log`;
CREATE TABLE `etb_goods_log` (
  `id` bigint(16) NOT NULL,
  `goods_id` varchar(64) NOT NULL DEFAULT '' COMMENT '淘宝商品id',
  `title` varchar(255) NOT NULL DEFAULT '' COMMENT '标题',
  `monthly_sales` int(11) NOT NULL DEFAULT '0' COMMENT '月销量或者30天内销量',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_goods_id` (`goods_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品信息爬去日志表';

-- ----------------------------
-- Records of etb_goods_log
-- ----------------------------

-- ----------------------------
-- Table structure for etb_goods_relation
-- ----------------------------
DROP TABLE IF EXISTS `etb_goods_relation`;
CREATE TABLE `etb_goods_relation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '用户id',
  `own_goods_id` varchar(64) NOT NULL DEFAULT '' COMMENT '自己店铺的商品淘宝id',
  `other_goods_id` varchar(64) NOT NULL DEFAULT '' COMMENT '关注商品的id',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='自己商品-关注商品-uid关系表';

-- ----------------------------
-- Records of etb_goods_relation
-- ----------------------------
INSERT INTO `etb_goods_relation` VALUES ('1', '1', '604075431419', '601289609578', '2019-10-09 12:49:49', '2019-10-09 12:51:07');

-- ----------------------------
-- Table structure for etb_goods_url
-- ----------------------------
DROP TABLE IF EXISTS `etb_goods_url`;
CREATE TABLE `etb_goods_url` (
  `goods_id` varchar(64) NOT NULL DEFAULT '' COMMENT '商品id',
  `url` varchar(255) NOT NULL DEFAULT '' COMMENT '商品详情销售详情页面地址',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`goods_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='淘宝商品与详情页面url关系表';

-- ----------------------------
-- Records of etb_goods_url
-- ----------------------------
INSERT INTO `etb_goods_url` VALUES ('601289609578', 'https://detail.tmall.com/item.htm?spm=a230r.1.14.39.4f6b3547vNtrST&id=601289609578&ns=1&abbucket=6', '2019-10-09 12:50:35', '2019-10-09 12:50:46');
INSERT INTO `etb_goods_url` VALUES ('604075431419', 'https://item.taobao.com/item.htm?spm=a2oq0.12575281.0.0.25911debe483LR&ft=t&id=604075431419', '2019-10-09 12:49:31', '2019-10-09 12:50:50');

-- ----------------------------
-- Table structure for etb_user
-- ----------------------------
DROP TABLE IF EXISTS `etb_user`;
CREATE TABLE `etb_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `username` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT '用户名',
  `password` varchar(255) NOT NULL DEFAULT '' COMMENT '用户密码',
  `salt` varchar(5) NOT NULL DEFAULT '' COMMENT '加密盐',
  `phone` varchar(11) NOT NULL DEFAULT '' COMMENT '绑定电话',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `un_phone` (`phone`),
  UNIQUE KEY `un_username` (`username`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- ----------------------------
-- Records of etb_user
-- ----------------------------
INSERT INTO `etb_user` VALUES ('1', 'chenhailong', '92415433d3891b196e0e369a4a2f6420', 'abcde', '17322036296', '2019-10-09 11:36:05', '2019-10-09 11:57:30');
INSERT INTO `etb_user` VALUES ('2', 'chenhailong6', '92415433d3891b196e0e369a4a2f6420', 'abcde', '17322036294', '2019-10-09 11:56:28', '2019-10-09 11:56:28');
