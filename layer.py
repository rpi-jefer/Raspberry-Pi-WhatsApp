# -*- coding: utf-8 -*-
import os, subprocess, time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)

from yowsup.layers.interface                           import YowInterfaceLayer                 #Reply to the message
from yowsup.layers.interface                           import ProtocolEntityCallback            #Reply to the message
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity         #Body message
from yowsup.layers.protocol_presence.protocolentities  import AvailablePresenceProtocolEntity   #Online
from yowsup.layers.protocol_presence.protocolentities  import UnavailablePresenceProtocolEntity #Offline
from yowsup.layers.protocol_presence.protocolentities  import PresenceProtocolEntity            #Name presence
from yowsup.layers.protocol_chatstate.protocolentities import OutgoingChatstateProtocolEntity   #is writing, writing pause
from yowsup.common.tools                               import Jid                               #is writing, writing pause

name = "NAMEPRESENCE"
print "Bienvenido, ya puede empezar a escribir !"

class EchoLayer(YowInterfaceLayer):
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getType() == 'text':
            time.sleep(0.5)
            self.toLower(messageProtocolEntity.ack()) #Set received (double v)
            time.sleep(0.5)
            self.toLower(PresenceProtocolEntity(name = name)) #Set name Presence
            time.sleep(0.5)
            self.toLower(AvailablePresenceProtocolEntity()) #Set online
            time.sleep(0.5)
            self.toLower(messageProtocolEntity.ack(True)) #Set read (double v blue)
            time.sleep(0.5)
            self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_TYPING, Jid.normalize(messageProtocolEntity.getFrom(False)) )) #Set is writing
            time.sleep(1)
            self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_PAUSED, Jid.normalize(messageProtocolEntity.getFrom(False)) )) #Set no is writing
            time.sleep(1)
            self.onTextMessage(messageProtocolEntity) #Send the answer
            time.sleep(1)
            self.toLower(UnavailablePresenceProtocolEntity()) #Set offline

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        print entity.ack()
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        namemitt   = messageProtocolEntity.getNotify()
        message    = messageProtocolEntity.getBody()
        recipient  = messageProtocolEntity.getFrom()
        textmsg    = TextMessageProtocolEntity

        print "Mesaje: "+str(message)

        if message == 'Hola Turingpi':
            answer = "Hola como has estado hoy ?"
            self.toLower(textmsg(answer, to = recipient ))
            print answer

        elif message == 'Bien gracias':
            answer = "Me alegra\n Que deseas hacer? \n 1. Para encender bombillo.\n 0. Para apagar bombillo."
            self.toLower(textmsg(answer, to = recipient ))
            print answer

        elif message == '1':
            answer = "Opción 1\n El bombillo se ha encendido"
            GPIO.output(14, True) # Pin 2 en alto

            self.toLower(textmsg(answer, to = recipient ))
            print answer

        elif message == '0':

            answer = "Opción 0\n El bombillo se ha apagado"
            GPIO.output(14, False) # Pin 2 en alto

            self.toLower(textmsg(answer, to = recipient ))
            print answer
        else:
            answer = "No le entiendo"
            self.toLower(textmsg(answer, to = recipient ))
            print answer

