"""Builds the small, clean data files used by the Vega-Lite specs.

All values below were transcribed from the sources listed in each section
(retrieved 19 October 2026). Run from the project root:  python3 data/source/build_data.py
"""
import csv, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# 1. ARIA Music Awards: most wins (Wikipedia, "ARIA Music Awards", figures up to 2025)
#    + artist origin (Wikipedia infobox "Origin"; if absent, where the artist grew
#    up per the article; if that is absent, Australian birthplace).
# ---------------------------------------------------------------------------
aria = [
    # artist, wins, nominations, place, state, lat, lon, kind
    ("John Farnham", 22, 65, "Melbourne", "VIC", -37.814, 144.963, "Solo"),
    ("Silverchair", 21, 49, "Newcastle", "NSW", -32.927, 151.776, "Group"),
    ("Kylie Minogue", 18, 61, "Melbourne", "VIC", -37.814, 144.963, "Solo"),
    ("Powderfinger", 18, 47, "Brisbane", "QLD", -27.470, 153.026, "Group"),
    ("The Wiggles", 18, 34, "Sydney", "NSW", -33.869, 151.209, "Group"),
    ("Paul Kelly", 17, 63, "Adelaide", "SA", -34.929, 138.601, "Solo"),
    ("Kasey Chambers", 15, 34, "Adelaide", "SA", -34.929, 138.601, "Solo"),
    ("Tame Impala", 15, 32, "Perth", "WA", -31.952, 115.861, "Group"),
    ("Crowded House", 14, 43, "Melbourne", "VIC", -37.814, 144.963, "Group"),
    ("Savage Garden", 14, 26, "Brisbane", "QLD", -27.470, 153.026, "Group"),
    ("Gotye", 13, 21, "Melbourne", "VIC", -37.814, 144.963, "Solo"),
    ("Flume", 12, 33, "Sydney", "NSW", -33.869, 151.209, "Solo"),
    ("Missy Higgins", 12, 32, "Melbourne", "VIC", -37.814, 144.963, "Solo"),
    ("Midnight Oil", 11, 38, "Sydney", "NSW", -33.869, 151.209, "Group"),
    ("You Am I", 11, 33, "Sydney", "NSW", -33.869, 151.209, "Group"),
    ("Hilltop Hoods", 10, 41, "Adelaide", "SA", -34.929, 138.601, "Group"),
    ("Sia", 10, 33, "Adelaide", "SA", -34.929, 138.601, "Solo"),
    ("Troye Sivan", 10, 24, "Perth", "WA", -31.952, 115.861, "Solo"),
    ("Archie Roach", 10, 23, "Mooroopna", "VIC", -36.393, 145.360, "Solo"),
    ("Geoffrey Gurrumul Yunupingu", 10, 22, "Galiwin'ku (Elcho Island)", "NT", -11.987, 135.567, "Solo"),
    ("Nick Cave", 9, 35, "Warracknabeal", "VIC", -36.252, 142.396, "Solo"),
    ("Delta Goodrem", 9, 26, "Sydney", "NSW", -33.869, 151.209, "Solo"),
    ("Yothu Yindi", 9, 14, "Yirrkala", "NT", -12.253, 136.888, "Group"),
    ("Amy Shark", 8, 37, "Gold Coast", "QLD", -28.017, 153.400, "Solo"),
    ("Eskimo Joe", 8, 35, "Fremantle", "WA", -32.056, 115.747, "Group"),
    ("Joseph Tawadros", 8, 21, "Sydney", "NSW", -33.869, 151.209, "Solo"),
    ("The Cruel Sea", 8, 19, "Sydney", "NSW", -33.869, 151.209, "Group"),
    ("Empire of the Sun", 8, 18, "Sydney", "NSW", -33.869, 151.209, "Group"),
    ("Natalie Imbruglia", 8, 14, "Berkeley Vale", "NSW", -33.344, 151.432, "Solo"),
    ("Jet", 8, 11, "Melbourne", "VIC", -37.814, 144.963, "Group"),
    ("Guy Sebastian", 7, 35, "Adelaide", "SA", -34.929, 138.601, "Solo"),
    ("John Butler", 7, 34, "Pinjarra", "WA", -32.630, 115.873, "Solo"),
    ("Jimmy Barnes", 7, 27, "Adelaide", "SA", -34.929, 138.601, "Solo"),
    ("Regurgitator", 7, 23, "Brisbane", "QLD", -27.470, 153.026, "Group"),
    ("Wendy Matthews", 7, 22, None, None, None, None, "Solo"),  # Canadian-born, no Australian origin given: not mapped
    ("Tina Arena", 7, 20, "Melbourne", "VIC", -37.814, 144.963, "Solo"),
    ("Genesis Owusu", 7, 19, "Canberra", "ACT", -35.281, 149.129, "Solo"),
    ("INXS", 7, 18, "Sydney", "NSW", -33.869, 151.209, "Group"),
    ("Paul Grabowsky", 7, 17, "Melbourne", "VIC", -37.814, 144.963, "Solo"),
    ("The Presets", 7, 17, "Sydney", "NSW", -33.869, 151.209, "Group"),
    ("Richard Tognetti", 7, 16, "Wollongong", "NSW", -34.425, 150.893, "Solo"),
    ("Sydney Symphony Orchestra", 7, 16, "Sydney", "NSW", -33.869, 151.209, "Group"),
    ("Amyl and the Sniffers", 7, 15, "Melbourne", "VIC", -37.814, 144.963, "Group"),
    ("The Living End", 6, 30, "Melbourne", "VIC", -37.814, 144.963, "Group"),
    ("Courtney Barnett", 6, 23, "Melbourne", "VIC", -37.814, 144.963, "Solo"),
    ("Tones and I", 6, 23, "Frankston", "VIC", -38.144, 145.126, "Solo"),
    ("Angus & Julia Stone", 6, 21, "Sydney", "NSW", -33.869, 151.209, "Group"),
    ("Diesel", 6, 20, "Perth", "WA", -31.952, 115.861, "Solo"),
    ("The Teskey Brothers", 6, 17, "Melbourne", "VIC", -37.814, 144.963, "Group"),
    ("Troy Cassar-Daley", 6, 16, "Grafton", "NSW", -29.691, 152.933, "Solo"),
    ("Baker Boy", 6, 15, "Milingimbi", "NT", -12.100, 134.917, "Solo"),
    ("5 Seconds of Summer", 6, 14, "Sydney", "NSW", -33.869, 151.209, "Group"),
    ("Gabriella Cilmi", 6, 6, "Dandenong", "VIC", -37.987, 145.215, "Solo"),
]
with open(ROOT / "aria_artists.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["artist", "wins", "nominations", "strike_rate", "place", "state", "lat", "lon", "kind"])
    for a, wins, noms, place, st, lat, lon, kind in aria:
        w.writerow([a, wins, noms, round(wins / noms, 3), place or "", st or "", lat or "", lon or "", kind])

# ---------------------------------------------------------------------------
# 2. ABS estimated resident population, 31 March 2026 ('000), released 17 Sep 2026
# ---------------------------------------------------------------------------
pop = {"NSW": 8670.1, "VIC": 7154.2, "QLD": 5739.5, "SA": 1916.8,
       "WA": 3096.2, "TAS": 580.7, "NT": 268.9, "ACT": 489.7}
names = {"NSW": "New South Wales", "VIC": "Victoria", "QLD": "Queensland", "SA": "South Australia",
         "WA": "Western Australia", "TAS": "Tasmania", "NT": "Northern Territory",
         "ACT": "Australian Capital Territory"}
label_xy = {"NSW": (146.6, -32.4), "VIC": (144.0, -36.9), "QLD": (144.6, -22.8), "SA": (135.4, -30.2),
            "WA": (122.0, -26.0), "TAS": (146.6, -42.0), "NT": (133.4, -19.6), "ACT": (149.1, -35.5)}
rows = []
for st, p in pop.items():
    acts = [x for x in aria if x[4] == st]
    wins = sum(x[1] for x in acts)
    rows.append({"state": st, "state_name": names[st], "population_000": p,
                 "artists": len(acts), "wins": wins,
                 "artists_per_million": round(len(acts) / (p / 1000), 2),
                 "wins_per_million": round(wins / (p / 1000), 2),
                 "lon": label_xy[st][0], "lat": label_xy[st][1]})
with open(ROOT / "states.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)

# ---------------------------------------------------------------------------
# 3. Triple J Hottest 100 (Wikipedia: main article + each year's article)
#    aus = entries by Australian artists (each year's "by country" table; 1999 & 2020 from article text)
# ---------------------------------------------------------------------------
h100 = [
    (1993, 24, "Asshole", "Denis Leary", "US", 50000),
    (1994, 26, "Zombie", "The Cranberries", "IE", None),
    (1995, 30, "Wonderwall", "Oasis", "UK", 100000),
    (1996, 29, "Buy Me a Pony", "Spiderbait", "AU", 300000),
    (1997, 34, "No Aphrodisiac", "The Whitlams", "AU", 250000),
    (1998, 42, "Pretty Fly (For a White Guy)", "The Offspring", "US", 500000),
    (1999, 52, "These Days", "Powderfinger", "AU", 650000),
    (2000, 40, "My Happiness", "Powderfinger", "AU", 900000),
    (2001, 38, "Amazing", "Alex Lloyd", "AU", 350000),
    (2002, 50, "No One Knows", "Queens of the Stone Age", "US", None),
    (2003, 47, "Are You Gonna Be My Girl", "Jet", "AU", 383000),
    (2004, 47, "Take Me Out", "Franz Ferdinand", "UK", 475000),
    (2005, 50, "Wish You Well", "Bernard Fanning", "AU", 606060),
    (2006, 43, "One Crowded Hour", "Augie March", "AU", 671024),
    (2007, 52, "Knights of Cydonia", "Muse", "UK", 700000),
    (2008, 48, "Sex on Fire", "Kings of Leon", "US", 800000),
    (2009, 37, "Little Lion Man", "Mumford & Sons", "UK", 1100000),
    (2010, 51, "Big Jet Plane", "Angus & Julia Stone", "AU", 1260000),
    (2011, 44, "Somebody That I Used to Know", "Gotye feat. Kimbra", "AU", 1378869),
    (2012, 41, "Thrift Shop", "Macklemore & Ryan Lewis feat. Wanz", "US", 1516765),
    (2013, 45, "Riptide", "Vance Joy", "AU", 1490000),
    (2014, 60, "Talk Is Cheap", "Chet Faker", "AU", 2099707),
    (2015, 54, "Hoops", "The Rubens", "AU", 2094000),
    (2016, 66, "Never Be Like You", "Flume feat. Kai", "AU", 2255110),
    (2017, 65, "Humble.", "Kendrick Lamar", "US", 2286133),
    (2018, 65, "Confidence", "Ocean Alley", "AU", 2758584),
    (2019, 65, "Bad Guy", "Billie Eilish", "US", 3211596),
    (2020, 66, "Heat Waves", "Glass Animals", "UK", 2790224),
    (2021, 55, "Elephant (Like a Version)", "The Wiggles", "AU", 2700000),
    (2022, 57, "Say Nothing", "Flume feat. May-a", "AU", 2436565),
    (2023, 52, "Paint the Town Red", "Doja Cat", "US", 2355870),
    (2024, 29, "Good Luck, Babe!", "Chappell Roan", "US", 2489446),
    (2025, 54, "Man I Need", "Olivia Dean", "UK", 2100000),
]
country_name = {"AU": "Australia", "US": "United States", "UK": "United Kingdom", "IE": "Ireland"}
with open(ROOT / "hottest100.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["year", "aus_entries", "number_one", "number_one_artist", "number_one_country", "votes"])
    for y, aus, song, art, c, v in h100:
        w.writerow([y, aus, song, art, country_name[c], v if v else ""])

# Waffle data: 100 squares per selected year, one per countdown entry.
aus_by_year = {y: a for y, a, *_ in h100}
picks = {1993: "First countdown", 2016: "Record high", 2024: "Fewest since 1996", 2025: "The rebound"}
with open(ROOT / "hottest100_waffle.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["year", "title", "aus_entries", "cell", "col", "row", "group"])
    for yr, title in picks.items():
        a = aus_by_year[yr]
        for cell in range(100):
            w.writerow([yr, f"{yr}: {title}", a, cell, cell % 10, cell // 10,
                        "Australian artist" if cell < a else "International artist"])

# ---------------------------------------------------------------------------
# 4. ARIA Hall of Fame inductees by year (Wikipedia "ARIA Hall of Fame")
#    Rolf Harris omitted: ARIA withdrew his induction in 2014.
# ---------------------------------------------------------------------------
hof_raw = """1988|Joan Sutherland;Johnny O'Keefe;Slim Dusty;Col Joye;Vanda & Young;AC/DC
1989|Nellie Melba;Ross Wilson
1990|Percy Grainger;Sherbet
1991|Billy Thorpe;Glenn Shorrock;Don Burrows;Peter Dawson
1992|Skyhooks
1993|Cold Chisel;Peter Allen
1994|Men at Work
1995|The Seekers
1996|Australian Crawl;Horrie Dargie
1997|The Bee Gees;Paul Kelly;Graeme Bell
1998|The Masters Apprentices;The Angels
1999|Richard Clapton;Jimmy Little
2001|INXS;The Saints
2002|Olivia Newton-John
2003|John Farnham
2004|Little River Band
2005|Jimmy Barnes;Smoky Dawson;Renée Geyer;Normie Rowe;Split Enz;The Easybeats;Hunters & Collectors
2006|Daddy Cool;Divinyls;Icehouse;Helen Reddy;Rose Tattoo;Lobby Loyde;Midnight Oil
2007|Frank Ifield;Hoodoo Gurus;Marcia Hines;Jo Jo Zep & The Falcons;Brian Cadd;Radio Birdman;Nick Cave
2008|Dragon;Russell Morris;Max Merritt;The Triffids
2009|Kev Carmody;The Dingoes;Little Pattie;Mental As Anything;John Paul Young
2010|The Church;Models;Johnny Young;John Williamson;The Loved Ones
2011|Kylie Minogue;The Wiggles
2012|Yothu Yindi
2013|Air Supply
2014|Molly Meldrum;Countdown
2015|Tina Arena
2016|Crowded House
2017|Daryl Braithwaite
2018|Kasey Chambers
2019|Human Nature
2020|Archie Roach
2023|Jet
2024|Missy Higgins
2025|You Am I
2026|Gurrumul;Jenny Morris;Kate Ceberano;Spiderbait;The Living End;Vika and Linda"""
with open(ROOT / "hall_of_fame.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["year", "inductee", "stack"])
    for line in hof_raw.splitlines():
        yr, people = line.split("|")
        for i, p in enumerate(people.split(";")):
            w.writerow([int(yr), p, i])

# ---------------------------------------------------------------------------
# 5. International chart peaks of four Australian hits (Wikipedia "Weekly charts")
#    Best (lowest) peak per country across that country's main national charts.
# ---------------------------------------------------------------------------
iso = {  # chart-name prefix -> (country, ISO 3166 numeric, lat, lon of capital)
    "Argentina": ("Argentina", 32, -34.60, -58.38), "Australia": ("Australia", 36, -35.28, 149.13),
    "Austria": ("Austria", 40, 48.21, 16.37), "Belgium": ("Belgium", 56, 50.85, 4.35),
    "Belarus": ("Belarus", 112, 53.90, 27.57), "Bolivia": ("Bolivia", 68, -16.50, -68.15),
    "Brazil": ("Brazil", 76, -15.79, -47.88), "Bulgaria": ("Bulgaria", 100, 42.70, 23.32),
    "Canada": ("Canada", 124, 45.42, -75.70), "Chile": ("Chile", 152, -33.45, -70.67),
    "Colombia": ("Colombia", 170, 4.71, -74.07), "Costa Rica": ("Costa Rica", 188, 9.93, -84.08),
    "Croatia": ("Croatia", 191, 45.81, 15.98), "Czech Republic": ("Czechia", 203, 50.08, 14.44),
    "Denmark": ("Denmark", 208, 55.68, 12.57), "Dominican Republic": ("Dominican Rep.", 214, 18.49, -69.93),
    "Ecuador": ("Ecuador", 218, -0.18, -78.47), "El Salvador": ("El Salvador", 222, 13.69, -89.22),
    "Estonia": ("Estonia", 233, 59.44, 24.75), "Finland": ("Finland", 246, 60.17, 24.94),
    "France": ("France", 250, 48.86, 2.35), "Germany": ("Germany", 276, 52.52, 13.40),
    "Greece": ("Greece", 300, 37.98, 23.73), "Guatemala": ("Guatemala", 320, 14.63, -90.51),
    "Honduras": ("Honduras", 340, 14.07, -87.19), "Hong Kong": ("Hong Kong", 344, 22.32, 114.17),
    "Hungary": ("Hungary", 348, 47.50, 19.04), "Iceland": ("Iceland", 352, 64.15, -21.94),
    "India": ("India", 356, 28.61, 77.21), "Indonesia": ("Indonesia", 360, -6.21, 106.85),
    "Ireland": ("Ireland", 372, 53.35, -6.26), "Israel": ("Israel", 376, 31.77, 35.21),
    "Italy": ("Italy", 380, 41.90, 12.50), "Japan": ("Japan", 392, 35.68, 139.69),
    "Kazakhstan": ("Kazakhstan", 398, 51.17, 71.45), "Latvia": ("Latvia", 428, 56.95, 24.11),
    "Lebanon": ("Lebanon", 422, 33.89, 35.50), "Lithuania": ("Lithuania", 440, 54.69, 25.28),
    "Luxembourg": ("Luxembourg", 442, 49.61, 6.13), "Malaysia": ("Malaysia", 458, 3.14, 101.69),
    "Mexico": ("Mexico", 484, 19.43, -99.13), "Netherlands": ("Netherlands", 528, 52.37, 4.90),
    "New Zealand": ("New Zealand", 554, -41.29, 174.78), "Nicaragua": ("Nicaragua", 558, 12.11, -86.24),
    "Norway": ("Norway", 578, 59.91, 10.75), "Panama": ("Panama", 591, 8.98, -79.52),
    "Peru": ("Peru", 604, -12.05, -77.04), "Philippines": ("Philippines", 608, 14.60, 120.98),
    "Poland": ("Poland", 616, 52.23, 21.01), "Portugal": ("Portugal", 620, 38.72, -9.14),
    "Puerto Rico": ("Puerto Rico", 630, 18.47, -66.11), "Romania": ("Romania", 642, 44.43, 26.10),
    "Russia": ("Russia", 643, 55.76, 37.62), "San Marino": ("San Marino", 674, 43.94, 12.45),
    "Singapore": ("Singapore", 702, 1.35, 103.82), "Slovakia": ("Slovakia", 703, 48.15, 17.11),
    "Slovenia": ("Slovenia", 705, 46.06, 14.51), "South Africa": ("South Africa", 710, -25.75, 28.19),
    "South Korea": ("South Korea", 410, 37.57, 126.98), "Spain": ("Spain", 724, 40.42, -3.70),
    "Sweden": ("Sweden", 752, 59.33, 18.07), "Switzerland": ("Switzerland", 756, 46.95, 7.45),
    "Taiwan": ("Taiwan", 158, 25.03, 121.57), "Ukraine": ("Ukraine", 804, 50.45, 30.52),
    "UK": ("United Kingdom", 826, 51.51, -0.13), "US": ("United States", 840, 38.91, -77.04),
    "Uruguay": ("Uruguay", 858, -34.90, -56.16), "Venezuela": ("Venezuela", 862, 10.48, -66.90),
    "Vietnam": ("Vietnam", 704, 21.03, 105.85),
}
prefixes = sorted(iso, key=len, reverse=True)
peaks, song = {}, None
songs = []
for line in (ROOT / "source" / "chart_peaks_raw.txt").read_text().splitlines():
    if not line.strip() or line.startswith("#"):
        continue
    if line.startswith("== "):
        title, artist, yr = line[3:].split("|")
        song = title; songs.append((title, artist, int(yr))); continue
    chart, peak = line.rsplit("|", 1)
    pre = next(p for p in prefixes if chart.startswith(p + " ") or chart == p)
    key = (song, pre)
    peaks[key] = min(peaks.get(key, 999), int(peak))

out = []
for (s, pre), pk in peaks.items():
    c, code, lat, lon = iso[pre]
    title, artist, yr = next(x for x in songs if x[0] == s)
    band = "No. 1" if pk == 1 else ("Top 5" if pk <= 5 else ("Top 10" if pk <= 10 else ("Top 20" if pk <= 20 else "Top 100")))
    out.append({"song": s, "artist": artist, "year": yr, "label": f"{s} ({artist}, {yr})",
                "country": c, "id": code, "peak": pk, "band": band, "lat": lat, "lon": lon, "tiny": int(code in (344, 674, 702))})
out.sort(key=lambda r: (r["year"], r["country"]))
with open(ROOT / "chart_peaks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]))
    w.writeheader(); w.writerows(out)

# Flow lines: Canberra -> every country where at least one of the four songs hit No. 1
ones = {}
for r in out:
    if r["peak"] == 1 and r["country"] != "Australia":
        ones.setdefault(r["country"], {"country": r["country"], "lat": r["lat"], "lon": r["lon"], "songs": []})["songs"].append(r["song"])
flows = [{"country": v["country"], "lat": v["lat"], "lon": v["lon"], "number_ones": len(v["songs"]),
          "songs": ", ".join(v["songs"]), "o_lat": -35.28, "o_lon": 149.13} for v in ones.values()]
flows.sort(key=lambda r: -r["number_ones"])
with open(ROOT / "number_one_flows.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(flows[0]))
    w.writeheader(); w.writerows(flows)

print("aria", len(aria), "| states", len(rows), "| h100", len(h100), "| peaks", len(out), "| flows", len(flows))
for r in rows: print(r)

# ---------------------------------------------------------------------------
# 6. Derived helper files for the maps
# ---------------------------------------------------------------------------
import math
places = {}
for a, wins, noms, place, st, lat, lon, kind in aria:
    if not place:
        continue
    p = places.setdefault(place, {"place": place, "state": st, "lat": lat, "lon": lon, "artists": 0, "wins": 0, "names": []})
    p["artists"] += 1; p["wins"] += wins; p["names"].append(a)
with open(ROOT / "aria_places.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["place", "state", "lat", "lon", "artists", "wins", "names"])
    w.writeheader()
    for p in sorted(places.values(), key=lambda p: -p["wins"]):
        p["names"] = ", ".join(p["names"]); w.writerow(p)

# great-circle paths from Canberra to each No. 1 country (for the flow map)
def gc(lat1, lon1, lat2, lon2, n=48):
    p1, l1, p2, l2 = map(math.radians, (lat1, lon1, lat2, lon2))
    d = 2 * math.asin(math.sqrt(math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin((l2 - l1) / 2) ** 2))
    pts = []
    for i in range(n + 1):
        f = i / n
        A = math.sin((1 - f) * d) / math.sin(d); B = math.sin(f * d) / math.sin(d)
        x = A * math.cos(p1) * math.cos(l1) + B * math.cos(p2) * math.cos(l2)
        y = A * math.cos(p1) * math.sin(l1) + B * math.cos(p2) * math.sin(l2)
        z = A * math.sin(p1) + B * math.sin(p2)
        pts.append((math.degrees(math.atan2(z, math.hypot(x, y))), math.degrees(math.atan2(y, x)), i))
    return pts
with open(ROOT / "number_one_paths.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["country", "number_ones", "order", "lat", "lon"])
    for fl in flows:
        for lat, lon, i in gc(fl["o_lat"], fl["o_lon"], fl["lat"], fl["lon"]):
            w.writerow([fl["country"], fl["number_ones"], i, round(lat, 3), round(lon, 3)])
print("places", len(places))
