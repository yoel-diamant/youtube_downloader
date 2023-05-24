import argparse
import pytube
import requests


class NotFound(
    Exception,
):
    def __init__(
        self,
        msg: str,
    ) -> None:
        self.msg = msg


def extract_url(
    url: str,
) -> str:
    youtub_obj = pytube.YouTube(
        url=url,
    )
    for format_dict in youtub_obj.streaming_data["formats"]:
        if "mp4" in format_dict["mimeType"]:
            return format_dict["url"]

    raise NotFound(
        msg="mp4 fromat not found",
    )


def download(
    vidoe_url: str,
    output_path: str,
) -> None:
    request = requests.get(
        url=vidoe_url,
        stream=True,
    )

    with open(
        file=output_path,
        mode="wb",
    ) as file:
        for chunk in request.iter_content(
            chunk_size=1024 * 1024 * 40,
        ):
            if chunk:
                file.write(chunk)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
    )

    parser.add_argument(
        "-u",
        "--url",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    download(
        vidoe_url=extract_url(
            url=args.url,
        ),
        output_path=args.output,
    )
