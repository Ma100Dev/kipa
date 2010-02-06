# KiPa(KisaPalvelu), tuloslaskentajärjestelmä partiotaitokilpailuihin
#    Copyright (C) 2010  Espoon Partiotuki ry. ept@partio.fi


#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from random import uniform
from TulosLaskin import *

class Kisa(models.Model) :
        # code between "#gen_dia_class xxx"-> "#end_dia_class" tags is autogenerated from tietokanta.dia"
        # for these parts only make changes to data table definitions in tietokanta.dia!
        #gen_dia_class Kisa

        nimi = models.CharField(max_length=255)
        aika = models.CharField(max_length=255, blank=True, null=True )
        paikka = models.CharField(max_length=255, blank=True )

        #end_dia_class
        def __unicode__(self) :
                return self.nimi
        class Meta:
                verbose_name_plural = "Kisat"

class Sarja(models.Model) :
        # code between "#gen_dia_class xxx"-> "#end_dia_class" tags is autogenerated from tietokanta.dia"
        # for these parts only make changes to data table definitions in tietokanta.dia!
        #gen_dia_class Sarja

        nimi = models.CharField(max_length=255)
        vartion_maksimikoko = models.IntegerField(blank=True, null=True, default=0 )
        vartion_minimikoko = models.IntegerField(blank=True, null=True,default=0 )
        kisa = models.ForeignKey(Kisa)

        #end_dia_class
        def __unicode__(self) :
                return self.kisa.nimi+"."+self.nimi
        class Meta:
                verbose_name_plural = "Sarjat"
        def laskeTulokset(self) :
                return laskeSarja(self)

class Vartio(models.Model) :
        # code between "#gen_dia_class xxx"-> "#end_dia_class" tags is autogenerated from tietokanta.dia"
        # for these parts only make changes to data table definitions in tietokanta.dia!
        #gen_dia_class Vartio

        nro = models.IntegerField()
        nimi = models.CharField(max_length=255)
        sarja = models.ForeignKey(Sarja)
        piiri = models.CharField(max_length=255, blank=True )
        lippukunta = models.CharField(max_length=255, blank=True )
        puhelinnro = models.CharField(max_length=255, blank=True )
        sahkoposti = models.CharField(max_length=255, blank=True )
        osoite = models.CharField(max_length=255, blank=True )
        keskeyttanyt = models.IntegerField(blank=True, null=True )
        ulkopuolella = models.IntegerField(blank=True , null=True )

        #end_dia_class
        def __unicode__(self) :
                return self.sarja.kisa.nimi+"."+self.sarja.nimi+"."+str(self.nro)
        class Meta:
                verbose_name_plural = "Vartiot"

class Henkilo(models.Model) :
        # code between "#gen_dia_class xxx"-> "#end_dia_class" tags is autogenerated from tietokanta.dia"
        # for these parts only make changes to data table definitions in tietokanta.dia!
        #gen_dia_class Henkilo

        nimi = models.CharField(max_length=255)
        syntymavuosi = models.IntegerField(blank=True , null=True )
        lippukunta = models.CharField(max_length=255, blank=True, null=True )
        jasennumero = models.CharField(max_length=15, blank=True, null=True )
        puhelin_nro = models.CharField(max_length=15, blank=True, null=True )
        homma = models.CharField(max_length=255, blank=True, null=True )

        #end_dia_class
        def __unicode__(self) :
                return self.nimi
        class Meta:
                verbose_name_plural = "Henkilot"

class Tehtava(models.Model) :
        # code between "#gen_dia_class xxx"-> "#end_dia_class" tags is autogenerated from tietokanta.dia"
        # for these parts only make changes to data table definitions in tietokanta.dia!
        #gen_dia_class Tehtava

        nimi = models.CharField(max_length=255)
        tehtavaryhma = models.CharField(max_length=255, blank=True )
        tehtavaluokka = models.CharField(max_length=255, blank=True )
        rastikasky = models.TextField(blank=True )
        jarjestysnro = models.IntegerField()
        kaava = models.CharField(max_length=255)
        sarja = models.ForeignKey(Sarja)
        tarkistettu = models.BooleanField()

        #end_dia_class
        def mukanaOlevatVartiot(self):
                """
                Palauttaa listan Vartioista jotka ovat mukana tehtavan interpoloinneissa.
                """
                vartiot = self.sarja.vartio_set.all()
                mukana = []
                if vartiot:
                        for v in vartiot:
                                laskennassa = True
                                if not v.ulkopuolella==None:
                                        if self.jarjestysnro >= v.ulkopuolella:
                                                laskennassa = False
                                if not v.keskeyttanyt == None :
                                        if self.jarjestysnro >= v.keskeyttanyt:
                                                laskennassa = False
                                if laskennassa : 
                                        mukana.append(v)
                return mukana

        def __unicode__(self) :
                sarja = self.sarja
                kisa = sarja.kisa
                return kisa.nimi+"."+ sarja.nimi+"."+ self.nimi
        class Meta:
                ordering=("jarjestysnro",)
                verbose_name_plural = "Tehtavat"


