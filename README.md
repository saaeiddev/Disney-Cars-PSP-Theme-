# Disney Cars PSP Theme — preview build 1.0

An unofficial fan-made standard PSP PTF theme inspired by Disney and Pixar's *Cars*. The wallpaper and icon art were AI-generated for this project. Disney and Pixar own the Cars franchise and characters; this is not an official Disney, Pixar or Sony product. Redistribution of third-party intellectual property may require permission.

![PSP Go Game view](screenshots/psp_go_game.jpg)

## Status and features

This is a software-checked preview build, not a hardware-certified release. It contains a 480 × 272 wallpaper, eight category icons (including regional TV and Extras fallback), 29 first-level bodies and 29 focus graphics, two second-level bodies and two focuses, a preview icon, and preview image. It does not include the requested additional character wallpapers, all original movie characters or the official Cars logo. The source art consists of generated raster sheets; it is not a layered illustration file.

PTF Studio 1.0 reopened 73 image assets and its analysis reported zero errors and warnings; its PSP Go preview rendered the theme. LibPSPThemes independently extracted the PTF and decoded 73 images. PTF Studio is a visual approximation, not an emulator, and the user reported that this PTF worked on their device; the exact model and firmware were not specified. Compatibility across other hardware remains unconfirmed. Target: PSP-1000/2000/3000, Go and E1000 with standard PTF support. Available menu entries differ by model and region.

PSP Go System Storage, its saved data utility and Resume Game use the standard fallback icon in the PTF Studio preview rather than invented dedicated PTF records. Hardware behavior is unverified.

## Installation

1. Copy `build/Disney_Cars_PSP_Theme.ptf` into `PSP/THEME/` at the root of the connected storage device. Create the folder if missing.
2. On PSP Go, choose System Storage as the USB device if using internal storage, then copy to its `PSP/THEME/` folder; alternatively use the Memory Stick storage root.
3. Disconnect safely. On the PSP choose **Settings → Theme Settings → Theme**, select the theme and apply it. A standard PTF does not require CXMB.

## Build

Requires Python 3, Pillow and a checkout of [LibPSPThemes](https://github.com/GeofrontTeam/LibPSPThemes). Its sources are not included. Run:

```sh
python tools/extract_icons.py
python tools/build.py /path/to/LibPSPThemes
```

The scripts crop the provided raster masters, produce PSP-sized images and encode GIM resources; LibPSPThemes assembles the PTF. Rebuilding requires the same Pillow behavior; exact bytes are not guaranteed across versions. `assets/` holds PSP-sized PNG/BMP artwork and generated focus images, `artwork/` holds raster masters, `tools/` holds scripts, `build/` holds the preview PTF, and `screenshots/` holds the PTF Studio capture. No Sony firmware assets or fonts are included.

## Credits

Fan artwork created with OpenAI image generation. PTF compilation uses GeofrontTeam's LibPSPThemes; visual analysis uses S1implyBlue's PTF Studio. Disney, Pixar, Sony, PSP, and related marks belong to their owners. This project claims no affiliation or endorsement.
