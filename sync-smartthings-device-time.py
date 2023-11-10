#!/usr/bin/env python3

import argparse
import asyncio
import datetime
import sys


import aiohttp
import pysmartthings
import pytz


async def sync_time(access_token, device_id, dry_run, timezone):
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, access_token)
        devices = await api.devices()
        
        for device in devices:
            if device.device_id == device_id:
                break
        else:
            raise RuntimeError(f'Unable to find device with id {device_id}')

        now = datetime.datetime.now()
        formatted = f'{now.astimezone(timezone):%Y-%m-%dT%H:%M:%S}'

        if dry_run:
            print(f'Would sync with: {formatted}')
            return True

        return await device.command(
            'main',
            'execute',
            'execute',
            ['/configuration/vs/0', {'x.com.samsung.da.currentTime': formatted}]
        )


def parse_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--access-token', required=True)
    parser.add_argument('--device-id', required=True)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--timezone', type=pytz.timezone)
    
    return parser.parse_args()


def main():
    args = parse_args()
    
    return asyncio.run(
        sync_time(
            args.access_token,
            args.device_id,
            args.dry_run,
            args.timezone,
        )
    )


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
