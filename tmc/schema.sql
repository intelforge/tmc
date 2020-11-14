-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS adversaries;
DROP TABLE IF EXISTS tactics;
DROP TABLE IF EXISTS techniques;
DROP TABLE IF EXISTS subtechniques;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS tools;
DROP TABLE IF EXISTS industries;
DROP TABLE IF EXISTS event_x_industry;
DROP TABLE IF EXISTS adversaries_x_tools;
DROP TABLE IF EXISTS tools_x_techniques;
DROP TABLE IF EXISTS tools_x_subtechniques;
DROP TABLE IF EXISTS tactics_x_techniques;
DROP TABLE IF EXISTS techniques_x_subtechniques;


CREATE TABLE user (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE NOT NULL,
password TEXT NOT NULL
);

CREATE TABLE adversaries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  adversary_id TEXT NOT NULL,
  adversary_name TEXT NOT NULL,
  adversary_description TEXT NOT NULL,
  adversary_identifiers TEXT,
  adversay_sorigin TEXT,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE tactics (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tactic_id TEXT NOT NULL,
  tactic_name TEXT NOT NULL,
  tactic_description TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE techniques (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  technique_id TEXT NOT NULL,
  technique_name TEXT NOT NULL,
  technique_description TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE subtechniques (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  subtechnique_id TEXT NOT NULL,
  subtechnique_name TEXT NOT NULL,
  subtechnique_description TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE tools (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tool_id TEXT NOT NULL,
  tool_name TEXT NOT NULL,
  tool_description TEXT NOT NULL,
  tool_identifiers TEXT,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  event_id TEXT NOT NULL,
  event_name TEXT NOT NULL,
  event_description TEXT NOT NULL,
  event_industry TEXT,
  event_date DATETIME,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE adversaries_x_tools (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  adversary_id TEXT NOT NULL,
  tool_id TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (adversary_id) REFERENCES adversary (id),
  FOREIGN KEY (tool_id) REFERENCES tool (id)
);


CREATE TABLE tools_x_techniques (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tool_id TEXT NOT NULL,
  technique_id TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (tool_id) REFERENCES tool (id),
  FOREIGN KEY (technique_id) REFERENCES technique (id)
);

CREATE TABLE tools_x_subtechniques (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tool_id TEXT NOT NULL,
  subtechnique_id TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (tool_id) REFERENCES tool (id),
  FOREIGN KEY (subtechnique_id) REFERENCES subtechnique (id)
);

CREATE TABLE tactics_x_techniques (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tactic_id TEXT NOT NULL,
  technique_id TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (tactic_id) REFERENCES tactic (id),
  FOREIGN KEY (technique_id) REFERENCES technique (id)
);

CREATE TABLE techniques_x_subtechniques (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  technique_id TEXT NOT NULL,
  subtechnique_id TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (technique_id) REFERENCES technique (id),
  FOREIGN KEY (subtechnique_id) REFERENCES subtechnique (id)
);


-- Industries taken from STIX
-- https://docs.oasis-open.org/cti/stix/v2.1/cs01/stix-v2.1-cs01.html#_oogrswk3onck

CREATE TABLE industries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  industry_name TEXT NOT NULL,
  industry_description TEXT,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE countries (
id INTEGER PRIMARY KEY AUTOINCREMENT,
author_id INTEGER NOT NULL,
created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
code TEXT NOT NULL,
ctld TEXT NOT NULL,
country TEXT NOT NULL,
FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE event_x_industry (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  event_id TEXT NOT NULL,
  industry_id TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (event_id) REFERENCES event (id),
  FOREIGN KEY (industry_id) REFERENCES industry (id)
);


INSERT INTO industries (author_id, industry_name) 
VALUES (1, 'Agriculture'),
(1, 'Aerospace'),
(1, 'Automotive'),
(1, 'Chemical'),
(1, 'Commercial'),
(1, 'Communications'),
(1, 'Construction'),
(1, 'Defense'),
(1, 'Education'),
(1, 'Energy'),
(1, 'Entertainment'),
(1, 'Financial Services'),
(1, 'Government'),
(1, 'Healthcare'),
(1, 'Hospitality & Leisure'),
(1, 'Infrastructure'),
(1, 'Insurance'),
(1, 'Manufacturing'),
(1, 'Mining'),
(1, 'Non-profit'),
(1, 'Pharmaceuticals'),
(1, 'Retail'),
(1, 'Technology'),
(1, 'Telecommunications'),
(1, 'Transportation'),
(1, 'Utilities'),
(1, 'Unspecified');



INSERT INTO countries (author_id, code, ctld, country) 
VALUES (1, 'AFG', 'AF', 'Afghanistan'),
(1, 'ALA', 'AX', 'Aland Islands'),
(1, 'ALB', 'AL', 'Albania'),
(1, 'DZA', 'DZ', 'Algeria'),
(1, 'ASM', 'AS', 'American Samoa'),
(1, 'AGO', 'AO', 'Angola'),
(1, 'AIA', 'AI', 'Anguilla'),
(1, 'ATA', 'AQ', 'Antarctica'),
(1, 'ATG', 'AG', 'Antigua and Barbuda'),
(1, 'ARG', 'AR', 'Argentina'),
(1, 'ARM', 'AM', 'Armenia'),
(1, 'ABW', 'AW', 'Aruba'),
(1, 'AUS', 'AU', 'Australia'),
(1, 'AUT', 'AT', 'Austria'),
(1, 'AZE', 'AZ', 'Azerbaijan'),
(1, 'BHS', 'BS', 'Bahamas'),
(1, 'BHR', 'BH', 'Bahrain'),
(1, 'BGD', 'BD', 'Bangladesh'),
(1, 'BRB', 'BB', 'Barbados'),
(1, 'BLR', 'BY', 'Belarus'),
(1, 'BEL', 'BE', 'Belgium'),
(1, 'BLZ', 'BZ', 'Belize'),
(1, 'BEN', 'BJ', 'Benin'),
(1, 'BMU', 'BM', 'Bermuda'),
(1, 'BTN', 'BT', 'Bhutan'),
(1, 'BOL', 'BO', 'Bolivia'),
(1, 'BIH', 'BA', 'Bosnia and Herzegovina'),
(1, 'BWA', 'BW', 'Botswana'),
(1, 'BVT', 'BV', 'Bouvet Island'),
(1, 'BRA', 'BR', 'Brazil'),
(1, 'VGB', 'VG', 'British Virgin Islands'),
(1, 'IOT', 'IO', 'British Indian Ocean Territory'),
(1, 'BRN', 'BN', 'Brunei'),
(1, 'BGR', 'BG', 'Bulgaria'),
(1, 'BFA', 'BF', 'Burkina Faso'),
(1, 'BDI', 'BI', 'Burundi'),
(1, 'KHM', 'KH', 'Cambodia'),
(1, 'CMR', 'CM', 'Cameroon'),
(1, 'CAN', 'CA', 'Canada'),
(1, 'CPV', 'CV', 'Cape Verde'),
(1, 'CYM', 'KY', 'Cayman Islands'),
(1, 'CAF', 'CF', 'Central African Republic'),
(1, 'TCD', 'TD', 'Chad'),
(1, 'CHL', 'CL', 'Chile'),
(1, 'CHN', 'CN', 'China'),
(1, 'HKG', 'HK', 'Hong Kong'),
(1, 'MAC', 'MO', 'Macau'),
(1, 'CXR', 'CX', 'Christmas Island'),
(1, 'CCK', 'CC', 'Cocos Islands'),
(1, 'COL', 'CO', 'Colombia'),
(1, 'COM', 'KM', 'Comoros'),
(1, 'COG', 'CG', 'Republic of the Congo'),
(1, 'COD', 'CD', 'Democratic Republic of the Congo'),
(1, 'COK', 'CK', 'Cook Islands'),
(1, 'CRI', 'CR', 'Costa Rica'),
(1, 'CIV', 'CI', 'Côte d''Ivoire'),
(1, 'HRV', 'HR', 'Croatia'),
(1, 'CUB', 'CU', 'Cuba'),
(1, 'CYP', 'CY', 'Cyprus'),
(1, 'CZE', 'CZ', 'Czech Republic'),
(1, 'DNK', 'DK', 'Denmark'),
(1, 'DJI', 'DJ', 'Djibouti'),
(1, 'DMA', 'DM', 'Dominica'),
(1, 'DOM', 'DO', 'Dominican Republic'),
(1, 'ECU', 'EC', 'Ecuador'),
(1, 'EGY', 'EG', 'Egypt'),
(1, 'SLV', 'SV', 'El Salvador'),
(1, 'GNQ', 'GQ', 'Equatorial Guinea'),
(1, 'ERI', 'ER', 'Eritrea'),
(1, 'EST', 'EE', 'Estonia'),
(1, 'ETH', 'ET', 'Ethiopia'),
(1, 'FLK', 'FK', 'Falkland Islands'),
(1, 'FRO', 'FO', 'Faroe Islands'),
(1, 'FJI', 'FJ', 'Fiji'),
(1, 'FIN', 'FI', 'Finland'),
(1, 'FRA', 'FR', 'France'),
(1, 'GUF', 'GF', 'French Guiana'),
(1, 'PYF', 'PF', 'French Polynesia'),
(1, 'ATF', 'TF', 'French Southern Territories'),
(1, 'GAB', 'GA', 'Gabon'),
(1, 'GMB', 'GM', 'Gambia'),
(1, 'GEO', 'GE', 'Georgia'),
(1, 'DEU', 'DE', 'Germany'),
(1, 'GHA', 'GH', 'Ghana'),
(1, 'GIB', 'GI', 'Gibraltar'),
(1, 'GRC', 'GR', 'Greece'),
(1, 'GRL', 'GL', 'Greenland'),
(1, 'GRD', 'GD', 'Grenada'),
(1, 'GLP', 'GP', 'Guadeloupe'),
(1, 'GUM', 'gu', 'Guam'),
(1, 'GTM', 'GT', 'Guatemala'),
(1, 'GGY', 'GG', 'Guernsey'),
(1, 'GIN', 'GN', 'Guinea'),
(1, 'GNB', 'GW', 'Guinea-Bissau'),
(1, 'GUY', 'GY', 'Guyana'),
(1, 'HTI', 'HT', 'Haiti'),
(1, 'HMD', 'HM', 'Heard and Mcdonald Islands'),
(1, 'VAT', 'VA', 'Vatican'),
(1, 'HND', 'HN', 'Honduras'),
(1, 'HUN', 'HU', 'Hungary'),
(1, 'ISL', 'IS', 'Iceland'),
(1, 'IND', 'IN', 'India'),
(1, 'IDN', 'ID', 'Indonesia'),
(1, 'IRN', 'IR', 'Iran'),
(1, 'IRQ', 'IQ', 'Iraq'),
(1, 'IRL', 'IE', 'Ireland'),
(1, 'IMN', 'IM', 'Isle of Man'),
(1, 'ISR', 'IL', 'Israel'),
(1, 'ITA', 'IT', 'Italy'),
(1, 'JAM', 'JM', 'Jamaica'),
(1, 'JPN', 'JP', 'Japan'),
(1, 'JEY', 'JE', 'Jersey'),
(1, 'JOR', 'JO', 'Jordan'),
(1, 'KAZ', 'KZ', 'Kazakhstan'),
(1, 'KEN', 'KE', 'Kenya'),
(1, 'KIR', 'KI', 'Kiribati'),
(1, 'KOR', 'KR', 'South Korea'),
(1, 'PRK', 'KP', 'North Korea'),
(1, 'KWT', 'KW', 'Kuwait'),
(1, 'KGZ', 'KG', 'Kyrgyzstan'),
(1, 'LAO', 'LA', 'Laos'),
(1, 'LVA', 'LV', 'Latvia'),
(1, 'LBN', 'LB', 'Lebanon'),
(1, 'LSO', 'LS', 'Lesotho'),
(1, 'LBR', 'LR', 'Liberia'),
(1, 'LBY', 'LY', 'Libya'),
(1, 'LIE', 'LI', 'Liechtenstein'),
(1, 'LTU', 'LT', 'Lithuania'),
(1, 'LUX', 'LU', 'Luxembourg'),
(1, 'MKD', 'MK', 'Macedonia'),
(1, 'MDG', 'MG', 'Madagascar'),
(1, 'MWI', 'MW', 'Malawi'),
(1, 'MYS', 'MY', 'Malaysia'),
(1, 'MDV', 'MV', 'Maldives'),
(1, 'MLI', 'ML', 'Mali'),
(1, 'MLT', 'MT', 'Malta'),
(1, 'MHL', 'MH', 'Marshall Islands'),
(1, 'MTQ', 'MQ', 'Martinique'),
(1, 'MRT', 'MR', 'Mauritania'),
(1, 'MUS', 'MU', 'Mauritius'),
(1, 'MYT', 'YT', 'Mayotte'),
(1, 'MEX', 'MX', 'Mexico'),
(1, 'FSM', 'FM', 'Micronesia'),
(1, 'MDA', 'MD', 'Moldova'),
(1, 'MCO', 'MC', 'Monaco'),
(1, 'MNG', 'MN', 'Mongolia'),
(1, 'MNE', 'ME', 'Montenegro'),
(1, 'MSR', 'MS', 'Montserrat'),
(1, 'MAR', 'MA', 'Morocco'),
(1, 'MOZ', 'MZ', 'Mozambique'),
(1, 'MMR', 'MM', 'Myanmar'),
(1, 'NAM', 'NA', 'Namibia'),
(1, 'NRU', 'NR', 'Nauru'),
(1, 'NPL', 'NP', 'Nepal'),
(1, 'NLD', 'NL', 'Netherlands'),
(1, 'ANT', 'AN', 'Netherlands Antilles'),
(1, 'NCL', 'NC', 'New Caledonia'),
(1, 'NZL', 'NZ', 'New Zealand'),
(1, 'NIC', 'NI', 'Nicaragua'),
(1, 'NER', 'NE', 'Niger'),
(1, 'NGA', 'NG', 'Nigeria'),
(1, 'NIU', 'NU', 'Niue'),
(1, 'NFK', 'NF', 'Norfolk Island'),
(1, 'MNP', 'MP', 'Northern Mariana Islands'),
(1, 'NOR', 'NO', 'Norway'),
(1, 'OMN', 'OM', 'Oman'),
(1, 'PAK', 'PK', 'Pakistan'),
(1, 'PLW', 'PW', 'Palau'),
(1, 'PSE', 'PS', 'Palestine'),
(1, 'PAN', 'PA', 'Panama'),
(1, 'PNG', 'PG', 'Papua New Guinea'),
(1, 'PRY', 'PY', 'Paraguay'),
(1, 'PER', 'PE', 'Peru'),
(1, 'PHL', 'PH', 'Philippines'),
(1, 'PCN', 'PN', 'Pitcairn'),
(1, 'POL', 'PL', 'Poland'),
(1, 'PRT', 'PT', 'Portugal'),
(1, 'PRI', 'PR', 'Puerto Rico'),
(1, 'QAT', 'QA', 'Qatar'),
(1, 'REU', 'RE', 'Réunion'),
(1, 'ROU', 'RO', 'Romania'),
(1, 'RUS', 'RU', 'Russia'),
(1, 'RWA', 'RW', 'Rwanda'),
(1, 'BES', 'BQ', 'Saba'),
(1, 'BLM', 'BL', 'Saint-Barthélemy'),
(1, 'SHN', 'SH', 'Saint Helena'),
(1, 'KNA', 'KN', 'Saint Kitts and Nevis'),
(1, 'LCA', 'LC', 'Saint Lucia'),
(1, 'MAF', 'MF', 'Saint-Martin'),
(1, 'SPM', 'PM', 'Saint Pierre and Miquelon'),
(1, 'VCT', 'VC', 'Saint Vincent and Grenadines'),
(1, 'WSM', 'WS', 'Samoa'),
(1, 'SMR', 'SM', 'San Marino'),
(1, 'STP', 'ST', 'Sao Tome and Principe'),
(1, 'SAU', 'SA', 'Saudi Arabia'),
(1, 'SEN', 'SN', 'Senegal'),
(1, 'SRB', 'RS', 'Serbia'),
(1, 'SYC', 'SC', 'Seychelles'),
(1, 'SLE', 'SL', 'Sierra Leone'),
(1, 'SGP', 'SG', 'Singapore'),
(1, 'SVK', 'SK', 'Slovakia'),
(1, 'SVN', 'SI', 'Slovenia'),
(1, 'SLB', 'SB', 'Solomon Islands'),
(1, 'SOM', 'SO', 'Somalia'),
(1, 'ZAF', 'ZA', 'South Africa'),
(1, 'SGS', 'GS', 'South Georgia and the South Sandwich Islands'),
(1, 'SSD', 'SS', 'South Sudan'),
(1, 'ESP', 'ES', 'Spain'),
(1, 'LKA', 'LK', 'Sri Lanka'),
(1, 'SDN', 'SD', 'Sudan'),
(1, 'SUR', 'SR', 'Suriname'),
(1, 'SJM', 'SJ', 'Svalbard and Jan Mayen Islands'),
(1, 'SWZ', 'SZ', 'Swaziland'),
(1, 'SWE', 'SE', 'Sweden'),
(1, 'CHE', 'CH', 'Switzerland'),
(1, 'SYR', 'SY', 'Syria'),
(1, 'TWN', 'TW', 'Taiwan'),
(1, 'TJK', 'TJ', 'Tajikistan'),
(1, 'TZA', 'TZ', 'Tanzania'),
(1, 'THA', 'TH', 'Thailand'),
(1, 'TLS', 'TL', 'Timor-Leste'),
(1, 'TGO', 'TG', 'Togo'),
(1, 'TKL', 'TK', 'Tokelau'),
(1, 'TON', 'TO', 'Tonga'),
(1, 'TTO', 'TT', 'Trinidad and Tobago'),
(1, 'TUN', 'TN', 'Tunisia'),
(1, 'TUR', 'TR', 'Turkey'),
(1, 'TKM', 'TM', 'Turkmenistan'),
(1, 'TCA', 'TC', 'Turks and Caicos Islands'),
(1, 'TUV', 'TV', 'Tuvalu'),
(1, 'UGA', 'UG', 'Uganda'),
(1, 'UKR', 'UA', 'Ukraine'),
(1, 'ARE', 'AE', 'United Arab Emirates'),
(1, 'GBR', 'UK', 'United Kingdom'),
(1, 'USA', 'US', 'United States of America'),
(1, 'UMI', 'UM', 'US Minor Outlying Islands'),
(1, 'URY', 'UY', 'Uruguay'),
(1, 'UZB', 'UZ', 'Uzbekistan'),
(1, 'VUT', 'VU', 'Vanuatu'),
(1, 'VEN', 'VE', 'Venezuela'),
(1, 'VNM', 'VN', 'Vietnam'),
(1, 'VIR', 'VI', 'Virgin Islands'),
(1, 'WLF', 'WF', 'Wallis and Futuna Islands'),
(1, 'ESH', 'EH', 'Western Sahara'),
(1, 'YEM', 'YE', 'Yemen'),
(1, 'ZMB', 'ZM', 'Zambia'),
(1, 'ZWE', 'ZW', 'Zimbabwe'),
(1, 'MMR', 'MM', 'Myanmar'),
(1, 'CUW', 'CW', 'Curaçao'),
(1, 'SXM', 'SX', 'Sint Maarten');