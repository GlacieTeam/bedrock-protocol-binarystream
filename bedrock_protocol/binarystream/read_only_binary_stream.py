# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from bedrock_protocol.binarystream._internal.native_library import get_library_handle
from typing import Union
import ctypes


class ReadOnlyBinaryStream:
    """Provides read-only access to a binary data stream.

    This class implements various methods for reading primitive data types,
    variable-length integers, strings, and raw bytes from a binary stream.
    """

    _stream_handle: ctypes.c_void_p
    _lib_handle: ctypes.CDLL

    def __init__(
        self, buffer: Union[bytes, bytearray], big_endian: bool = False
    ) -> None:
        """Initializes a read-only binary stream.

        Args:
            buffer: The binary data to read from
            copy_buffer: Whether to create a copy of the input buffer
            big_endian: Whether to use big endian byte order
        """
        length = len(buffer)
        if isinstance(buffer, bytes):
            char_ptr = ctypes.c_char_p(buffer)
            buf = ctypes.cast(char_ptr, ctypes.POINTER(ctypes.c_uint8 * length))
        elif isinstance(buffer, bytearray):
            buf = (ctypes.c_uint8 * length).from_buffer(buffer)
        else:
            raise TypeError("Unsupported buffer type. Use bytearray or bytes.")
        self._lib_handle = get_library_handle()
        self._stream_handle = self._lib_handle.read_only_binary_stream_create(
            ctypes.cast(buf, ctypes.POINTER(ctypes.c_uint8)), length, True, big_endian
        )

    def __del__(self):
        """Free memory."""
        if self._stream_handle is not None:
            get_library_handle().read_only_binary_stream_destroy(self._stream_handle)

    def size(self) -> int:
        """Gets the total size of the buffer.

        Returns:
            The total number of bytes in the stream
        """
        return self._lib_handle.read_only_binary_stream_size(self._stream_handle)

    def get_position(self) -> int:
        """Gets the current read position.

        Returns:
            The current position in the stream
        """
        return self._lib_handle.read_only_binary_stream_get_position(
            self._stream_handle
        )

    def set_position(self, value: int) -> None:
        """Sets the current read position.

        Args:
            value: The new read position
        """
        self._lib_handle.read_only_binary_stream_set_position(
            self._stream_handle, value
        )

    def reset_position(self) -> None:
        """Resets the read position to the start of the stream."""
        self._lib_handle.read_only_binary_stream_reset_position(self._stream_handle)

    def ignore_bytes(self, length: int) -> None:
        """Advances the read position by the specified number of bytes.

        Args:
            length: Number of bytes to skip
        """
        self._lib_handle.read_only_binary_stream_ignore_bytes(
            self._stream_handle, length
        )

    def get_left_buffer(self) -> bytes:
        """Gets the remaining unread portion of the buffer.

        Returns:
            The unread bytes from current position to end
        """
        buf = self._lib_handle.read_only_binary_stream_get_left_buffer(
            self._stream_handle
        )
        result = bytes(ctypes.string_at(buf.data, buf.size))
        self._lib_handle.stream_buffer_destroy(ctypes.byref(buf))
        return result

    def is_overflowed(self) -> bool:
        """Checks if the stream has overflowed.

        Returns:
            True if an overflow error occurred during reading
        """
        return self._lib_handle.read_only_binary_stream_overflowed(self._stream_handle)

    def has_data_left(self) -> bool:
        """Checks if there is unread data remaining.

        Returns:
            True if there is more data to read
        """
        return self._lib_handle.read_only_binary_stream_has_data_left(
            self._stream_handle
        )

    def get_byte(self) -> int:
        """Reads a single byte from the stream.

        Returns:
            The byte value (0-255)
        """
        return self._lib_handle.read_only_binary_stream_get_unsigned_char(
            self._stream_handle
        )

    def get_unsigned_char(self) -> int:
        """Reads an unsigned char (1 byte).

        Returns:
            The byte value (0-255)
        """
        return self._lib_handle.read_only_binary_stream_get_unsigned_char(
            self._stream_handle
        )

    def get_unsigned_short(self) -> int:
        """Reads an unsigned short (2 bytes, little-endian).

        Returns:
            The 16-bit unsigned integer value
        """
        return self._lib_handle.read_only_binary_stream_get_unsigned_short(
            self._stream_handle
        )

    def get_unsigned_int(self) -> int:
        """Reads an unsigned int (4 bytes, little-endian).

        Returns:
            The 32-bit unsigned integer value
        """
        return self._lib_handle.read_only_binary_stream_get_unsigned_int(
            self._stream_handle
        )

    def get_unsigned_int64(self) -> int:
        """Reads an unsigned 64-bit integer (8 bytes, little-endian).

        Returns:
            The 64-bit unsigned integer value
        """
        return self._lib_handle.read_only_binary_stream_get_unsigned_int64(
            self._stream_handle
        )

    def get_bool(self) -> bool:
        """Reads a boolean value (1 byte).

        Returns:
            True if byte is non-zero, False otherwise
        """
        return self._lib_handle.read_only_binary_stream_get_bool(self._stream_handle)

    def get_double(self) -> float:
        """Reads a double-precision floating point number (8 bytes).

        Returns:
            The double value
        """
        return self._lib_handle.read_only_binary_stream_get_double(self._stream_handle)

    def get_float(self) -> float:
        """Reads a single-precision floating point number (4 bytes).

        Returns:
            The float value
        """
        return self._lib_handle.read_only_binary_stream_get_float(self._stream_handle)

    def get_signed_int(self) -> int:
        """Reads a signed int (4 bytes, little-endian).

        Returns:
            The 32-bit signed integer value
        """
        return self._lib_handle.read_only_binary_stream_get_signed_int(
            self._stream_handle
        )

    def get_signed_int64(self) -> int:
        """Reads a signed 64-bit integer (8 bytes, little-endian).

        Returns:
            The 64-bit signed integer value
        """
        return self._lib_handle.read_only_binary_stream_get_signed_int64(
            self._stream_handle
        )

    def get_signed_short(self) -> int:
        """Reads a signed short (2 bytes, little-endian).

        Returns:
            The 16-bit signed integer value
        """
        return self._lib_handle.read_only_binary_stream_get_signed_short(
            self._stream_handle
        )

    def get_unsigned_varint(self) -> int:
        """Reads an unsigned variable-length integer (1-5 bytes, little-endian).

        Returns:
            The decoded unsigned integer value
        """
        return self._lib_handle.read_only_binary_stream_get_unsigned_varint(
            self._stream_handle
        )

    def get_unsigned_varint64(self) -> int:
        """Reads an unsigned 64-bit variable-length integer (1-10 bytes, little-endian).

        Returns:
            The decoded 64-bit unsigned integer value
        """
        return self._lib_handle.read_only_binary_stream_get_unsigned_varint64(
            self._stream_handle
        )

    def get_unsigned_big_varint(self) -> int:
        """Reads an unsigned big variable-length integer (little-endian).

        Returns:
            The decoded big unsigned integer value
        """
        value = 0
        shift = 0
        while True:
            byte = self.get_byte()
            value |= (byte & 0x7F) << shift
            if not (byte & 0x80):
                break
            shift += 7
        return value

    def get_varint(self) -> int:
        """Reads a signed variable-length integer (1-5 bytes, little-endian).

        Returns:
            The decoded signed integer value
        """
        return self._lib_handle.read_only_binary_stream_get_varint(self._stream_handle)

    def get_varint64(self) -> int:
        """Reads a signed 64-bit variable-length integer (1-10 bytes, little-endian).

        Returns:
            The decoded 64-bit signed integer value
        """
        return self._lib_handle.read_only_binary_stream_get_varint64(
            self._stream_handle
        )

    def get_big_varint(self) -> int:
        """Reads a signed big variable-length integer (little-endian).

        Returns:
            The decoded big signed integer value
        """
        decoded = self.get_unsigned_big_varint()
        return ~(decoded >> 1) if (decoded & 1) else decoded >> 1

    def get_normalized_float(self) -> float:
        """Reads a normalized float value.

        Returns:
            Float value normalized between -1.0 and 1.0
        """
        return self.get_varint64() / 2147483647.0

    def get_signed_big_endian_int(self) -> int:
        """Reads a big-endian signed integer (4 bytes).

        Returns:
            The 32-bit signed integer value
        """
        return self._lib_handle.read_only_binary_stream_get_signed_big_endian_int(
            self._stream_handle
        )

    def get_raw_bytes(self, length: int) -> bytes:
        """Reads raw bytes from the stream.

        Args:
            length: Number of bytes to read

        Returns:
            The raw bytes read from the stream
        """
        buffer_type = ctypes.c_uint8 * length
        buffer = buffer_type()
        self._lib_handle.read_only_binary_stream_get_raw_bytes(
            self._stream_handle,
            ctypes.cast(buffer, ctypes.POINTER(ctypes.c_uint8)),
            length,
        )
        return bytes(buffer)

    def get_bytes(self) -> bytes:
        """Reads a raw bytes.

        Returns:
            The raw bytes value
        """
        buf = self._lib_handle.read_only_binary_stream_get_string(self._stream_handle)
        result = bytes(ctypes.string_at(buf.data, buf.size))
        self._lib_handle.stream_buffer_destroy(ctypes.byref(buf))
        return result

    def get_string(self) -> str:
        """Reads a UTF-8 encoded string.

        The string is prefixed with its length as a varint.

        Returns:
            The decoded UTF-8 string
        """
        data = self.get_bytes()
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            return ""

    def get_unsigned_int24(self) -> int:
        """Reads a 24-bit unsigned integer (3 bytes, little-endian).

        Returns:
            The 24-bit unsigned integer value
        """
        return self._lib_handle.read_only_binary_stream_get_unsigned_int24(
            self._stream_handle
        )
