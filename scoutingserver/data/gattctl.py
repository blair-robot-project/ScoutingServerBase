import asyncio
from typing import Callable

import bleak

from scoutingserver.config import EventConfig, FieldConfig, FieldType
from scoutingserver.interface import printing


class BluetoothController:
    def __init__(
        self,
        on_receive: Callable[[dict, bleak.BleakClient], None],
        config: EventConfig,
        timeout=5,
    ):
        self.on_receive = on_receive
        self.config = config
        self.timeout = timeout

    def start(self):
        """
        Start scanning for devices. Connect to the ones with
        the service we want and get data from them.
        """
        loop = asyncio.get_event_loop()
        self.task = loop.create_task(self._run())

    def stop(self):
        """Stop scanning for and connecting to devices"""
        self.task.cancel()

    async def _run(self):
        # Scan for devices with the service we want
        scanner = bleak.BleakScanner(service_uuids=[self.config.service_id])
        scanner.register_detection_callback(_on_advertise)

        while True:
            await scanner.start()
            await asyncio.sleep(5.0)
            await scanner.stop()

    async def _on_advertise(device, ad_data):
        with bleak.BleakClient(device) as client:
            if not client.is_connected():
                try:
                    await client.connect()
                except Exception as e:
                    printing.printf(e, style=printing.ERROR)
            if not client.is_connected():
                return

            # Tell the peripheral it hasn't synced yet
            await client.write_gatt_char(SYNCED_CHAR_UUID, bytearray([0x0]))

            fields = {}
            for field_config in self.config.field_configs:
                bytearr = await client.read_gatt_char(field_config.char_id)
                fields[field_config.name] = self._bytearr_to_field(
                    field_config, bytearr
                )

            self.on_receive(fields, client)

            # Tell the peripheral syncing is done
            await client.write_gatt_char(SYNCED_CHAR_UUID, bytearray([0x1]))

            await client.disconnect()

    def _bytearr_to_field(self, field_config: FieldConfig, bytearr: bytearray):
        """Convert a bytearray to a proper value based on that field's config"""
        if field_config.type == FieldType.NUM:
            return int.from_bytes(bytearr, "big")
        elif field_config.type == FieldType.BOOL:
            return bool(int.from_bytes(bytearr, "big"))
        elif field_config.type == FieldType.CHOICE:
            ind = int.from_bytes(bytearr, "big")
            return field_config.choices[ind]
        elif field_config.type == FieldType.TEXT:
            return bytearr.decode("utf-8")
