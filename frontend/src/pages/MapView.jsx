import React from "react";
import { Box, Stack, Divider, CircularProgress } from "@mui/material";
import { Wrapper, Status } from "@googlemaps/react-wrapper";

import Map from "../components/Map";

const MapView = () => {
  const center = { lat: 47.58536201892643, lng: -122.14791354386401 };
  const zoom = 12;

  const render = (status) => {
    switch (status) {
      case Status.LOADING:
        return <CircularProgress />;
      case Status.FAILURE:
        return "Failed to load Google Maps API";
      default:
        return null;
    }
  };

  return (
    <Stack
      direction="row"
      divider={<Divider orientation="vertical" flexItem />}
      spacing={0}
      sx={{ width: "100%", height: "calc(100% - 58px)" }}
    >
      <Box sx={{ width: "50%", height: "50%" }}>Top state</Box>

      <Box
        border="1px grey solid"
        width="100%"
        height="100"
        sx={{ alignItems: "center", justifyContent: "center", width: "50%" }}
      >
        <Wrapper
          apiKey={"AIzaSyD6FfjQK2HkU7BEbYZit0gSdpm-9e7IabI"}
          render={render}
        >
          <Map center={center} zoom={zoom} />
        </Wrapper>
      </Box>
    </Stack>
  );
};

export default MapView;
