# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import os


USER_AGENT = ('Mozilla/5.0 (X11; CrOS armv7l 5116.3.0) AppleWebKit/537.36' +
      '(KHTML, like Gecko) Chrome/33.0.1750.5 Safari/537.36')

GOOGLE_QUERY = 'GOOGLE_QUERY'

GOOGLE_GET_RESULTS = lambda soup: map(
    lambda result: dict(
        title=result.text,
        url=result.get('href')),
    map(
        lambda result: result.find('a'),
        soup.findAll('h3', {'class': 'r'})))
MEDIA_TYPE_EXTENSIONS = dict(
    video=['avi', 'mkv', 'flv', 'wmv', 'mp4'],
    document=['epub', 'mobi', 'zip', 'rar'])

DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '../data')

MEDIA_VIDEO = 'video'

MEDIA_DOCUMENT = 'document'

REAL_DEBRID_REGEX = (
    r'1fichier.com|1st-files.com|2shared.com|4shared.com|aetv.com' +
    '|bayfiles.com|bitshare.com|canalplus.fr|cbs.com|cloudzer.net|crocko.com' +
    '|cwtv.com|dailymotion.com|dengee.net|depfile.com|dizzcloud.com|dl.free.fr' +
    '|extmatrix.com|filebox.com|filecloud.io|filefactory.com|fileflyer.com' +
    '|fileover.net|filepost.com|filerio.com|filesabc.com|filesend.net|filesflash.co' +
    '|filesmonster.com|freakshare.net|gigasize.com|hipfile.com|hotfile.co' +
    '|hugefiles.net|hulkshare.com|hulu.com|jumbofiles.com|justin.tv|keep2share.c' +
    '|letitbit.net|load.to|mediafire.com|mega.co.nz|megashares.com|mixturevideo.co' +
    '|netload.in|nowdownload.eu|nowvideo.eu|purevid.com|putlocker.com|rapidgator.net' +
    '|rapidshare.com|redtube.com|rutube.ru|scribd.com|sendspace.com|share-online.bi' +
    '|sharefiles.co|shareflare.net|slingfile.com|sockshare.com|soundcloud.co' +
    '|speedyshare.com|turbobit.net|ultramegabit.com|unibytes.co' +
    '|uploaded.to|uploaded.net|ul.to|uploadhero.co|uploading.com|uptobox.co' +
    '|userporn.com|veevr.com|vimeo.com|vip-file.com|wat.tv|youporn.com|youtube.com'
)
