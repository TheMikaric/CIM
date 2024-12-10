import flet as ft
import logic5 as lp # Pay attention that the version of logic module is up to date!
import pandas as pd
import copy # For deepcopy function, making it so that the data frame df is not changed by referencing it
import fcc # Importing custom components for the application
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
from datetime import datetime, timedelta
import os
import copy

global system_threshold_dict
global base_path
base_path = os.path.dirname(__file__)
global dictionaries
global mode # 'Alarm' or 'Warning', mainly changed through show_warnings toggles on each page

# The following three dictionaries are named after systems,
# and the content of each dictionary contains names of subsystems.
# These dictionaries are used regardless of if only the alarms are displayed, or both the warnings and alarms
stromrichter_dict = {
    'kühl': 'Kühlung',
    'batt': 'Batterie',
    'temp': 'Temperatur',
    'chlos': 'Schrank',
    'haltschr': 'Schrank',
    'mrichterschr': 'Schrank',
    'ruckelt': 'Drehzahlgeber',
    'ehzahl': 'Drehzahlgeber',
    'kommun': 'Kommunikation',
    'pec': 'Kommunikation',
    'berstr': 'Überstrom',
    'wischenkr': 'Zwischenkreis',
    'räusch': 'Gerausch',
    'rausch': 'Gerausch',
    'tzeingangsm': 'Netzeingangsmodul',
    'pepp': 'PEPP Modul',
    'gestört': 'Störung',
    'ausfall': 'Störung',
    'störung': 'Störung',}
wc_dict={
    'leck':'Leckage',
    'erstop':'Verstopfung',
    'ruckaufb':'Druckaufbau',
    'evac':'Evac'}
tur_dict = {
    'tsg': 'TSG',
    'steuer': 'TSG',
    'schlos': 'Türschloss',
    'tast': 'Taster',
    'antrie': 'Türantrieb',
    'sensor': 'Sensor',
    'notent': 'Notentriegelung',
    'tritt': 'Schiebetritt',
    'abdeck': 'Abdeckung',
    'stopp': 'Stopper',
    'puffe': 'Bodentürpuffer',
    'gesper': 'Abgesperrt',
    'dicht': 'Dichtung',
    'grünschl': 'Grünschleife',
    'lexigla': 'Plexiglas',
    'püffer': 'Bodentürpüffer',
    'puff': 'Puffer',
    'pikto': 'Piktogramm & Aufkleber',
    'aufkle': 'Piktogramm & Aufkleber',
    'kabel': 'Kabel',
    'berstsche': 'Berstscheibe',
    'klinke': 'Türklinke',
    'plomb': 'Plombe',
    'licht': 'Lichtschranke',
    'klemm': 'Klemmt',
    'beschädig': 'Beschädigung',
    'schlus': 'Türschloss',
    'scheib': 'Scheibe',
    'verriege': 'Verriegelung',
    'gumm': 'Gummi',
    'motor': 'Motor',
    'ewicht': 'Gewichtsdetektor',
    'blend': 'Frontblende',
    'vorreibe': 'Vorreiber',
    'spalt': 'Spaltüberbrückung',
    'getren': 'Abgetrennt'}

# The following dictionary contains thresholds for WARNING by each subsystem
threshold_dict_warning={
    ('WC','Leckage'): 2,
    ('WC','Verstopfung'): 2,
    ('WC','Druckaufbau'): 2,
    ('WC','Evac'): 2,
    ('Tür','Sensor'): 2,
    ('Tür','Spaltüberbrückung'): 2,
    ('Tür','Türschloss'): 2,
    ('Stromrichter','Kühlung'): 2,
    ('Stromrichter','Drehzahlgeber'): 2,
    ('Stromrichter','Schrank'): 2,
    ('Stromrichter','Temperatur'): 2,
    ('Stromrichter','Batterie'): 2,
    ('Stromrichter','PEPP Modul'): 2,
    ('Stromrichter','Störung'): 2,
    ('Stromrichter','Zwischenkreis'): 2,
    ('Stromrichter','Überstrom'): 2,}

# The following eight dictionaries contain system thresholds by fleet,
# so it is possible to only raise warning if 3 WC's are broken on Mireo fleet
# but raise warning if at least 5 WC's are broken on flirt3, enabling different system thresholds by fleet
flirt3_dict_warning={
    'WC': 2,
    'Plombe': 2,
    'Klima': 2,
    'Sitz': 2,
    'Fahrpläne': 2,
    'Verbandkasten': 2,
    'Sonnenblende & Sonnenrolle': 2,
    'Bremse': 2,
    'Tür': 2,
    'PZB': 2,
    'BSG': 2,
    'ASG': 2,
    'Leittechnik': 2,
    'Radsatz': 2,
    'Stromrichter': 2,
    'Stromabnehmer': 2,
    'Puffer': 2,
    'FIS': 2,
    'Abdeckung': 2,
    'Abfallbehälter': 2,
    'Piktogramme & Aufkleber': 2,
    'BMA': 2,
    'Dämpfer': 2,
    'Energiezähler': 2,
    'Fenster & Scheiben': 2,
    'Feuerlöscher': 2,
    'Graffiti': 2,
    'Hauptschalter': 2,
    'Hublift': 2,
    'Kompressor': 2,
    'Kupplung': 2,
    'Fahrmotor': 2,
    'Scheibenwischer': 2,
    'TDD/CDD': 2,
    'Tritt': 2,
    'Wagenkasten': 2,
    'Luftfeder': 2,
    'Zugfunk': 2,
    'Redbox': 2,
    'Drucksensor': 2,
    'Spurkranzschmierung': 2,
    'Beleuchtung': 2,
    'Lack': 2,
    'Magnet bremse': 2,
    'Streckenbücher': 2,
    'Getriebe': 2,
    'Transformator': 2,
    'Steckdose': 2,
    'Ölkühlung': 2,
    'Wildunfall': 2,
    'Schalter': 2}
emu3_dict_warning={
    'WC': 2,
    'Plombe': 2,
    'Klima': 2,
    'Sitz': 2,
    'Fahrpläne': 2,
    'Verbandkasten': 2,
    'Sonnenblende & Sonnenrolle': 2,
    'Bremse': 2,
    'Tür': 2,
    'PZB': 2,
    'BSG': 2,
    'ASG': 2,
    'Leittechnik': 2,
    'Radsatz': 2,
    'Stromrichter': 2,
    'Stromabnehmer': 2,
    'Puffer': 2,
    'FIS': 2,
    'Abdeckung': 2,
    'Abfallbehälter': 2,
    'Piktogramme & Aufkleber': 2,
    'BMA': 2,
    'Dämpfer': 2,
    'Energiezähler': 2,
    'Fenster & Scheiben': 2,
    'Feuerlöscher': 2,
    'Graffiti': 2,
    'Hauptschalter': 2,
    'Hublift': 2,
    'Kompressor': 2,
    'Kupplung': 2,
    'Fahrmotor': 2,
    'Scheibenwischer': 2,
    'TDD/CDD': 2,
    'Tritt': 2,
    'Wagenkasten': 2,
    'Luftfeder': 2,
    'Zugfunk': 2,
    'Redbox': 2,
    'Drucksensor': 2,
    'Spurkranzschmierung': 2,
    'Beleuchtung': 2,
    'Lack': 2,
    'Magnet bremse': 2,
    'Streckenbücher': 2,
    'Getriebe': 2,
    'Transformator': 2,
    'Steckdose': 2,
    'Ölkühlung': 2,
    'Wildunfall': 2,
    'Schalter': 2}
emu4_dict_warning={
    'WC': 2,
    'Plombe': 2,
    'Klima': 2,
    'Sitz': 2,
    'Fahrpläne': 2,
    'Verbandkasten': 2,
    'Sonnenblende & Sonnenrolle': 2,
    'Bremse': 2,
    'Tür': 2,
    'PZB': 2,
    'BSG': 2,
    'ASG': 2,
    'Leittechnik': 2,
    'Radsatz': 2,
    'Stromrichter': 2,
    'Stromabnehmer': 2,
    'Puffer': 2,
    'FIS': 2,
    'Abdeckung': 2,
    'Abfallbehälter': 2,
    'Piktogramme & Aufkleber': 2,
    'BMA': 2,
    'Dämpfer': 2,
    'Energiezähler': 2,
    'Fenster & Scheiben': 2,
    'Feuerlöscher': 2,
    'Graffiti': 2,
    'Hauptschalter': 2,
    'Hublift': 2,
    'Kompressor': 2,
    'Kupplung': 2,
    'Fahrmotor': 2,
    'Scheibenwischer': 2,
    'TDD/CDD': 2,
    'Tritt': 2,
    'Wagenkasten': 2,
    'Luftfeder': 2,
    'Zugfunk': 2,
    'Redbox': 2,
    'Drucksensor': 2,
    'Spurkranzschmierung': 2,
    'Beleuchtung': 2,
    'Lack': 2,
    'Magnet bremse': 2,
    'Streckenbücher': 2,
    'Getriebe': 2,
    'Transformator': 2,
    'Steckdose': 2,
    'Ölkühlung': 2,
    'Wildunfall': 2,
    'Schalter': 2}
emu5_dict_warning={
    'WC': 2,
    'Plombe': 2,
    'Klima': 2,
    'Sitz': 2,
    'Fahrpläne': 2,
    'Verbandkasten': 2,
    'Sonnenblende & Sonnenrolle': 2,
    'Bremse': 2,
    'Tür': 2,
    'PZB': 2,
    'BSG': 2,
    'ASG': 2,
    'Leittechnik': 2,
    'Radsatz': 2,
    'Stromrichter': 2,
    'Stromabnehmer': 2,
    'Puffer': 2,
    'FIS': 2,
    'Abdeckung': 2,
    'Abfallbehälter': 2,
    'Piktogramme & Aufkleber': 2,
    'BMA': 2,
    'Dämpfer': 2,
    'Energiezähler': 2,
    'Fenster & Scheiben': 2,
    'Feuerlöscher': 2,
    'Graffiti': 2,
    'Hauptschalter': 2,
    'Hublift': 2,
    'Kompressor': 2,
    'Kupplung': 2,
    'Fahrmotor': 2,
    'Scheibenwischer': 2,
    'TDD/CDD': 2,
    'Tritt': 2,
    'Wagenkasten': 2,
    'Luftfeder': 2,
    'Zugfunk': 2,
    'Redbox': 2,
    'Drucksensor': 2,
    'Spurkranzschmierung': 2,
    'Beleuchtung': 2,
    'Lack': 2,
    'Magnet bremse': 2,
    'Streckenbücher': 2,
    'Getriebe': 2,
    'Transformator': 2,
    'Steckdose': 2,
    'Ölkühlung': 2,
    'Wildunfall': 2,
    'Schalter': 2}
emu6_dict_warning={
    'WC': 2,
    'Plombe': 2,
    'Klima': 2,
    'Sitz': 2,
    'Fahrpläne': 2,
    'Verbandkasten': 2,
    'Sonnenblende & Sonnenrolle': 2,
    'Bremse': 2,
    'Tür': 2,
    'PZB': 2,
    'BSG': 2,
    'ASG': 2,
    'Leittechnik': 2,
    'Radsatz': 2,
    'Stromrichter': 2,
    'Stromabnehmer': 2,
    'Puffer': 2,
    'FIS': 2,
    'Abdeckung': 2,
    'Abfallbehälter': 2,
    'Piktogramme & Aufkleber': 2,
    'BMA': 2,
    'Dämpfer': 2,
    'Energiezähler': 2,
    'Fenster & Scheiben': 2,
    'Feuerlöscher': 2,
    'Graffiti': 2,
    'Hauptschalter': 2,
    'Hublift': 2,
    'Kompressor': 2,
    'Kupplung': 2,
    'Fahrmotor': 2,
    'Scheibenwischer': 2,
    'TDD/CDD': 2,
    'Tritt': 2,
    'Wagenkasten': 2,
    'Luftfeder': 2,
    'Zugfunk': 2,
    'Redbox': 2,
    'Drucksensor': 2,
    'Spurkranzschmierung': 2,
    'Beleuchtung': 2,
    'Lack': 2,
    'Magnet bremse': 2,
    'Streckenbücher': 2,
    'Getriebe': 2,
    'Transformator': 2,
    'Steckdose': 2,
    'Ölkühlung': 2,
    'Wildunfall': 2,
    'Schalter': 2}
