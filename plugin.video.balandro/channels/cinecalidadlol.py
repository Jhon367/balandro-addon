# -*- coding: utf-8 -*-

import re

from platformcode import config, logger, platformtools
from core.item import Item
from core import httptools, scrapertools, servertools, tmdb


host = 'https://ww3.cinecalidad.link/'


def do_downloadpage(url, post=None, headers=None):
    # ~ por si viene de enlaces guardados
    ant_hosts = ['https://cinecalidad.lol/', 'https://cinecalidad.link/']

    for ant in ant_hosts:
        url = url.replace(ant, host)

    raise_weberror = True
    if '/fecha-de-lanzamiento/' in url: raise_weberror = False

    data = httptools.downloadpage(url, post=post, headers=headers, raise_weberror=raise_weberror).data

    return data


def mainlist(item):
    logger.info()
    itemlist = []

    itemlist.append(item.clone( title = 'Buscar ...', action = 'search', search_type = 'all', text_color = 'yellow' ))

    itemlist.append(item.clone( title = 'Películas', action = 'mainlist_pelis', text_color = 'deepskyblue' ))
    itemlist.append(item.clone( title = 'Series', action = 'mainlist_series', text_color = 'hotpink' ))

    return itemlist


def mainlist_pelis(item):
    logger.info()
    itemlist = []

    itemlist.append(item.clone( title = 'Buscar película ...', action = 'search', search_type = 'movie', text_color = 'deepskyblue' ))

    itemlist.append(item.clone( title = 'En castellano:', folder=False, text_color='plum' ))
    itemlist.append(item.clone( title = ' - Catálogo', action = 'list_all', url = host + 'espana/?ref=es', search_type = 'movie' ))
    itemlist.append(item.clone( title = ' - Más destacadas', action = 'destacadas', url = host + 'espana/?ref=es', search_type = 'movie' ))
    itemlist.append(item.clone( title = ' - En 4K', action = 'list_all', url = host + 'genero-de-la-pelicula/peliculas-en-calidad-4k/?ref=es', search_type = 'movie' ))
    itemlist.append(item.clone( title = ' - Por género', action='generos', search_type = 'movie', group = '?ref=es' ))
    itemlist.append(item.clone( title = ' - Por año', action='anios', search_type = 'movie', group = '?ref=es' ))


    itemlist.append(item.clone( title = 'En latino:', folder=False, text_color='plum' ))
    itemlist.append(item.clone( title = ' - Catálogo', action = 'list_all', url = host, search_type = 'movie' ))
    itemlist.append(item.clone( title = ' - Más destacadas', action = 'destacadas', url = host, search_type = 'movie' ))
    itemlist.append(item.clone( title = ' - En 4K', action = 'list_all', url = host + 'genero-de-la-pelicula/peliculas-en-calidad-4k/', search_type = 'movie' ))
    itemlist.append(item.clone( title = ' - Por género', action='generos', search_type = 'movie' ))
    itemlist.append(item.clone( title = ' - Por año', action='anios', search_type = 'movie' ))

    return itemlist


def mainlist_series(item):
    logger.info()
    itemlist = []

    itemlist.append(item.clone( title = 'Buscar serie ...', action = 'search', search_type = 'tvshow', text_color = 'hotpink' ))

    itemlist.append(item.clone( title = 'En castellano:', folder=False, text_color='plum' ))
    itemlist.append(item.clone( title = ' - Catálogo', action = 'list_all', url = host + 'ver-serie/?ref=es', search_type = 'tvshow' ))
    itemlist.append(item.clone( title = ' - Últimas', action = 'destacadas', url = host + '?ref=es', search_type = 'tvshow' ))
    itemlist.append(item.clone( title = ' - Por género', action='generos', search_type = 'tvshow', group = '?ref=es' ))

    itemlist.append(item.clone( title = 'En latino:', folder=False, text_color='plum' ))
    itemlist.append(item.clone( title = ' - Catálogo', action = 'list_all', url = host + 'ver-serie/', search_type = 'tvshow' ))
    itemlist.append(item.clone( title = ' - Últimas', action = 'destacadas', url = host, search_type = 'tvshow' ))
    itemlist.append(item.clone( title = ' - Por género', action='generos', search_type = 'tvshow' ))

    return itemlist


