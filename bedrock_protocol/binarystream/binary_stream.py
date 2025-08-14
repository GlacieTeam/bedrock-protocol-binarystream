# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from bedrock_protocol.binarystream.read_only_binary_stream import ReadOnlyBinaryStream
from bedrock_protocol.binarystream._internal.native_library import get_library_handle
from typing import Union
import ctypes


class BinaryStream(ReadOnlyBinaryStream):
    """Provides read/write access to a binary data stream.

    This class extends ReadOnlyBinaryStream with methods for writing
    various data types to the stream.
    """

    def __init__(self, buffer: Union[bytearray, bytes, None] = None) -> None:
        """Initializes a binary stream.

        Args:
            buffer: The buffer to read from/write to
        """
        self._lib_handle = get_library_handle()
        if buffer is not None:
            length = len(buffer)
            if isinstance(buffer, bytearray):
                buffer_ptr = (ctypes.c_uint8 * length).from_buffer(buffer)
                self._stream_handle = self._lib_handle.binary_stream_create_with_buffer(
                    ctypes.cast(buffer_ptr, ctypes.POINTER(ctypes.c_uint8)),
                    length,
                    True,
                )
            elif isinstance(buffer, bytes):
                buffer_ptr = (ctypes.c_uint8 * length).from_buffer_copy(buffer)
                self._stream_handle = self._lib_handle.binary_stream_create_with_buffer(
                    ctypes.cast(buffer_ptr, ctypes.POINTER(ctypes.c_uint8)),
                    length,
                    True,
                )
            else:
                raise TypeError("Unsupported buffer type. Use bytearray or bytes.")
        else:
            self._stream_handle = self._lib_handle.binary_stream_create()

    def __del__(self):
        """Free memory."""
        get_library_handle().binary_stream_destroy(self._stream_handle)

    def reset(self) -> None:
        """Clears the stream buffer and resets read state."""
        self._lib_handle.binary_stream_reset(self._stream_handle)

    def data(self) -> bytearray:
        """Gets direct access to the mutable byte buffer.

        Returns:
            The underlying bytearray containing stream data
        """
        buf = self._lib_handle.binary_stream_get_buffer(self._stream_handle)
        result = bytes(ctypes.string_at(buf.data, buf.size))
        self._lib_handle.stream_buffer_destroy(ctypes.byref(buf))
        return result

    def get_and_release_data(self) -> bytes:
        """Retrieves and clears the current buffer contents.

        Returns:
            Current stream data as bytes
        """
        data = self.data()
        self.reset()
        return data

    def write_byte(self, value: int) -> None:
        """Writes a single byte to the stream.

        Args:
            value: Byte value to write (0-255)
        """
        self._lib_handle.binary_stream_write_unsigned_char(self._stream_handle, value)

    def write_unsigned_char(self, value: int) -> None:
        """Writes an unsigned char (1 byte).

        Args:
            value: Byte value to write (0-255)
        """
        self._lib_handle.binary_stream_write_unsigned_char(self._stream_handle, value)

    def write_unsigned_short(self, value: int) -> None:
        """Writes an unsigned short (2 bytes, little-endian).

        Args:
            value: 16-bit unsigned integer to write
        """
        self._lib_handle.binary_stream_write_unsigned_short(self._stream_handle, value)

    def write_unsigned_int(self, value: int) -> None:
        """Writes an unsigned int (4 bytes, little-endian).

        Args:
            value: 32-bit unsigned integer to write
        """
        self._lib_handle.binary_stream_write_unsigned_int(self._stream_handle, value)

    def write_unsigned_int64(self, value: int) -> None:
        """Writes an unsigned 64-bit integer (8 bytes, little-endian).

        Args:
            value: 64-bit unsigned integer to write
        """
        self._lib_handle.binary_stream_write_unsigned_int64(self._stream_handle, value)

    def write_bool(self, value: bool) -> None:
        """Writes a boolean value (1 byte).

        Args:
            value: Boolean value to write
        """
        self._lib_handle.binary_stream_write_bool(self._stream_handle, value)

    def write_double(self, value: float) -> None:
        """Writes a double-precision floating point number (8 bytes).

        Args:
            value: Double value to write
        """
        self._lib_handle.binary_stream_write_double(self._stream_handle, value)

    def write_float(self, value: float) -> None:
        """Writes a single-precision floating point number (4 bytes).

        Args:
            value: Float value to write
        """
        self._lib_handle.binary_stream_write_float(self._stream_handle, value)

    def write_signed_int(self, value: int) -> None:
        """Writes a signed int (4 bytes, little-endian).

        Args:
            value: 32-bit signed integer to write
        """
        self._lib_handle.binary_stream_write_signed_int(self._stream_handle, value)

    def write_signed_int64(self, value: int) -> None:
        """Writes a signed 64-bit integer (8 bytes, little-endian).

        Args:
            value: 64-bit signed integer to write
        """
        self._lib_handle.binary_stream_write_signed_int64(self._stream_handle, value)

    def write_signed_short(self, value: int) -> None:
        """Writes a signed short (2 bytes, little-endian).

        Args:
            value: 16-bit signed integer to write
        """
        self._lib_handle.binary_stream_write_unsigned_short(self._stream_handle, value)

    def write_unsigned_varint(self, value: int) -> None:
        """Writes an unsigned variable-length integer (1-5 bytes, little-endian).

        Args:
            uvalue: Unsigned integer value to write
        """
        self._lib_handle.binary_stream_write_unsigned_varint(self._stream_handle, value)

    def write_unsigned_varint64(self, value: int) -> None:
        """Writes an unsigned 64-bit variable-length integer (1-10 bytes, little-endian).

        Args:
            uvalue: 64-bit unsigned integer to write
        """
        self._lib_handle.binary_stream_write_unsigned_varint64(
            self._stream_handle, value
        )

    def write_unsigned_big_varint(self, uvalue: int) -> None:
        """Writes an unsigned big variable-length integer (little-endian).

        Args:
            uvalue: Unsigned big integer value to write
        """
        while True:
            byte = uvalue & 0x7F
            uvalue >>= 7
            if uvalue != 0:
                byte |= 0x80
            self.write_byte(byte)
            if uvalue == 0:
                break

    def write_varint(self, value: int) -> None:
        """Writes a signed variable-length integer (1-5 bytes, little-endian).

        Args:
            value: Signed integer value to write
        """
        self._lib_handle.binary_stream_write_varint(self._stream_handle, value)

    def write_varint64(self, value: int) -> None:
        """Writes a signed 64-bit variable-length integer (1-10 bytes, little-endian).

        Args:
            value: 64-bit signed integer to write
        """
        self._lib_handle.binary_stream_write_varint64(self._stream_handle, value)

    def write_big_varint(self, value: int) -> None:
        """Writes a signed big variable-length integer (1-5 bytes, little-endian).

        Args:
            value: Signed big integer value to write
        """
        if value >= 0:
            self.write_unsigned_varint(2 * value)
        else:
            self.write_unsigned_varint(~(2 * value))

    def write_normalized_float(self, value: float) -> None:
        """Writes a normalized float value.

        Args:
            value: Float value to write (should be normalized between -1.0 and 1.0)
        """
        self.write_varint64(int(value * 2147483647.0))

    def write_signed_big_endian_int(self, value: int) -> None:
        """Writes a big-endian signed integer (4 bytes).

        Args:
            value: 32-bit signed integer to write
        """
        self._lib_handle.binary_stream_write_signed_big_endian_int(
            self._stream_handle, value
        )

    def write_raw_bytes(self, raw_buffer: Union[bytearray, bytes]) -> None:
        """Writes raw bytes to the stream.

        Args:
            raw_buffer: Byte data to write
        """
        length = len(raw_buffer)
        if isinstance(raw_buffer, bytes):
            char_ptr = ctypes.c_char_p(raw_buffer)
            buf = ctypes.cast(char_ptr, ctypes.POINTER(ctypes.c_uint8 * length))
        else:
            buf = (ctypes.c_uint8 * length).from_buffer(raw_buffer)
        self._lib_handle.binary_stream_write_bytes(
            self._stream_handle,
            ctypes.cast(buf, ctypes.POINTER(ctypes.c_uint8)),
            length,
        )

    def write_bytes(self, value: bytes) -> None:
        """Writes raw bytes.

        Args:
            raw_buffer: Byte data to write
        """
        self.write_unsigned_varint(len(value))
        self.write_raw_bytes(value)

    def write_string(self, value: str) -> None:
        """Writes a UTF-8 string.

        Args:
            value: String to write
        """
        data = value.encode("utf-8")
        self.write_bytes(data)

    def write_unsigned_int24(self, value: int) -> None:
        """Writes a 24-bit unsigned integer (3 bytes, little-endian).

        Args:
            value: 24-bit unsigned integer to write
        """
        self._lib_handle.binary_stream_write_unsigned_int24(self._stream_handle, value)

    def write_stream(self, stream: ReadOnlyBinaryStream) -> None:
        """Writes all remaining data from another stream.

        Args:
            stream: Source stream to copy data from
        """
        self.write_raw_bytes(stream.get_left_buffer())
