#-*- coding: utf-8 -*-
"""
@file
@brief Various function to download data about population
"""
import re
from pyquickhelper.loghelper import noLOG
from pymyinstall.installcustom import download_page
from pyensae import download_data
from pyrsslocal.xmlhelper import xml_filter_iterator
from .data_exceptions import LinkNotFoundError


def wolf_xml(url="http://alpage.inria.fr/~sagot/wolf.html", temp_folder=".", fLOG=noLOG):
    """
    The `WOLF <http://alpage.inria.fr/~sagot/wolf-en.html>`_
    (Wordnet Libre du Français, Free French Wordnet) is a free semantic lexical resource (wordnet) for French.

    This data is licensed under
    `Cecill-C license <http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html>`_.
    Language is French.

    @param      url             url
    @param      fLOG            logging function
    @param      temp_folder     where to download
    @return                     list of files
    """
    link = url
    page = download_page(link)
    reg = re.compile("href=\\\"(.*wolf.*?[.]bz2)\\\"")
    alls = reg.findall(page)
    if len(alls) == 0:
        raise LinkNotFoundError(
            "unable to find a link on a .exe file on page: " +
            page)

    url = alls[0]
    spl = url.split("/")
    url = "/".join(spl[:-1]) + "/"
    url2 = "/".join(spl[:-2]) + "/31718/"
    name = spl[-1]
    dtd = download_data("debvisdic-strict.dtd", url=url2,
                        fLOG=fLOG, whereTo=temp_folder)
    local = download_data(name, url=url, fLOG=fLOG, whereTo=temp_folder)
    if isinstance(local, str):
        local = [local]
    return local + [dtd]


def enumerate_wolf_xml_row(filename, fLOG=noLOG, xmlformat=False, encoding="utf-8"):
    """
    walk through an XML file returned by function
    @see fn wolf_xml

    @param      filename        filename
    @param      fLOG            logging function
    @param      xmlformat       if True, return the xml, otherwise return the node,
                                see `XMLHandlerDictNode <http://www.xavierdupre.fr/app/pyrsslocal/helpsphinx//pyrsslocal/xmlhelper/xml_tree_node.html#module-pyrsslocal.xmlhelper.xml_tree_node>`_
    @param      encoding        encoding
    @return                     elements
    """
    for row in xml_filter_iterator(filename, xmlformat=xmlformat, fLOG=fLOG, encoding=encoding):
        yield row


def enumerate_wolf_synonyms(filename, fLOG=noLOG, encoding="utf-8"):
    """
    enumerate list of synonyms
    Language is French.

    @param      filename        xml file
    @param      fLOG            logging function
    @param      encoding        encoding
    @return                     iterator on list of words
    """
    for row in enumerate_wolf_xml_row(filename, fLOG=fLOG, encoding=encoding):
        syn = [v for k, v in row.iterfields() if k == "SYNSET/SYNONYM/LITERAL/_"]
        if len(syn) > 1:
            yield syn