def generos(item):
    logger.info()
    itemlist = []

    data = do_downloadpage(host)

    bloque = scrapertools.find_single_match(data, '<ul id="menu-menu"(.*?)<a id="close_menu"')

    matches = re.compile('<a href="(.*?)">(.*?)</a>').findall(bloque)

    for url, title in matches:
        if title == '4K UHD': continue
        elif title == 'Estrenos': continue
        elif title == 'Destacadas': continue
        elif title == 'Series': continue

        url = host[:-1] + url

        if item.group == '?ref=es': url = url + item.group

        itemlist.append(item.clone( title = title, action = 'list_all', url = url ))

    return sorted(itemlist, key=lambda x: x.title)


def anios(item):
    logger.info()
    itemlist = []

    from datetime import datetime
    current_year = int(datetime.today().year)

    for x in range(current_year, 1999, -1):
        url = host + 'fecha-de-lanzamiento/' + str(x) + '/'

        if item.group == '?ref=es': url = url + item.group

        itemlist.append(item.clone( title = str(x), url = url, action = 'list_all' ))

    return itemlist


def list_all(item):
    logger.info()
    itemlist = []

    data = do_downloadpage(item.url)
    data = re.sub(r'\n|\r|\t|\s{2}|&nbsp;', '', data)

    matches = scrapertools.find_multiple_matches(data, '<article(.*?)</article>')

    if not matches:
        bloque = scrapertools.find_single_match(data, '<div id="content">(.*?)>Destacadas<')
        matches = scrapertools.find_multiple_matches(bloque, '<div class="home_post_content">(.*?)</div></div>')

    for match in matches:
        title = scrapertools.find_single_match(match, '<h2>.*?">(.*?)</h2>')
        if not title: title = scrapertools.find_single_match(match, 'alt="(.*?)"')

        url = scrapertools.find_single_match(match, ' href="(.*?)"')

        if not url or not title: continue

        plot = scrapertools.find_single_match(match, '<p>.*?">(.*?)</p>').strip()
        thumb = scrapertools.find_single_match(match, 'src="(.*?)"')

        m = re.match(r"^(.*?)\((\d+)\)$", title)
        if m:
            title = m.group(1).strip()
            year = m.group(2)
        else:
            year = '-'

        tipo = 'tvshow' if '/ver-serie/' in url else 'movie'
        sufijo = '' if item.search_type != 'all' else tipo

        if item.search_type == 'movie':
            if '/ver-serie/' in url: continue
        elif item.search_type == 'tvshow':
            if not '/ver-serie/' in url: continue

        if tipo == 'movie':
            itemlist.append(item.clone( action = 'findvideos', url = url, title = title, thumbnail = thumb, fmt_sufijo=sufijo,
                                        contentType = 'movie', contentTitle = title, infoLabels = {'year': year, 'plot': plot} ))

        if tipo == 'tvshow':
            itemlist.append(item.clone( action='temporadas', url = url, title = title, thumbnail = thumb, fmt_sufijo=sufijo,
                                        contentType = 'tvshow', contentSerieName = title,  infoLabels = {'year': '-'} ))

    tmdb.set_infoLabels(itemlist)

    if itemlist:
        next_page = scrapertools.find_single_match(data, "<span class='pages'>.*?class='current'>.*?" + 'href="(.*?)"')
        if next_page:
            if '/page/' in next_page:
                itemlist.append(item.clone( title='Siguientes ...', url = next_page, action = 'list_all', text_color='coral' ))

    return itemlist


