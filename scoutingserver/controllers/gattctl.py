import asyncio
import bleak

from scoutingserver.config import EventConfig, FieldConfig, FieldType
from scoutingserver.interface import printing

# todo write this
SYNCED_CHAR_UUID = "dfsa;ijaf;jasdf;jasdfk;lfas;lj"

class GattController:
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
        loop = asyncio.get_event_loop()
        self.task = loop.create_task(self._run())

    def stop(self):
        self.task.cancel()

    async def _run(self):
        # Scan for devices with the service we want
        scanner = bleak.BleakScanner(service_uuids=[self.config.service_id])
        scanner.register_detection_callback(_on_advertise)

        while True:
            await scanner.start()
            await asyncio.sleep(5.0)
            await scanner.stop()

    def _on_advertise(device, ad_data):
        with bleak.BleakClient(device) as client:
            if not client.is_connected():
                try:
                    client.connect()
                except Exception as e:
                    printing.printf(e, style=printing.ERROR)
            if not client.is_connected():
                return

            client.read_gatt_char(SYNCED_CHAR_UUID, bytearray([0x0]))

            fields = {}
            for field_config in self.config.field_configs:
                bytes = client.read_gatt_char(field_config.char_id)
                fields[field_config.name] = self._bytes_to_field(field_config, bytes)

            self.on_receive(fields, client)

            client.write_gatt_char(SYNCED_CHAR_UUID, bytearray([0x1]))

            client.disconnect()

    def _bytes_to_field(self, field_config: FieldConfig, bytes):
        """Convert a byte array to a proper value based on that field's config"""
        if field_config.type == FieldType.NUM:
            return int.from_bytes(bytes)
        elif field_config.type == FieldType.BOOL:
            return bool(int.from_bytes(bytes))
        elif field.config_type == FieldType.CHOICE:
            ind = int.from_bytes(bytes)
            return field_config.choices[ind]
        elif field.config_type == FieldType.TEXT:
            return bytes.decode("utf-8")
