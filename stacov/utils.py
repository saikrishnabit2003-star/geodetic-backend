# stacov/utils.py
import math

# -------------------------------
# ECEF → Geodetic (WGS84)
# -------------------------------
def ecef_to_llh(x, y, z):
    a = 6378137.0
    f = 1 / 298.257223563
    e2 = f * (2 - f)

    lon = math.atan2(y, x)
    p = math.sqrt(x*x + y*y)
    lat = math.atan2(z, p * (1 - e2))

    for _ in range(5):
        N = a / math.sqrt(1 - e2 * math.sin(lat)**2)
        h = p / math.cos(lat) - N
        lat = math.atan2(z, p * (1 - e2 * (N / (N + h))))

    return (
        math.degrees(lat),
        math.degrees(lon),
        h
    )


# -------------------------------
# Parse STACOV file
# -------------------------------
def parse_stacov_file(filepath):
    stations = {}
    results = []

    with open(filepath, "r") as file:
        for line in file:
            if "STA X" in line or "STA Y" in line or "STA Z" in line:
                parts = line.split()

                station = parts[1]       # 1LSU
                coord = parts[3]         # X / Y / Z
                value = float(parts[4])  # ECEF value

                stations.setdefault(station, {})[coord] = value

    for station, xyz in stations.items():
        if {"X", "Y", "Z"}.issubset(xyz):
            lat, lon, h = ecef_to_llh(
                xyz["X"],
                xyz["Y"],
                xyz["Z"]
            )

            results.append({
                "station": station,
                "latitude": lat,
                "longitude": lon,
                "height": round(h, 3)
            })

    return results
