import asyncio
import bleak

from scoutingserver.config import EventConfig
from scoutingserver.interface import printing

class GattController:

    def __init__(self, on_receive, config: EventConfig, timeout = 5):
        self.on_receive = on_receive
        self.config = config
        self.timeout

    def start(self):
        loop = asyncio.get_event_loop()
        self.task = loop.create_task(self._run())

    def stop(self):
        self.task.cancel()

    async def _run(self):
        while True:
            devices = await bleak.discover(timeout=self.timeout)
            for device in devices:
                async with bleak.BleakClient(device) as client:
                    services = client.get_services()
                    try:
                        await client.connect()
                        
                    except Exception as e:
                        printing.printf(e, style=printing.ERROR)
                    finally:
                        await client.disconnect()