emu9_dict_warning={
    'WC': 2,
    'Plombe': 2,
    'Klima': 2,
    'Sitz': 2,
    'Fahrpläne': 2,
    'Verbandkasten': 2,
    'Sonnenblende & Sonnenrolle': 2,
    'Bremse': 2,
    'Tür': 2,
    'PZB': 2,
    'BSG': 2,
    'ASG': 2,
    'Leittechnik': 2,
    'Radsatz': 2,
    'Stromrichter': 2,
    'Stromabnehmer': 2,
    'Puffer': 2,
    'FIS': 2,
    'Abdeckung': 2,
    'Abfallbehälter': 2,
    'Piktogramme & Aufkleber': 2,
    'BMA': 2,
    'Dämpfer': 2,
    'Energiezähler': 2,
    'Fenster & Scheiben': 2,
    'Feuerlöscher': 2,
    'Graffiti': 2,
    'Hauptschalter': 2,
    'Hublift': 2,
    'Kompressor': 2,
    'Kupplung': 2,
    'Fahrmotor': 2,
    'Scheibenwischer': 2,
    'TDD/CDD': 2,
    'Tritt': 2,
    'Wagenkasten': 2,
    'Luftfeder': 2,
    'Zugfunk': 2,
    'Redbox': 2,
    'Drucksensor': 2,
    'Spurkranzschmierung': 2,
    'Beleuchtung': 2,
    'Lack': 2,
    'Magnet bremse': 2,
    'Streckenbücher': 2,
    'Getriebe': 2,
    'Transformator': 2,
    'Steckdose': 2,
    'Ölkühlung': 2,
    'Wildunfall': 2,
    'Schalter': 2}
desiro_dict_warning={
    'WC': 2,
    'Plombe': 2,
    'Klima': 2,
    'Sitz': 2,
    'Fahrpläne': 2,
    'Verbandkasten': 2,
    'Sonnenblende & Sonnenrolle': 2,
    'Bremse': 2,
    'Tür': 2,
    'PZB': 2,
    'BSG': 2,
    'ASG': 2,
    'Leittechnik': 2,
    'Radsatz': 2,
    'Stromrichter': 2,
    'Stromabnehmer': 2,
    'Puffer': 2,
    'FIS': 2,
    'Abdeckung': 2,
    'Abfallbehälter': 2,
    'Piktogramme & Aufkleber': 2,
    'BMA': 2,
    'Dämpfer': 2,
    'Energiezähler': 2,
    'Fenster & Scheiben': 2,
    'Feuerlöscher': 2,
    'Graffiti': 2,
    'Hauptschalter': 2,
    'Hublift': 2,
    'Kompressor': 2,
    'Kupplung': 2,
    'Fahrmotor': 2,
    'Scheibenwischer': 2,
    'TDD/CDD': 2,
    'Tritt': 2,
    'Wagenkasten': 2,
    'Luftfeder': 2,
    'Zugfunk': 2,
    'Redbox': 2,
    'Drucksensor': 2,
    'Spurkranzschmierung': 2,
    'Beleuchtung': 2,
    'Lack': 2,
    'Magnet bremse': 2,
    'Streckenbücher': 2,
    'Getriebe': 2,
    'Transformator': 2,
    'Steckdose': 2,
    'Ölkühlung': 2,
    'Wildunfall': 2,
    'Schalter': 2}
mireo_dict_warning={
    'WC': 2,
    'Plombe': 2,
    'Klima': 2,
    'Sitz': 2,
    'Fahrpläne': 2,
    'Verbandkasten': 2,
    'Sonnenblende & Sonnenrolle': 2,
    'Bremse': 2,
    'Tür': 2,
    'PZB': 2,
    'BSG': 2,
    'ASG': 2,
    'Leittechnik': 2,
    'Radsatz': 2,
    'Stromrichter': 2,
    'Stromabnehmer': 2,
    'Puffer': 2,
    'FIS': 2,
    'Abdeckung': 2,
    'Abfallbehälter': 2,
    'Piktogramme & Aufkleber': 2,
    'BMA': 2,
    'Dämpfer': 2,
    'Energiezähler': 2,
    'Fenster & Scheiben': 2,
    'Feuerlöscher': 2,
    'Graffiti': 2,
    'Hauptschalter': 2,
    'Hublift': 2,
    'Kompressor': 2,
    'Kupplung': 2,
    'Fahrmotor': 2,
    'Scheibenwischer': 2,
    'TDD/CDD': 2,
    'Tritt': 2,
    'Wagenkasten': 2,
    'Luftfeder': 2,
    'Zugfunk': 2,
    'Redbox': 2,
    'Drucksensor': 2,
    'Spurkranzschmierung': 2,
    'Beleuchtung': 2,
    'Lack': 2,
    'Magnet bremse': 2,
    'Streckenbücher': 2,
    'Getriebe': 2,
    'Transformator': 2,
    'Steckdose': 2,
    'Ölkühlung': 2,
    'Wildunfall': 2,
    'Schalter': 2}
# A dictionary containg appropriate dictionaries based on fleet name, in warning mode
fleet_system_dict_warning={
    'FLIRT 3 GABY': flirt3_dict_warning,
    'GABW Stadler FLIRT3 EMU3': emu3_dict_warning,
    'GABW Stadler FLIRT3 EMU4': emu4_dict_warning,
    'GABW Stadler FLIRT3 EMU5': emu5_dict_warning,
    'GABW Stadler FLIRT3 EMU6': emu6_dict_warning,
    'GABW Stadler FLIRT3 EMU9': emu9_dict_warning,
    'Siemens Desiro GABY': desiro_dict_warning,
    'Siemens Mireo GABY': mireo_dict_warning}
# Used for thresholds on main page and "Analyze by fleet"
system_threshold_dict_warning={
    'WC': 2,
    'Plombe': 2,
    'Klima': 2,
    'Sitz': 2,
    'Fahrpläne': 2,
    'Verbandkasten': 2,
    'Sonnenblende & Sonnenrolle': 2,
    'Bremse': 2,
    'Tür': 2,
    'PZB': 2,
    'BSG': 2,
    'ASG': 2,
    'Leittechnik': 2,
    'Radsatz': 2,
    'Stromrichter': 2,
    'Stromabnehmer': 2,
    'Puffer': 2,
    'FIS': 2,
    'Abdeckung': 2,
    'Abfallbehälter': 2,
    'Piktogramme & Aufkleber': 2,
    'BMA': 2,
    'Dämpfer': 2,
    'Energiezähler': 2,
    'Fenster & Scheiben': 2,
    'Feuerlöscher': 2,
    'Graffiti': 2,
    'Hauptschalter': 2,
    'Hublift': 2,
    'Kompressor': 2,
    'Kupplung': 2,
    'Fahrmotor': 2,
    'Scheibenwischer': 2,
    'TDD/CDD': 2,
    'Tritt': 2,
    'Wagenkasten': 2,
    'Luftfeder': 2,
    'Zugfunk': 2,
    'Redbox': 2,
    'Drucksensor': 2,
    'Spurkranzschmierung': 2,
    'Beleuchtung': 2,
    'Lack': 2,
    'Magnet bremse': 2,
    'Streckenbücher': 2,
    'Getriebe': 2,
    'Transformator': 2,
    'Steckdose': 2,
    'Ölkühlung': 2,
    'Wildunfall': 2,
    'Schalter': 2}

# Same logic as is in warnings, but for alarms
flirt3_dict_alarm={
    'WC': 2,
    'Plombe': 2,
    'Klima': 2,
    'Sitz': 2,
    'Fahrpläne': 2,
    'Verbandkasten': 2,
    'Sonnenblende & Sonnenrolle': 2,
    'Bremse': 2,
    'Tür': 2,
    'PZB': 2,
    'BSG': 2,
    'ASG': 2,
    'Leittechnik': 2,
    'Radsatz': 2,
    'Stromrichter': 2,
    'Stromabnehmer': 2,
    'Puffer': 2,
    'FIS': 2,
    'Abdeckung': 2,
    'Abfallbehälter': 2,
    'Piktogramme & Aufkleber': 2,
    'BMA': 2,
    'Dämpfer': 2,
    'Energiezähler': 2,
    'Fenster & Scheiben': 2,
    'Feuerlöscher': 2,
    'Graffiti': 2,
    'Hauptschalter': 2,
    'Hublift': 2,
    'Kompressor': 2,
    'Kupplung': 2,
    'Fahrmotor': 2,
    'Scheibenwischer': 2,
    'TDD/CDD': 2,
    'Tritt': 2,
    'Wagenkasten': 2,
    'Luftfeder': 2,
    'Zugfunk': 2,
    'Redbox': 2,
    'Drucksensor': 2,
    'Spurkranzschmierung': 2,
    'Beleuchtung': 2,
    'Lack': 2,
    'Magnet bremse': 2,
    'Streckenbücher': 2,
    'Getriebe': 2,
    'Transformator': 2,
    'Steckdose': 2,
    'Ölkühlung': 2,
    'Wildunfall': 2,
    'Schalter': 2}
emu3_dict_alarm={
    'WC': 2,
    'Plombe': 2,
    'Klima': 2,
    'Sitz': 2,
    'Fahrpläne': 2,
    'Verbandkasten': 2,
    'Sonnenblende & Sonnenrolle': 2,
    'Bremse': 2,
    'Tür': 2,
    'PZB': 2,
    'BSG': 2,
    'ASG': 2,
    'Leittechnik': 2,
    'Radsatz': 2,
    'Stromrichter': 2,
    'Stromabnehmer': 2,
    'Puffer': 2,
    'FIS': 2,
    'Abdeckung': 2,
    'Abfallbehälter': 2,
    'Piktogramme & Aufkleber': 2,
    'BMA': 2,
    'Dämpfer': 2,
    'Energiezähler': 2,
    'Fenster & Scheiben': 2,
    'Feuerlöscher': 2,
    'Graffiti': 2,
    'Hauptschalter': 2,
    'Hublift': 2,
    'Kompressor': 2,
    'Kupplung': 2,
    'Fahrmotor': 2,
    'Scheibenwischer': 2,
    'TDD/CDD': 2,
    'Tritt': 2,
    'Wagenkasten': 2,
    'Luftfeder': 2,
    'Zugfunk': 2,
    'Redbox': 2,
    'Drucksensor': 2,
    'Spurkranzschmierung': 2,
    'Beleuchtung': 2,
    'Lack': 2,
    'Magnet bremse': 2,
    'Streckenbücher': 2,
    'Getriebe': 2,
    'Transformator': 2,
    'Steckdose': 2,
    'Ölkühlung': 2,
    'Wildunfall': 2,
    'Schalter': 2}
