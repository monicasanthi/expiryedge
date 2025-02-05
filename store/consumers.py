import json
import cv2
import numpy as np
import base64
from pyzbar.pyzbar import decode
from channels.generic.websocket import WebsocketConsumer

class BarcodeScannerConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        image_data = data.get('image')

        if image_data:
            encoded_data = image_data.split(',')[1]
            nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            barcodes = decode(img)
            for barcode in barcodes:
                barcode_data = barcode.data.decode('utf-8')
                self.send(text_data=json.dumps({'barcode': barcode_data}))