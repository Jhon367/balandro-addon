# -*- coding: utf-8 -*-

import sys

PY3 = False
if sys.version_info[0] >= 3: PY3 = True

import re, os, string

from platformcode import config, logger, platformtools
from core.item import Item
from core import httptools, scrapertools, tmdb


host = 'https://dontorrent.cx/'


# ~ por si viene de enlaces guardados
ant_hosts = ['https://dontorrents.org/', 'https://dontorrents.net/', 'https://dontorrent.one/',
             'https://dontorrent.app/', 'https://dontorrent.lol/', 'https://dontorrent.nz/', 'https://dontorrent.rip/',
             'https://dontorrent.vip/', 'https://dontorrent.ws/', 'https://dontorrent.win/', 'https://dontorrent.rs/',
             'https://dontorrent.bz/', 'https://dontorrent.men/', 'https://dontorrent.fit/', 'https://dontorrent.art/',
             'https://dontorrent.fun/', 'https://dontorrent.se/', 'https://dontorrent.pw/', 'https://dontorrent.li/',
             'https://dontorrent.it/', 'https://dontorrent.red/', 'https://dontorrent.nu/', 'https://dontorrent.si/',
             'https://dontorrent.sk/', 'https://dontorrent.eu/', 'https://dontorrent.top/', 'https://dontorrent.pm/',
             'https://dontorrent.re/', 'https://dontorrent.wf/', 'https://dontorrent.run/', 'https://dontorrent.cat/'
             'https://dontorrent.pl/', 'https://dontorrent.tel/', 'https://dontorrent.nl/']

domain = config.get_setting('dominio', 'dontorrents', default='')

if domain:
    if domain in str(ant_hosts): config.set_setting('dominio', '', 'dontorrents')
    else: host = domain


def item_configurar_proxies(item):
    plot = 'Es posible que para poder utilizar este canal necesites configurar algún proxy, ya que no es accesible desde algunos países/operadoras.'
    plot += '[CR]Si desde un navegador web no te funciona el sitio ' + host + ' necesitarás un proxy.'
    return item.clone( title = 'Configurar proxies a usar ... [COLOR plum](si no hay resultados)[/COLOR]', action = 'configurar_proxies', folder=False, plot=plot, text_color='red' )

def configurar_proxies(item):
    from core import proxytools
    return proxytools.configurar_proxies_canal(item.channel, host)


def do_downloadpage(url, post=None, headers=None):
    # ~ por si viene de enlaces guardados
    for ant in ant_hosts:
        url = url.replace(ant, host)

    # ~ data = httptools.downloadpage(url, post=post).data
    data = httptools.downloadpage_proxy('dontorrents', url, post=post, headers=headers).data
    return data


def mainlist(item):
    logger.info()
    itemlist = []

    itemlist.append(Item( channel='actions', action='last_domain_dontorrents', title='Comprobar último dominio vigente [COLOR plum](si no hay resultados)[/COLOR]',
                          thumbnail=config.get_thumb('settings'), text_color='chocolate' ))

    itemlist.append(item_configurar_proxies(item))

    itemlist.append(item.clone( title = 'Buscar ...', action = 'search', search_type = 'all', text_color = 'yellow' ))

    itemlist.append(item.clone( title = 'Películas', action = 'mainlist_pelis', text_color = 'deepskyblue' ))
    itemlist.append(item.clone( title = 'Series', action = 'mainlist_series', text_color = 'hotpink' ))
    itemlist.append(item.clone( title = 'Documentales', action = 'mainlist_documentary', text_color='cyan' ))

    return itemlist