emu4_dict_alarm={
    'WC': 2,
    'Plombe': 2,
    'Klima': 2,
    'Sitz': 2,
    'Fahrpläne': 2,
    'Verbandkasten': 2,
    'Sonnenblende & Sonnenrolle': 2,
    'Bremse': 2,
    'Tür': 2,
    'PZB': 2,
    'BSG': 2,
    'ASG': 2,
    'Leittechnik': 2,
    'Radsatz': 2,
    'Stromrichter': 2,
    'Stromabnehmer': 2,
    'Puffer': 2,
    'FIS': 2,
    'Abdeckung': 2,
    'Abfallbehälter': 2,
    'Piktogramme & Aufkleber': 2,
    'BMA': 2,
    'Dämpfer': 2,
    'Energiezähler': 2,
    'Fenster & Scheiben': 2,
    'Feuerlöscher': 2,
    'Graffiti': 2,
    'Hauptschalter': 2,
    'Hublift': 2,
    'Kompressor': 2,
    'Kupplung': 2,
    'Fahrmotor': 2,
    'Scheibenwischer': 2,
    'TDD/CDD': 2,
    'Tritt': 2,
    'Wagenkasten': 2,
    'Luftfeder': 2,
    'Zugfunk': 2,
    'Redbox': 2,
    'Drucksensor': 2,
    'Spurkranzschmierung': 2,
    'Beleuchtung': 2,
    'Lack': 2,
    'Magnet bremse': 2,
    'Streckenbücher': 2,
    'Getriebe': 2,
    'Transformator': 2,
    'Steckdose': 2,
    'Ölkühlung': 2,
    'Wildunfall': 2,
    'Schalter': 2}
emu5_dict_alarm={
    'WC': 2,
    'Plombe': 2,
    'Klima': 2,
    'Sitz': 2,
    'Fahrpläne': 2,
    'Verbandkasten': 2,
    'Sonnenblende & Sonnenrolle': 2,
    'Bremse': 2,
    'Tür': 20,
    'PZB': 2,
    'BSG': 2,
    'ASG': 2,
    'Leittechnik': 2,
    'Radsatz': 2,
    'Stromrichter': 2,
    'Stromabnehmer': 2,
    'Puffer': 2,
    'FIS': 2,
    'Abdeckung': 2,
    'Abfallbehälter': 2,
    'Piktogramme & Aufkleber': 2,
    'BMA': 2,
    'Dämpfer': 2,
    'Energiezähler': 2,
    'Fenster & Scheiben': 2,
    'Feuerlöscher': 2,
    'Graffiti': 2,
    'Hauptschalter': 2,
    'Hublift': 2,
    'Kompressor': 2,
    'Kupplung': 2,
    'Fahrmotor': 2,
    'Scheibenwischer': 2,
    'TDD/CDD': 2,
    'Tritt': 2,
    'Wagenkasten': 2,
    'Luftfeder': 2,
    'Zugfunk': 2,
    'Redbox': 2,
    'Drucksensor': 2,
    'Spurkranzschmierung': 2,
    'Beleuchtung': 2,
    'Lack': 2,
    'Magnet bremse': 2,
    'Streckenbücher': 2,
    'Getriebe': 2,
    'Transformator': 2,
    'Steckdose': 2,
    'Ölkühlung': 2,
    'Wildunfall': 2,
    'Schalter': 2}
emu6_dict_alarm={
    'WC': 2,
    'Plombe': 2,
    'Klima': 2,
    'Sitz': 2,
    'Fahrpläne': 2,
    'Verbandkasten': 2,
    'Sonnenblende & Sonnenrolle': 2,
    'Bremse': 2,
    'Tür': 2,
    'PZB': 2,
    'BSG': 2,
    'ASG': 2,
    'Leittechnik': 2,
    'Radsatz': 2,
    'Stromrichter': 2,
    'Stromabnehmer': 2,
    'Puffer': 2,
    'FIS': 2,
    'Abdeckung': 2,
    'Abfallbehälter': 2,
    'Piktogramme & Aufkleber': 2,
    'BMA': 2,
    'Dämpfer': 2,
    'Energiezähler': 2,
    'Fenster & Scheiben': 2,
    'Feuerlöscher': 2,
    'Graffiti': 2,
    'Hauptschalter': 2,
    'Hublift': 2,
    'Kompressor': 2,
    'Kupplung': 2,
    'Fahrmotor': 2,
    'Scheibenwischer': 2,
    'TDD/CDD': 2,
    'Tritt': 2,
    'Wagenkasten': 2,
    'Luftfeder': 2,
    'Zugfunk': 2,
    'Redbox': 2,
    'Drucksensor': 2,
    'Spurkranzschmierung': 2,
    'Beleuchtung': 2,
    'Lack': 2,
    'Magnet bremse': 2,
    'Streckenbücher': 2,
    'Getriebe': 2,
    'Transformator': 2,
    'Steckdose': 2,
    'Ölkühlung': 2,
    'Wildunfall': 2,
    'Schalter': 2}
emu9_dict_alarm={
    'WC': 2,
    'Plombe': 2,
    'Klima': 2,
    'Sitz': 2,
    'Fahrpläne': 2,
    'Verbandkasten': 2,
    'Sonnenblende & Sonnenrolle': 2,
    'Bremse': 2,
    'Tür': 2,
    'PZB': 2,
    'BSG': 2,
    'ASG': 2,
    'Leittechnik': 2,
    'Radsatz': 2,
    'Stromrichter': 2,
    'Stromabnehmer': 2,
    'Puffer': 2,
    'FIS': 2,
    'Abdeckung': 2,
    'Abfallbehälter': 2,
    'Piktogramme & Aufkleber': 2,
    'BMA': 2,
    'Dämpfer': 2,
    'Energiezähler': 2,
    'Fenster & Scheiben': 2,
    'Feuerlöscher': 2,
    'Graffiti': 2,
    'Hauptschalter': 2,
    'Hublift': 2,
    'Kompressor': 2,
    'Kupplung': 2,
    'Fahrmotor': 2,
    'Scheibenwischer': 2,
    'TDD/CDD': 2,
    'Tritt': 2,
    'Wagenkasten': 2,
    'Luftfeder': 2,
    'Zugfunk': 2,
    'Redbox': 2,
    'Drucksensor': 2,
    'Spurkranzschmierung': 2,
    'Beleuchtung': 2,
    'Lack': 2,
    'Magnet bremse': 2,
    'Streckenbücher': 2,
    'Getriebe': 2,
    'Transformator': 2,
    'Steckdose': 2,
    'Ölkühlung': 2,
    'Wildunfall': 2,
    'Schalter': 2}
desiro_dict_alarm={
    'WC': 2,
    'Plombe': 2,
    'Klima': 2,
    'Sitz': 2,
    'Fahrpläne': 2,
    'Verbandkasten': 2,
    'Sonnenblende & Sonnenrolle': 2,
    'Bremse': 2,
    'Tür': 2,
    'PZB': 2,
    'BSG': 2,
    'ASG': 2,
    'Leittechnik': 2,
    'Radsatz': 2,
    'Stromrichter': 2,
    'Stromabnehmer': 2,
    'Puffer': 2,
    'FIS': 2,
    'Abdeckung': 2,
    'Abfallbehälter': 2,
    'Piktogramme & Aufkleber': 2,
    'BMA': 2,
    'Dämpfer': 2,
    'Energiezähler': 2,
    'Fenster & Scheiben': 2,
    'Feuerlöscher': 2,
    'Graffiti': 2,
    'Hauptschalter': 2,
    'Hublift': 2,
    'Kompressor': 2,
    'Kupplung': 2,
    'Fahrmotor': 2,
    'Scheibenwischer': 2,
    'TDD/CDD': 2,
    'Tritt': 2,
    'Wagenkasten': 2,
    'Luftfeder': 2,
    'Zugfunk': 2,
    'Redbox': 2,
    'Drucksensor': 2,
    'Spurkranzschmierung': 2,
    'Beleuchtung': 2,
    'Lack': 2,
    'Magnet bremse': 2,
    'Streckenbücher': 2,
    'Getriebe': 2,
    'Transformator': 2,
    'Steckdose': 2,
    'Ölkühlung': 2,
    'Wildunfall': 2,
    'Schalter': 2}
mireo_dict_alarm={
    'WC': 2,
    'Plombe': 2,
    'Klima': 2,
    'Sitz': 2,
    'Fahrpläne': 2,
    'Verbandkasten': 2,
    'Sonnenblende & Sonnenrolle': 2,
    'Bremse': 2,
    'Tür': 2,
    'PZB': 2,
    'BSG': 2,
    'ASG': 2,
    'Leittechnik': 2,
    'Radsatz': 2,
    'Stromrichter': 2,
    'Stromabnehmer': 2,
    'Puffer': 2,
    'FIS': 2,
    'Abdeckung': 2,
    'Abfallbehälter': 2,
    'Piktogramme & Aufkleber': 2,
    'BMA': 2,
    'Dämpfer': 2,
    'Energiezähler': 2,
    'Fenster & Scheiben': 2,
    'Feuerlöscher': 2,
    'Graffiti': 2,
    'Hauptschalter': 2,
    'Hublift': 2,
    'Kompressor': 2,
    'Kupplung': 2,
    'Fahrmotor': 2,
    'Scheibenwischer': 2,
    'TDD/CDD': 2,
    'Tritt': 2,
    'Wagenkasten': 2,
    'Luftfeder': 2,
    'Zugfunk': 2,
    'Redbox': 2,
    'Drucksensor': 2,
    'Spurkranzschmierung': 2,
    'Beleuchtung': 2,
    'Lack': 2,
    'Magnet bremse': 2,
    'Streckenbücher': 2,
    'Getriebe': 2,
    'Transformator': 2,
    'Steckdose': 2,
    'Ölkühlung': 2,
    'Wildunfall': 2,
    'Schalter': 2}
fleet_system_dict_alarm={
    'FLIRT 3 GABY': flirt3_dict_alarm,
    'GABW Stadler FLIRT3 EMU3': emu3_dict_alarm,
    'GABW Stadler FLIRT3 EMU4': emu4_dict_alarm,
    'GABW Stadler FLIRT3 EMU5': emu5_dict_alarm,
    'GABW Stadler FLIRT3 EMU6': emu6_dict_alarm,
    'GABW Stadler FLIRT3 EMU9': emu9_dict_alarm,
    'Siemens Desiro GABY': desiro_dict_alarm,
    'Siemens Mireo GABY': mireo_dict_alarm}
threshold_dict_alarm={
    ('WC','Leckage'): 2,
    ('WC','Verstopfung'): 20,
    ('WC','Druckaufbau'): 2,
    ('WC','Evac'): 29,
    ('Tür','Sensor'): 2,
    ('Tür','Spaltüberbrückung'): 2,
    ('Tür','Türschloss'): 2,
    ('Stromrichter','Kühlung'): 2,
    ('Stromrichter','Drehzahlgeber'): 2,
    ('Stromrichter','Schrank'): 2,
    ('Stromrichter','Temperatur'): 2,
    ('Stromrichter','Batterie'): 2,
    ('Stromrichter','PEPP Modul'): 2,
    ('Stromrichter','Störung'): 2,
    ('Stromrichter','Zwischenkreis'): 2,
    ('Stromrichter','Überstrom'): 2}