def destacadas(item):
    logger.info()
    itemlist = []

    data = do_downloadpage(item.url)
    data = re.sub(r'\n|\r|\t|\s{2}|&nbsp;', '', data)

    bloque = scrapertools.find_single_match(data, '>Destacadas</h2>(.*?)>Herramientas')

    matches = scrapertools.find_multiple_matches(bloque, '<a(.*?)</li>')

    for match in matches:
        url = scrapertools.find_single_match(match, 'href="(.*?)"')
        title = scrapertools.find_single_match(match, 'title="(.*?)"')

        if not url or not title: continue

        if item.search_type == 'movie':
            if '/ver-serie/' in url: continue
        else:
            if '/ver-pelicula/' in url: continue

        thumb = scrapertools.find_single_match(match, 'data-src="(.*?)"')

        m = re.match(r"^(.*?)\((\d+)\)$", title)
        if m:
            title = m.group(1).strip()
            year = m.group(2)
        else:
            year = '-'

        if item.search_type == 'movie':
            itemlist.append(item.clone( action = 'findvideos', url = url, title = title, thumbnail = thumb,
                                        contentType = 'movie', contentTitle = title, infoLabels = {'year': year} ))
        else:
            itemlist.append(item.clone( action='temporadas', url = url, title = title, thumbnail = thumb,
                                        contentType = 'tvshow', contentSerieName = title,  infoLabels = {'year': '-'} ))

    tmdb.set_infoLabels(itemlist)

    return itemlist


def temporadas(item):
    logger.info()
    itemlist = []

    data = do_downloadpage(item.url)

    matches = scrapertools.find_multiple_matches(data, '<span data-tab="(.*?)"')

    for tempo in matches:
        title = 'Temporada ' + tempo

        if len(matches) == 1:
            platformtools.dialog_notification(item.contentSerieName.replace('&#038;', '&').replace('&#8217;', "'"), 'solo [COLOR tan]' + title + '[/COLOR]')
            item.contentType = 'season'
            item.contentSeason = tempo
            itemlist = episodios(item)
            return itemlist

        itemlist.append(item.clone( action = 'episodios', title = title, url = item.url, contentType = 'season', contentSeason = tempo ))

    tmdb.set_infoLabels(itemlist)

    return itemlist


def tracking_all_episodes(item):
    return episodios(item)


def episodios(item):
    logger.info()
    itemlist = []

    if not item.page: item.page = 0
    if not item.perpage: item.perpage = 50

    data = do_downloadpage(item.url)
    data = re.sub(r'\n|\r|\t|\s{2}|&nbsp;', '', data)

    bloque = scrapertools.find_single_match(data, '<b>Temporada ' + str(item.contentSeason) + '(.*?)</div></div>')

    matches = scrapertools.find_multiple_matches(bloque, '<li class="mark-.*?data-src="(.*?)".*?<div class="numerando">(.*?)</div>.*?<a href="(.*?)">(.*?)</a')

    if item.page == 0:
        sum_parts = len(matches)
        if sum_parts > 250:
            if platformtools.dialog_yesno(item.contentSerieName.replace('&#038;', '&').replace('&#8217;', "'"), '¿ Hay [COLOR yellow][B]' + str(sum_parts) + '[/B][/COLOR] elementos disponibles, desea cargarlos en bloques de [COLOR cyan][B]250[/B][/COLOR] elementos?'):
                platformtools.dialog_notification('CineCalidadLol', '[COLOR cyan]Cargando elementos[/COLOR]')
                item.perpage = 250

    for thumb, temp_epis, url, title in matches[item.page * item.perpage:]:
        epis = scrapertools.find_single_match(temp_epis, '.*?E(.*?)$')
        if not epis: epis = '0'

        titulo = str(item.contentSeason) + 'x' + str(epis) + ' ' + title

        itemlist.append(item.clone( action='findvideos', url = url, title = titulo, thumbnail = thumb,
                                    contentType = 'episode', contentSeason = item.contentSeason, contentEpisodeNumber = epis ))

        if len(itemlist) >= item.perpage:
            break

    tmdb.set_infoLabels(itemlist)

    if len(matches) > ((item.page + 1) * item.perpage):
        itemlist.append(item.clone( title = "Siguientes ...", action = "episodios", page = item.page + 1, perpage = item.perpage, text_color='coral' ))

    return itemlist


