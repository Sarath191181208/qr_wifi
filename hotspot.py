import subprocess
from qrcode.main import QRCode
import wifi_qrcode_generator

def get_wifi_credentials_windows() -> tuple[str, str]:
    """
        Get's the wifi credentials from the windows machine
    """
    id = (
        subprocess.check_output(["netsh", "wlan", "show", "interfaces"])
        .decode("utf-8")
        .split("\n")
    )

    id_results = str([b.split(":")[1][1:-1] for b in id if "Profile" in b])[2:-3]

    # traverse the password
    password = (
        subprocess.check_output(
            ["netsh", "wlan", "show", "profiles", id_results, "key=clear"]
        )
        .decode("utf-8")
        .split("\n")
    )

    pass_results = str([b.split(":")[1][1:-1] for b in password if "Key Content" in b])[
        2:-2
    ]
    print("User name :", id_results)
    print("Password :", pass_results)
    return (id_results, pass_results)

def generate_login_qr() -> QRCode:
    id_results, pass_results = get_wifi_credentials_windows()
    return wifi_qrcode_generator.wifi_qrcode(id_results, False, "WPA", pass_results)


