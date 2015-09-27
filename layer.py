# -*- coding: utf-8 -*-
import os, subprocess, time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)

from yowsup.layers                                     import YowLayer
from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
 
class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        if messageProtocolEntity.getType() == 'text':
            self.onTextMessage(messageProtocolEntity)

        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        print "ack: ", entity.ack()
        self.toLower(entity.ack())


    def onTextMessage(self,messageProtocolEntity):

        nombre  = messageProtocolEntity.getNotify()
        mensaje = messageProtocolEntity.getBody()
        para    = messageProtocolEntity.getFrom()

        if mensaje=='Hola Turingpi':

            msg1 = "Hola "+nombre+" como ha estado hoy ?" 
            print msg1

            self.toLower(TextMessageProtocolEntity( msg1, to = para ))

        elif mensaje == 'Bien gracias':

            msg2 = "Me alegra"
            msg3 = "Que deseas hacer?"
            msg4 = "1. Para encender bombillo."
            msg5 = "0. Para apagar bombillo."
            print msg2
            print msg3
            print msg4
            print msg5

            self.toLower(TextMessageProtocolEntity( msg2, to = para ))
            self.toLower(TextMessageProtocolEntity( msg3, to = para ))
            self.toLower(TextMessageProtocolEntity( msg4, to = para ))
            self.toLower(TextMessageProtocolEntity( msg5, to = para ))

        elif mensaje == '1':

            msg6 = "Opción 1"
            msg7 = "El bombillo se ha encendido"
            print msg6
            print msg7
            
            GPIO.output(14, True) # Pin 2 en alto

            self.toLower(TextMessageProtocolEntity( msg6, to = para ))
            self.toLower(TextMessageProtocolEntity( msg7, to = para ))

        elif mensaje == '0':

            msg8 = "Opción 0"
            msg9 = "El bombillo se ha apagado"
            print msg8
            print msg9

            GPIO.output(14, False) # Pin 2 en bajo

            self.toLower(TextMessageProtocolEntity( msg8, to = para ))
            self.toLower(TextMessageProtocolEntity( msg9, to = para ))

        else:

            msgN = "No le entiendo !" 
            print msgN
            
            self.toLower(TextMessageProtocolEntity( msgN, to = para ))
