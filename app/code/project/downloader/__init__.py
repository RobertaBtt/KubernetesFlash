DOWNLOADER = dict()


def register():
    DOWNLOADER['download_only_headers'] = download_only_headers
    DOWNLOADER['download_whole_resource'] = download_whole_resource


# Since we just need the header, the file is saved just for one chunk of 1kb,
# enough to contain the header even for files with 100 columns
def download_only_headers(url: str, response):
    with open(url, mode="wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
            break


def download_whole_resource(url: str, response):
    with open(url, mode="wb") as file:
        for chunk in response.iter_content(chunk_size=10 * 1024):
            file.write(chunk)


def get_downloader(function_name):
    return DOWNLOADER[function_name]


register()
