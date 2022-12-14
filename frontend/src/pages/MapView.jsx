import React from "react";
import {
  Box,
  Stack,
  Divider,
  CircularProgress,
  Typography,
} from "@mui/material";
import { Wrapper, Status } from "@googlemaps/react-wrapper";
import { useSearchParams } from "react-router-dom";

import Map from "../components/Map";

const MapView = () => {
  const [searchParams] = useSearchParams();

  const jobTitle = searchParams.get("jobTitle");
  const state = searchParams.get("state");

  const [data, setData] = React.useState([{}]);

  React.useEffect(() => {
    fetch("/test")
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        console.log(data);
      });
  }, []);

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

  React.useEffect(() => {
    fetch("/search/" + jobTitle)
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
        {jobTitle ? (
          <Typography textAlign="center">
            Search by Job Title: {jobTitle}
          </Typography>
        ) : null}
        {state ? (
          <Typography textAlign="center">Search by state: {state}</Typography>
        ) : null}
        <Box textAlign="center">
          {typeof data.results === "undefined" ? (
            <p>Loading...</p>
          ) : (
            data.results.map((row, i) => (
              <p sx={{ padding: "1em" }} key={i}>
                {row["City"] + " $" + row["Salary"]}
              </p>
            ))
          )}
        </Box>
      </Box>

      <Box
        border="1px grey solid"
        width="100%"
        height="100%"
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
