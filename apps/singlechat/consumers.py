# import json

# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = f"chat_{self.room_name}"

#         # Join room Group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,  self.channel_name
#         )

#         self.accept()


#     def disconnect(self, close_code):
#         # Leave Room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name, self.channel_name
#         )


#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name, {"type": "chat.message", "message": message}
#         )

#     # Receive message from group
#     def chat_message(self, event):
#         message = event["message"]
#         # Send message to webSocket
#         self.send(text_data=json.dumps({"message": message}))


# import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = f"chat_{self.room_name}"
#         async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
#         self.accept()

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

#     def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data.get("message", "")
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name, {"type": "chat_message", "message": message}
#         )

#     def chat_message(self, event):
#         self.send(text_data=json.dumps({"message": event["message"]}))
        
# import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = f"chat_{self.room_name}"
#         async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
#         self.accept()

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

#     def receive(self, text_data):
#         data = json.loads(text_data or "{}")
#         if "message" in data:
#             async_to_sync(self.channel_layer.group_send)(
#                 self.room_group_name, {"type": "chat_message", "message": data["message"]}
#             )
#         elif data.get("event") == "typing":
#             async_to_sync(self.channel_layer.group_send)(
#                 self.room_group_name, {"type": "typing_event", "user": data.get("user", "Someone")}
#             )
#         elif data.get("event") == "stop_typing":
#             async_to_sync(self.channel_layer.group_send)(
#                 self.room_group_name, {"type": "stop_typing_event", "user": data.get("user", "Someone")}
#             )

#     # broadcast handlers
#     def chat_message(self, event):
#         self.send(text_data=json.dumps({"message": event["message"]}))

#     def typing_event(self, event):
#         self.send(text_data=json.dumps({"typing": event["user"]}))

#     def stop_typing_event(self, event):
#         self.send(text_data=json.dumps({"stop_typing": event["user"]}))


# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def receive(self, text_data):
        data = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "chat_message", "message": data.get("message", ""), "user": data.get("user", "Anon")}
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps({"message": event["message"], "user": event.get("user", "Anon")}))
