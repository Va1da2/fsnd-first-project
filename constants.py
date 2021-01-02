import enum
from dataclasses import dataclass
from typing import List


@dataclass
class StateInfo:
    name: str
    phone_codes: List[str]


class Genres(enum.Enum):
    Alternative = 'Alternative'
    Blues = 'Blues'
    Classical = 'Classical'
    Country = 'Country'
    Electronic = 'Electronic'
    Folk = 'Folk'
    Funk = 'Funk'
    HipHop = 'Hip-Hop'
    HeavyMetal = 'Heavy Metal'
    Instrumental = 'Instrumental'
    Jazz = 'Jazz'
    MusicalTheatre = 'Musical Theatre'
    Pop = 'Pop'
    Punk = 'Punk'
    RB = 'R&B'
    Reggae = 'Reggae'
    RocknRoll = 'Rock n Roll'
    Soul = 'Soul'
    Swing = 'Swing'
    Other = 'Other'

    def __str__(self):
        return self.name

    def __html__(self):
        return self.value


class States(enum.Enum):
    """
    Source: https://www.allareacodes.com/area_code_listings_by_state.htm
    """
    AL = StateInfo('Alabama', ['205', '251', '256', '334', '938'])
    AK = StateInfo('Alaska', ['907'])
    AZ = StateInfo('Arizona', ['480', '520', '602', '623', '928'])
    AR = StateInfo('Arkansas', ['479', '501', '870'])
    CA = StateInfo('California', [
        '209', '213', '279', '310', '323', '408', '415', '424', '442', '510', '530', '559', '562', 
        '619', '626', '628', '650', '657', '661', '669', '707', '714', '747', '760', '805', '818', 
        '820', '831', '858', '909', '916', '925', '949', '951'
        ])
    CO = StateInfo('Colorado', ['303', '719', '720', '970'])
    CT = StateInfo('Connecticut', ['203', '475', '860', '959'])
    DE = StateInfo('Delaware', ['302'])
    DC = StateInfo('Washington, DC', ['202'])
    FL = StateInfo('Florida', [
        '239', '305', '321', '352', '386', '407', '561', '727', '754', '772', '786', '813', '850', 
        '863', '904', '941', '954'
        ])
    GA = StateInfo('Georgia', ['229', '404', '470', '478', '678', '706', '762', '770', '912'])
    HI = StateInfo('Hawaii', ['808'])
    ID = StateInfo('Idaho', ['208', '986'])
    IL = StateInfo('Illonois', [
        '217', '224', '309', '312', '331', '618', '630', '708', '773', '779', '815', '847', '872'
        ])
    IN = StateInfo('Indiana', ['219', '260', '317', '463', '574', '765', '812', '930'])
    IA = StateInfo('Iowa', ['319', '515', '563', '641', '712'])
    KS = StateInfo('Kansas', ['316', '620', '785', '913'])
    KY = StateInfo('Kentucky', ['270', '364', '502', '606', '859'])
    LA = StateInfo('Louisiana', ['225', '318', '337', '504', '985'])
    ME = StateInfo('Maine', ['207'])
    MT = StateInfo('Montana', ['406'])
    NE = StateInfo('Nebraska', ['308', '402', '531'])
    NV = StateInfo('Nevada', ['702', '725', '775'])
    NH = StateInfo('New Hampshire', ['603'])
    NJ = StateInfo('New Jersey', ['201', '551', '609', '640', '732', '848', '856', '862', '908', '973'])
    NM = StateInfo('New Mexico', ['505', '575'])
    NY = StateInfo('New York', [
        '212', '315', '332', '347', '516', '518', '585', '607', '631', '646', '680', '716', '718', '838',
        '845', '914', '917', '929', '934'
        ])
    NC = StateInfo('North Carolina', ['252', '336', '704', '743', '828', '910', '919', '980', '984'])
    ND = StateInfo('North Dakota', ['701'])
    OH = StateInfo('Ohio', ['216', '220', '234', '330', '380', '419', '440', '513', '567', '614', '740', '937'])
    OK = StateInfo('Oklahoma', ['405', '539', '580', '918'])
    OR = StateInfo('Oregon', ['458', '503', '541', '971'])
    MD = StateInfo('Meryland', ['215', '223', '267', '272', '412', '445', '484', '570', '610', '717', '724', '814', '878'])
    MA = StateInfo('Massachusetts', ['339', '351', '413', '508', '617', '774', '781', '857', '978'])
    MI = StateInfo('Michigan', ['231', '248', '269', '313', '517', '586', '616', '734', '810', '906', '947', '989'])
    MN = StateInfo('Minnesota', ['218', '320', '507', '612', '651', '763', '952'])
    MS = StateInfo('Mississippi', ['228', '601', '662', '769'])
    MO = StateInfo('Missouri', ['314', '417', '573', '636', '660', '816'])
    PA = StateInfo('Pennsylvania', ['215', '223', '267', '272', '412', '445', '484', '570', '610', '717', '724', '814', '878'])
    RI = StateInfo('Rhode Island', ['401'])
    SC = StateInfo('South Carolina', ['803', '843', '854', '864'])
    SD = StateInfo('South Dakota', ['605'])
    TN = StateInfo('Tennessee', ['423', '615', '629', '731', '865', '901', '931'])
    TX = StateInfo('Texas', [
        '210', '214', '254', '281', '325', '346', '361', '409', '430', '432', '469', '512', '682', '713', '726',
        '737', '806', '817', '830', '832', '903', '915', '936', '940', '956', '972', '979'
        ])
    UT = StateInfo('Utah', ['385', '435', '801'])
    VT = StateInfo('Vermont', ['802'])
    VA = StateInfo('Virginia', ['276', '434', '540', '571', '703', '757', '804'])
    WA = StateInfo('Washington', ['206', '253', '360', '425', '509', '564'])
    WV = StateInfo('West Virginia', ['304', '681'])
    WI = StateInfo('Wisconsin', ['262', '414', '534', '608', '715', '920'])
    WY = StateInfo('Wyoming', ['307'])

    def __str__(self):
        return self.name

    def __html__(self):
        return self.value.name


def coerce_for_enum(enum):
    # Taken from https://stackoverflow.com/a/51858425/6602729
    def coerce(name):
        if isinstance(name, enum):
            return name
        try:
            return enum[name]
        except KeyError:
            raise ValueError(name)
    return coerce
