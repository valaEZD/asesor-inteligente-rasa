# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from pymongo import MongoClient

SERVER = 'localhost'
PORT = 27017

# SERVER = '0.tcp.ngrok.io'
# PORT = 17553

class ActionAgregarPregunta(Action):
    
    def name(self) -> Text:
        return "action_agregar_pregunta"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Claro que se puede ;D")

        return []


class ActionAgregarPreguntaBaseDatos(Action):
    
    def name(self) -> Text:
        return "action_agregar_pregunta_base_datos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Agregar a la base de datos")
        
        client = MongoClient(SERVER, PORT)
        db = client.preguntas

        preguntas = db.preguntas
        print(tracker.latest_message['text'])

        prregunta = { 'pregunta' : tracker.latest_message['text'] }
        result = preguntas.insert_one(prregunta)
        print('Pregunta: {0}'.format(result))

        dispatcher.utter_message(text="Bien, tu pregunta sera revisada")

        return []



class ActionVerPreguntas(Action):
    
    def name(self) -> Text:
        return "action_ver_preguntas"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Ver preguntas")
        
        client = MongoClient(SERVER, PORT)
        db = client.preguntas

        preguntas = db.preguntas
        preguntasText = "Preguntas que seran revisadas"

        for x in preguntas.find():
            print(x)
            # preguntasText.append(x['pregunta'])
            preguntasText += '\n' + x 

        print(preguntasText)

        dispatcher.utter_message(text=preguntasText)

        return []