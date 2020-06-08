from roomEditor import RoomEditor
from assembler import ASM


def removeOwlEvents(rom):
    # Remove all the owl events from the entity tables.
    for room in range(0x100):
        re = RoomEditor(rom, room)
        if re.hasEntity(0x41):
            re.removeEntities(0x41)
            re.store(rom)
    # Clear texts used by the owl. Potentially reused somewhere else.
    rom.texts[0x0D9] = b'\xff'  # used by boomerang
    # 1 Used by empty chest (master stalfos message)
    # 9 used by keysanity items
    # 1 used by bowwow in chest
    # 1 used by item for other player message
    # 2 used by arrow chest messages
    # 2 more available.
    for idx in range(0x0BE, 0x0CE):
        rom.texts[idx] = b'\xff'


def upgradeOwlStatues(rom):
    # Call our custom handler after the check for the stone beak
    rom.patch(0x18, 0x1EA2, ASM("ldh a, [$F7]\ncp $FF\njr nz, $05"), ASM("ld a, $09\nrst 8\nret"), fill_nop=True)
    # Put 20 rupees in all owls by default.
    rom.patch(0x3E, 0x3B16, "00" * 0x316, "1C" * 0x316)
