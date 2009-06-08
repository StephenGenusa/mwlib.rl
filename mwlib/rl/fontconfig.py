#! /usr/bin/env python
#! -*- coding:utf-8 -*-

# Copyright (c) 2007, PediaPress GmbH
# See README.txt for additional licensing information.


import os
import mwlib.fonts
from mwlib.fontswitcher import FontSwitcher
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

font_paths = [os.path.dirname(mwlib.fonts.__file__),
              os.path.expanduser('~/mwlibfonts/')
              ]

# from the fonts defined below only DejaVu is part of the mwlib packet
# the other fonts can be obtained by installing the following debian packets:
# aptitude install ttf-indic-fonts ttf-unfonts ttf-farsiweb ttf-arphic-uming ttf-gfs-artemisia ttf-sil-ezra ttf-thai-arundina linux-libertine
# after that the fonts need to be moved or symlinked to one of the font_paths
fonts = [
    {'name': 'DejaVuSerif',
     'code_points': ['Latin Extended-B', 'Latin-1 Supplement', 'Latin Extended-A', 'Basic Latin'] ,
     'file_names': ['ttf-dejavu/DejaVuSerif.ttf', 'ttf-dejavu/DejaVuSerif-Bold.ttf', 'ttf-dejavu/DejaVuSerif-Italic.ttf', 'ttf-dejavu/DejaVuSerif-BoldItalic.ttf'],
     },
    {'name': 'DejaVuSans',
     'code_points': [] ,
     'file_names': ['ttf-dejavu/DejaVuSans.ttf', 'ttf-dejavu/DejaVuSans-Bold.ttf', 'ttf-dejavu/DejaVuSans-Oblique.ttf', 'ttf-dejavu/DejaVuSans-BoldOblique.ttf'],
     },
    {'name': 'DejaVuSansMono',
     'code_points': ['Box Drawing'] , # also used for code/source/etc.
     'file_names': ['ttf-dejavu/DejaVuSansMono.ttf', 'ttf-dejavu/DejaVuSansMono-Bold.ttf', 'ttf-dejavu/DejaVuSansMono-Oblique.ttf', 'ttf-dejavu/DejaVuSansMono-BoldOblique.ttf'],
     },
    {'name': 'STSong-Light', # built in Adobe font - only used if AR PL UMing HK is not found
     'code_points': ['Bopomofo', 'CJK Radicals Supplement', 'Bopomofo Extended', 'CJK Unified Ideographs Extension A', 'CJK Unified Ideographs', 'Small Form Variants'],
     'type': 'cid',
     },
    {'name': 'HYSMyeongJo-Medium', # built in Adobe font - only used if AR PL UMing HK is not found
     'code_points': ['CJK Compatibility Ideographs', 'Hangul Compatibility Jamo', 'Hangul Syllables'],
     'type': 'cid',
     },
    {'name': 'AR PL UMing HK',
     'code_points': ['CJK Unified Ideographs', 'CJK Strokes', 'CJK Unified Ideographs Extension A', 'Halfwidth and Fullwidth Forms', 'CJK Compatibility Ideographs', 'Small Form Variants', 'Low Surrogates', 'CJK Radicals Supplement', 'Hiragana', 'Katakana', 'Bopomofo', 'Bopomofo Extended'] ,
     'file_names': ['arphic/uming.ttc'],
     },   
    {'name': 'Ezra SIL',
     'code_points': ['Alphabetic Presentation Forms', 'Hebrew'] ,
     'file_names': ['ttf-sil-ezra/SILEOT.ttf'],
     },
#      {'name': 'GFS Artemisia', # fixme open type fonts are not supported by reportlab. currently dejavu is used - seems to work
#       'code_points': ['Greek Extended', 'Greek and Coptic'] ,
#       'file_names': ['ttf-gfs-artemisia/GFSArtemisia.otf', 'ttf-gfs-artemisia/GFSArtemisiaBold.otf', 'ttf-gfs-artemisia/GFSArtemisiaIt.otf', 'ttf-gfs-artemisia/GFSArtemisiaBoldIt.otf'],
#       },
    {'name': 'Nazli',
     'code_points': ['Arabic Presentation Forms-A', 'Arabic', 'Arabic Presentation Forms-B', 'Arabic Supplement'] ,
     'file_names': ['ttf-farsiweb/nazli.ttf'],
     },
    {'name': 'UnBatang',
     'code_points': ['Hangul Syllables', 'Hangul Jamo', 'Hangul Compatibility Jamo'] ,
     'file_names': ['unfonts/UnBatang.ttf'],
     },
    {'name': 'Arundina Serif', 
    'code_points': ['Thai'] ,
     'file_names': ['ttf-thai-arundina/ArundinaSans.ttf', 'ttf-thai-arundina/ArundinaSans-Bold.ttf', 'ttf-thai-arundina/ArundinaSans-Oblique.ttf', 'ttf-thai-arundina/ArundinaSans-BoldOblique.ttf' ],
    },
    {'name': 'Lohit Telugu',
     'code_points': ['Telugu'] ,
     'file_names': ['ttf-telugu-fonts/lohit_te.ttf'],
     },
    {'name': 'Sarai',
     'code_points': ['Gujarati', 'Devanagari'] ,
     'file_names': ['ttf-devanagari-fonts/Sarai_07.ttf'],
     },
    {'name': 'Lohit Punjabi',
     'code_points': ['Gurmukhi'] ,
     'file_names': ['ttf-indic-fonts-core/lohit_pa.ttf'],
     },
    {'name': 'Lohit Oriya',
     'code_points': ['Oriya'] ,
     'file_names': ['ttf-oriya-fonts/lohit_or.ttf'],
     },
    {'name': 'AnjaliOldLipi',
     'code_points': ['Malayalam'] ,
     'file_names': ['ttf-malayalam-fonts/AnjaliOldLipi.ttf'],
     },
    {'name': 'Kedage',
     'code_points': ['Kannada'] ,
     'file_names': ['ttf-kannada-fonts/Kedage-n.ttf', 'ttf-kannada-fonts/Kedage-b.ttf', 'ttf-kannada-fonts/Kedage-i.ttf', 'ttf-kannada-fonts/Kedage-t.ttf'],
     },
    {'name': 'LikhanNormal',
     'code_points': ['Bengali'] ,
     'file_names': ['ttf-bengali-fonts/LikhanNormal.ttf'],
     },
    {'name': 'Lohit Tamil',
     'code_points': ['Tamil'] ,
     'file_names': ['ttf-indic-fonts-core/lohit_ta.ttf'],
     },
    {'name': 'Linux Libertine',
     'code_points': ['Cyrillic'] ,
     'file_names': ['linux-libertine/LinLibertine_Re.ttf', 'linux-libertine/LinLibertine_Bd.ttf', 'linux-libertine/LinLibertine_It.ttf', 'linux-libertine/LinLibertine_BI.ttf', ],
     },
    ]


