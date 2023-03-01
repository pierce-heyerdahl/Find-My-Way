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

import BarChart, { convertBarChartData } from "../components/BarChart";

import Map from "../components/Map";
import Marker from "../components/Marker";

const MapView = () => {
  const [searchParams] = useSearchParams();

  const jobTitle = searchParams.get("jobTitle");
  const state = searchParams.get("state");

  const flag = true;

  // returns null for the one not searched
  //console.log(jobTitle);
  //console.log(state);

  const [data, setData] = React.useState([{}]);

  const center = { lat: 47.58536201892643, lng: -122.14791354386401 };
  const positions = [{ lat: 30, lng: -97}, { lat: 20, lng: 85}];
  const zoom = 12;

  const tilesLoaded = (m) => {
    console.log(m.getZoom());
    console.log("tilesloaded");
    var bounds = new window.google.maps.LatLngBounds();
    console.log(data.results);
    {typeof data.results === "undefined" ? (
      console.log("No Data Yet")
    ) : (
      data.results.map((row) => (
        bounds.extend(new window.google.maps.LatLng(row["lat"], row["lng"])))
      ))
    }
    //data.results.map((row) => (bounds.extend(new window.google.maps.LatLng(row["lat"], row["lng"]))));
    m.fitBounds(bounds);
  };

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

  //const queries = [];

  // searchParams.forEach((val, kv) => {
  //   queries.push(`${kv}=${val}`);
  // });

  // const url = `/search/?${queries.join("&")}`;

  // console.log({ url });

  // search/?jobTitle=Lawyer
  // search/?state=Washington
  // search/?jobTitle=Lawyer&state=Washington

  React.useEffect(() => {
    if (state !== null) {
      fetch("/searchState/" + state)
        .then((res) => res.json())
        .then((data) => {
          setData(data);
          console.log(data);
          console.log(data[0]);
        });
    } else {
      fetch("/searchTitle/" + jobTitle)
        .then((res) => res.json())
        .then((data) => {
          setData(data);
          console.log(data);
          console.log(data[0]);
        });
    }
  }, [jobTitle, state]);

  // http://localhost:3000/mapview?jobTitle=Lawyer&state=Washington

  return (
    <Stack
      direction="row"
      divider={<Divider orientation="vertical" flexItem />}
      spacing={0}
      sx={{
        width: "100%",
        height: "calc(100% - 58px)",
        backgroundColor: "snow",
      }}
    >
      <Box sx={{ width: "50%", height: "50%", margin: "2em" }}>
        {jobTitle ? (
          <Typography
            textAlign="center"
            sx={{
              fontSize: "20px",
              fontWeight: "bold",
              color: "#F1C40F",
            }}
          >
            Search by Job Title:{" "}
            <span style={{ color: "#28B463 " }}>{jobTitle.toUpperCase()}</span>
          </Typography>
        ) : null}
        {state ? (
          <Typography
            textAlign="center"
            sx={{
              fontSize: "20px",
              fontWeight: "bold",
              color: "#F1C40F",
            }}
          >
            Search by State:{" "}
            <span style={{ color: "#28B463 " }}>{state.toUpperCase()}</span>
          </Typography>
        ) : null}
        <Box
          sx={{
            textAlign: "left",
            margin: "auto",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            width: "fit-content",
          }}
        >
          {typeof data.results === "undefined" ? (
            <p>Loading...</p>
          ) : (
            data.results.map((row, i) => (
              <Box
                sx={{ padding: "1em", textAlign: "left", width: "100%" }}
                key={i}
              >
                {i + 1}. {row["City"] + " $" + row["Salary"].toLocaleString()}
              </Box>
            ))
          )}
        </Box>

        <Divider orientation="horizontal" flexItem sx={{ margin: "2em 0" }} />
        {/*where graph will go*/}
        <Box sx={{ display: "flex", justifyContent: "center", margin: "1em" }}>
          <Box
            sx={{
              maxWidth: "100%",
              maxHeight: "100%",
              width: "600px",
              height: "300px",
            }}
          >
            <BarChart chartData={convertBarChartData(data)} />
          </Box>
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
          <Map center={center} zoom={zoom} locations={data.results} tilesLoaded={tilesLoaded}>
            {typeof data.results === "undefined" ? (
              console.log("This makes the markers work")
            ) : (
              data.results.map((row) => (
                <Marker position={{lat: row["lat"], lng: row["lng"]}} />
              ))
            )}
          </Map>
        </Wrapper>
      </Box>
    </Stack>
  );
};

export default MapView;
