import React from "react";
import { useState, useEffect } from "react";
import { Box, Stack, Divider, CircularProgress } from "@mui/material";
import { Wrapper, Status } from "@googlemaps/react-wrapper";
import { useLocation } from "react-router-dom";

import Map from "../components/Map";

const MapView = () => {
  const center = { lat: 47.58536201892643, lng: -122.14791354386401 };
  const zoom = 12;
  const [data, setData] = useState([{}]);
  const {state} = useLocation();
  const {job_title} = state;

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

  useEffect(() => {
    fetch("/search/" + job_title)
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        console.log(data);
        console.log(data[0]);
      });
  }, []);

  return (
    <Stack
      direction="row"
      divider={<Divider orientation="vertical" flexItem />}
      spacing={0}
      sx={{ width: "100%", height: "calc(100% - 58px)" }}
    >
      <Box sx={{ width: "50%", height: "50%" }}>
        Results
        {typeof data.results === "undefined" ? (
          <p>Loading...</p>
        ) : (
          data.results.map((row, i) => <p key={i}>{row["City"] + " " + row["Job Title"] + " " + row["Salary"]}</p>)
        )}
      </Box>

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
