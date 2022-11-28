import React from "react";
import { TextField, Box, Button, Stack, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

import FilterList from "../components/FilterList";
import FilterItem from "../components/FilterItem";

const Main = () => {
  const [jobTitle, setJobTitle] = React.useState("");
  const [city, setCity] = React.useState("");
  const navigate = useNavigate();

  const handleSearch = () => {
    if (!jobTitle.trim() && !city.trim()) {
      alert("You must enter either Job Title or City!");
      return;
    }

    const url = "/mapview";

    const searchParams = [];

    if (jobTitle) {
      searchParams.push("jobTitle=" + encodeURI(jobTitle.trim()));
    }

    if (city) {
      searchParams.push("city=" + encodeURI(city.trim()));
    }

    navigate(url + `?${searchParams.join("&")}`);
  };

  const handleChangeJobTitle = (ev) => {
    const newValue = ev.target.value;

    setJobTitle(newValue);
  };

  const handleChangeCity = (ev) => {
    const newValue = ev.target.value;

    setCity(newValue);
  };

  return (
    <Box p={3}>
      <Box display="flex" justifyContent="center">
        <Stack
          alignItems="center"
          display="flex"
          justifyContent="center"
          spacing={3}
          width="400px"
        >
          <TextField
            label="Job Title"
            type="search"
            onChange={handleChangeJobTitle}
          />
          <Typography>OR</Typography>
          <TextField label="City" type="search" onChange={handleChangeCity} />
          <Button onClick={handleSearch} variant="contained">
            Search in Map
          </Button>
          <FilterList>
            <FilterItem label="Avg. Rent Amount" />
            <FilterItem label="Avg. Gas Price" />
            <FilterItem label="Avg. Utility Cost" />
          </FilterList>
        </Stack>
      </Box>
    </Box>
  );
};

export default Main;