system_threshold_dict_alarm={
    'WC': 2,
    'Plombe': 2,
    'Klima': 2,
    'Sitz': 2,
    'Fahrpläne': 2,
    'Verbandkasten': 2,
    'Sonnenblende & Sonnenrolle': 2,
    'Bremse': 2,
    'Tür': 2,
    'PZB': 2,
    'BSG': 2,
    'ASG': 2,
    'Leittechnik': 2,
    'Radsatz': 2,
    'Stromrichter': 2,
    'Stromabnehmer': 2,
    'Puffer': 2,
    'FIS': 2,
    'Abdeckung': 2,
    'Abfallbehälter': 2,
    'Piktogramme & Aufkleber': 2,
    'BMA': 2,
    'Dämpfer': 2,
    'Energiezähler': 2,
    'Fenster & Scheiben': 2,
    'Feuerlöscher': 2,
    'Graffiti': 2,
    'Hauptschalter': 2,
    'Hublift': 2,
    'Kompressor': 2,
    'Kupplung': 2,
    'Fahrmotor': 2,
    'Scheibenwischer': 2,
    'TDD/CDD': 2,
    'Tritt': 2,
    'Wagenkasten': 2,
    'Luftfeder': 2,
    'Zugfunk': 2,
    'Redbox': 2,
    'Drucksensor': 2,
    'Spurkranzschmierung': 2,
    'Beleuchtung': 2,
    'Lack': 2,
    'Magnet bremse': 2,
    'Streckenbücher': 2,
    'Getriebe': 2,
    'Transformator': 2,
    'Steckdose': 2,
    'Ölkühlung': 2,
    'Wildunfall': 2,
    'Schalter': 2}

# Universal dictionaries that both alarms and warnings use
wrong_spelling_dict={
    'tuer':'tür'}
fleets_dict = {
    "[SiemensMireoGABY] Siemens Mireo GABY": "Siemens Mireo GABY",
    "[SiemensDesirGABY] Siemens Desiro GABY": "Siemens Desiro GABY",
    "[FLIRT3GABY] FLIRT 3 GABY": "FLIRT 3 GABY",
    "[FLIRT3_EMU9_GABW] GABW Stadler FLIRT3 EMU9": "GABW Stadler FLIRT3 EMU9",
    "[FLIRT3_EMU6_GABW] GABW Stadler FLIRT3 EMU6": "GABW Stadler FLIRT3 EMU6",
    "[FLIRT3_EMU5_GABW] GABW Stadler FLIRT3 EMU5": "GABW Stadler FLIRT3 EMU5",
    "[FLIRT3_EMU4_GABW] GABW Stadler FLIRT3 EMU4": "GABW Stadler FLIRT3 EMU4",
    "[FLIRT3_EMU3_GABW] GABW Stadler FLIRT3 EMU3": "GABW Stadler FLIRT3 EMU3"}
column_dict={
    'Indication Number / Номер заказа':'Indication Number',
    'Vehicle Number / Номер вагона':'No.',
    'Coach type / Модель вагона':'Fleet',
    'Date of Receipt':'Date',
    'Merged':'System',
    'Merged1':'Subsystem',
    'Counter':'Counter',}
keyword_dict = {
    'wc': 'WC',
    'lomb': 'Plombe',
    'klima': 'Klima',
    'sitz': 'Sitz',
    'ahrpl': 'Fahrpläne',
    'verband': 'Verbandkasten',
    'sonnen': 'Sonnenblende & Sonnenrolle',
    'brems': 'Bremse',
    'tür': 'Tür',
    'pzb': 'PZB',
    'bsg': 'BSG',
    'asg': 'ASG',
    'eittech': 'Leittechnik',
    'adsat': 'Radsatz',
    'tromric': 'Stromrichter',
    'tromab': 'Stromabnehmer',
    'chleifl': 'Stromabnehmer',
    'puff': 'Puffer',
    'fis': 'FIS',
    'monitor': 'Monitor',
    'audio': 'Audio',
    'kamera': 'Kamera',
    'mikro': 'Mikrofon',
    'makro': 'Makrofon',
    'bdecku': 'Abdeckung',
    'bfallbe': 'Abfallbehälter',
    'aufkleb': 'Piktogramme & Aufkleber',
    'pikto': 'Piktogramme & Aufkleber',
    'bma': 'BMA',
    'ämpfe': 'Dämpfer',
    'nergiez': 'Energiezähler',
    'fenster': 'Fenster & Scheiben',
    'rontscheib': 'Fenster & Scheiben',
    'feuerl': 'Feuerlöscher',
    'graf': 'Graffiti',
    'auptschal': 'Hauptschalter',
    'hs': 'Hauptschalter',
    'hublift': 'Hublift',
    'kompress': 'Kompressor',
    'kupplu': 'Kupplung',
    'fahrmotor': 'Fahrmotor',
    'wisch': 'Scheibenwischer',
    'tdd': 'TDD/CDD',
    'cdd': 'TDD/CDD',
    'tritt': 'Tritt',
    'agenkast': 'Wagenkasten',
    'luftfed': 'Luftfeder',
    'zugfun': 'Zugfunk',
    'redbox': 'Redbox',
    'drucksens': 'Drucksensor',
    'spurkran': 'Spurkranzschmierung',
    'leucht': 'Beleuchtung',
    'licht': 'Beleuchtung',
    'lack': 'Lack',
    'mg': 'Magnet bremse',
    'streckenb': 'Streckenbücher',
    'getrieb': 'Getriebe',
    'transf': 'Transformator',
    'steckd': 'Steckdose',
    'lkühl': 'Ölkühlung',
    'wild': 'Wildunfall',
    'schalte': 'Schalter',
    'luftfed':'Luftfeder'}
duplicates_dict={
    'WC':'Tür'}
subsystem_dict_dict={
    'WC':wc_dict,
    'Tür':tur_dict,
    'Stromrichter':stromrichter_dict,}

def dict_values(dictionary):
    for key,value in dictionary.items():
        temp_dict={}
    return dictionary

def exceeds_threshold_component(row):
    threshold_dict_fnc=threshold_dict_alarm if mode=='alarm' else threshold_dict_warning
    # Create a tuple from Column1 and Column2
    key = (row['Merged'], row['Merged1'])
    
    # Check if the tuple exists in the dictionary and if the counter exceeds the threshold
    return key in threshold_dict_fnc and row['Counter'] > threshold_dict_fnc[key]

def exceeds_threshold_system(df,fleet_system_dict):
    new_rows=[]
    for index,row in df.iterrows():
        for key,value in fleet_system_dict.items():
            if key in row['Coach type / Модель вагона']:
                if row['Counter'] > value[row['Merged']]:
                    new_rows.append(row)
    return pd.DataFrame(new_rows)

def start_driver():
    try:
        os.remove(os.path.join(base_path, "IH-Meldungen Export Report.xlsx"))
    except FileNotFoundError:
        print('Nije bilo prethodnog exporta')
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {"download.default_directory": base_path})
    global driver 
    driver = webdriver.Chrome(options=chrome_options) 
    driver.get("https://amigo.eucorail.com/asset/#type=Custom&name=MaintenanceIndications")
    global action_chains
    action_chains= ActionChains(driver)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "un"))).send_keys('04StPu')
    time.sleep(1)
    password=driver.find_element(By.ID, "pw")
    password.send_keys('2024')
    login=driver.find_element(By.CLASS_NAME, "login-button")
    login.click()

def calculate_date(df):
    global yesterday
    global today
    global most_recent_date
    global scrape_date
    yesterday = datetime.now() - timedelta(days=1)
    yesterday = yesterday.strftime('%m/%d/%Y')
    today=datetime.now()
    today= today.strftime('%m/%d/%Y')
    df['Date of Receipt'] = pd.to_datetime(df['Date of Receipt'], format='%m/%d/%Y')
    most_recent_date = df['Date of Receipt'].max()
    most_recent_date = most_recent_date.strftime('%m/%d/%Y')
    scrape_date=df['Date of Receipt'].max() + timedelta(days=1)
    scrape_date=scrape_date.strftime('%m/%d/%Y')
        
def table_scrape():
    while True:
        try:
            export_button=driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div/div[1]/div[2]/div[2]/div[2]/div[8]/span[2]")
            export_button.click()
            break
        except:
            time.sleep(0.5)
    time.sleep(1)
    while True:
        try:
            from_date=driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[1]/div[2]/input')
            from_date.send_keys(scrape_date)
            break
        except Exception as e:
            time.sleep(1)
    to_date=driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div[1]/div[2]/input')
    to_date.clear()
    to_date.send_keys(today)
    time.sleep(2)
    save=driver.find_element(By.XPATH, "//*[@id='dialog0']/div[3]/div[1]/span[2]")
    save.click()
    time.sleep(5)

def read_export_excel():
    global result
    global df
    while True:
        try:
            df = pd.read_excel(os.path.join(base_path, "IH-Meldungen Export Report.xlsx"))
            break
        except:
            time.sleep(1)
    del df["Component Serial Number / Серийный номер компонента"]
    del df["Date of notification to the equipment supplier / Дата сообщения поставщику оборудования"]
    filtered_df = df[df['Main Category'] == 'Corrective']
    filtered_df = filtered_df[filtered_df['Status'] != 'Canceled']
    df_excel=pd.read_excel(os.path.join(base_path, "Corrective Indications Monitor.xlsx"))
    frames=[df_excel,filtered_df]
    result=pd.concat(frames)
    driver.quit()
    os.remove(os.path.join(base_path, "Corrective Indications Monitor.xlsx"))
    today=datetime.now()
    result['Date of Receipt'] = pd.to_datetime(result['Date of Receipt'])
    result=result[result['Date of Receipt']>=today-timedelta(weeks=12)]
    with pd.ExcelWriter(os.path.join(base_path, "Corrective Indications Monitor.xlsx"), engine='openpyxl', mode='w') as writer:
        result.to_excel(writer, sheet_name='Base (15.7.2024  -', index=False, header=True)

def update_table(df):
    calculate_date(df)
    if yesterday==most_recent_date:
        return df
    else:
        
        start_driver()
        table_scrape()
        read_export_excel()
        return result

def filter_data_by_date(pre_result, filter_choice):
    # Get today's date
    today = pd.Timestamp(datetime.now())

    # Apply filters based on the choice
    if filter_choice == 'In last week':
        date_limit = today - timedelta(weeks=1)
    elif filter_choice == 'In last 2 weeks':
        date_limit = today - timedelta(weeks=2)
    elif filter_choice == 'In last 3 weeks':
        date_limit = today - timedelta(weeks=3)
    elif filter_choice == 'Last month':
        date_limit = today - timedelta(weeks=4)
    elif filter_choice == 'Last 2 months':
        date_limit = today - timedelta(weeks=8)
    elif filter_choice == 'Last 3 months':
        date_limit = today - timedelta(weeks=12)
    else:
        # If no filter or invalid filter is selected, return the entire DataFrame
        raise

    # Filter the DataFrame by 'Date of Receipt'

    filtered_df = pre_result[pre_result['Date of Receipt'] >= date_limit]
    return filtered_df

def split_row_by_partial_match(df, word_dict):
    new_rows = []
    seen_rows = set()  # To track unique row identifiers (e.g., tuples of values)

    for _, row in df.iterrows():
        # Check if 'Merged' is a valid string
        summary = row['Merged']
        if isinstance(summary, str) and summary.strip():  # Ensure it's a non-empty string
            # Split the summary into individual words
            comment_words = summary.split()
            comment_words = [word.lower() for word in summary.split()]


            # Check for any part of the words in the comment
            for word in comment_words:
                for key, associated_word in word_dict.items():
                    if key in word:  # Check if key is part of the word
                        # Create a unique identifier for the current row
                        row_imp=[row['Indication Number / Номер заказа'], associated_word]
                        row_identifier = tuple(row_imp)  # Use a tuple of row values as identifier
                        

                        # Check if this identifier has already been seen
                        if row_identifier not in seen_rows:
                            new_row = row.copy()  # Create a copy of the row
                            new_row['Merged'] = associated_word
                            new_rows.append(new_row)  # Append the modified row
                            seen_rows.add(row_identifier)  # Mark this identifier as seen

    # Create a new DataFrame from the duplicated rows
    return pd.DataFrame(new_rows)

