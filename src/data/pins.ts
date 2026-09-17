/**
 * Map pins for the Earth pop-up on the About page.
 *
 * Add or edit entries here — the map places them automatically from lat/lon,
 * so nothing else needs to change when you add a place.
 *
 * lat: degrees north (negative = south)
 * lon: degrees east  (negative = west)
 */
export type Pin = {
  id: string;
  place: string;
  label: string;
  lat: number;
  lon: number;
  blurb: string;
};

export const pins: Pin[] = [
  {
    id: "boston",
    place: "Hyde Park / Canton, MA",
    label: "Where I grew up",
    lat: 42.22,
    lon: -71.13,
    blurb:
      "Home. Boston born and raised — this is the stretch between Hyde Park and Canton where I grew up. [Placeholder: add what you want to say about growing up here, and how it connects to caring about local impact.]",
  },
  {
    id: "dc",
    place: "Washington, DC",
    label: "George Washington University — B.S.",
    lat: 38.9,
    lon: -77.05,
    blurb:
      "B.S. in Mechanical Engineering (aerospace concentration), summa cum laude, at George Washington University. Orbital mechanics and controls research, plus onboard computation tested on drones. [Placeholder: add more on the DC years.]",
  },
  {
    id: "cambridge",
    place: "Cambridge, MA",
    label: "MIT — SM and PhD",
    lat: 42.36,
    lon: -71.09,
    blurb:
      "MIT AeroAstro and the Media Lab. SM in 2022 on Mars entry trajectory optimization; now a PhD candidate with the Space Enabled Research Group. [Placeholder: add what MIT has meant to the work.]",
  },
  {
    id: "pasadena",
    place: "Pasadena, CA",
    label: "NASA JPL — SURP collaboration",
    lat: 34.2,
    lon: -118.17,
    blurb:
      "NASA Jet Propulsion Laboratory, where the JPL Strategic University Research Partnership grant work on adaptive sensing lives. [Placeholder: add more about the JPL collaboration and the visit.]",
  },
  {
    id: "mayaguez",
    place: "Mayagüez, Puerto Rico",
    label: "CARICOOS — stakeholder collaboration",
    lat: 18.2,
    lon: -67.14,
    blurb:
      "Working with the Caribbean Coastal Ocean Observing System (CARICOOS), the National Weather Service San Juan office, and the Landslide Ready team — the decision-makers whose needs shape what the satellite should actually be looking for. [Placeholder: add more on this collaboration.]",
  },
  {
    id: "luanda",
    place: "Luanda, Angola",
    label: "Global Classroom — teaching",
    lat: -8.84,
    lon: 13.23,
    blurb:
      "Taught alongside my advisor in the Global Classroom program with ~50 students from ISPTEC, mentoring a group mapping aquifers for water security in drought-affected southern Angola. [Placeholder: add more about this experience.]",
  },
];
