import requests
from requests.exceptions import ConnectionError, HTTPError
from json.decoder import JSONDecodeError
from math import ceil
import asyncio
import concurrent.futures
import aiohttp
from aiohttp import ClientSession


def _make_request(url):
    return requests.get(url).json()


def get_spec_count():
    try:
        return requests.get("https://app.swaggerhub.com/apiproxy/specs?limit=1&page=1").json().get("totalCount")

    except ConnectionError:
        print(f"Failed to get spec count: Connection Failed")
        return

    except JSONDecodeError:
        print(f"Failed to get spec count: Invalid JSON")
        return

    except Exception as e:
        print(f"Failed to get spec count: {e}")
        return


async def get_spec_list(session, page, sort_by="CREATED", order="DESC", limit=100):
    try:
        response = await session.request(method='GET', url=(
            f"https://app.swaggerhub.com/apiproxy/specs"
            f"?sort={sort_by}&order={order}&limit={limit}&page={page}"
        ))
        response.raise_for_status()
        response_json = await response.json()
        return list(map(lambda api: api["properties"][0]["url"], response_json.get("apis")))

    except HTTPError as http_err:
        print(f"Failed to get spec list: HTTP error occurred ({http_err})")

    except Exception as err:
        print(f"An error occurred: {err}")


async def save_spec(session, url, file_name):
    try:
        response = await session.request(method='GET', url=url)
        response.raise_for_status()
        response_text = await response.text()

        with open(f"scrape/swaggerhub/{file_name}", "w+") as f:
            f.write(response_text)

        print(f"Saved new swagger spec: {file_name}")

    except HTTPError as http_err:
        print(f"Failed to save file ({file_name}): HTTP Error ({http_err})")

    except ConnectionError:
        print(f"Failed to save file ({file_name}): Connection Failed")

    except JSONDecodeError:
        print(f"Failed to save file ({file_name}): Invalid JSON")

    except Exception as e:
        print(f"Failed to save file ({file_name}): {e}")


async def save_spec_page(session, page):
    print(f"Saving page: {page}")

    try:
        urls = await get_spec_list(session, page)

        for idx, url in enumerate(urls):
            await save_spec(session, url, f"swagger.json.{((page-1)*100)+idx}")

    except Exception as err:
        print(f"Exception: {err}")
        pass


async def main():
    async with ClientSession() as session:
        spec_count = get_spec_count()
        page_count = ceil(spec_count / 100)

        print(f"Collecting {spec_count} specs (pages: {page_count})")

        await asyncio.gather(*[save_spec_page(session, page) for page in range(1, 99)])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
