# Let's Double Check
A website to help citizens host their own nonpartisan hand-counted exit poll for federal and state elections.

## Top-Level Requirements
- We are creating a data visualization website for showing voting precincts across the United States.
- Branding for the site should be "Citizen Exit Poll". "Let's Double Check" is just the internal name for the repo.
- The site should work on desktop and mobile devices.
- The site should load quickly and should use caching wherever possible.
- The site should be user-friendly and it should look really good.

## Sprint 1
- Data gathering
  - We will need GeoJSON shapefiles downloaded into the /data/states folder for each state.
  - The top-level state shapefile will contain the names and outlines of its counties.
    - Use this URL format to grab these (note the {STATENAME} url-encoded param placeholder): https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-united-states-of-america-county/exports/geojson?lang=en&refine=ste_name%3A%22{STATENAME}%22&facet=facet(name%3D%22ste_name%22%2C%20disjunctive%3Dtrue)&timezone=America%2FNew_York
  - Keep files neatly organized into the preexisting state folder structure. Use the filename "counties.json".

- Create the home page
  - Show a map of the United States with the states outlined. Include Alaska and Hawaii.
  - Display a sidebar that will show details about the currently selected item. Initially, show a message there to instruct the user to click.
  - Each state should be clickable. When selected, the screen should zoom in on the state.
  - Once a state is selected, the outline of each county should be made visible and clickable.
  - States and counties should have a tooltip with the name.

## Techincal Specs
- Use the Dotnet stack (C#).
- All data used by the site should be pulled from the Github repo.
- State and county boundaries are to be stored in the /data folder.
- The site is to be hosted using Github Pages.
- The website needs a CI/CD pipeline.
  - When changes are pushed, Github pages should get updated and the client's cache should bust.