def mainlist_pelis(item):
    logger.info()
    itemlist = []

    itemlist.append(Item( channel='actions', action='last_domain_dontorrents', title='Comprobar último dominio vigente [COLOR plum](si no hay resultados)[/COLOR]',
                          thumbnail=config.get_thumb('settings'), text_color='chocolate' ))

    itemlist.append(item_configurar_proxies(item))

    itemlist.append(item.clone( title = 'Buscar película ...', action = 'search', search_type = 'movie', text_color = 'deepskyblue' ))

    itemlist.append(item.clone( title = 'Catálogo', action = 'list_all', url = host + 'peliculas/page/1', search_type = 'movie' ))

    itemlist.append(item.clone( title = 'Lo último', action = 'list_last', url = host + 'ultimos', search_type = 'movie' ))

    itemlist.append(item.clone( title = 'Por calidad', action = 'calidades',  search_type = 'movie' ))

    itemlist.append(item.clone( title = 'Por género', action = 'generos', search_type = 'movie', tipo = 'genero' ))

    itemlist.append(item.clone( title = 'Por año', action = 'call_post', url = host + 'peliculas/buscar', search_type = 'movie', tipo = 'anyo' ))

    itemlist.append(item.clone( title = 'Por letra (A - Z)', action = 'alfabetico', url = host + 'peliculas/buscar', search_type = 'movie' ))

    return itemlist


def mainlist_series(item):
    logger.info()
    itemlist = []

    itemlist.append(Item( channel='actions', action='last_domain_dontorrents', title='Comprobar último dominio vigente [COLOR plum](si no hay resultados)[/COLOR]',
                          thumbnail=config.get_thumb('settings'), text_color='chocolate' ))

    itemlist.append(item_configurar_proxies(item))

    itemlist.append(item.clone( title = 'Buscar serie ...', action = 'search', search_type = 'tvshow', text_color = 'hotpink' ))

    itemlist.append(item.clone( title = 'Catálogo (alfabético)', action = 'list_all', url = host + 'series/letra-.', search_type = 'tvshow' ))

    itemlist.append(item.clone( title = 'Lo último', action = 'list_last', url = host + 'ultimos', search_type = 'tvshow' ))

    itemlist.append(item.clone( title = 'En HD (alfabético)', action = 'list_all', url = host + 'series/hd/letra-.', search_type = 'tvshow' ))

    itemlist.append(item.clone( title = 'Por letra (A - Z)', action = 'alfabetico', url = host + 'tv-series', search_type = 'tvshow' ))

    return itemlist


def mainlist_documentary(item):
    logger.info()
    itemlist = []

    itemlist.append(Item( channel='actions', action='last_domain_dontorrents', title='Comprobar último dominio vigente [COLOR plum](si no hay resultados)[/COLOR]',
                          thumbnail=config.get_thumb('settings'), text_color='chocolate' ))

    itemlist.append(item_configurar_proxies(item))

    itemlist.append(item.clone( title = 'Buscar documental ...', action = 'search', search_type = 'documentary', text_color='cyan' ))

    itemlist.append(item.clone( title = 'Catálogo (alfabético)', action = 'list_all', url = host + 'documentales/letra-.', search_type = 'documentary'))

    itemlist.append(item.clone( title = 'Lo último', action = 'list_last', url = host + 'ultimos', search_type = 'documentary' ))

    itemlist.append(item.clone( title = 'Por letra (A - Z)', action = 'alfabetico', url = host + 'documentales', search_type = 'documentary' ))

    return itemlist


def calidades(item):
    logger.info()
    itemlist = []

    itemlist.append(item.clone( title = 'En 4K', action = 'list_all', url = host + 'peliculas/4K/page/1', search_type = 'movie' ))
    itemlist.append(item.clone( title = 'En HD', action = 'list_all', url = host + 'peliculas/hd/page/1', search_type = 'movie' ))

    return itemlist


def generos(item):
    logger.info()
    itemlist = []

    genres = ['Acción',
       'Animación',
       'Aventuras',
       'Bélica',
       'Biográfica',
       'Ciencia Ficción',
       'Cine Negro',
       'Comedia',
       'Crimen',
       'Documental',
       'Drama',
       'Fantasía',
       'Musical',
       'Romántica',
       'Suspense',
       'Terror',
       'Western'
       ]

    for genre in genres:
        itemlist.append(item.clone( action = "call_post", title = genre, url = host + 'peliculas/buscar', tipo='genero', genre=genre ))

    return itemlist