class OsaTehtava(models.Model) :
        OSA_TYYPIT=(    ("kp","kisapisteita"),
                        ("rp","raakapisteita"),
                        ("ka","kokonaisaika"),
                        ("ala","alkuaika ja loppuaika"),
                        ("vk","vapaa kaava"), )
        # code between "#gen_dia_class xxx"-> "#end_dia_class" tags is autogenerated from tietokanta.dia"
        # for these parts only make changes to data table definitions in tietokanta.dia!
        #gen_dia_class OsaTehtava

        nimi = models.CharField(max_length=255)
        tyyppi = models.CharField(max_length=255, choices = OSA_TYYPIT )
        kaava = models.CharField(max_length=255)
        tehtava = models.ForeignKey(Tehtava)

        #end_dia_class
        def __unicode__(self) :
                tehtava= self.tehtava
                sarja = tehtava.sarja
                kisa = sarja.kisa
                return kisa.nimi+"."+ sarja.nimi+"."+ tehtava.nimi+"."+self.nimi
        class Meta:
                verbose_name_plural = "Osatehtavat"

class SyoteMaarite(models.Model) :
        TYYPPI_VAIHTOEHDOT = (
                ('aika', 'aika'),
                ('piste', 'piste'),)

        # code between "#gen_dia_class xxx"-> "#end_dia_class" tags is autogenerated from tietokanta.dia"
        # for these parts only make changes to data table definitions in tietokanta.dia!
        #gen_dia_class SyoteMaarite

        nimi = models.CharField(max_length=255)
        tyyppi = models.CharField(max_length=255, choices=TYYPPI_VAIHTOEHDOT )
        kali_vihje = models.CharField(max_length=255, blank=True , null=True )
        osa_tehtava = models.ForeignKey(OsaTehtava)

        #end_dia_class
        def __unicode__(self) :
                ot = self.osa_tehtava
                tehtava= ot.tehtava
                sarja = tehtava.sarja
                kisa = sarja.kisa
                return kisa.nimi+"."+ sarja.nimi+"."+ tehtava.nimi+"."+ot.nimi+"."+self.nimi
        class Meta:
                ordering = ['osa_tehtava','nimi']
                verbose_name_plural = "Syotteen maaritteet"

class Syote(models.Model) :
        # code between "#gen_dia_class xxx"-> "#end_dia_class" tags is autogenerated from tietokanta.dia"
        # for these parts only make changes to data table definitions in tietokanta.dia!
        #gen_dia_class Syote

        arvo = models.CharField(max_length=255, blank = True, null=True )
        vartio = models.ForeignKey(Vartio, blank=True, null=True )
        maarite = models.ForeignKey(SyoteMaarite)
        tarkistus = models.CharField(max_length=255, blank=True,null=True )

        #end_dia_class

        def __unicode__(self) :
                vartio = self.vartio
                maarite=self.maarite
                ot = maarite.osa_tehtava
                tehtava= ot.tehtava
                sarja = tehtava.sarja
                kisa = sarja.kisa
                return kisa.nimi+"."+ sarja.nimi+"."+ tehtava.nimi+"."+ot.nimi+"."+maarite.nimi+"."+str(vartio.nro)
        class Meta:
                verbose_name_plural = "Syotteet"


class TulosTaulu(models.Model) :
        # code between "#gen_dia_class xxx"-> "#end_dia_class" tags is autogenerated from tietokanta.dia"
        # for these parts only make changes to data table definitions in tietokanta.dia!
        #gen_dia_class TulosTaulu

        vartio = models.ForeignKey(Vartio)
        tehtava = models.ForeignKey(Tehtava)
        pisteet = models.CharField(max_length=255)

        #end_dia_class
        def __unicode__(self) :
                tehtava= self.tehtava
                sarja = tehtava.sarja
                kisa = sarja.kisa
                return kisa.nimi+"."+ sarja.nimi+"."+ tehtava.nimi +"."+ str(self.vartio.nro)
        class Meta:
                abstract = True

class TuomarineuvosTulos(TulosTaulu) :
        class Meta :
                verbose_name_plural = "Tuomarineuvoston tulokset"

class TestausTulos(TulosTaulu):
        class Meta:
                verbose_name_plural = "Testattavat tulokset"

class Parametri(models.Model) :
        # code between "#gen_dia_class xxx"-> "#end_dia_class" tags is autogenerated from tietokanta.dia"
        # for these parts only make changes to data table definitions in tietokanta.dia!
        #gen_dia_class Parametri

        nimi = models.CharField(max_length=255)
        arvo = models.CharField(max_length=255)
        osa_tehtava = models.ForeignKey(OsaTehtava)

        #end_dia_class
        class Meta:
                verbose_name_plural = "OsaTehtavan Paramentrit" 

        def __unicode__(self):
                ot = self.osa_tehtava
                tehtava= ot.tehtava
                sarja = tehtava.sarja
                kisa = sarja.kisa
                return kisa.nimi+"."+ sarja.nimi+"."+ tehtava.nimi+"."+ot.nimi+"."+self.nimi

