#!/usr/bin/env python

import sys
import asyncio
import datetime
import random
import websockets

from os.path import join

from monitor import FileMonitor



async def time(websocket, path):
    log_file = join("./../data/data.log")
    fm = FileMonitor(log_file)
    while True:
        # now = datetime.datetime.utcnow().isoformat() + 'Z'
        modified_data = fm.watch()
        for data in modified_data:
            await websocket.send(now)
            await asyncio.sleep(random.random() * 3)


if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("Please provide path to log file .. ")
    #     sys.exit(-1)
    #
    # log_file = sys.argv[1]
    start_server = websockets.serve(time, '127.0.0.1', 5000)
    print("Server running on http://localhost:5000 ... ")

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
