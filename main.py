import wmi
import copy
import json
import time
import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup

api_url = "https://www.asus.com/support/api/product.asmx/GetPDBIOS?website=global"
rog_url = "https://rog.asus.com/motherboards/"

user_agent = "ThxAndBot/0.2 (+https://github.com/ThxAndBye/ROG-BIOS-update-check)"
request = urllib.request.Request(
    "https://www.asus.com",
    data=None,
    headers={
        'User-Agent': user_agent
    }
)


class BIOS:
    def __init__(self, title, version, release_date, description, download_url, is_stable):
        self.title = title
        self.version = version
        self.release_date = release_date
        self.description = description
        self.download_url = download_url
        self.is_stable = bool(is_stable)

    def __str__(self):
        return "Version " + self.version + " " + ("Stable" if self.is_stable else "Beta") + \
               " release from: " + self.release_date.strftime("%d %b %Y")


def sleep_with_output(sec):
    if sec > 0:
        print("\rWaiting for: " + str(sec), end=" ", flush=True)
        time.sleep(1)
        sleep_with_output(sec - 1)
    else:
        print("\rDone.", end=" ", flush=True)

# The Product ID is encoded into a JSON that is inline in the HTML
def get_rog_id_by_name(model):
    # ROG-STRIX, ROG-MAXIMUS, etc.
    rog_series = "-".join(str(model).lower().split("-")[:2])

    id_request = copy.deepcopy(request)
    id_request.full_url = rog_url + rog_series + "/" + str(model).lower() + "-model/"

    with urllib.request.urlopen(id_request) as url:
        html = url.read()
        soup = BeautifulSoup(html, "html.parser")
        for script in soup.findAll("script"):
            if "window[\"__INITIAL_STATE__\"] = JSON.parse" in str(script):
                json_board = json.loads(str(script).split("\"")[3].encode().decode('unicode-escape'))
                return json_board["Cookie"]["productId"]["value"]


def get_bios_releases(pid, model):
    bios_request = copy.deepcopy(request)
    bios_request.full_url = api_url + "&model=" + str(model) + "&pdid=" + str(pid)

    bios_array = []
    with urllib.request.urlopen(bios_request) as url:
        result = json.loads(url.read().decode())["Result"]
        bios_files = result["Obj"][0]["Files"]

        for bios_file in bios_files:
            bios_array.append(BIOS(bios_file["Title"],
                                   bios_file["Version"],
                                   datetime.strptime(bios_file["ReleaseDate"], "%Y/%m/%d"),
                                   bios_file["Description"].replace("<br/>", "\n").replace("\"", ""),
                                   bios_file["DownloadUrl"]["Global"],
                                   bios_file["IsRelease"]))
    return bios_array


def get_installed_bios_version():
    wmic = wmi.WMI()
    for bios in wmic.Win32_bios():
        return bios.Name


def get_board_model():
    wmic = wmi.WMI()
    for model in wmic.Win32_BaseBoard():
        return str(model.Product).replace(" ", "-")


if __name__ == '__main__':
    # Retrieve installed Hardware and BIOS version via WMIC
    installed_bios = get_installed_bios_version()
    board_model = get_board_model()
    print("Your Board: " + str(board_model) + ", installed BIOS: " + str(installed_bios))

    # Retrieve ASUS ProductID to query API for BIOS releases
    print("Retrieving Board ID ...", end=" ", flush=True)
    product_id = get_rog_id_by_name(board_model)
    print(str(product_id))

    # Retrieve BIOS Releases for the installed mainboard
    print("Retrieving newest BIOS version ...", end=" ", flush=True)
    BIOS_array = get_bios_releases(product_id, board_model)

    # Print newest stable version and notify the user if the installed version is outdated
    for release in BIOS_array:
        if release.is_stable:
            print(release.version + "\n")
            if release.version > installed_bios:
                print("BIOS Update Available! " + str(release) + "\n" +
                      str(release.description) + "\n" +
                      "Download: " + release.download_url)
                input("Press Enter to exit ...")
            else:
                print("No new BIOS release found!")
                sleep_with_output(3)
            exit()