import { Box } from "@mui/material";
import React from "react";

const Map = ({ center, zoom }) => {
  const ref = React.useRef(null);
  const [map, setMap] = React.useState();

  React.useEffect(() => {
    if (ref.current && !map) {
      setMap(new window.google.maps.Map(ref.current, { center, zoom }));
    }
  }, [ref, map]);

  return <Box ref={ref} id="map" sx={{ height: "100%", width: "100%" }} />;
};

export default Map;
