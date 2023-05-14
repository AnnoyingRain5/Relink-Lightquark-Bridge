import Relink_Communication.communication as communication
import asyncio
import websockets.client as websockets
import requests
import dotenv
import json
import os

dotenv.load_dotenv()


class preferences():
    def __init__(self):
        self.RL_CHANNEL_NAME: str
        self.RL_SERVER_ADDRESS: str
        self.LQ_CHANNEL_ID: str
        self.LQ_WEBHOOK_ADDRESS: str
        self.LQ_SERVER_ADDRESS: str
        self.LQ_USER_ID: str
        self.TOKEN: str

    def __getattribute__(self, __name: str) -> str:
        defaults = {
            "LQ_CHANNEL_ID": "638b815b4d55b470d9d6fa19",
            "RL_CHANNEL_NAME": "litdevs_general",
            "RL_SERVER_ADDRESS": "localhost",
            "LQ_WEBHOOK_ADDRESS": "lq-gateway.litdevs.org",
            "LQ_SERVER_ADDRESS": "lq.litdevs.org",
            "LQ_USER_ID": "645f08ca5bb68883fe2046c4"
        }
        envvar = os.getenv(f"LQB_{__name}")
        if envvar is not None:
            return envvar
        else:
            if __name == "TOKEN":
                print("You must provide a TOKEN in the environment or a .env file.")
                exit()
            try:
                return defaults[__name]
            except:
                raise KeyError

    def __setattr__(self, __name: str, __value) -> None:
        raise NotImplementedError


prefs = preferences()


async def HeartBeat(LQSocket):
    while True:
        await LQSocket.send(
            json.dumps({"event": "heartbeat", "message": "Still alive -GLaDOS probably"}))
        await asyncio.sleep(30)


async def LQMessageLoop(LQSocket, RLSocket):
    while True:
        message: dict = json.loads(await LQSocket.recv())
        print(message)
        if message["eventId"] == "messageCreate":
            print(message['author']['_id'])
            # if this is our own message, ignore it
            if message['author']['_id'] == prefs.LQ_USER_ID:
                continue
            fr = communication.FederationRequest()
            fr.channel = prefs.RL_CHANNEL_NAME
            if "specialAttributes" in message['message']:
                for attribute in message['message']['specialAttributes']:
                    print(attribute)
                    if "username" in attribute:
                        username = attribute["username"]
                        break
                else:
                    username = message['author']['username']
            else:
                username = message['author']['username']

            fr.username = f"{username}@LightquarkBridge"
            await RLSocket.send(fr.json)
            RLMessage = communication.Message()
            RLMessage.text = message['message']['content']
            RLMessage.username = username
            await RLSocket.send(RLMessage.json)
            print(
                f"{username} said {message['message']['content']}")
        else:
            print(message)


async def RLMessageLoop(RLSocket):
    while True:
        packet = communication.packet(await RLSocket.recv())
        print()
        match type(packet):
            case communication.Message:
                if not packet.username.endswith(  # type: ignore
                        "@LightquarkBridge"):
                    print(
                        requests.post(
                            f"https://{prefs.LQ_SERVER_ADDRESS}/v2/channel/{prefs.LQ_CHANNEL_ID}/messages",
                            json={
                                "content": packet.text,  # type: ignore
                                "specialAttributes": [
                                    {
                                        "type": "botMessage",
                                        "username": packet.username  # type: ignore
                                    }
                                ]
                            },
                            headers={"Authorization": f"Bearer {prefs.TOKEN}", "lq-agent": "Relinked Bridge"}).text)


async def main():
    # LightQuark auth
    async with websockets.connect(  # type: ignore
            f"wss://{prefs.LQ_WEBHOOK_ADDRESS}", subprotocols=[prefs.TOKEN]) as LQSocket:  # type: ignore
        asyncio.create_task(HeartBeat(LQSocket))
        async with websockets.connect(  # type: ignore
                f"ws://{prefs.RL_SERVER_ADDRESS}:8765") as RLSocket:
            # we are now connected to both LQ and RL
            await LQSocket.send(json.dumps(
                {"event": "subscribe",
                 "message": f"channel_{prefs.LQ_CHANNEL_ID}"}))
            LQMessageTask = asyncio.create_task(
                LQMessageLoop(LQSocket, RLSocket))
            asyncio.create_task(RLMessageLoop(RLSocket))
            await LQMessageTask


asyncio.run(main())
