from abc import ABC
import re 

class Song(ABC):

    def __init__(self):
        self.TITLE = ''
        self.SUBTITLE = ''
        self.ARTIST = ''
        self.TITLETRANSLIT = ''
        self.SUBTITLETRANSLIT = ''
        self.ARTISTTRANSLIT = ''
        self.GENRE = ''
        self.CREDIT = ''
        self.MENUCOLOR = ''
        self.METERTYPE = 'DDR'
        self.BANNER = ''
        self.BACKGROUND = ''
        self.LYRICSPATH = ''
        self.CDTITLE = ''
        self.MUSIC =''
        self.OFFSET = 0
        self.SAMPLESTART = 0
        self.SAMPLELENGTH = 15.500
        self.SELECTABLE = 'YES'
        self.LISTSORT = ''
        self.BPMS = 120
        self.STOPS = ''
        self.BGCHANGES = ''
        self.ATTACKS = ''
        self.Notes = []

    def parse_sm_string(self, file_to_read):
        with open(file_to_read, 'r', encoding='utf-8') as f:
            sm_string = f.read()
        #remove_comment    
        sm_string = re.sub("\/\/.*",'', sm_string, re.MULTILINE)
        items = sm_string.split(';')
        for item in items:
            self.parse_single_item(item)
                            
    def parse_single_item(self, item):
        item = item.strip()
        item_array =  item.split(':')
        match item_array[0]:
            case '#TITLE':
                self.TITLE = item_array[1]
            case '#SUBTITLE':
                self.SUBTITLE = item_array[1]
            case '#ARTIST':
                self.ARTIST = item_array[1]
            case '#TITLETRANSLIT':
                self.TITLETRANSLIT = item_array[1]
            case '#SUBTITLETRANSLIT':
                self.SUBTITLETRANSLIT = item_array[1]
            case '#ARTISTTRANSLIT':
                self.ARTISTTRANSLIT = item_array[1]
            case '#GENRE':
                self.GENRE = item_array[1]
            case '#CREDIT':
                self.CREDIT = item_array[1]
            case '#MENUCOLOR':
                self.MENUCOLOR = item_array[1]
            case '#BANNER':
                self.BANNER = item_array[1]
            case '#BACKGROUND':
                self.BACKGROUND = item_array[1]
            case '#LYRICSPATH':
                self.LYRICSPATH = item_array[1]
            case '#CDTITLE':
                self.CDTITLE = item_array[1]
            case '#MUSIC':
                self.MUSIC = item_array[1]
            case '#OFFSET':
                self.OFFSET = item_array[1]
            case '#SAMPLESTART':
                self.SAMPLESTART = item_array[1]
            case '#SAMPLELENGTH':
                self.SAMPLELENGTH = item_array[1]
            case '#SELECTABLE':
                self.SELECTABLE = item_array[1]
            case '#LISTSORT':
                self.LISTSORT = item_array[1]
            case '#BPMS':
                self.BPMS = item_array[1]
            case '#STOPS':
                self.STOPS = item_array[1]
            case '#BGCHANGES':
                self.BGCHANGES = item_array[1]
            case '#ATTACKS':
                self.ATTACKS = item_array[1]
            case _:
                return
        return
    