import logging

logging.basicConfig(filename='test.log', level=logging.INFO, format='%(asctime)s:(levelname)s:%(message)s')

import os
from pymodbus.client.sync import ModbusTcpClient
from time import sleep

#import voice
"""
%M 10  -  security
%M 9  -  liquide
%M 11  -  bac
%M 13  -  metal
%M 15 - verre
output
%M 1  -  acier
%M 2  -  alu
%M 3  -  pet
%M 4  -  pehd
%M 5 -  ppps
%M 6  -  verre
%M 7 -  carton
%M 8 -  papier
%M 14  -  tetra

liquide = [False, False, True] -> liquide[0] état précédent, liquide[1] état présent, liquide[2] autorisation envoi sms
"""

logging.info("Creating variables")

liquide = [False, False, True]
bac = [False, False, True]
secu = [False, False, True]
secuInstant = [False, False, True]
metal = False
verre = False



global plc
global ipPLC 

plc = None
ipPLC = "192.168.1.15"

logging.info("DONE Creating variables" + " from PLC")

def play(f):
    try:
        os.system("play /home/erw525/finalModules/voice/" + f)
    except Exception as e:
        logging.info(str(e) + " from PLC")

def init(ipPLC):

    logging.info("Init plc connection" + " from PLC")

    global plc

    try:
        plc = ModbusTcpClient(ipPLC)
    except Exception as e:
        logging.info(str(e) + " from PLC" + " from PLC")

    count = 0

    while plc.connect() != True:
        
        try:
            plc.connect()

            print("Couldn't Connect to PLC, check ip adress")
            
            play("plcNonCo.wav")

            sleep(5)

            count = count + 1

        except:
            if count < 5:
                logging.info(str(e) + " from PLC")

    logging.info("Connexion done" + " from PLC")

    play("plcOK.wav")

    # play("verifDebut.wav")

    # sleep(5)

    # testSorties()

    # play("verifDebutOK?.wav")

def testSorties():

    logging.info("Trying plc outputs" + " from PLC")
    try:
        setCoil(1)
        sleep(5)
        setCoil(2)
        sleep(5)
        setCoil(3)
        
        sleep(5)
        setCoil(7)
        sleep(5)
        setCoil(6)
        sleep(5)
    except Exception as e:
        logging.info(str(e) + " from PLC")

    logging.info("DONE Trying plc outputs" + " from PLC")

def setCoil(coil):
    """
    Pour activer une sortie
    %M --- > %Q

    %M 1 --> Q0
    %M 2 --> Q1
    %M 3 --> Q2
    %M 7 --> Q3
    %M 6 --> Q4
    """
    global plc

    try:
        plc.write_coil(coil, False)
        plc.write_coil(coil, True)
        sleep(3)
        plc.write_coil(coil, False)
    except Exception as e:
        logging.info(str(e) + " from PLC")
        play("plcNonCo.wav")
    

def unsetCoil(coil):

    global plc

    try:
        plc.write_coil(coil, False)
    except Exception as e:
        logging.info("Coudn't deactivate PLC's output, with error : " + str(e))

def getCoil(name):

    if name == "liquide":
        coil = 9
    elif name == "bac":
        coil = 11
    elif name == "secu":
        coil = 10
    elif name == "secuInstant":
        coil = 16
    elif name == "metal":
        coil = 13
    elif name == "verre":
        coil = 15

    global plc

    value = None

    try:
        value = plc.read_coils(coil,1)


        return value.bits[0]

    except Exception as e:
        logging.info(str(e) + " from PLC")

def check():
    try:
        liquide[1] = getCoil("liquide")
        bac[1] = getCoil("bac")
        secu[1] = getCoil("secu")
        secuInstant[1] = getCoil("secuInstant")
        metal = getCoil("metal")
        verre = getCoil("verre")
    except Exception as e:
        logging.info(str(e) + " from plc")
        play("pasDeCo.wav")

        return None

    liquide[0] = liquide[1]
    secu[0] = secu[1]
    secuInstant[0] = secuInstant[1]
    bac[0] = bac[1]

    if liquide[1] == liquide[0] == True:
        if liquide[2] == True:
            play("liquide.wav")
            try:
                sms.sendNiveauLiquide()
                logging.info("NIVEAU LIQUIDE REMPLI :  " + "from plc")
            except Exception as e:
                logging.info(str(e) + " from plc")
                play("pasDeCo.wav")
            liquide[2] = False
    else:
        if liquide[1] == liquide[0] == False:
            liquide[2] = True

    if bac[1] == bac[0] == True:
        if bac[2] == True:
            play("bacPlein.wav")
            try:
                sms.sendNiveauBac()
                logging.info("NIVEAU BAC REMPLI :  " + "from plc")
            except Exception as e:
                logging.info(str(e) + " from plc")
                play("pasDeCo.wav")
            bac[2] = False
    else:
        if bac[1] == bac[0] == False:
            bac[2] = True

    if secu[1] == secu[0] == True:
        if secu[2] == True:
            play("reglesNonResp.wav")
            logging.info("REGLES NON RESPECTEES : trappe cassee ou bloquee" + "from plc")
            try:
                sms.sendTrappe()
            except Exception as e:
                logging.info(str(e) + " from plc")
                play("pasDeCo.wav")
            secu[2] = False
    else:
        if secu[1] == secu[0] == False:
            secu[2] = True

    if secuInstant[1] == secuInstant[0] == True:
        if secuInstant[2] == True:
            play("reglesNonResp.wav")
            logging.info("REGLES NON RESPECTEES : trappe cassee ou bloquee" + "from plc")
            try:
                sms.sendTrappe()
            except Exception as e:
                logging.info(str(e) + " from plc")
                play("pasDeCo.wav")
            secuInstant[2] = False
    else:
        if secuInstant[1] == secuInstant[0] == False:
            secuInstant[2] = True

    print("bac - {} - {}".format(bac[0], bac[1]))
    print("liquide - {} - {}".format(liquide[0], liquide[1]))
    print("secu - {} - {}".format(secu[0], secu[1]))
    print("secuInstant - {} - {}".format(secuInstant[0], secuInstant[1]))

    return metal, verre

init(ipPLC)