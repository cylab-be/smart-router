DROP TABLE IF EXISTS `DNSQueries`;

CREATE TABLE `DNSQueries` (
  `ip` varchar(20) NOT NULL DEFAULT '',
  `domain` varchar(200) NOT NULL DEFAULT '',
  `datetime` datetime NOT NULL,
  PRIMARY KEY (ip,"domain", datetime)
) ENGINE=InnoDB AUTO_INCREMENT=115 DEFAULT CHARSET=latin1 ;



DROP TABLE IF EXISTS `HTTPQueries`;

CREATE TABLE `HTTPQueries` (
  `mac_iot` varchar(20) NOT NULL DEFAULT '',
  `domain` varchar(200) NOT NULL DEFAULT '',
  `datetime` datetime NOT NULL,
  PRIMARY KEY (mac_iot, "domain", datetime )
) ENGINE=InnoDB AUTO_INCREMENT=115 DEFAULT CHARSET=latin1 ;


DROP TABLE IF EXISTS `Hosts`;

CREATE TABLE `Hosts` (
  `mac` varchar(20) NOT NULL DEFAULT '',
  `hostname` varchar(200) DEFAULT '',
  `first_activity` datetime NOT NULL,
  PRIMARY KEY (mac, first_activity)
) ENGINE=InnoDB AUTO_INCREMENT=115 DEFAULT CHARSET=latin1 ;



DROP TABLE IF EXISTS `Alerts`;

CREATE TABLE `Alerts` (
  `mac` varchar(20) NOT NULL DEFAULT '',
  `hostname` varchar(200) DEFAULT '',
  `domain_reached` varchar(200) NOT NULL DEFAULT '',
  `infraction_date` datetime NOT NULL,
  PRIMARY KEY (mac, domain_reached,infraction_date)
) ENGINE=InnoDB AUTO_INCREMENT=115 DEFAULT CHARSET=latin1 ;