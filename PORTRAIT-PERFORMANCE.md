# Hero portrait quality audit

## Source and master

Best repository source: `img/nadun-kaushalya.webp`, lossless RGBA, 1199 × 1312, 700,726 bytes. Original PNG fallback: same dimensions, 1,059,976 bytes. Both remain unchanged.

New master: `img/masters/nadun-kaushalya-master.webp`, 2398 × 2624, lossless RGBA, 1,763,142 bytes. This is faithful 2× resampling of the original, not recovered photographic detail. The master is a build asset and is never downloaded by the hero.

A built-in image_gen identity-preserving restoration was attempted and visually compared with the original. It returned 1199 × 1312 and altered subtle facial/clothing details. Rejected; not deployed. Original identity, composition, pose, clothing, colors and alpha are prioritized over synthetic detail. No successful AI super-resolution claim is made.

## Delivery assets

WebP quality 94, sharp YUV conversion, lossless alpha. Small variants use the lossless original directly to avoid redundant up/downsampling; large variants use the new master. The script regenerates the master and all active variants. The former 1199px variant remains on disk for compatibility but is no longer referenced by the hero.

| Dimensions | Bytes |
| --- | ---: |
| 480 × 526 | 30,470 |
| 640 × 701 | 46,694 |
| 800 × 876 | 66,940 |
| 1000 × 1095 | 95,128 |
| 1440 × 1576 | 150,626 |
| 1800 × 1970 | 207,914 |
| 2200 × 2408 | 275,956 |

The requested 1400px size is adjusted to 1440px: a conservative 709 CSS-pixel desktop hint needs 1418 pixels at DPR 2. Added 2200px covers 2127 pixels at DPR 3. This avoids jumping from 1400px straight to 1800px at DPR 2. 1800px remains a useful candidate for intermediate zoom/DPR and mobile DPR 3.

## HTML, CSS and expected selection

Preload and picture source sets/hints are identical. Hero remains eager, high priority, asynchronously decoded, with width/height attributes. No UI/CSS edits. Existing crop, position, cover, 1.25× scale and screen blend are preserved. No portrait blur filter or lingering blurred placeholder is present. Screen blending changes contrast; changing it would change the existing appearance.

Mobile uses a 480px hint (420px height × 1199/1312 × 1.25 ≈ 479.8px). Desktop uses a conservative 709px hint, accounting for the existing 620px maximum height (≈708.3px effective width). Standard desktop minimum height only needs ≈605.4px. The conservative hint intentionally favors sharpness with modest extra transfer.

Calculated first candidates meeting hints, not measured browser selections:

| Viewports | DPR 1 | DPR 2 | DPR 3 |
| --- | --- | --- | --- |
| 375 / 430px | 480px | 1000px | 1440px |
| 1280 / 1440 / 1920px | 800px | 1440px | 2200px |

Browser heuristics/cache/network preferences may choose differently. Larger encoded images satisfy sampling dimensions but cannot recreate missing source detail. Native photographic detail at DPR 3 still requires a higher-resolution original. The old PNG fallback has the original resolution ceiling.

## Verification and performance limits

Inspected decoded original, rejected AI edit, and the 1800px quality-94 output. Preserved transparent silhouette and facial appearance; original edge imperfections are not represented as fixed. All active WebPs pass metadata validation, contain alpha, and match their width descriptors. Preload/source parity and eager/high priority are checked. Unrelated images regenerate byte-for-byte unchanged. `git diff --check` passes.

Browser automation retry returned “browser access host is unavailable”. Actual currentSrc, post-load visual appearance, decode/paint timing, network timing, preload reuse and real transfer bytes remain unmeasured. Byte counts above are encoded payload sizes, excluding HTTP overhead. No production performance claim is made.

Manual Chrome verification: open DevTools Device Toolbar, expose DPR, test each listed width at DPR 1/2/3 with cache disabled and reload each time. Await `document.querySelector('.hero-photo-desktop img').decode()`, inspect its `currentSrc`, then record Network Size/Time and confirm one portrait request (preload reused). Inspect hair/glasses/skin and alpha edges after decoding. Repeat with Fast 4G throttling. Test on a real high-DPI display for final perceived sharpness.

## Changed files

`index.html`, `scripts/optimize-images.py`, `image-optimization.json`, `PORTRAIT-PERFORMANCE.md`, new master under `img/masters/`, and active portrait variants under `img/responsive/`. Original source, PNG fallback, CSS and unrelated UI are unchanged.

## Built-in image_gen prompt (rejected output)

> Use case: identity-preserve. Edit target: supplied original transparent portfolio portrait. Perform restrained photographic super-resolution/restoration only, aiming for a 2398 x 2624 or larger master with EXACT same aspect ratio, framing, subject size, location and transparent margins as the input. Preserve this specific man's identity precisely: same facial geometry, eyes, nose, smile, teeth, facial hair, hairline, glasses shape and blue reflections, skin tone, suit and shirt. Recover subtle natural hair, beard and fabric detail and reduce resizing softness; clean cutout edges minimally. Keep original lighting and colors. No beautification, no face reshaping, no invented accessories, no changed clothing, no altered expression, no plastic skin, no oversharpening or halos. Keep real alpha transparency everywhere outside the original silhouette, no background or checkerboard baked in. Do not crop, recenter or change composition. This is a faithful enhancement of the same photograph, not a new portrait.
