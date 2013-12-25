# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

from common import GOOGLE_QUERY, MEDIA_VIDEO, MEDIA_DOCUMENT, GOOGLE_GET_RESULTS

providers = (
    dict(
        name='pdfspider.com',
        query_url=GOOGLE_QUERY,
        get_results=GOOGLE_GET_RESULTS,
        supported_media=(MEDIA_DOCUMENT,)
    ),
)
