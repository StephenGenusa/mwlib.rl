#! /usr/bin/env python
#! -*- coding:utf-8 -*-

# Copyright (c) 2007, 2008, 2009 PediaPress GmbH
# See README.txt for additional licensing information.

import os
import subprocess
import shutil

import mwlib.ext
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.platypus.tables import Table

from mwlib.rl import pdfstyles
from mwlib.rl import fontconfig

import pickle

class TocRenderer(object):

    def __init__(self):
        font_switcher = fontconfig.RLFontSwitcher()
        font_switcher.font_paths = fontconfig.font_paths
        font_switcher.registerDefaultFont(pdfstyles.default_font)
        font_switcher.registerFontDefinitionList(fontconfig.fonts)
        font_switcher.registerReportlabFonts(fontconfig.fonts)

        
    def build(self, pdfpath, toc_entries, has_title_page=False, rtl=False):
        outpath = os.path.dirname(pdfpath)
        tocpath = os.path.join(outpath, 'toc.pdf')
        finalpath = os.path.join(outpath, 'final.pdf')
        self.renderToc(tocpath, toc_entries, rtl=rtl)
        return self.combinePdfs(pdfpath, tocpath, finalpath, has_title_page)

    def _getColWidths(self):
        p = Paragraph('<b>%d</b>' % 9999, pdfstyles.text_style(mode='toc_article', text_align='right'))        
        w, h = p.wrap(0, pdfstyles.print_height)
        # subtracting 30pt below is *probably* necessary b/c of the table margins
        return [pdfstyles.print_width - w - 30, w]
    
    def renderToc(self, tocpath, toc_entries, rtl):
        log.info("beginning renderToc")
        # Workaround for failed TOC rendering
		"""
        if os.path.isfile('toc.pkl'):
            _ = self.return_contents
            pkl_file = open('toc.pkl', 'rb')
            toc_entries = pickle.load(pkl_file)
            pkl_file.close()
            rtl=False
        else:
            output = open('toc.pkl', 'wb')
            pickle.dump(toc_entries, output)
            output.close()
		"""

        doc = SimpleDocTemplate(tocpath, pagesize=(pdfstyles.page_width, pdfstyles.page_height))
        elements = []
        elements.append(Paragraph(_('Contents'), pdfstyles.heading_style(mode='chapter', text_align='left' if not rtl else 'right')))
        toc_table =[]
        styles = []
        col_widths = self._getColWidths()
        for row_idx, (lvl, txt, page_num) in enumerate(toc_entries):
            if lvl == 'article':
                page_num = str(page_num)
            elif lvl == 'chapter':
                page_num = '<b>%d</b>' % page_num
                styles.append(('TOPPADDING', (0, row_idx), (-1, row_idx), 10))
            elif lvl == 'group':
                page_num = ' '
                styles.append(('TOPPADDING', (0, row_idx), (-1, row_idx), 10))

            toc_table.append([
                Paragraph(txt, pdfstyles.text_style(mode='toc_%s' % str(lvl), text_align='left')),
                Paragraph(page_num, pdfstyles.text_style(mode='toc_article', text_align='right'))
                ])
        t = Table(toc_table, colWidths=col_widths)
        t.setStyle(styles)
        elements.append(t)
        doc.build(elements)
        log.info("ending renderToc")

    def run_cmd(self, cmd):
        try:
            retcode = subprocess.call(cmd, stdout=subprocess.PIPE)
        except OSError:
            retcode = 1
        return retcode

    def pdftk(self, pdfpath, tocpath, finalpath, has_title_page):
        cmd =  ['pdftk',
                'A=%s' % pdfpath,
                'B=%s' % tocpath,
                ]
        if not has_title_page:
            cmd.extend(['cat', 'B', 'A'])
        else:
            cmd.extend(['cat', 'A1', 'B', 'A2-end'])
        cmd.extend(['output', finalpath])
        return self.run_cmd(cmd)

    def pdfsam(self, pdfpath, tocpath, finalpath, has_title_page):
        cmd = ['pdfsam-console']
        if not has_title_page:
            cmd.extend(['-f', tocpath, '-f', pdfpath])
        else:
            cmd.extend(['-f', pdfpath, '-f', tocpath, '-f', pdfpath, '-u', '1-1:all:2-:'])
        cmd.extend(['-o', finalpath, '-overwrite', 'concat'])
        return self.run_cmd(cmd)

    def combinePdfs(self, pdfpath, tocpath, finalpath, has_title_page):
        if os.path.splitext(pdfpath)[1] == '.pdf':
            safe_pdfpath = pdfpath
        else:
            safe_pdfpath = pdfpath + '.pdf'
            shutil.move(pdfpath, safe_pdfpath)
        retcode = self.pdfsam(safe_pdfpath, tocpath, finalpath, has_title_page=has_title_page)
        if retcode != 0:
            retcode = self.pdftk(safe_pdfpath, tocpath, finalpath, has_title_page=has_title_page)
        if retcode == 0:
            shutil.move(finalpath, pdfpath)
        if os.path.exists(tocpath):
            os.unlink(tocpath)
        return retcode

if __name__ == '__main__':
    # Workaround for failed TOC rendering
    toc_renderer = TocRenderer()
    tocpath=os.path.join(os.path.expanduser('~/Documents'), "toc.pdf")
    pdfpath=tocpath=os.path.join(os.path.expanduser('~/Documents'), "tempA.pdf")
    finalpath=tocpath=os.path.join(os.path.expanduser('~/Documents'), "Final Product.pdf")
    toc_renderer.renderToc(tocpath, [], False)
    toc_renderer.combinePdfs(pdfpath, tocpath, finalpath, True)
