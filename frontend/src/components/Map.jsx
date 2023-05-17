import { Box } from "@mui/material";
import React from "react";

const Map = ({ center, zoom, children, locations, tilesLoaded }) => {
  const ref = React.useRef(null);
  const [map, setMap] = React.useState();

  React.useEffect(() => {
    if (ref.current && !map) {
      setMap(new window.google.maps.Map(ref.current, { center, zoom }));
    }
  }, [ref, map, center, zoom]);

  React.useEffect(() => {
    if (map && tilesLoaded) {
      tilesLoaded(map);
    }
  }, [map, tilesLoaded]);

  return (
    <Box ref={ref} id="map" sx={{ height: "100%", width: "100%" }}>
      {React.Children.map(children, (child) =>
        React.cloneElement(child, { map })
      )}
    </Box>
  );
};

export default Map;