def findvideos(item):
    logger.info()
    itemlist = []

    IDIOMAS = {'latino': 'Lat', 'castellano': 'Esp', 'subtitulado': 'Vose'}

    lang = 'Lat'

    if '?ref=es' in item.url: lang = 'Esp'

    data = do_downloadpage(item.url)

    ses = 0

    if '>VER ONLINE<' in data:
        bloque = scrapertools.find_single_match(data, '>VER ONLINE<(.*?)>DESCARGAR<')

        matches = scrapertools.find_multiple_matches(bloque, '<li id="player-option-.*?data-option="(.*?)".*?data-src=.*?/flags/(.*?).png')

        for url, idio in matches:
            ses += 1

            if '/play/' in url: continue
            elif '/netu' in url or '/waaw' in url or '/hqq' in url: continue
            elif 'youtube' in url: continue

            servidor = servertools.get_server_from_url(url)
            servidor = servertools.corregir_servidor(servidor)

            url = servertools.normalize_url(servidor, url)

            qlty = '1080'

            language = lang
            if not '?ref=es' in item.url:
               if idio == 'mx': language = 'Lat'
               elif idio == 'es': language = 'Esp'
               elif idio == 'en': language = 'Vose'

            itemlist.append(Item (channel = item.channel, action = 'play', server = servidor, title = '', url = url, quality = qlty, language = language ))

    if '>DESCARGAR<' in data:
        bloque = scrapertools.find_single_match(data, '>DESCARGAR<(.*?)</ul>')

        matches = scrapertools.find_multiple_matches(bloque, 'href="(.*?)".*?">(.*?)</li>')

        for url, servidor in matches:
            ses += 1

            if url == '#':
                ses = ses - 1
                continue
            elif not servidor:
                ses = ses - 1
                continue
            elif '<div class="episodiotitle">' in servidor:
                ses = ses - 1
                continue

            if '<span' in servidor: servidor = scrapertools.find_single_match(servidor, '(.*?)<span')

            servidor = servidor.lower().strip()

            qlty = '1080'

            if '4k' in servidor or '4K' in servidor:
               qlty = '4K'
               servidor = servidor.replace('4k', '').replace('4K', '').strip()

            if 'subtítulo' in servidor: continue
            elif 'forzado' in servidor: continue

            elif servidor == '1fichier': continue
            elif servidor == 'turbobit': continue

            elif servidor == 'utorrent': servidor = 'torrent'
            elif 'torrent' in servidor: servidor = 'torrent'

            other = ''
            if url.startswith('?download='):
                other = 'D'
                url = item.url.replace('?ref=es', '') + url

            itemlist.append(Item (channel = item.channel, action = 'play', server = servidor, title = '', url = url,
                                  quality = qlty, language = lang, other = other ))

    if not itemlist:
        if not ses == 0:
            platformtools.dialog_notification(config.__addon_name, '[COLOR tan][B]Sin enlaces Soportados[/B][/COLOR]')
            return

    return itemlist


def play(item):
    logger.info()
    itemlist = []

    url = item.url

    servidor = item.server

    if url.startswith(host):
        data = do_downloadpage(url)

        url = scrapertools.find_single_match(data, 'target="_blank" href="(.*?)"')
        if not url: url = scrapertools.find_single_match(data, 'target="_blank" value="(.*?)"')

        if url:
            url = url.replace('&amp;', '&')

            if '/hqq.' in url or '/waaw.' in url or '/netu.' in url:
                return 'Requiere verificación [COLOR red]reCAPTCHA[/COLOR]'

            elif '/1fichier.' in url:
                return 'Servidor NO soportado [COLOR tan]1fichier[/COLOR]'

            if url:
                servidor = servertools.get_server_from_url(url)
                servidor = servertools.corregir_servidor(servidor)

                url = servertools.normalize_url(servidor, url)

                if servidor == 'mega':
                    if url.startswith('#'): url = 'https://mega.nz/' + url
                    elif not url.startswith('http'): url = 'https://mega.nz/file/' + url

    if url:
        if url.endswith('.torrent'):
            itemlist.append(item.clone( url = url, server = 'torrent' ))
            return itemlist

        elif 'magnet:?' in url:
            itemlist.append(item.clone( url = url, server = 'torrent' ))
            return itemlist

        itemlist.append(item.clone(url = url, servidor = servidor))

    return itemlist


def search(item, texto):
    logger.info()
    try:
        item.url = host + '?s=' + texto.replace(" ", "+")
        return list_all(item)
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []
