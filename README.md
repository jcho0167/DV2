# Made in Australia — FIT3179 Data Visualisation 2
## Structure

| Path | Description |
|---|---|
| `index.html` | The page: narrative, layout, sources and acknowledgements |
| `css/style.css` | Typography, layout, fancy elements, and colours |
| `js/main.js` | Embeds each spec; shared Vega-Lite config (fonts, axis colours); scroll-triggered entrance animations |
| `specs/*.json` | One human-readable Vega-Lite spec per chart, numbered in page order |
| `data/*.csv`, `data/*.json` | The small data files the specs load (about 260 KB in total) |
| `data/source/` | Transcribed source values and `build_data.py`, which produces the CSVs |

## The 11 charts

| # | Spec | Idiom | Interaction |
|---|---|---|---|
| 1 | `01_origins_map` | Proportional symbol map | Click a state to filter its towns; tooltips |
| 2 | `02_state_choropleth` | Choropleth (per-capita, ABS population) | Radio buttons switch measure |
| 3 | `03_radial_states` | Radial / polar-area chart | Tooltips |
| 4 | `04_aria_dumbbell` | Dumbbell chart | Solo / group filter |
| 5 | `05_hall_of_fame_timeline` | Unit (dot-stack) timeline | Tooltips |
| 6 | `06_hottest100_aussie_share` | Annotated line chart | Nearest-point hover |
| 7 | `07_hottest100_waffle` | Small-multiple waffle charts | Tooltips |
| 8 | `08_number_ones_votes` | Bar chart | Click legend to highlight |
| 9 | `09_world_peaks_map` | World choropleth (Equal Earth) | Song dropdown |
| 10 | `10_peaks_heatmap` | Heatmap | Tooltips |
| 11 | `11_number_one_flow_map` | Flow map, Pacific-centred Equal Earth | Hover a country to isolate its route |

Map idioms: 4 (symbol map, state choropleth, world choropleth, flow map). Advanced idioms: 9 (the four maps, radial, dumbbell, unit timeline, waffle, heatmap).

## Rebuilding the data

```bash
python3 data/source/build_data.py
```

All values were transcribed from the sources listed in the page footer on 19 October 2026.

## Design system

- **Colour roles (one colour = one category, never reused):** green `#1f7a4d` = Australian artists and songs; blue `#3b6fb6` = international artists and songs; gold `#b58200` = ARIA Awards (gold ramp `#d6a226` → `#3f2c00` for award rates); plum ramp (`#d68fbd` → `#41143c`) = chart position overseas; greys = other / no data. Page chrome uses forest green and gold, Australia's national colours. A colour key at the top of the page explains this.
- **Type:** Big Shoulders Stencil Display (title, track numbers, stats), Big Shoulders Display (headings), Newsreader (reading text), Archivo (chart and UI text), DM Mono (kickers, captions, liner notes).
- **Grid:** one 1032px column split into a main column and a 320px side column; charts start on the text's left edge and full-width charts end on the same right edge.
- **Overlaps:** symbol-map circles have see-through fills with a solid outline, so overlapping towns stay visible.
- **Motion:** each chart animates once when it scrolls into view (lines draw in time order, dots appear chronologically, waffles count up); text fades up; stats count up. All motion is disabled when the viewer has *reduce motion* turned on.
