# MyMapCache

## Porpose

The porpose of this project is to create a lightweight, click-to-run tile server for my specific requirements. It should be only used as a local solution, and it's **NOT** built for heavy load services. Also, this project doesn't have complex features like vector querying; it only focus on the tile service, and doesn't include full services like a working WMTS server with all capabilities. I knew MapProxy can serve such demands, but I need some more specific customizing and easier configures.

If someone ask me why ... isn't in this, my answer is use MapProxy.

## Basic Configure

Click the executable to run it, and it will start with a blank config near the execuable named `congigure.json` (this path is hardcoded for now). You can prettify it as you like (be careful don't break the json rules):
```
{
    "port": 8001, 
    "debug": false, 
    "sources": [], 
    "converted": [], 
    "standalone": [{"type": "serviceInfo"}]
}
```
The first two lines are obvious. The main content is devided into two major blocks and another less important block: `sources`, `converted`, `standalone`.

### "Sources"

*Sources* are the places where you get the original tile, e.g. `tile.openstreetmap.org`. Currently the project can handle following types:

* `simple_tile`: simple tile service (like osm tile);
* `wmts`: WMTS server (only the tiles, go checkout MapProxy if you need more features like `getCapabilities` response / feature query / ...);
* `arcgis`: ArcGIS server (same as above, no query provided);
* `local`: Organized files on your local storage.

#### simple tile
To add a tile service, start a new block in the `sources` array:
```
    ...
    "sources":[
        {
            "type": "simple_tile",
            "remotePath": [
                {
                    "type": "literal",
                    "content": "https://tile.openstreetmap.org/"
                },
                {
                    "type": "z"
                },
                {
                    "type": "literal",
                    "content": "/"
                },
                {
                    "type": "x"
                },
                {
                    "type": "literal",
                    "content": "/"
                },
                {
                    "type": "y"
                },
                {
                    "type": "literal",
                    "content": ".png"
                }
            ],
            "serverPath": "/osm",
            "cacheBase": "./.cache/osm"
        }
    ],
    ...
```
The key `type` defines the type of this configure block. The key `remotePath` is split into multiple components to indicate what to place in the url string. Your "`remotePath`" is formed in the following scheme (compared with typical string scheme you would see in GIS softwares):

| configure component type  | description                       | typical string scheme     |
| ------------------------- | --------------------------------- | ------------------------- |
| `literal`                 | literal content in key `content`  | *(plain text)*            |
| `x`                       | tile column                       | `{x}`                     |
| `y`                       | tile row                          | `{y}`                     |
| `z`                       | tile zoom                         | `{zoom}` or `{z}`         |
| `z` with key `offset`     | tile zoom with offset             | `{zoom + <offset>}`       |
| `switch`                  | random switch                     | `{switch:<content list>}` |
| *(unsupported)*           | *(unsupported list)*              | `{proj}`, `{wkid}`, `{bbox}`, `{width}`, `{height}`, `{ty}`, `{-y}`, `{u}`, `{@2x}`(or `{r}`); anything not on the above list|

I admit it's annoying to repeatly type `{"type": "literal"}` so I will work on this later.

The key `serverPath` defines where the tiles available on your local server. For this configuration, you can use the tiles at `127.0.0.1:8001/osm/{z}/{x}/{y}`. **Note that this project only provides such tile service.**

The key `cacheBase` defines a directory to store cache files. This path is required. **Donot place anything important in this directory!** It might be deleted if too old. (Defined by key `cacheTime` in seconds, 3 days by default, or forever if negative value set.)

#### WMTS
The basic keys `serverPath`, `cacheBase`, `remotePath` are same as simple tile source. (Note: Don't mannually fill parameters in `remotePath`, stop before `?`.) The additional key in wmts configure is `presetParams`. Typically you need to fillin those:
```
        ...
        "presetParams": {
            "layer": "some_layer",
            "style": "default",
            "format": "tiles"
        },
        ...
```
The param `service=WMTS&request=GetTile&version=1.0.0&tileMatrix={zoom}&tileCol={x}&tileRow={y}` is automaticly added.

In very rare cases the server might reject requests not in ALL CAPITAL param names. Use `"capParam":true` in this case. 

#### ArcGIS Server

Nothing new. Basically same as simple tile. For the `remotePath` part, stop before `/MapServer/`. If you need zoom offset, put it in the following place:

```
        ...
        {
            "type": "arcgis",
            "remotePath": [
                {
                    "type": "literal",
                    "content": "https://www.example.com/ArcGIS/rest/services/some_image"
                }
            ],
            "zOffset": -10,
            ...
        }
        ...
```

#### local sources

```
        ...
        {
            "type": "local",
            "localPath": "path/to/your/map/directory",
            "serverPath": "/my_map"
        }
        ...
```

### "Converted"

*"Converted"* tiles are somehow generated from original sources. Currently there's two conversions supported: layer merging and reprojecting (wgs84 tile to web mercator tile only).

Before using conversions, you need to configure every source in the `sources` block, and label them with the key `id`.

#### layer merging
```
        ...
        {
            "type": "merge_layers",
            "serverPath": "/map_with_label",
            "cacheBase": "./.cache/somewhere",
            "inputSources": 
            [
                "some_map",
                "some_label"
            ]
        },
        ...
```
The values in `inputSources` will be matched with `id` key in the source configure block. Note that you must place the "dependency" above the conversion block. This is important when you use the conversion product for a secondary conversion.

#### reprojecting
```
        ...
        {
            "type": "reproject",
            "serverPath": "/mercator/tiles",
            "cacheBase": "./.cache/mercator/tiles",
            "id": "some_mercator_map",
            "transform": {
                "type": "wgs84_to_webmercator"
            },
            "inputSources": [
                "stupid_map_not_projected"
            ]
        },
        ...
```
Currently only web mercator is supported.

### Standalone services

#### Service info
The generated "service info" block does nothing but saying hello world when you visits `http://127.0.0.1:8001/` in your browser. You can simply disable it by removing this block.

#### "Static"
A static web server sending a directory. Maybe useful if you place a Leaflet webpage in it?

## Network Configure

> Actually I started this project after spending a whole day trying to figure out how to configure proxy parameters for MapProxy and learnt nothing.

Network configures only apply on *sources* (except for local source), and you can configure different value for every source.

### Request headers

**Faking other applications might violate rules of some services.**

Add a `headers` block in the *source* configure:
```
            ...
            "remotePath": ...,
            "headers": {
                "Referer": "somewhere"
            },
            ...
```

Currently the default UA is `MyMapCache/1.0.0`

### Network Proxy

Configuration same as `requests` library (in json form). An example:
```
            ...
            "remotePath": ...,
            "proxies": {
                "http": "127.0.0.1:9910",
                "https": "127.0.0.1:9910"
            },
            ...
```
Consult your *"Internet tool"* provider if you don't know the port.

If you need something bypass that proxy, use
```
            ...
            "proxies": {
                "http": "",
                "https": ""
            },
            ...
```

## Known issues
* Currently the cache cleanning program only runs once at startup. (So you need to mannually restart the program to clean it.)

## Notes

The file `start_with_private.py` is included in the github repository, but it's my private code, so don't ask about anything about it.