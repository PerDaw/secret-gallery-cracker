## Pattern Lock Cracking Script for PhotoVault Secret Photo Album (com.sneakergif.secretgallery2)

This script is designed to crack a pattern lock based on a hashed password stored in MMKV storage. It accomplishes this by generating and comparing possible lock patterns. Decryption of the data is unnecessary since the media remains unencrypted.

## Background
The Android app **PhotoVault Secret Photo Album** (com.sneakergif.secretgallery2):
> [Google Play Store Link](https://play.google.com/store/apps/details?id=com.sneakergif.secretgallery2)

employs the **MMKV** framework:
> [MMKV GitHub Repository](https://github.com/Tencent/MMKV)

It stores the unsalted hashed user password, which is hashed using SHA1 and then encoded as Base64. This information is stored in an encrypted MMKV database located at:
> /data/media/0/Android/data/com.sneakergif.secretgallery2/files/Documents/.secret_gallery/storage

The app utilizes a hardcoded secret for database encryption. Additionally, storing the database file in a publicly accessible area facilitates pattern lock cracking without exploitation. In summary, the security measures employed by this app are notably inadequate.

## Requirements

- Python 3.x
- MMKV Python library (installation guide: [MMKV Python Setup](https://github.com/Tencent/MMKV/wiki/python_setup))

## Prerequisites

Retrieve the **storage** directory containing the files **secretgallery** and **secretgallery.crc** via ADB from the device.

## Usage

1. **Clone the repository:**

   ```bash
   git clone https://github.com/PerDaw/secret-gallery-cracker.git
   cd secret-gallery-cracker
   python3 sg_bruteforce.py -d storage
   
## Output
````
### User information ###
<UserInfo mail=*****@*****.net, creation_date=2024-**-** 00:11:22, session_key=************************, hashed_password=b'SNHLDpSRTOEMJlvIBELeVwBjLbk='>

### Attacking pattern lock ###
Building lock pattern list for password attack...
Trying to crack the lock pattern using the generated list...

### SUCCESS! ###
<LockPattern(9 -> 8 -> 7 -> 5 -> 6 -> 4 -> 3 -> 2 -> 1)>

It's interpreted like in this field:
[1]	[2]	[3]
[4]	[5]	[6]
[7]	[8]	[9]
````

### Disclaimer:

The script is strictly for educational purposes only.