class RLFontSwitcher(FontSwitcher):

    def __init__(self):
        FontSwitcher.__init__(self)
        self.font_paths = []
        self.force_font = None
        
    def registerFontDefinitionList(self, font_list):
        for font in font_list:
            if not font['name'] or not self.fontInstalled(font):
                continue            
            self.registerFont(font['name'], code_points=font.get('code_points'))
                     
    def fakeHyphenate(self, font_list):
        breakChars = ['/', '.', '+', '-', '_', '?']
        zws = '<font fontSize="1"> </font>'        
        res = []
        for txt, font in font_list:
            for breakChar in breakChars:
                txt = txt.replace(breakChar, breakChar + zws)
            res.append((txt, font))
        return res
    
    def fontifyText(self, txt, break_long=False):
        if self.force_font:
            return '<font name="%s">%s</font>' % (self.force_font, txt)
        font_list = self.getFontList(txt)
        if break_long:
            font_list = self.fakeHyphenate(font_list)

        res = []
        for txt, font in font_list:
            if font != self.default_font:
                res.append('<font name="%s">%s</font>' % (font, txt))
            else:
                res.append(txt)

        return ''.join(res)
        

    def fontInstalled(self, font_def):
        if font_def.get('type') == 'cid':
            return True
        for file_name in font_def.get('file_names'):
            if not self.getAbsFontPath(file_name):
                print "font not found:", file_name
                return False
        return True
        

    def getAbsFontPath(self, file_name):
        for base_dir in self.font_paths:
            full_path = os.path.join(base_dir, file_name)
            if os.path.exists(full_path):
                return full_path
        return None

    def registerReportlabFonts(self, font_list):
        font_variants = ['', 'bold', 'italic', 'bolditalic']
        for font in font_list:
            if not font.get('name'):
                continue
            if font.get('type') == 'cid':
                pdfmetrics.registerFont(UnicodeCIDFont(font['name']))
            else:
                for (i, font_variant) in enumerate(font_variants):
                    if i == len(font.get('file_names')) or not self.fontInstalled(font):
                        break
                    full_font_name = font['name'] + font_variant
                    pdfmetrics.registerFont(TTFont(full_font_name,  self.getAbsFontPath(font.get('file_names')[i]) ))
                    italic = font_variant in ['italic', 'bolditalic']
                    bold = font_variant in ['bold', 'bolditalic']
                    addMapping(font['name'], bold, italic, full_font_name)
