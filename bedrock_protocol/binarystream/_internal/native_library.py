# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

import os
import sys
import ctypes
import threading


class BufferData(ctypes.Structure):
    _fields_ = [
        ("data", ctypes.POINTER(ctypes.c_uint8)),
        ("size", ctypes.c_size_t),
    ]


class NativeLibrary:
    _lock = threading.Lock()
    _lib_handle = None
    _initialized = False
    _initialization_error = None

    def __init__(self):
        raise RuntimeError("Use get_handle() method instead")

    @classmethod
    def _initialize(cls):
        if cls._initialized or cls._initialization_error is not None:
            return

        lib_dir = os.path.dirname(os.path.abspath(__file__))
        platform_map = {
            "win32": "BinaryStream.dll",
            "linux": "libBinaryStream.so",
            # "darwin": "libBinaryStream.dylib",
        }

        if sys.platform not in platform_map:
            cls._initialization_error = OSError(f"Unsupported platform: {sys.platform}")
            raise cls._initialization_error

        lib_name = platform_map[sys.platform]
        dll_path = os.path.join(lib_dir, lib_name)

        if not os.path.isfile(dll_path):
            cls._initialization_error = FileNotFoundError(
                f"Native library not found at: {dll_path}"
            )
            raise cls._initialization_error

        try:
            cls._lib_handle = ctypes.CDLL(dll_path)
            cls._setup_function_prototypes()
            cls._initialized = True
        except Exception as e:
            cls._initialization_error = RuntimeError(
                f"Failed to load native library: {e}"
            )
            raise cls._initialization_error from e

    @classmethod
    def _setup_function_prototypes(cls):
        cls._lib_handle.stream_buffer_destroy.restype = None
        cls._lib_handle.stream_buffer_destroy.argtypes = [ctypes.POINTER(BufferData)]
        cls._lib_handle.read_only_binary_stream_create.restype = ctypes.c_void_p
        cls._lib_handle.read_only_binary_stream_create.argtypes = [
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.c_size_t,
            ctypes.c_bool,
        ]
        cls._lib_handle.read_only_binary_stream_create_empty.restype = ctypes.c_void_p
        cls._lib_handle.read_only_binary_stream_create_empty.argtypes = []
        cls._lib_handle.read_only_binary_stream_destroy.restype = None
        cls._lib_handle.read_only_binary_stream_destroy.argtypes = [ctypes.c_void_p]
        cls._lib_handle.read_only_binary_stream_size.restype = ctypes.c_size_t
        cls._lib_handle.read_only_binary_stream_size.argtypes = [ctypes.c_void_p]
        cls._lib_handle.read_only_binary_stream_get_position.restype = ctypes.c_size_t
        cls._lib_handle.read_only_binary_stream_get_position.argtypes = [
            ctypes.c_void_p
        ]
        cls._lib_handle.read_only_binary_stream_set_position.restype = None
        cls._lib_handle.read_only_binary_stream_set_position.argtypes = [
            ctypes.c_void_p,
            ctypes.c_size_t,
        ]
        cls._lib_handle.read_only_binary_stream_reset_position.restype = None
        cls._lib_handle.read_only_binary_stream_reset_position.argtypes = [
            ctypes.c_void_p
        ]
        cls._lib_handle.read_only_binary_stream_overflowed.restype = ctypes.c_bool
        cls._lib_handle.read_only_binary_stream_overflowed.argtypes = [ctypes.c_void_p]
        cls._lib_handle.read_only_binary_stream_has_data_left.restype = ctypes.c_bool
        cls._lib_handle.read_only_binary_stream_has_data_left.argtypes = [
            ctypes.c_void_p
        ]
        cls._lib_handle.read_only_binary_stream_ignore_bytes.restype = None
        cls._lib_handle.read_only_binary_stream_ignore_bytes.argtypes = [
            ctypes.c_void_p,
            ctypes.c_size_t,
        ]
        cls._lib_handle.read_only_binary_stream_get_bytes.restype = ctypes.c_size_t
        cls._lib_handle.read_only_binary_stream_get_bytes.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.c_size_t,
        ]
        cls._lib_handle.read_only_binary_stream_get_bool.restype = ctypes.c_bool
        cls._lib_handle.read_only_binary_stream_get_bool.argtypes = [ctypes.c_void_p]
        cls._lib_handle.read_only_binary_stream_get_unsigned_char.restype = (
            ctypes.c_uint8
        )
        cls._lib_handle.read_only_binary_stream_get_unsigned_char.argtypes = [
            ctypes.c_void_p
        ]
        cls._lib_handle.read_only_binary_stream_get_unsigned_short.restype = (
            ctypes.c_uint16
        )
        cls._lib_handle.read_only_binary_stream_get_unsigned_short.argtypes = [
            ctypes.c_void_p
        ]
        cls._lib_handle.read_only_binary_stream_get_signed_short.restype = (
            ctypes.c_int16
        )
        cls._lib_handle.read_only_binary_stream_get_signed_short.argtypes = [
            ctypes.c_void_p
        ]
        cls._lib_handle.read_only_binary_stream_get_unsigned_int.restype = (
            ctypes.c_uint32
        )
        cls._lib_handle.read_only_binary_stream_get_unsigned_int.argtypes = [
            ctypes.c_void_p
        ]
        cls._lib_handle.read_only_binary_stream_get_unsigned_int24.restype = (
            ctypes.c_uint32
        )
        cls._lib_handle.read_only_binary_stream_get_unsigned_int24.argtypes = [
            ctypes.c_void_p
        ]
        cls._lib_handle.read_only_binary_stream_get_signed_int.restype = ctypes.c_int32
        cls._lib_handle.read_only_binary_stream_get_signed_int.argtypes = [
            ctypes.c_void_p
        ]
        cls._lib_handle.read_only_binary_stream_get_unsigned_int64.restype = (
            ctypes.c_uint64
        )
        cls._lib_handle.read_only_binary_stream_get_unsigned_int64.argtypes = [
            ctypes.c_void_p
        ]
        cls._lib_handle.read_only_binary_stream_get_signed_int64.restype = (
            ctypes.c_int64
        )
        cls._lib_handle.read_only_binary_stream_get_signed_int64.argtypes = [
            ctypes.c_void_p
        ]
        cls._lib_handle.read_only_binary_stream_get_float.restype = ctypes.c_float
        cls._lib_handle.read_only_binary_stream_get_float.argtypes = [ctypes.c_void_p]
        cls._lib_handle.read_only_binary_stream_get_double.restype = ctypes.c_double
        cls._lib_handle.read_only_binary_stream_get_double.argtypes = [ctypes.c_void_p]
        cls._lib_handle.read_only_binary_stream_get_unsigned_varint.restype = (
            ctypes.c_uint32
        )
        cls._lib_handle.read_only_binary_stream_get_unsigned_varint.argtypes = [
            ctypes.c_void_p
        ]
        cls._lib_handle.read_only_binary_stream_get_varint.restype = ctypes.c_int32
        cls._lib_handle.read_only_binary_stream_get_varint.argtypes = [ctypes.c_void_p]
        cls._lib_handle.read_only_binary_stream_get_unsigned_varint64.restype = (
            ctypes.c_uint64
        )
        cls._lib_handle.read_only_binary_stream_get_unsigned_varint64.argtypes = [
            ctypes.c_void_p
        ]
        cls._lib_handle.read_only_binary_stream_get_varint64.restype = ctypes.c_int64
        cls._lib_handle.read_only_binary_stream_get_varint64.argtypes = [
            ctypes.c_void_p
        ]
        cls._lib_handle.read_only_binary_stream_get_string.restype = BufferData
        cls._lib_handle.read_only_binary_stream_get_string.argtypes = [ctypes.c_void_p]
        cls._lib_handle.read_only_binary_stream_get_left_buffer.restype = BufferData
        cls._lib_handle.read_only_binary_stream_get_left_buffer.argtypes = [
            ctypes.c_void_p
        ]
        cls._lib_handle.read_only_binary_stream_get_raw_bytes.restype = ctypes.c_size_t
        cls._lib_handle.read_only_binary_stream_get_raw_bytes.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.c_size_t,
        ]
        cls._lib_handle.read_only_binary_stream_get_signed_big_endian_int.restype = (
            ctypes.c_int32
        )
        cls._lib_handle.read_only_binary_stream_get_signed_big_endian_int.argtypes = [
            ctypes.c_void_p
        ]
        # BinaryStream
        cls._lib_handle.binary_stream_create.restype = ctypes.c_void_p
        cls._lib_handle.binary_stream_create.argtypes = []
        cls._lib_handle.binary_stream_create_with_buffer.restype = ctypes.c_void_p
        cls._lib_handle.binary_stream_create_with_buffer.argtypes = [
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.c_size_t,
            ctypes.c_bool,
        ]
        cls._lib_handle.binary_stream_destroy.restype = None
        cls._lib_handle.binary_stream_destroy.argtypes = [ctypes.c_void_p]
        cls._lib_handle.binary_stream_reset.restype = None
        cls._lib_handle.binary_stream_reset.argtypes = [ctypes.c_void_p]
        cls._lib_handle.binary_stream_write_bytes.restype = None
        cls._lib_handle.binary_stream_write_bytes.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.c_size_t,
        ]
        cls._lib_handle.binary_stream_write_bool.restype = None
        cls._lib_handle.binary_stream_write_bool.argtypes = [
            ctypes.c_void_p,
            ctypes.c_bool,
        ]
        cls._lib_handle.binary_stream_write_unsigned_char.restype = None
        cls._lib_handle.binary_stream_write_unsigned_char.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint8,
        ]
        cls._lib_handle.binary_stream_write_unsigned_short.restype = None
        cls._lib_handle.binary_stream_write_unsigned_short.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint16,
        ]
        cls._lib_handle.binary_stream_write_signed_short.restype = None
        cls._lib_handle.binary_stream_write_signed_short.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int16,
        ]
        cls._lib_handle.binary_stream_write_signed_int.restype = None
        cls._lib_handle.binary_stream_write_signed_int.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int32,
        ]
        cls._lib_handle.binary_stream_write_unsigned_int.restype = None
        cls._lib_handle.binary_stream_write_unsigned_int.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint32,
        ]
        cls._lib_handle.binary_stream_write_unsigned_int24.restype = None
        cls._lib_handle.binary_stream_write_unsigned_int24.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint32,
        ]
        cls._lib_handle.binary_stream_write_signed_int64.restype = None
        cls._lib_handle.binary_stream_write_signed_int64.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int64,
        ]
        cls._lib_handle.binary_stream_write_unsigned_int64.restype = None
        cls._lib_handle.binary_stream_write_unsigned_int64.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint64,
        ]
        cls._lib_handle.binary_stream_write_float.restype = None
        cls._lib_handle.binary_stream_write_float.argtypes = [
            ctypes.c_void_p,
            ctypes.c_float,
        ]
        cls._lib_handle.binary_stream_write_double.restype = None
        cls._lib_handle.binary_stream_write_double.argtypes = [
            ctypes.c_void_p,
            ctypes.c_double,
        ]
        cls._lib_handle.binary_stream_write_unsigned_varint.restype = None
        cls._lib_handle.binary_stream_write_unsigned_varint.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint32,
        ]
        cls._lib_handle.binary_stream_write_varint.restype = None
        cls._lib_handle.binary_stream_write_varint.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int32,
        ]
        cls._lib_handle.binary_stream_write_unsigned_varint64.restype = None
        cls._lib_handle.binary_stream_write_unsigned_varint64.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint64,
        ]
        cls._lib_handle.binary_stream_write_varint64.restype = None
        cls._lib_handle.binary_stream_write_varint64.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int64,
        ]
        cls._lib_handle.binary_stream_write_string.restype = None
        cls._lib_handle.binary_stream_write_string.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.c_size_t,
        ]
        cls._lib_handle.binary_stream_write_signed_big_endian_int.restype = None
        cls._lib_handle.binary_stream_write_signed_big_endian_int.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int32,
        ]
        cls._lib_handle.binary_stream_get_buffer.restype = BufferData
        cls._lib_handle.binary_stream_get_buffer.argtypes = [ctypes.c_void_p]

    @classmethod
    def get_handle(cls):
        if cls._initialized:
            return cls._lib_handle
        if cls._initialization_error:
            raise cls._initialization_error
        with cls._lock:
            if cls._initialized:
                return cls._lib_handle
            if cls._initialization_error:
                raise cls._initialization_error
            try:
                cls._initialize()
            except Exception:
                pass
            if cls._initialization_error:
                raise cls._initialization_error
            return cls._lib_handle


def get_library_handle():
    return NativeLibrary.get_handle()