def subsystem_row_split(df,subsystem_dict_dict):
    new_rows = []
    seen_rows = set()  # To track unique row identifiers (e.g., tuples of values)

    for _, row in df.iterrows():
        # Check if 'Merged' is a valid string
        system = row['Merged']
        for key1,value1 in subsystem_dict_dict.items():
            if key1 in system:
                summary=row['Merged1']
                if isinstance(summary, str) and summary.strip():  # Ensure it's a non-empty string
            # Split the summary into individual words
                    comment_words = summary.split()
                    comment_words = [word.lower() for word in summary.split()]
                    for word in comment_words:
                        for key, associated_word in value1.items():
                            if key in word:  # Check if key is part of the word
                                # Create a unique identifier for the current row
                               # print(f"{associated_word} je nasao u {word}")
                                row_imp=[row['Indication Number / Номер заказа'], associated_word]
                                row_identifier = tuple(row_imp)  # Use a tuple of row values as identifier
                                

                                # Check if this identifier has already been seen
                                if row_identifier not in seen_rows:
                                    new_row = row.copy()  # Create a copy of the row
                                    new_row['Merged1'] = associated_word
                                    new_rows.append(new_row)  # Append the modified row
                                    seen_rows.add(row_identifier)  # Mark this identifier as seen
                



    # Create a new DataFrame from the duplicated rows
    return pd.DataFrame(new_rows)
                        
def unwanted_duplicates_filter(df, duplicates_dict):
    unwanted_rows = []
    for index, row in df.iterrows():
        for key, value in duplicates_dict.items():
            if row['Merged'] == key:
                primary_key = [row['Indication Number / Номер заказа'], value]
                unwanted_rows.append(primary_key)
    
    # Filter the dataframe based on the conditions in unwanted_rows
    for unwanted in unwanted_rows:
        df = df[~((df['Merged'] == unwanted[1]) & (df['Indication Number / Номер заказа'] == unwanted[0]))]

    return df
    
def vehicle_type_counter(adf, threshold_dict):
    system_threshold_dict_fnc = system_threshold_dict_alarm if mode=='alarm' else system_threshold_dict_warning
    # Group by 'Vehicle Number / Номер вагона' and 'Merged', and count occurrences
    try:
        adf['Counter'] = adf.groupby(['Vehicle Number / Номер вагона', 'Merged'])['Vehicle Number / Номер вагона'].transform('size')
    except Exception as e:
        return pd.DataFrame({'Indication Number / Номер заказа':[],'Vehicle Number / Номер вагона':[],
                            'Coach type / Модель вагона':[],'Date of Receipt':[],
                            'Merged':[],'Counter':[]})

    # Apply the threshold filtering based on the 'Merged' column
    adf['Threshold'] = adf['Merged'].map(system_threshold_dict_fnc)
    adf_filtered = adf[adf['Counter'] > adf['Threshold']]

    # Drop duplicates based on 'Vehicle Number / Номер вагона' and 'Merged'
    new_df3 = adf_filtered[['Indication Number / Номер заказа',
                           'Vehicle Number / Номер вагона',
                           'Coach type / Модель вагона',
                           'Date of Receipt',
                           'Merged',
                           'Counter']].drop_duplicates(subset=['Vehicle Number / Номер вагона', 'Merged'])

    return new_df3

def vehicle_type_counter_components(adf):
    # Group by 'Vehicle Number / Номер вагона' and 'Merged', and count occurrences
    adf['Counter'] = adf.groupby(['Vehicle Number / Номер вагона','Merged', 'Merged1'])['Vehicle Number / Номер вагона'].transform('size')


    adf = adf[adf.apply(exceeds_threshold_component, axis=1)]

    # Drop duplicates based on 'Vehicle Number / Номер вагона' and 'Merged'
    new_df = adf[['Indication Number / Номер заказа',
                           'Vehicle Number / Номер вагона',
                           'Coach type / Модель вагона',
                           'Date of Receipt',
                           'Merged',
                           'Merged1',
                           'Counter']].drop_duplicates(subset=['Vehicle Number / Номер вагона', 'Merged','Merged1'])

    return new_df

def vehicle_type_counter_components_fleet(adf):
    # Group by 'Vehicle Number / Номер вагона' and 'Merged', and count occurrences
    adf['Counter'] = adf.groupby(['Coach type / Модель вагона', 'Merged1','Merged'])['Coach type / Модель вагона'].transform('size')

    adf = adf[adf.apply(exceeds_threshold_component, axis=1)]

    # Drop duplicates based on 'Vehicle Number / Номер вагона' and 'Merged'
    new_df = adf[['Indication Number / Номер заказа',
                           'Vehicle Number / Номер вагона',
                           'Coach type / Модель вагона',
                           'Date of Receipt',
                           'Merged',
                           'Merged1',
                           'Counter']].drop_duplicates(subset=['Coach type / Модель вагона', 'Merged1', 'Merged'])

    return new_df

def fleet_type_counter(adf):
    system_threshold_dict_fnc = system_threshold_dict_alarm if mode=='alarm' else system_threshold_dict_warning
    # Group by 'Vehicle Number / Номер вагона' and 'Merged', and count occurrences
    adf['Counter'] = adf.groupby(['Coach type / Модель вагона', 'Merged'])['Coach type / Модель вагона'].transform('size')

    adf['Threshold'] = adf['Merged'].map(system_threshold_dict_fnc)
    adf_filtered = adf[adf['Counter'] > adf['Threshold']]

    # Drop duplicates based on 'Vehicle Number / Номер вагона' and 'Merged'
    new_df = adf_filtered[['Indication Number / Номер заказа',
                           'Coach type / Модель вагона',
                           'Date of Receipt',
                           'Merged',
                           'Counter']].drop_duplicates(subset=['Coach type / Модель вагона', 'Merged'])
    return new_df  

def filter_by_fleet(df,fleet_filter_menu):
    fleet_choice=fleet_filter_menu
    if fleet_choice=='All' or fleet_choice=='':
        return df
    elif fleet_choice=='All Siemens Vehicles':
        df=df[df['Coach type / Модель вагона'].isin(['Siemens Mireo GABY','Siemens Desiro GABY'])]
        return df
    elif fleet_choice=='All Stadler Vehicles':
        df=df[df['Coach type / Модель вагона'].isin(['FLIRT 3 GABY', 
    'GABW Stadler FLIRT3 EMU9', 
    'GABW Stadler FLIRT3 EMU6', 
    'GABW Stadler FLIRT3 EMU5', 
    'GABW Stadler FLIRT3 EMU4', 
    'GABW Stadler FLIRT3 EMU3'])]
        return df
    else:
        df=df[df['Coach type / Модель вагона']==fleet_choice]
        return df

def filter_by_vehicle(df,vehicle_filter_menu):
    vehicle_choice=vehicle_filter_menu
    if vehicle_choice=='All':
        return df
    else:
        df=df[df['Vehicle Number / Номер вагона']==float(vehicle_choice)]
        return df

def on_date_filter_change(pre_result, date_filter_menu,fleet_filter_menu, vehicle_filter_menu): #Ova 3 poslednja parametra su prosti stringovi
    fleet_system_dict_fnc = fleet_system_dict_alarm if mode=='alarm' else fleet_system_dict_warning
    filter_choice = date_filter_menu  # Get selected date filter
    try: # This try will only raise exception if not all the filters are selected (only expected to happen during the first filter applied)
        filtered_df = filter_data_by_date(pre_result, filter_choice)  # Filter data
        filtered_df = filter_by_fleet(filtered_df, fleet_filter_menu)
        filtered_df = filter_by_vehicle(filtered_df, vehicle_filter_menu)
    except Exception as e:
        return pd.DataFrame({'Vehicle Number / Номер вагона':[],'Coach type / Модель вагона':[],'Merged':[],'Counter':[]})
    filtered_df = split_row_by_partial_match(filtered_df, keyword_dict)
    filtered_df = unwanted_duplicates_filter(filtered_df, duplicates_dict)
    filtered_df = vehicle_type_counter(filtered_df, fleet_system_dict_fnc)
    filtered_df = exceeds_threshold_system(filtered_df,fleet_system_dict_fnc)
    try:
        filtered_df.sort_values(by='Vehicle Number / Номер вагона')
    except Exception as x:
        return pd.DataFrame({'Vehicle Number / Номер вагона':[],'Coach type / Модель вагона':[],'Merged':[],'Counter':[]})
    filtered_df = filtered_df.filter(['Vehicle Number / Номер вагона','Coach type / Модель вагона', 
                                    'Merged', 'Counter'])
    global export_df
    export_df = filtered_df
#print("Izasao iz on_date_filter_change")
#print("Tablica iz on_date_filter_change: ")
#print(filtered_df)
    return filtered_df
    # print(export_df)
    
def fleet_filter_change(df_fleet,date_filter_menu_fleet,fleet_filter_menu_fleet):
    fleet_system_dict_fnc = fleet_system_dict_alarm if mode=='alarm' else fleet_system_dict_warning
    filter_choice = date_filter_menu_fleet  # Get selected date filter
    filtered_df=filter_data_by_date(df_fleet,filter_choice)
    filtered_df=filter_by_fleet(filtered_df,fleet_filter_menu_fleet)
    filtered_df=split_row_by_partial_match(filtered_df, keyword_dict)
    filtered_df = unwanted_duplicates_filter(filtered_df, duplicates_dict)
    filtered_df=fleet_type_counter(filtered_df)
    filtered_df = exceeds_threshold_system(filtered_df,fleet_system_dict_fnc)
    filtered_df = filtered_df.filter(['Coach type / Модель вагона', 
                                    'Merged', 'Counter'])
    global export_df_fleet
    export_df_fleet=filtered_df
    return filtered_df

def component_filter_change(pre_result, date_filter_menu_component,fleet_filter_menu_component, vehicle_filter_menu_component,subsystem_dict_dict):
    filter_choice = date_filter_menu_component  # Get selected date filter
    filtered_df = filter_data_by_date(pre_result, filter_choice)  # Filter data
    filtered_df = filter_by_fleet(filtered_df, fleet_filter_menu_component)
    filtered_df = filter_by_vehicle(filtered_df, vehicle_filter_menu_component)
    filtered_df = split_row_by_partial_match(filtered_df, keyword_dict)
    filtered_df = unwanted_duplicates_filter(filtered_df, duplicates_dict)
    filtered_df = subsystem_row_split(filtered_df,subsystem_dict_dict)
    filtered_df = vehicle_type_counter_components(filtered_df)
    filtered_df = filtered_df.filter(['Vehicle Number / Номер вагона', 'Coach type / Модель вагона', 
                                    'Merged', 'Merged1', 'Counter'])
    filtered_df = filtered_df.sort_values(by='Vehicle Number / Номер вагона')
    global export_df_component 
    export_df_component = filtered_df
    return filtered_df
   
def component_filter_change_fleet(df_components, date_filter_menu_component_fleet,fleet_filter_menu_component_fleet,subsystem_dict_dict):
    filter_choice = date_filter_menu_component_fleet.get()  # Get selected date filter
    filtered_df = filter_data_by_date(df_components, filter_choice)  # Filter data
    filtered_df = filter_by_fleet(filtered_df, fleet_filter_menu_component_fleet)
    filtered_df = split_row_by_partial_match(filtered_df, keyword_dict)
    filtered_df = unwanted_duplicates_filter(filtered_df, duplicates_dict)
    filtered_df = subsystem_row_split(filtered_df,subsystem_dict_dict)
    filtered_df = vehicle_type_counter_components_fleet(filtered_df)
    filtered_df = filtered_df.filter(['Coach type / Модель вагона', 
                                    'Merged', 'Merged1', 'Counter'])
    global export_df_component
    export_df_component = filtered_df
    return filtered_df

