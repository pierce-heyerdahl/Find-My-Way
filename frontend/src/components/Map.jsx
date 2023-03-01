import { Box } from "@mui/material";
import React from "react";

const Map = ({ center, zoom, children, locations, tilesLoaded }) => {
  const ref = React.useRef(null);
  const [map, setMap] = React.useState();

  React.useEffect(() => {
    if (ref.current && !map) {
      setMap(new window.google.maps.Map(ref.current, { center, zoom }));
      //window.google.maps.event.addListenerOnce(map, 'tilesloaded', function(){console.log("yeet")});
    }
  }, [ref, map]);

  // should be able to delete this
  React.useEffect(() => {
    if (map) {
      console.log("map useEffect firing 1");
      console.log(locations);
      var bounds = new window.google.maps.LatLngBounds();
      locations.map((row) => (bounds.extend(new window.google.maps.LatLng(row["lat"], row["lng"]))));
      map.fitBounds(bounds);
    }
  }, []);

  React.useEffect(() => {
    if (map) {
      if (tilesLoaded) {
        //map.addListener("tilesloaded", () => tilesLoaded(map));
        window.google.maps.event.addListenerOnce(map, 'tilesloaded', () => tilesLoaded(map));
      }
    }
  }, [map, tilesLoaded]);

  //map.addListenerOnce('tilesloaded', console.log("event list"));
  //window.google.maps.event.addListenerOnce(map, 'tilesloaded', console.log("yeet"));

  return (
    <Box ref={ref} id="map" sx={{ height: "100%", width: "100%" }}>
      {React.Children.map(children, (child) => React.cloneElement(child, {map}))}
    </Box>
  );
};

export default Map;
