# Image performance audit

The visual layout and color scheme are unchanged. Existing PNGs and full-resolution lossless WebPs are preserved. Generated images live in `img/responsive/`; regenerate with `python3 scripts/optimize-images.py` using installed `cwebp`. No runtime or build dependencies were added.

## Before and after

Decimal KB (1,000 bytes). Before is the WebP already served by the site, not the larger PNG. Originals and exact bytes are recorded in `image-optimization.json`.

| Image | Original PNG | Previously served WebP | New 480px | New 800px | New 1200px |
|---|---:|---:|---:|---:|---:|
| Portrait | Source PNG missing at audit | 700.7 KB | 26.1 KB | 57.2 KB | 116.2 KB (1199px) |
| SFA / SSIS | 2,121.8 KB | 1,357.8 KB | 43.9 KB | 89.8 KB | 155.9 KB |
| Retail / Snowflake | 1,549.6 KB | 1,028.0 KB | 38.2 KB | 82.6 KB | 151.3 KB |
| Car service | 1,516.8 KB | 940.6 KB | 36.9 KB | 77.7 KB | 138.4 KB |
| Reporting database | 1,592.8 KB | 1,017.7 KB | 37.8 KB | 83.3 KB | 153.0 KB |
| USJP crest | 603.0 KB | 382.3 KB | 12.3 KB at 96px | — | — |
| UCSC crest | 27.9 KB | 13.7 KB | 3.7 KB at 96px | — | — |
| Rahula crest | 175.4 KB | 130.3 KB | 7.9 KB at 96px | — | — |

Previously served images total **5,571,276 bytes**. One 800px variant per photograph/diagram plus all 96px logos totals **414,516 bytes**, saving **5,156,760 bytes (92.6%)**. The 480px set totals 206,832 bytes; the largest set totals 738,762 bytes (86.7% saving). These are asset-size scenarios, not measured browser transfers: actual selection depends on viewport and pixel density, lazy loading, cache and whether previews are opened. Storing multiple variants increases repository size while reducing ordinary page transfers.

## Audit findings and changes

- Project images were 1536×1024 lossless WebPs, approximately 0.94–1.36 MB each, even in small cards. Cards now select 480/800/1200px variants using `srcset` and `sizes`.
- Hero was a 700.7 KB, 1199×1312 lossless WebP. Its PNG fallback referenced a missing file and had mismatched dimensions. Restored a pixel-preserving PNG fallback by decoding the existing lossless WebP; corrected dimensions to 1199×1312.
- Hero remains eager, async-decoded and high priority. A responsive WebP preload uses the same source candidates and sizes as its picture source, so the browser can reuse the early request rather than fetch an extra variant.
- Hero and diagrams use quality-92 WebP with sharp YUV conversion. This is high-quality **lossy** compression, not pixel-identical compression; resizing is proportional, alpha encoding is lossless, and no face manipulation or new cropping was introduced. Logos use lossless encoding after proportional resizing. Full-resolution originals remain available.
- AVIF was not generated: no AVIF encoder is installed. WebP is available without adding dependencies.
- The 280–800px crests now use 96px variants for their 40–48px frames, including typical 2× displays. PNG fallbacks remain.
- Below-fold images retain native lazy loading and async decoding. Existing frame dimensions/aspect ratios reserve their space. No new fade delays hide loaded content.
- Existing dark hero, pale screenshot frames and logo frames provide stable placeholders. Errors retry the source fallback and then show an accessible message. Project previews announce loading/failure and can be retried by closing and reopening.
- Full-resolution preview assets are referenced only as button data and assigned on demand, with a PNG error fallback. There is no preload for modal images. Removed the empty preview `src`.
- The hidden résumé iframe previously loaded a 390,136-byte PDF on startup. It now receives its URL only on first open, preserving preview and download functionality.
- Removed unused Inter weight 800. Retained used weights 400/500/600/700, existing preconnections and `display=swap`.

## Validation and limitations

- Static checks: HTML nesting; all local image, source-set and preview paths; hero preload/source consistency; hero eager/high priority and explicit dimensions; below-fold lazy loading; deferred PDF; JavaScript syntax; decoding every generated WebP; whitespace checks.
- Inspected the generated 800px portrait and SFA diagram directly. Their proportions, portrait transparency and diagram text remain intact at that resolution. This does not substitute for full page rendering or a pixel-identical quality guarantee.
- Browser inventory reported **“The browser access host is unavailable.”** No rendered desktop/mobile inspection, normal/slow-4G/slow-3G benchmark, LCP, CLS or measured network comparison could be run. No performance scores are claimed.
- This is a buildless HTML/CSS site with no package manifest or configured lint/build suite.

## Hosting and remaining bottlenecks

No deployment manifest or provider-specific caching configuration exists in this checkout; provider and production response headers cannot be established locally. No speculative hosting configuration was added.

Configure the actual host/CDN to serve correct image MIME types, validators (ETag or Last-Modified), and browser caching. For the current **non-fingerprinted** image paths, a conservative policy is `Cache-Control: public, max-age=86400` with conditional revalidation afterward. HTML should revalidate (`Cache-Control: no-cache`). For year-long `immutable` caching, first use content-hashed filenames and update references whenever bytes change. Apply Brotli/gzip to HTML/CSS/JS/SVG rather than recompressing WebP. Confirm effective production headers and CDN behavior after deployment.

Remaining costs: Google Fonts requires external connections; unsupported-WebP clients use larger PNG fallbacks; explicit full-resolution project previews remain 0.94–1.36 MB; DPR and viewport affect chosen variants. Measure a cold-cache deployed page at mobile and desktop sizes using normal, slow-4G and slow-3G profiles, then inspect LCP/CLS, selected `currentSrc`, duplicate downloads, errors and actual response cache headers.
