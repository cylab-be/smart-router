DROP TABLE IF EXISTS `DNSQueries`;

CREATE TABLE `DNSQueries` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `ip_iot` varchar(20) NOT NULL DEFAULT '',
  `ip_dst` varchar(20) NOT NULL DEFAULT '',
  `domain` varchar(200) NOT NULL DEFAULT '',
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=115 DEFAULT CHARSET=latin1 ;



DROP TABLE IF EXISTS `HTTPQueries`;

CREATE TABLE `HTTPQueries` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT ,
  `ip_iot` varchar(20) NOT NULL DEFAULT '',
  `domain` varchar(200) NOT NULL DEFAULT '',
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=115 DEFAULT CHARSET=latin1 ;


