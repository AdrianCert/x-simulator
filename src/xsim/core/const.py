MAX_U8 = 0xFF
SIGN_U8 = 0x80
MAX_U16 = 0xFF_FF
SIGN_U16 = 0x80_00
MAX_U32 = 0xFF_FF_FF_FF
SIGN_U32 = 0x80_00_00_00
MAX_U64 = 0xFF_FF_FF_FF_FF_FF_FF_FF
SIGN_U64 = 0x80_00_00_00_00_00_00_00
MAX_U128 = 0xFF_FF_FF_FF_FF_FF_FF_FF_FF_FF_FF_FF_FF_FF_FF_FF
SIGN_U128 = 0x80_00_00_00_00_00_00_00_00_00_00_00_00_00_00_00


def parity(value: int) -> bool:
    """Calculate parity of a given value."""
    return bin(value).count("1") % 2 == 0


def complement(value: int) -> int:
    """Calculate two's complement of a given value."""
    return value ^ MAX_U16 + 1


def signed(value: int) -> int:
    """Calculate signed value of a given value."""
    return value - MAX_U16 if value & 0x8000 else value


def unsigned(value: int) -> int:
    """Calculate unsigned value of a given value."""
    return value & MAX_U16


def rotate_left(value: int, shift: int) -> int:
    """Rotate left a given value by a given shift."""
    return (value << shift) | (value >> (16 - shift))


def rotate_right(value: int, shift: int) -> int:
    """Rotate right a given value by a given shift."""
    return (value >> shift) | (value << (16 - shift))


def swap_nibbles(value: int) -> int:
    """Swap nibbles of a given value."""
    return (value << 8) | (value >> 8)


def swap_bytes(value: int) -> int:
    """Swap bytes of a given value."""
    return ((value & 0xFF) << 8) | ((value & 0xFF00) >> 8)


def swap_words(value: int) -> int:
    """Swap words of a given value."""
    return ((value & 0xFFFF) << 16) | ((value & 0xFFFF0000) >> 16)


def mask(value: int, mask: int) -> int:
    """Mask a given value with a given mask."""
    return value & mask


def set_bit(value: int, bit: int) -> int:
    """Set a bit of a given value."""
    return value | (1 << bit)


def clear_bit(value: int, bit: int) -> int:
    """Clear a bit of a given value."""
    return value & ~(1 << bit)


def toggle_bit(value: int, bit: int) -> int:
    """Toggle a bit of a given value."""
    return value ^ (1 << bit)


def test_bit(value: int, bit: int) -> bool:
    """Test a bit of a given value."""
    return bool(value & (1 << bit))


def set_bits(value: int, bits: int) -> int:
    """Set bits of a given value."""
    return value | bits


def clear_bits(value: int, bits: int) -> int:
    """Clear bits of a given value."""
    return value & ~bits