def sort_treeview(tree, col, descending):
    data = [(tree.set(item, col), item) for item in tree.get_children('')]
    data.sort(reverse=descending)
    for index, (val, item) in enumerate(data):
        tree.move(item, '', index)
    tree.heading(col, command=lambda: sort_treeview(tree, col, not descending))

def export_to_excel(df):
    now_time=datetime.now()
    now_time=now_time.strftime("%Y-%m-%d_%H-%M-%S")
    df = df.rename(columns=column_dict)
    df.to_excel(os.path.join(base_path, f"System Export for vehicles {now_time}.xlsx"), index=False, sheet_name="System export")
    #`messagebox.showinfo("Export Successful", "Export to Excel completed")

def export_to_excel_fleet(df):
    now_time=datetime.now()
    now_time=now_time.strftime("%Y-%m-%d_%H-%M-%S")
    df = df.rename(columns=column_dict)
    df.to_excel(os.path.join(base_path, f"System Export for fleet {now_time}.xlsx"), index=False, sheet_name="System export")


def export_to_excel_component(df):
    now_time=datetime.now()
    now_time=now_time.strftime("%Y-%m-%d_%H-%M-%S")
    df = df.rename(columns=column_dict)
    df.to_excel(os.path.join(base_path, f"System Export for component {now_time}.xlsx"), index=False, sheet_name="System export")



def setup_vehicle_component_analysis():
    pre_result['Merged1']=pre_result['Merged']
    global df_components
    df_components = pre_result.filter(['Indication Number / Номер заказа','Vehicle Number / Номер вагона', 'Coach type / Модель вагона', 'Date of Receipt', 
                                    'Merged', 'Merged1', 'Counter'])
    return copy.deepcopy(df_components)

def daj_pre_result():
    return pre_result


def setup():
    global mode
    mode = 'warning'

    global pre_result
    df_excel = pd.read_excel(os.path.join(base_path, "Corrective Indications Monitor.xlsx"))
    df_excel=update_table(df_excel)
    
    
    pre_result = df_excel
    pre_result = pre_result.filter(['Indication Number / Номер заказа', 'Vehicle Number / Номер вагона', 'Coach type / Модель вагона', 
                                    'Date of Receipt', 'Summary', 'Works performed / Выполненные работы', 'Description of the failure / Описание неисправности'])
    
    pre_result['Date of Receipt'] = pd.to_datetime(pre_result['Date of Receipt'])
    pre_result['Merged'] = pre_result.apply(lambda row: f"{row['Summary']} {row['Works performed / Выполненные работы']} {row['Description of the failure / Описание неисправности']}", axis=1)
    pre_result['Merged1']=pre_result['Merged']
    pre_result = pre_result.filter(['Indication Number / Номер заказа', 'Vehicle Number / Номер вагона', 'Coach type / Модель вагона', 
                                    'Date of Receipt','Merged1', 'Merged'])
    pre_result['Counter'] = 0
    pre_result = pre_result.replace(to_replace=fleets_dict)
    pre_result['Merged'] = pre_result['Merged'].str.lower()
    pre_result = pre_result.replace(to_replace=wrong_spelling_dict)
    
    global df_components
    df_components = pre_result.filter(['Indication Number / Номер заказа','Vehicle Number / Номер вагона', 'Coach type / Модель вагона', 'Date of Receipt', 
                                    'Merged', 'Merged1', 'Counter'])



# This function takes a (pandas) DataFrame and returns a list containing ft.DataRow objects.
# Every row from given input is converted.
def rows(df : pd.DataFrame) -> list:
    rows = []
    for index, row in df.iterrows(): # Go through every row of the given DataFrame
        # To the "rows" append flet "DataRow" objact consisting of list of flet "DataCell" objects
        # where each "DataCell" object contains a single value from the given row matching the column name
        rows.append(ft.DataRow(cells = [ft.DataCell(ft.Text(row[header])) for header in df.columns]))
    return rows

# Switched the value of global variable 'mode' from 'warning' to 'alarm' when called, and vice versa
def update_mode_alarms_warnings():
    global mode
    if mode == 'warning':
        mode = 'alarm'
    else:
        mode = 'warning'

def main(page: ft.Page):



    # --------------------
    #
    # Settings for the main window and setting up the page
    #
    # --------------------

    # The seetings for the main window in which all the content
    # from all the pages is displayed   
    page.padding = ft.padding.only(left=75, right=0, top=0, bottom=0) # Padding on the left so the logo and the table are aligned
    # Application isn't supported on any resolutions other than 1920x1080
    page.window.width = 1920 # Set the width of the window of the whole application
    page.window.height = 1080 # Set the height of the window of the whole application 
    #Set page colors to transparent because the actual background is the image
    page.bgcolor = ft.colors.TRANSPARENT
    page.window.bgcolor = ft.colors.TRANSPARENT 
    page.window.maximized = True # Set the window to be maximized by default
    page.title = "Corrective Indications Monitor - CIM  |  W&L" # Set the title of the page to the name of the application
    page.decoration = ft.BoxDecoration( # Set the actual background of the page to the image
        image = ft.DecorationImage(
                # For the compatibility and portability reasons the image should be a link rather than a local file
                src="https://i.imgur.com/bQElUhc.png",
                fit=ft.ImageFit.FIT_WIDTH # If the image fits wrong, play around with this setting
            ),
        )
    global warnings_alarms_text
    warnings_alarms_text = 'init'
    warnings_alarms_text_container=ft.Text(warnings_alarms_text)

    global export_mode # Controls what kind of table will be export to excel
    export_mode = 'Main window'

    # ----------------------------------------
    #
    # Setting up the logic module for all pages
    #
    # ----------------------------------------

    # Initialiation of the logic module and downloading
    # of the data from Amigo Boom platform
    
    setup()
    # Initial table, without ANY filters applied
    # which will be used as a base for filtering
    initial_df=copy.deepcopy(daj_pre_result())

    # Global variable for the data frame in the main window
    global df # At the beggining, fill datafarme df with all the data, or filter it least strictly
    df = on_date_filter_change(initial_df,"Last three months","All","All")

    global dff #df is for main window data manipulation, whereas dff is for fleet analysis page 
    dff=copy.deepcopy(df.filter(['Coach type / Модель вагона', 'Merged', 'Counter']))

    # This is the data_table which will be displayed in the main window
    # contains all the filtered data
    global data_table

    # Make the data_table which will be displayed in the main window, but don't display it yet
    # This function is called every time when the filters in main window are changed by update_display_table function
    def make_display_table(*args):
        # Create data table (scrollable, without headers)
        global data_table
        data_table = copy.deepcopy(ft.DataTable( # Create a deep copy so data_table is not changed atuomatically if df is changed
            columns=[ # In order to make sticky header, this table only displays row data, so the column names are empty
                ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[0])), #Vehicle ID
                ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[1])), #Fleet
                ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[2])), #System
                ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[4])), #Indications
            ],
            
            # Display the rows from df, and sort them by 'Counter' ('Indciations'), in descending order
            rows=rows(copy.deepcopy(df.sort_values('Counter',ascending=False))),
            heading_row_height=0, #Heading row consists of empty column names, so there's no need to display it
            show_bottom_border=True,))
        
    global fleet_selector
    global time_interval_selector
    global vehicle_selector

    # This function is called every time when the filters in main window are changed
    # It will make the datd_table filled with filtered data, AND display it
    def update_display_table(*args):
        page.snack_bar = fcc.Snack_bar_cl("Table is being updated...") # Notifies user of the update process strarting
        page.snack_bar.open = True 
        page.update() # snack_bar won't display until both snack_bar.open is set to True and page is updated
        global df # Make filtered data frame that will need to be converted to ft.DataTable

        # Data frame based on which the display table will be made
        # is created by the logic module based on the filters applied,
        # and the value of filters is the value from the dropdown menus
        df = copy.deepcopy(on_date_filter_change(copy.deepcopy(initial_df),time_interval_selector.value,fleet_selector.value,vehicle_selector.value))

        try:
            make_display_table() # Make data_table based on dataframe df
        except Exception as e:
            page.snack_bar.open=False
            page.add(ft.Text("Aha"))
            page.update()
        data_container.controls = [data_table]  # Update the data_container with the new data_table
        data_container.update()  # Refresh the data_container to reflect changes
        page.snack_bar = fcc.Snack_bar_cl("Table updated!",4234) # Let the user know that the new table is now displayed
        if len(data_table.rows) == 0: # If there are no rows returned (at the startup when not all filters are applied)
            page.snack_bar = fcc.Snack_bar_cl("",1) # Quickly close the snack_bar
        page.snack_bar.open = True # Display the new snack_bar whateer it may be
        #warnings_alarms_text_container.controls = ft.Text(show_warnings_toggle.text())
        #warnings_alarms_text_container.update()
        page.update() # Refresh the whole page so the user sees the changes
        print(df)

    # Do this when the toggle to switch between warning and alarm mode is clicked
    def toggle_mode_switch(*args):
        update_mode_alarms_warnings() # Update the value of the variable 'mode' that toggles between alarms and warnings
        update_display_table() # To reflect new filters

    # Create the display table that user will see in the main window
    # on the application start, it will be empty
    # but by calling this function dataframe df will be set correctly
    make_display_table()

    global data_table
    data_table.rows=[] # The initial data table is empty because the user hasn't applied any filters yet


    # Clicking on any of these buttons will take the user to the wanted page
    # Though the fucntion acutally making them navigate on click is implemented below because it needs to have all the
    # pages it links to already defined
    analyze_fleet_button = fcc.Std_button_cl("Fleet Analysis",None) #  std_button isn't a library defined thing, but a standard button for this application
    analyze_component_button = fcc.Std_button_cl("Fleet Component Analysis",None)
    analyze_vehicle_component_button = fcc.Std_button_cl("Vehicle Component Analysis",None)
    
    def show_export_dialog(e): # Dialog for exxporting to excel
        dodatak = 'successful'
        def close_export_dialog(e): # This function handles closing of the export dialog
            if export_mode == 'Main window': # This elif block determines which table exactly to export
                export_to_excel(df) # This function actually makes excel file
            elif export_mode == 'Fleet analysis window':
                export_to_excel_fleet(dff)
            elif export_mode == 'Fleet component window':
                export_to_excel_component(dfc)
            elif export_mode == 'Vehicle component window':
                export_to_excel_component(df_vehicle)
            else:
                dodatak = 'unsuccessful' # If none of the support export modes are selected, make error message.
            export_dialog.open = False
            page.update()

        export_dialog = ft.AlertDialog(
            title=ft.Text("Export to Excel"),
            content=ft.Text(value=f'\n    Exporting to excel {dodatak} !\n     ',max_lines=3),
            actions=[
                ft.TextButton("Close", on_click=close_export_dialog)
            ],
        )        
        
        page.overlay.append(export_dialog)
        export_dialog.open = True
        page.update()

    # Create export button (for exporting to excel)
    export_button = fcc.Std_button_cl("Export to Excel",None,True)
    

    # Create header table, that's the one that contains only column names and no rows
    header_table = ft.DataTable(
        columns=[ # Adjust these strings for the visual alignment
            ft.DataColumn(ft.Container(ft.Text("Vehicle ID"), width=fcc.column_widths[0])),
            ft.DataColumn(ft.Container(ft.Text("                     Fleet"), width=fcc.column_widths[1])),
            ft.DataColumn(ft.Container(ft.Text("                                           System"), width=fcc.column_widths[2]*1.2)),
            ft.DataColumn(ft.Container(ft.Text("                                                      Indications"), width=fcc.column_widths[4]*5)),
        ],
        rows=[],
        heading_row_height=60,
        border=None,  # Remove border from header table
        show_bottom_border=True,
    )  

    # Create a container for the fixed header
    header_container = ft.Container(
        content=header_table,
        padding=ft.padding.only(left=30, right=30),
    )

    # data_container consists of ListView which contains data_table in which the actual data is stored
    # This is done so there are more customization options for the way data_table is displayed
    data_container = ft.ListView(
        controls=[data_table],
        height=600,  # Adjust height to account for header and make sure logo isn't obscured
        padding=fcc.tables_padding
    )

    # Combine header and data in a Column
    styled_container = ft.Container(
        #width=(fcc.column_widths[0] + fcc.column_widths[1] + fcc.column_widths[2] + fcc.column_widths[3] + fcc.column_widths[4])*1.5,
        width = 1242,
        bgcolor = ft.colors.WHITE,
        content=ft.Column(
            controls=[
                header_container,
                data_container
            ],
            spacing=0, # No spacing between header and data tables in order to make them appear as one
        ),
        border=ft.border.all(1, "#DBDBDB"), # Options for the tasteful appearance
        border_radius=10,
    )



    # ----------------------------------------
    #
    # Code for fleet analysis page
    #
    # ----------------------------------------

