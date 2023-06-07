import React from "react";
import {
  Box,
  Stack,
  Divider,
  CircularProgress,
  Typography,
  Pagination,
} from "@mui/material";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import { Wrapper, Status } from "@googlemaps/react-wrapper";
import { useSearchParams, useNavigate } from "react-router-dom";
import { useMediaQuery } from 'react-responsive';

import BarChart, { convertBarChartData } from "../components/BarChart";

import Map from "../components/Map";
import Marker from "../components/Marker";

const MapView = () => {
  const [searchParams] = useSearchParams();

  const navigate = useNavigate();

  const isMobile = useMediaQuery({ query: '(max-width: 920px)' });
  const isMobileLarge = useMediaQuery({ query: '(max-width: 1200px)' });
  const isMobileSmall = useMediaQuery({ query: '(max-width: 450px)' });

  const jobTitle = searchParams.get("jobTitle");
  const state = searchParams.get("state");
  const city = searchParams.get("city");
  const minSalary = searchParams.get("minSalary");
  const maxSalary = searchParams.get("maxSalary");

  const RESULTS_PER_PAGE = 10;

  let currentPage = parseInt(searchParams.get("page")) || 1;

  const handlePageChange = (event, value) => {
    let newSearchParams = new URLSearchParams(searchParams.toString());
    newSearchParams.set("page", value);


    navigate({
      pathname: window.location.pathname,
      search: newSearchParams.toString()
    });

    currentPage = value;
  }

  const [data, setData] = React.useState({results: [], total_pages: 1});
  const [loading, setLoading] = React.useState(true);

  const center = { lat: 47.58536201892643, lng: -122.14791354386401 };
  const positions = [
    { lat: 30, lng: -97 },
    { lat: 20, lng: 85 },
  ];
  const zoom = 12;

  const tilesLoaded = (m) => {
    var bounds = new window.google.maps.LatLngBounds();
    {
      typeof data.results === "undefined"
        ? console.log("No Data Yet")
        : data.results.map((row) =>
            bounds.extend(new window.google.maps.LatLng(row["lat"], row["lng"]))
          );
    }
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

  React.useEffect(() => {
    setLoading(true);
    fetch("/search/" + jobTitle + "/" + state + "/" + city + "/" + minSalary + "/" + maxSalary + "/" + currentPage)
      .then((res) => res.json())
      .then((data) => {
        setData({results: data.results, total_pages: data.total_pages});
        setLoading(false);
      });
  }, [jobTitle, state, city, minSalary, maxSalary, currentPage]);

  return (
    <Stack
      direction={isMobile ? "column-reverse" : "row"}
      divider={<Divider orientation="vertical" flexItem />}
      spacing={0}
      justifyContent={isMobile ? "flex-end" : ""}
      sx={{
        width: "100%",
        height: isMobile ? "100%" : "calc(100% - 56px)",
        backgroundColor: "snow",
        overflow: "hidden"
      }}
    >
      {!loading ? (
        <Box sx={{ width: isMobile ? "auto" : "50%", overflowY: "auto" }}>
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
          {city ? (
          <Typography
            textAlign="center"
            sx={{
              fontSize: "20px",
              fontWeight: "bold",
              color: "#F1C40F",
            }}
          >
            Search by City:{" "}
            <span style={{ color: "#28B463 " }}>{city.toUpperCase()}</span>
          </Typography>
          ) : null}
          {!loading ? (
            <Box
              sx={{
                textAlign: "left",
                margin: "auto",
                display: "flex",
                flexDirection: isMobile ? "column-reverse" : "column",
                justifyContent: "center",
                alignItems: "center",
                width: "fit-content",
              }}
            >
              {typeof data.results === "undefined" ? (
                <p>Loading...</p>
              ) : (
                <TableContainer component={Paper} sx={{ maxWidth: "100%", margin: "1em" }}>
                <Table aria-label="simple table">
                  <TableHead>
                    <TableRow>
                      <TableCell align="left" sx={{ p: isMobileSmall ? '0.15em' : isMobileLarge ? '0.5em' : 'default' }}>No.</TableCell>
                      <TableCell align="left" sx={{ p: isMobileSmall ? '0.15em' : isMobileLarge ? '0.5em' : 'default' }}>Location</TableCell>
                      <TableCell align="left" sx={{ p: isMobileSmall ? '0.15em' : isMobileLarge ? '0.5em' : 'default' }}>Job Title</TableCell>
                      <TableCell align="left" sx={{ p: isMobileSmall ? '0.15em' : isMobileLarge ? '0.5em' : 'default' }}>Salary</TableCell>
                      <TableCell align="left" sx={{ p: isMobileSmall ? '0.15em' : isMobileLarge ? '0.5em' : 'default' }}>Job Links</TableCell>
                      <TableCell align="left" sx={{ p: isMobileSmall ? '0.15em' : isMobileLarge ? '0.5em' : 'default' }}>Cost of Living</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {data.results.map((row, i) => (
                      <TableRow
                        key={i}
                        sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                      >
                        <TableCell align="left" sx={{ p: isMobileSmall ? '0.15em' : isMobileLarge ? '0.5em' : 'default' }}>{((currentPage - 1) * RESULTS_PER_PAGE) + i + 1}</TableCell>
                        <TableCell align="left" sx={{ p: isMobileSmall ? '0.15em' : isMobileLarge ? '0.5em' : 'default' }}>{row["City"] + ", " + row["State"]}</TableCell>
                        <TableCell align="left" sx={{ p: isMobileSmall ? '0.15em' : isMobileLarge ? '0.5em' : 'default' }}>{row["Job Title"]}</TableCell>
                        <TableCell align="left" sx={{ p: isMobileSmall ? '0.15em' : isMobileLarge ? '0.5em' : 'default' }}>${row["Salary"].toLocaleString()}</TableCell>
                        <TableCell align="left" sx={{ p: isMobileSmall ? '0.15em' : isMobileLarge ? '0.5em' : 'default' }}>
                          <a href={encodeURI(`https://www.google.com/search?q=${row["City"]}+${row["State"]}+${row["Job Title"]}&ibp=htl;jobs`)}
                            target="_blank" 
                            rel="noopener noreferrer"
                          >
                            Search on Google
                          </a>
                        </TableCell>
                        <TableCell align="left" sx={{ p: isMobileSmall ? '0.15em' : isMobileLarge ? '0.5em' : 'default', color: row["coli"] > 100 ? 'red' : 'green' }}>
                          {row["coli"] > 100 ? '+' : '-'}{(row["coli"] - 100).toFixed(1)}%
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}


              <Pagination count={data.total_pages} page={currentPage} onChange={handlePageChange} sx={{padding: "0.25em"}} />
            </Box>
          ) : null}

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
      ) : (
        <Box
          sx={{
            textAlign: "left",
            margin: "auto",
            display: "flex",
            flexDirection: isMobile ? "column-reverse" : "column",
            justifyContent: "center",
            alignItems: "center",
            width: "fit-content",
          }}
        >
          <Typography>Loading...</Typography>
        </Box>
      )}

      <Box
        border="1px grey solid"
        width="100%"
        height={isMobile ? "25vh" : "100%"}
        sx={{ alignItems: "center", justifyContent: "center", width: isMobile ? "100%" : "50%", overflow: "hidden" }}
      >
        <Wrapper
          apiKey={"AIzaSyD6FfjQK2HkU7BEbYZit0gSdpm-9e7IabI"}
          render={render}
        >
          <Map
            center={center}
            zoom={zoom}
            locations={data.results}
            tilesLoaded={tilesLoaded}
          >
            {typeof data.results === "undefined"
              ? console.log("This makes the markers work")
              : data.results.map((row) => (
                  <Marker position={{ lat: row["lat"], lng: row["lng"] }} />
                ))}
          </Map>
        </Wrapper>
      </Box>
    </Stack>
  );
};

export default MapView;
