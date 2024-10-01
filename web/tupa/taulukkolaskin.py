# encoding: utf-8
# KiPa(KisaPalvelu), tuloslaskentajärjestelmä partiotaitokilpailuihin
#    Copyright (C) 2010  Espoon Partiotuki ry. ept@partio.fi

import re
from .laskentatyypit import *
from .funktiot import perusfunktiot
from .funktiot import listafunktiot
import settings
#from tupa.log import *
from . import log

pfunktiot={}
lfunktiot={}

for k in list(perusfunktiot.keys()) :
        def pfunctionfactory( funktio ) : return lambda *a : suorita(funktio,*a)
        pfunktiot[k]= pfunctionfactory( perusfunktiot[k] )
for k in list(listafunktiot.keys()) :
        def lfunctionfactory( funktio ) : return lambda *a : suorita_lista(funktio,*a)
        lfunktiot[k]= lfunctionfactory(listafunktiot[k] )

def dictToMathDict(dictionary) :
        """
        Muuttaa tavallisen sanakirjan rekursiivisesti laskennalliseksi sanakirjaksi.
        """
        new=MathDict({})
        for k in list(dictionary.keys()):
                if type(dictionary[k])==dict : new[k]= dictToMathDict(dictionary[k])
                else : new[k]=dictionary[k]
        return new

# FIXME: WIP
def laske(lauseke, m={}, funktiot={}):
    """
    Laskee lauseen mikäli se on laskettavissa. Käyttää muuttujista loytyviä arvoja, sekä funktioita.
    """
    # Määritetään numeroluokka eli vakiona lasketaan desimaaliluvuilla:
    f = { "num" : DictDecimal}
    f.update(funktiot)
    f.update(pfunktiot)
    f.update(lfunktiot)
    f=dictToMathDict(f)

    log.logString("<h4> Laskenta: </h4>")
    log.logString("Tehtävän lause = " + lauseke)

    # Poistetaan välilyönnit ja enterit:
    lause = lauseke.replace('\n','')
    lause = lause.replace('\r','')
    lause = lause.replace(' ','')
    # Poistetaan "-0" termit
    lause=re.sub(r"([-][0](?![0-9.]))",r"",lause)
    # Poistetaan etunollat
    lause=re.sub(r"0+([0-9]+)", r"\g<1>",lause)
    # Korvataan funktiot
    # Vakionumerot numeroinstansseiksi:
    oper=re.escape(r"-+*/(,[<>=")
    num =re.escape(r"-?\d+([.]\d+)?")
    lause=re.sub(r"((?<![^"+oper+"])"+num+")(?=["+oper+"]|$|\]|\))",r"num('\g<1>')",lause)
    #lause=re.sub(r"((?<![^-+*/(,[])-?\d+([.]\d+)?)(?![\.0-9])",r"num('\g<1>')",lause)    
    # Korvataan muuttujien nimet oikeilla muuttujilla:
    lause=re.sub(r"\.([a-zA-Z_]\w*)(?=\.)",r"['\g<1>']",lause) # .x. -> [x].
    lause=re.sub(r"\.([a-zA-Z_]+[a-zA-Z_0-9]*)",r"['\g<1>']",lause)       # .x  -> [x]
    lause=re.sub(r"\.(\d+)(?=["+oper+"]|$|\]|\))",r"['\g<1>']",lause)       # .n  -> [n]
    lause=re.sub(r"(?<=["+oper+r"])([a-zA-Z_0-9]\w*(?=[[]))",r"m['\g<1>']",lause) # x[  -> m[x][
    # Korvataan yksinäiset muuttujat (lähinnä funktioita):
    lause=re.sub(r"([a-zA-Z_][a-zA-Z_0-9]*(?![a-zA-Z_0-9.(]|[[']))",r"m['\g<1>']",lause) # x -> m[x]
    lause=re.sub(r"([a-zA-Z_][a-zA-Z_0-9]*(?![a-zA-Z_0-9.]|[[']))",r"f['\g<1>']",lause) # x( -> f[x](
    # lause=re.sub(r"\'([0-9]+)\'", r"\g<1>", lause) # Poistetaan kokonaislukuja ympäröivät heittomerkit
    tulos=None
    # Lasketaan tulos:
    print(lause) # TODO: Remove debug print and extra stuff
    """
    if settings.DEBUG:
        try:
            tulos = eval(lause)
        except KeyError:
            tulos = "S"  # Syöttämättömiä muuttujia
        except TypeError:
            tulos = None
    else:
        try:
            tulos = eval(lause)
        except DivisionByZero:
            tulos = None
        except KeyError:
            tulos = "S"  # Syöttämättömiä muuttujia
        except TypeError:
            tulos = None
        except SyntaxError:
            tulos = None
        except NameError:
            tulos = None
        except:
            tulos = None
    """
    tulos = eval(lause)
    
    try:
        log.logString("laskettu tulos= " + str(tulos.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)))
    except:
        log.logString("laskettu tulos= " + str(tulos))
    
    if isinstance(tulos, DictDecimal):
        tulos = Decimal(tulos)
    
    return tulos

def laskeTaulukko(taulukko,muuttujat) :
        """
        Laskee taulukon alkiot jotka ovat laskettavissa, muuttujista loytyvilla muuttujilla seka funktioilla.
        """
        # Päivitetään käyttajän muuttujilla:
        m=dictToMathDict(muuttujat)
        tulokset=[]
        for x in taulukko :
                rivi=[]
                for lause in x :
                        tulos=laske(lause,m)
                        if type(tulos)==Decimal : rivi.append(Decimal(tulos).quantize(Decimal('0.1'),
                                                                        rounding=ROUND_HALF_UP ))
                        else: rivi.append(tulos)
                tulokset.append(rivi)
        return tulokset