def alfabetico(item):
    logger.info()
    itemlist = []

    for letra in string.ascii_uppercase:
        itemlist.append(item.clone(action="call_post", title=letra, letra=letra, tipo='letra'))

    return itemlist


def list_all(item):
    logger.info()
    itemlist = []

    data = do_downloadpage(item.url)
    data = re.sub(r'\n|\r|\t|\s{2}|&nbsp;', '', data)

    if item.search_type == "movie":
        matches = re.compile(r'<a href="([^"]+)">\s*<img.*?src="([^"]+)').findall(data)

        for url, thumb in matches:
            title = os.path.basename(os.path.normpath(url)).replace("-", " ")
            if "4K" in title: title = title.split("4K")[0]
            if "ESP" in title: title = title.split("ESP")[0]

            thumb if "http" in thumb else "https:" + thumb

            itemlist.append(item.clone( action='findvideos', url=host[:-1] + url, title=title, thumbnail=thumb,
                                        contentType='movie', contentTitle=title, infoLabels={'year': "-"} ))

    elif item.search_type== 'tvshow':
        matches = re.compile(r"<a href='([^']+)'>([^<]+)").findall(data)

        for url, title in matches:
            if "-" in title: SerieName = title.split("-")[0]
            else: SerieName = title
            itemlist.append(item.clone( action='episodios', url=host[:-1] + url, title=title, 
                                        contentType = 'tvshow', contentSerieName = SerieName, infoLabels={'year': "-"} ))

    else:
        matches = re.compile(r"<a href='([^']+)'>([^<]+)").findall(data)

        for url, title in matches:
            itemlist.append(item.clone( action = 'findvideos', url = host[:-1] + url, title = title,
                                        contentType = 'movie', contentTitle = title, contentExtra = 'documentary', infoLabels={'year': "-"} ))

    tmdb.set_infoLabels(itemlist)

    next_url = scrapertools.find_single_match(data, '<a class="page-link" href="([^"]+)">Siguiente')
    if next_url:
        next_url = host[:-1] + next_url

        itemlist.append(item.clone( title='Siguientes ...', url=next_url, action='list_all', text_color='coral' ))

    return itemlist


def list_last(item):
    logger.info()
    itemlist = []

    if item.search_type == "movie": search_type = "PELÍCULAS"
    elif item.search_type == "tvshow": search_type = "SERIES"
    elif item.search_type == "documentary": search_type = "DOCUMENTALES"

    data = do_downloadpage(item.url)

    match = re.compile("""(?s)<div class="h5 text-dark">%s:<\/div>(.*?)<br><br>""" % (search_type)).findall(data)[0]
    matches = re.compile(r"""<span class="text-muted">\d+-\d+-\d+<\/span> <a href='([^']+)' class="text-primary">([^<]+)""").findall(match)

    for url, title in matches:
        if "(" in title: title = title.split("(")[0]

        if item.search_type== 'movie':
            itemlist.append(item.clone( action='findvideos', url=host + url, title=title,
                                        contentType=item.search_type, contentTitle=title, infoLabels={'year': "-"} ))
        else:
            itemlist.append(item.clone( action='episodios', url=host + url, title=title, 
                                        contentType=item.search_type, contentSerieName=title, infoLabels={'year': "-"} ))

    tmdb.set_infoLabels(itemlist)

    return itemlist


