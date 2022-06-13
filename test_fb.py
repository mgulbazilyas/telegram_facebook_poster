import facebook_poster
import functions

self = facebook_poster.Setup()
driver = functions.get_webdriver()

import json
#%%
with open('filtered.log', 'w') as w:
    with open('facebook_handle.log') as stream:

        for line in stream.readlines():
            if '[facebook_handle] - Posts: 5' not in line:
                w.write(line)