# Create new page data table
    global page_data_table_fleet
    page_data_table_fleet = ft.DataTable(columns=[ft.DataColumn(ft.Text("")),ft.DataColumn(ft.Text("")),ft.DataColumn(ft.Text("")),], 
    rows=[]) # Make the rows empty, so the displayed table is empty upon opening the page

        # Make the table for displaying data based on data from dff
    def make_display_table_fleet():
            print("In make_display_table_fleet")
            global page_data_table_fleet
            page_data_table_fleet = copy.deepcopy(ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[1])), # Fleet
                    ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[2])), # System
                    ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[4])), # Indications
                ],
                rows=rows(copy.deepcopy(dff)),
                heading_row_height=0,
                show_bottom_border=True,
            ))
            print("dff = ")
            print(dff)
            print("rows in the table itself: ")
            print(page_data_table_fleet.rows)
            page.data_table_fleet.update()
            page.update()
            # Create a copy data table for the fleet analysis page specifically, contains only row data
    
    page_data_table_fleet = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[0])),
                ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[2])),
                ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[4])),
            ],
            rows=[], # The initial data table is empty because the user hasn't applied any filters yet
            heading_row_height=0,
            show_bottom_border=True,
        )

    global page_data_container_fleet
    page_data_container_fleet = ft.ListView(
            controls=[page_data_table_fleet],
            height=630,
            spacing=0,
            padding=ft.padding.only(left=10, right=10, bottom=10),
        )
    
    # Create a copy header table for the fleet analysis page specifically, contains only column names
    page_header_table_fleet = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Container(ft.Text("Fleet"), width=fcc.column_widths[0])),
                ft.DataColumn(ft.Container(ft.Text("                                       System"), width=fcc.column_widths[2])),
                ft.DataColumn(ft.Container(ft.Text("                                       Indications"), width=fcc.column_widths[4]*3)),
            ], 
            rows=[],
            heading_row_height=50, # Do not change
            border=None, # In order to make this table and data table look like one
            show_bottom_border=True,
        )

    # Create containers for the table components, these enable us to tweak the look further
    page_header_container_fleet = ft.Container(
            content=page_header_table_fleet,
            width=1400,
            padding=ft.padding.only(left=10, right=10, top=10),
        )

    global page_styled_container_fleet
    page_styled_container_fleet = ft.Container( # Container containing both header and data tables
            width=(fcc.column_widths[0] + fcc.column_widths[1] + fcc.column_widths[2] + fcc.column_widths[3] + fcc.column_widths[4])*1.5,
            bgcolor=ft.colors.WHITE,
            content=ft.Column(
                controls=[
                    page_header_container_fleet,
                    page_data_container_fleet
                ],
                spacing=0, # No spacing between header and data tables in order to make them appear as one
            ),
            border=ft.border.all(1, "#DBDBDB"), # Options for the tasteful appearance
            border_radius=10,
        )

    
        # This function is called every time the filters on the fleet analysis page are changed
        # This function updates the values in the dff datafarme, makes a page_data_table_fleet based on it,
        # and displays it by updating the page_data_container_fleet and the page itself
    def update_display_table_fleet(*args): 
            page.snack_bar = fcc.Snack_bar_cl("Table is being updated...") # Notifies user of the update process strarting
            page.snack_bar.open = True 
            page.update() # snack_bar won't display until both snack_bar.open is set to True and page is updated
            global page_data_table_fleet
            global dff # dff equals the dataframe returned from fleet_filter_change function, which starts with initial_df and then filters it based on the selected time interval and fleet
            # Finally, the result is sorted by 'Counter' which is 'Indications' column in the display, in descending order, so the most alarming indications are displayed first
            try:
                global dff
                dff = copy.deepcopy(fleet_filter_change(copy.deepcopy(initial_df),time_interval_selector.value,fleet_selector.value).sort_values('Counter',ascending=False))
                make_display_table_fleet() # Make the table for displaying data based on data from dff
            except Exception as e:
                print("Error in update_display_table_fleet",e)
            global page_data_container_fleet
            page_data_container_fleet.controls = [page_data_table_fleet]  # Update the data_container with the new data_table
            page_data_container_fleet.update()  # Refresh the data_container to reflect changes
            global page_styled_container_fleet
            page_styled_container_fleet.update()
            page.snack_bar = fcc.Snack_bar_cl("Table updated!",4234) # Let the user know that the new table is now displayed
            if len(data_table.rows) == 0: # If there are no rows returned (at the startup when not all filters are applied)
                page.snack_bar = fcc.Snack_bar_cl("",1) # Quickly close the snack_bar
            page.snack_bar.open = True # Display the new snack_bar whateer it may be
            page.update() # Update the whole page to display changes to data_container and the data_table within it

    # The function that gets called upon clicking the 'Fleet Analysis' button
    # This function clears old page, constructs new page, displays new filtered data grouped by fleet
    def go_to_fleet_analysis(e):

        # Clear the old page
        page.clean()

        global page_styled_container_fleet
        
        global export_mode #So the right kind of table is exported upon clicking the "Export to Excel" button on this page
        export_mode = "Fleet analysis window"

        # Do this when the toggle to switch between warning and alarm mode is clicked
        def toggle_mode_switch_fleet(*args):
            update_mode_alarms_warnings() # # Update the value of the variable 'mode' that toggles between alarms and warnings
            update_display_table_fleet() # To reflect new filters

        page_export_button = fcc.Std_button_cl("Export to Exccel",show_export_dialog,True) # Create local export button
        back_button = fcc.Std_button_cl("Back",lambda e: go_to_main(e)) # Clicking on this button sends the user back to the main page (one seen on bootup)
        back_button.width = 100 # Back button is smaller than others

        show_warnings_toggle_fleet = fcc.Show_warnings_toggle_cl(toggle_mode_switch_fleet,False if mode == 'alarm'else True)

        page.add( # Render the page for the "Fleet Analysis" window
            ft.Container(
                margin=ft.margin.only(left=40, top=40),
                content=ft.Column([
                    ft.Row([
                        back_button,
                        ft.Container(width=fcc.std_spacing_width),
                        time_interval_selector,
                        ft.Container(width=fcc.std_spacing_width),
                        fleet_selector,
                        ft.Container(width=fcc.std_spacing_width),
                        show_warnings_toggle_fleet,
                        ft.Container(width=fcc.std_spacing_width),
                        page_export_button,
                    ]),
                    ft.Container(height=30),
                    page_styled_container_fleet,
                ])
            )
        )
        update_display_table_fleet()
        page.update() # Update the page to display changes
        

    # ----------------------------------------
    #
    # Code for component analysis page
    #
    # ----------------------------------------
    
    global df_components # Global dataframe on which any filters will be applies
    df_components = copy.deepcopy(pre_result.filter(['Vehicle Number / Номер вагона', 'Coach type / Модель вагона', 
                                    'Merged', 'Merged1', 'Counter']))
    global page_data_table_component
    page_data_table_component = ft.DataTable(columns=[ft.DataColumn(ft.Text("")),ft.DataColumn(ft.Text("")),ft.DataColumn(ft.Text("")),ft.DataColumn(ft.Text("")),ft.DataColumn(ft.Text("")),], 
    rows=[])

    component_page_data_container = ft.ListView(
            controls=[page_data_table_component],
            height=630,
            spacing=0,
            padding=ft.padding.only(left=10, right=10, bottom=10),
        )

    def make_display_table_component(*args): # Make the table that will be displayed based on the data from dfc
            global page_data_table_component
            page_data_table_component = copy.deepcopy(ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[0])),
                    ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[1])),
                    ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[2])),
                    ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[3])),
                    ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[4])),
                ],
                rows=rows(copy.deepcopy(dfc)),
                heading_row_height=0,
                show_bottom_border=True,
                    
            ))


    def update_display_table_component(*args): # Update the data in the table based on filters and display it
            page.snack_bar = fcc.Snack_bar_cl("Table is being updated...") # Notifies user of the update process strarting
            page.snack_bar.open = True 
            page.update() # snack_bar won't display until both snack_bar.open is set to True and page is updated
            global dfc
            global df_components
            try:
                df_components = copy.deepcopy(pre_result.filter(['Indication Number / Номер заказа','Vehicle Number / Номер вагона', 'Coach type / Модель вагона', 'Date of Receipt', 
                                    'Merged', 'Merged1', 'Counter']))
                dfc = copy.deepcopy(component_filter_change(copy.deepcopy(df_components),time_interval_selector.value,fleet_selector.value,"All",subsystem_dict_dict).sort_values('Counter',ascending=False))

                make_display_table_component()
            except:
                print("Error in update_display_table_component")
            component_page_data_container.controls = [page_data_table_component] # Update the data_container with the new data_table
            component_page_data_container.update()  # Refresh the data_container to reflect changes
            page.snack_bar = fcc.Snack_bar_cl("Table updated!",4234) # Let the user know that the new table is now displayed
            if len(data_table.rows) == 0: # If there are no rows returned (at the startup when not all filters are applied)
                page.snack_bar = fcc.Snack_bar_cl("",1) # Quickly close the snack_bar
            page.snack_bar.open = True # Display the new snack_bar whateer it may be
            page.update() # Update the whole page to display changes to data_container and the data_table within it
        

    def go_to_component_analysis(e):
        page.clean() # Clear the old page

        global export_mode #So the right kind of table is exported upon clicking the "Export to Excel" button on this page
        export_mode = "Fleet component window"

        # Do this when the toggle to switch between warning and alarm mode is clicked
        def toggle_mode_switch_component(*args):
            update_mode_alarms_warnings() # # Update the value of the variable 'mode' that toggles between alarms and warnings
            update_display_table_component() # To reflect new filters

        # Create local export button and back button
        page_export_button = fcc.Std_button_cl("Export to Exccel",show_export_dialog,True)
        back_button = fcc.Std_button_cl("Back",lambda e: go_to_main(e)) # Clicking on this button sends the user back to the main page (one seen on bootup)
        back_button.width = 100 
        
        # Create a header table for fleet fleet component analysis page
        page_header_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Container(ft.Text("Fleet"), width=fcc.column_widths[0])),
                ft.DataColumn(ft.Container(ft.Text("      Vehicle ID"), width=fcc.column_widths[1])),
                ft.DataColumn(ft.Container(ft.Text("            System"), width=fcc.column_widths[2])),
                ft.DataColumn(ft.Container(ft.Text("                  Subsystem"), width=fcc.column_widths[3])),
                ft.DataColumn(ft.Container(ft.Text("                       Indications"), width=fcc.column_widths[4]*3)),
            ],
            rows=[],
            heading_row_height=50,
            border=None,
            show_bottom_border=True,
        )

        page_data_table_component = ft.DataTable( # Create a data table for fleet component analysis page
            columns=[
                ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[0])),
                ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[1])),
                ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[2])),
                ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[3])),
                ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[4])),
            ],
            rows=[],
            heading_row_height=0,
            show_bottom_border=True,
        )

        # Create containers for the table components
        page_header_container = ft.Container(
            content=page_header_table,
            padding=ft.padding.only(left=10, right=10, top=10),
        )

        component_page_styled_container = ft.Container( # Create a container for the header and data tables together
            width=(fcc.column_widths[0] + fcc.column_widths[1] + fcc.column_widths[2] + fcc.column_widths[3] + fcc.column_widths[4])*1.5,
            bgcolor=ft.colors.WHITE,
            content=ft.Column(
                controls=[
                    page_header_container,
                    component_page_data_container
                ],
                spacing=0, # No spacing between header and data tables in order to make them appear as one
            ),
            border=ft.border.all(1, "#DBDBDB"), # Options for the tasteful appearance
            border_radius=10,
        )

        
        show_warnings_toggle_component = fcc.Show_warnings_toggle_cl(toggle_mode_switch_component,False if mode == 'alarm'else True) # Create a toggle for showing alarms or all indications

        page.add( # Add all the components to the Fleet component analysis page
            ft.Container(
                margin=ft.margin.only(left=40, top=40),
                content=ft.Column([
                    ft.Row([
                        back_button,
                        ft.Container(width=fcc.std_spacing_width),
                        time_interval_selector,
                        ft.Container(width=fcc.std_spacing_width),
                        fleet_selector,
                        ft.Container(width=fcc.std_spacing_width),
                        show_warnings_toggle_component,
                        ft.Container(width=fcc.std_spacing_width),
                        page_export_button,
                    ]),
                    ft.Container(height=30),
                    component_page_styled_container,
                ])
            )
        )
        update_display_table_component()
        page.update() # Update the page to display changes

    # ----------------------------------------
    #
    # Code for VEHICLE component analysis page
    #
    # ----------------------------------------

    def update_display_table_vehicle(*args): # Updates the data in the table based on filters and displays it
            page.snack_bar = fcc.Snack_bar_cl("Table is being updated...") # Notifies user of the update process strarting
            page.snack_bar.open = True 
            page.update() # snack_bar won't display until both snack_bar.open is set to True and page is updated

            page_data_table.rows=[]
            global df_vehicle # Global dataframe on which any filters will be applies
            df_vehicle = copy.deepcopy(component_filter_change(setup_vehicle_component_analysis(),time_interval_selector.value,fleet_selector.value,vehicle_selector.value,subsystem_dict_dict).sort_values('Counter',ascending=False))
            page_data_table.rows=rows(df_vehicle) # Update the data in the data_table based on the data_frame
            page_data_table.update() # Refresh the data_table to reflect changes
            page.snack_bar = fcc.Snack_bar_cl("Table updated!",4234) # Let the user know that the new table is now displayed
            if len(data_table.rows) == 0: # If there are no rows returned (at the startup when not all filters are applied)
                page.snack_bar = fcc.Snack_bar_cl("",1) # Quickly close the snack_bar
            page.snack_bar.open = True # Display the new snack_bar whateer it may be
            page.update() # Update the whole page to display changes to data_table

    page_data_table = ft.DataTable( # Create a data table for vehicle component analysis page
            columns=[
                ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[0])),
                ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[1])),
                ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[2])),
                ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[3])),
                ft.DataColumn(ft.Container(ft.Text(""), width=fcc.column_widths[4])),
            ],
            rows=[], # The initial data table is empty because the user hasn't applied any filters yet
            heading_row_height=0, # Do not change, makes header table and this tabble appear as one
            show_bottom_border=True,
        )

    def go_to_vehicle_component_analysis(e):

        page.clean() # Clear the old page

        global export_mode #So the right kind of table is exported upon clicking the "Export to Excel" button on this page
        export_mode = "Vehicle component window"

        # Do this when the toggle to switch between warning and alarm mode is clicked
        def toggle_mode_switch_vehicle_component(*args):
            update_mode_alarms_warnings() # Update the global variable 'mode' that switched between 'alarm' and 'warning'
            update_display_table_vehicle() # To reflect new filters
        

        # Create local export button and back buttons
        page_export_button = fcc.Std_button_cl("Export to Exccel",show_export_dialog,True)
        back_button = fcc.Std_button_cl("Back",lambda e: go_to_main(e)) # Clicking on this button sends the user back to the main page (one seen on bootup)
        back_button.width = 100 
        
        # Create a header table for vehicle component analysis page, contains only column names
        page_header_table = ft.DataTable( 
            columns=[
                ft.DataColumn(ft.Container(ft.Text("Fleet"), width=fcc.column_widths[0])),
                ft.DataColumn(ft.Container(ft.Text("      Vehicle ID"), width=fcc.column_widths[1])),
                ft.DataColumn(ft.Container(ft.Text("            System"), width=fcc.column_widths[2])),
                ft.DataColumn(ft.Container(ft.Text("                  Subsystem"), width=fcc.column_widths[3])),
                ft.DataColumn(ft.Container(ft.Text("                 Indications"), width=fcc.column_widths[4]*2)),
            ],
            rows=[],
            heading_row_height=50, # Do not change
            border=None, # In order to make this table and data table look like one
            show_bottom_border=True,
        )

        # Create containers for the table components
        page_header_container = ft.Container(
            content=page_header_table,
            padding=ft.padding.only(left=10, right=10, top=10),
        )

        page_data_container = ft.ListView(
            controls=[page_data_table],
            height=630,
            spacing=0,
            padding=ft.padding.only(left=10, right=10, bottom=10),
        )

        page_styled_container = ft.Container( # Container containing containers for data table and header table
            width=(fcc.column_widths[0] + fcc.column_widths[1] + fcc.column_widths[2] + fcc.column_widths[3] + fcc.column_widths[4])*1.5,
            bgcolor=ft.colors.WHITE,
            content=ft.Column(
                controls=[
                    page_header_container,
                    page_data_container
                ],
                spacing=0,
            ),
            border=ft.border.all(1, "#DBDBDB"),
            border_radius=10,
        )
        
        show_warnings_toggle_vehicle = fcc.Show_warnings_toggle_cl(toggle_mode_switch_vehicle_component,False if mode == 'alarm'else True) # Create a toggle for showing alarms or all indications

        page.add( # Add all the components to the Vehicle component analysis page
            ft.Container(
                margin=ft.margin.only(left=40, top=40),
                content=ft.Column([
                    ft.Row([
                        back_button,
                        ft.Container(width=fcc.std_spacing_width),
                        time_interval_selector,
                        ft.Container(width=fcc.std_spacing_width),
                        fleet_selector,
                        ft.Container(width=fcc.std_spacing_width),
                        vehicle_selector,
                        ft.Container(width=fcc.std_spacing_width),
                        show_warnings_toggle_vehicle,
                        ft.Container(width=fcc.std_spacing_width),
                        
                    ]),
                    ft.Container(height=30),
                    ft.Row([page_styled_container,
                            ft.Container(width=fcc.std_spacing_width),
                            ft.Column([page_export_button,ft.Container(height = 500),]),

                        ])
                ]),
            )
        )
        update_display_table_vehicle()
        page.update() # Update the page to display changes


    def go_to_main(e): # Cleans the page and displays main page again
        page.clean()
        global show_warnings_toggle
        show_warnings_toggle.update_me(False if mode == 'alarm' else True) # Update the warnings and alarms toggle in the main page
        global export_mode # Bring the export mode back to the one appopriate for the main page
        export_mode = 'Main window'
        build_main_page()
        page.update()

    def build_main_page():
        page.add(
            ft.Stack([
                ft.Container(
                    margin=ft.margin.only(left=40, top=40),
                    content=ft.Row([
                        ft.Column([   
                            ft.Row([
                                time_interval_selector,
                                ft.Container(width=fcc.expanded_spacing_width),
                                fleet_selector,
                                ft.Container(width=fcc.expanded_spacing_width),
                                vehicle_selector,
                                ft.Container(width=fcc.expanded_spacing_width),
                                show_warnings_toggle,
                            ]),
                            ft.Container(height=40),
                            styled_container, # This one displays the actual data
                            #warnings_alarms_text_container,
                            ft.Container(height=30),
                        ]),
                        ft.Container(width=fcc.table_buttons_separation_width),
                        ft.Column([ # Fiddle with these values, if required in order to align the top of the button with the top of the table
                            ft.Container(height=fcc.table_buttons_top_separation),
                            analyze_fleet_button,
                            ft.Container(height=fcc.table_buttons_separation_height),
                            analyze_component_button,
                            ft.Container(height=fcc.table_buttons_separation_height),
                            analyze_vehicle_component_button,
                            ft.Container(height=fcc.table_buttons_separation_height*6),
                            export_button,
                            ft.Container(height=245),
                        ])
                    ]),
                )
            ])
        )

    

    # ----------------------------------------
    #
    # Code for dropdown menus, buttons, and UI in general
    #
    # ----------------------------------------

    def update_table_resolver(*args):
        global export_mode
        if export_mode == 'Main Window' or export_mode == 'Main window': update_display_table() # Update display table to reflect new fleet filter``
        elif export_mode == "Fleet analysis window": update_display_table_fleet()
        elif export_mode == "Fleet component window": update_display_table_component()
        elif export_mode == "Vehicle component window": update_display_table_vehicle()
        else:
            print("Update table resolver error, no valid window string! Export mode is: ")
            print(export_mode)

    # Create a time interval selector for main page, which updates main display table when clicked
    time_interval_selector = fcc.Time_interval_selector_cl(update_table_resolver)
    
    def fleet_selector_update(*args): # When updating fleet you also have to update vehicle dropdown
        vehicle_selector.fleet_resolver(fleet_selector.value) # Update the options offered in vehicle dropdown according to fleet
        vehicle_selector.update()
        update_table_resolver() # Resolve which table to update depending on which window you're in
        
    # Create a fleet selector for main page, which updates main display table when clicked
    fleet_selector = fcc.Fleet_selector_cl(fleet_selector_update)
    # Create a vehicle selector for main page, which updates main display table when clicked
    vehicle_selector = fcc.Vehicle_selector_cl(update_table_resolver,'All')



    # Create a toggle that can switch between showing all indications or only warnings
    global show_warnings_toggle
    show_warnings_toggle = fcc.Show_warnings_toggle_cl(toggle_mode_switch,False if mode == 'alarm'else True)

    
    def connect_main_page_buttons(): # Make the appropriate buttons do what they should when clicked (open their respective pages)
        analyze_fleet_button.on_click = go_to_fleet_analysis # When the button that says "Fleet Analysis" is clicked, go to the fleet analysis page
        analyze_component_button.on_click = go_to_component_analysis # When the button that says "Fleet Component Analysis" is clicked, go to the fleet component analysis page
        analyze_vehicle_component_button.on_click = go_to_vehicle_component_analysis # When the button that says "Vehicle Component Analysis" is clicked, go to the vehicle component analysis page
        export_button.on_click = show_export_dialog # Show the export dialog that notifies of excel export being sucessful or unsuccessful

    # Build the initial main page, that's what the user sees when the application starts
    build_main_page()
    connect_main_page_buttons()

ft.app(target=main, assets_dir="assets")