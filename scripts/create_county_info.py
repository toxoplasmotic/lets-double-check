import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
import xml.dom.minidom as minidom
from urllib.parse import quote
import requests
import sys

def get_wikipedia_link(state_name, county_name):
    """Generate Wikipedia link for the county."""
    county_clean = county_name.replace(" County", "").replace(" ", "_")
    state_clean = state_name.replace(" ", "_")
    wiki_title = f"{county_clean}_County,_{state_clean}"
    return f"https://en.wikipedia.org/wiki/{quote(wiki_title)}"

def fetch_county_data(state_name, county_name):
    """Fetch JSON data from the API."""
    base_url = ("https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/"
                "georef-united-states-of-america-county/records")
    params = {
        "order_by": "coty_name",
        "limit": 100,
        "offset": 0,
        "refine": [f"ste_name:{state_name}", f"coty_name:{county_name}"]
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        if data.get("total_count", 0) == 0:
            print(f"No data found for state: {state_name}, county: {county_name}")
            sys.exit(1)
        return data
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        if response.status_code == 400:
            print(f"API Error: {response.json().get('message', 'Unknown error')}")
        sys.exit(1)

def main(state_name, county_name, output_file):
    # Fetch JSON data
    json_data = fetch_county_data(state_name, county_name)
    
    # Create root element with namespace
    ns = {'cd': 'http://example.com/countydata'}
    ET.register_namespace('', ns['cd'])
    root = ET.Element("CountyData", xmlns=ns['cd'])

    # Extract first result
    result = json_data["results"][0]

    # Add LastUpdated with current timestamp in EDT
    last_updated = ET.SubElement(root, "LastUpdated")
    edt = timezone(timedelta(hours=-4))  # EDT is UTC-4
    last_updated.text = datetime.now(edt).isoformat()

    # Add CountyName
    county_elem = ET.SubElement(root, "CountyName")
    county_elem.text = result["coty_name_long"][0]

    # Add StateName
    state_elem = ET.SubElement(root, "StateName")
    state_elem.text = result["ste_name"][0]

    # Add WikipediaLink
    wiki_link = ET.SubElement(root, "WikipediaLink")
    wiki_link.text = get_wikipedia_link(state_name, county_name)

    # Add Population (placeholder, 2020 census for Autauga County as example)
    population = ET.SubElement(root, "Population")
    population.text = ""  # Replace with actual data if available

    # Add Coordinates (GeoPoint)
    coordinates = ET.SubElement(root, "Coordinates")
    latitude = ET.SubElement(coordinates, "Latitude")
    latitude.text = str(result["geo_point_2d"]["lat"])
    longitude = ET.SubElement(coordinates, "Longitude")
    longitude.text = str(result["geo_point_2d"]["lon"])

    # Add Shape (GeoShape)
    shape = ET.SubElement(root, "Shape")
    shape_type = ET.SubElement(shape, "Type")
    shape_type.text = result["geo_shape"]["type"]
    geometry = ET.SubElement(shape, "Geometry")
    geometry_type = ET.SubElement(geometry, "Type")
    geometry_type.text = result["geo_shape"]["geometry"]["type"]
    coords = ET.SubElement(geometry, "Coordinates")
    ring = ET.SubElement(coords, "Ring")
    for point in result["geo_shape"]["geometry"]["coordinates"][0]:
        point_elem = ET.SubElement(ring, "Point")
        point_lon = ET.SubElement(point_elem, "Longitude")
        point_lon.text = str(point[0])
        point_lat = ET.SubElement(point_elem, "Latitude")
        point_lat.text = str(point[1])

    # Add Precincts (empty)
    precincts = ET.SubElement(root, "Precincts")

    # Convert to formatted XML
    xml_str = minidom.parseString(ET.tostring(root, encoding='unicode')).toprettyxml(indent="  ")

    # Write to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_str)

    print(f"XML file '{output_file}' generated.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <state_name> <county_name> <output_file>")
        sys.exit(1)
    state_name = sys.argv[1]
    county_name = sys.argv[2]
    output = sys.argv[3]
    main(state_name, county_name, output)