def call_post(item):
    logger.info()

    if not item.page: item.page = 1

    if item.tipo == 'anyo':
        val = platformtools.dialog_numeric(0, "Indicar el año a buscar", default="")
        if not val: return

        item.post = "campo=%s&valor=%s&valor2=&valor3=&valor4=&pagina=%s" % ('anyo', val, str(item.page))

    elif item.tipo == 'genero':
        item.post = "campo=%s&valor=&valor2=%s&valor3=&valor4=&pagina=%s" % ('genero', item.genre, str(item.page))

    elif item.tipo == 'letra':
        if item.search_type == 'movie':
            item.post = "campo=%s&valor=&valor2=&valor3=%s&valor4=&pagina=%s" % ('letra', item.letra, str(item.page))
        else:
            if item.search_type == "tvshow": tipo = "series"
            else: tipo = "documentales"
            item.url = host + "%s/letra-%s" %(tipo, item.letra.lower())
            return list_all(item)
 
    return list_post(item)


def list_post(item):
    logger.info()
    itemlist = []

    data = do_downloadpage(item.url, post=item.post)
    data = re.sub(r'\n|\r|\t|\s{2}|&nbsp;', '', data)

    patron = '''<a class="position-relative" href="([^"]+)" data-toggle="popover" '''
    patron += '''data-content="<div><p class='lead text-dark mb-0'>([^<]+)'''
    patron += '''<\/p><hr class='my-2'><p>([^<]+).*?src='([^']+)'''

    matches = re.compile(patron).findall(data)

    for url, title, info, thumb in matches:
        itemlist.append(item.clone( action='findvideos', url=host[:-1] + url, title=title, thumbnail=thumb if "http" in thumb else "https:" + thumb,
                                            contentType=item.contentType, contentTitle=title, infoLabels={'year': "-", 'plot': info} ))

    tmdb.set_infoLabels(itemlist)

    if itemlist:
        if item.post:
            next_page = scrapertools.find_single_match(item.post, '(.*?)pagina=')
            if next_page:
                item.page = item.page + 1
                exist_page = scrapertools.find_single_match(data, "<option value='" + str(item.page) + "'")

                if exist_page:
                     post = next_page + 'pagina=' + str(item.page)

                     itemlist.append(item.clone( title='Siguientes ...', url=item.url, action='list_post', post=post, text_color='coral' ))

    return itemlist


def episodios(item):
    logger.info()
    itemlist = []

    data = do_downloadpage(item.url)

    patron = """<td style='vertical-align: middle;'>([^<]+)<\/td>\s*<td>"""
    patron += """<a class="text-white bg-primary rounded-pill d-block shadow-sm text-decoration-none my-1 py-1" """
    patron += """style="font-size: 18px; font-weight: 500;" href='([^']+)'"""

    matches = re.compile(patron).findall(data)

    if not matches:
        matches = scrapertools.find_multiple_matches(data, "<td style='vertical-align.*?>(.*?)</td>.*?<a.*?href='(.*?)'.*?download>Descargar</a>.*?</tr>")

    for title, url in matches:
        s_e = scrapertools.get_season_and_episode(title)

        try:
           season = int(s_e.split("x")[0])
           episode = s_e.split("x")[1]
        except:
           season = 0
           episode = 0

        if url.startswith("//"): url = "https:" + url

        itemlist.append(item.clone( action='findvideos', url=url, title="%s %s" %(title, item.contentSerieName), 
                                    language = 'Esp', contentType = 'episode', contentEpisodeNumber = episode ))

    tmdb.set_infoLabels(itemlist)

    return itemlist


def findvideos(item):
    logger.info()
    itemlist = []

    if item.contentType == "episode":
        url = item.url
        qlty = ''

    elif not item.contentType == "tvshow":
        data = do_downloadpage(item.url)

        qlty = scrapertools.find_single_match(data, '<b class="bold">Formato:</b>(.*?)</p>').strip()

        patron = '<div class="text-center">.*?'
        patron += "href='([^']+)'.*?download.*?Descargar</a>"
        url = scrapertools.find_single_match(data, patron)

        if not url:
            if item.contentType == 'documentary' or item.contentExtra == 'documentary':
                patron = '<b class="bold">Formato:</b>.*?'
                patron += "href='([^']+)'.*?download.*?Descargar</a>"
                url = scrapertools.find_single_match(data, patron)

        if url:
            url = url if url.startswith("http") else "https:" + url
    else:
        url = item.url
        qlty = ''

    if url:
        if not url == 'https:':
           lang = 'Esp'

           itemlist.append(Item( channel = item.channel, action = 'play', title = '', language = lang, quality = qlty, url = url, server = 'torrent'))

    return itemlist


def play(item):
    logger.info()
    itemlist = []

    if item.url.endswith('.torrent'):
        if config.get_setting('proxies', item.channel, default=''):
            if PY3:
                from core import requeststools
                data = requeststools.read(item.url, 'dontorrents')
            else:
                data = do_downloadpage(item.url)

            if data:
                if '<h1>Not Found</h1>' in str(data) or '<!DOCTYPE html>' in str(data) or '<!DOCTYPE>' in str(data):
                    return 'Archivo [COLOR red]Inexistente[/COLOR]'

                file_local = os.path.join(config.get_data_path(), "temp.torrent")
                with open(file_local, 'wb') as f: f.write(data); f.close()

                itemlist.append(item.clone( url = file_local, server = 'torrent' ))
        else:
            itemlist.append(item.clone( url = item.url, server = 'torrent' ))

    return itemlist


def list_search(item):
    logger.info()
    itemlist = []

    headers = {'Referer': host}

    data = do_downloadpage(item.url, headers=headers)

    patron = "<a href='(.*?)'.*?"
    patron += 'class="text-decoration-none">(.*?)</a>'

    matches = re.compile(patron).findall(data)

    for url, title in matches:
        title = title.replace('<span class="text-secondary">', '').replace('<span class="text-secondary" >', '').replace('</span>', '').strip()

        if not url or not title: continue

        if "pelicula" in url:
            contentType = "movie"
        elif "documental" in url:
            contentType = "documentary"
        else:            
            contentType = "tvshow"

        if item.search_type not in ['all', contentType]: continue

        sufijo = ''
        if item.search_type == 'all': 
            sufijo = contentType
            if sufijo == "documentary":
                sufijo = '[COLOR yellowgreen](documental)[/COLOR]'

        if contentType == 'tvshow':
            if not item.search_type == 'all':
                if item.search_type == "movie": continue
            itemlist.append(item.clone( action='episodios', url=host[:-1] + url, title=title, fmt_sufijo=sufijo, 
                                        contentType = 'tvshow', contentSerieName = title, infoLabels={'year': "-"} ))
        else:
            if not item.search_type == 'all':
                if item.search_type == "tvshow": continue

            if contentType == 'documentary':
                itemlist.append(item.clone( action = 'findvideos', url = host[:-1] + url, title = title, fmt_sufijo=sufijo,
                                            contentType = 'movie', contentTitle = title, contentExtra = 'documentary', infoLabels={'year': "-"} ))
            else:
                itemlist.append(item.clone( action='findvideos', url=host[:-1] + url, title=title, fmt_sufijo=sufijo,
                                            contentType='movie', contentTitle=title, infoLabels={'year': "-"} ))

    tmdb.set_infoLabels(itemlist)

    if itemlist:
        if '>Siguiente<' in data:
             next_page = scrapertools.find_single_match(data, '<a class="page-link".*?current="page">.*?li class="page-item"><a class="page-link".*?href="(.*?)"')

             if next_page:
                 next_page = host[:-1] + next_page

                 itemlist.append(item.clone( title='Siguientes ...', url=next_page, action='list_search', text_color='coral' ))

    return itemlist

def search(item, texto):
    logger.info()
    try:
       item.url = host + 'buscar/' + texto
       return list_search(item)
    except:
       import sys
       for line in sys.exc_info():
           logger.error("%s" % line)
       return []
