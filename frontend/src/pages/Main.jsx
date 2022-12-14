import React from "react";
import { TextField, Box, Button, Stack, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

import WeatherFilter from "../components/WeatherFilter";

const Main = () => {
  const [jobTitle, setJobTitle] = React.useState("");
  const [state, setState] = React.useState("");
  const navigate = useNavigate();

  const handleSearch = () => {
    if (!jobTitle.trim() && !state.trim()) {
      alert("You must enter either Job Title or state!");
      return;
    }

    const url = "/mapview";

    const searchParams = [];

    if (jobTitle) {
      searchParams.push("jobTitle=" + encodeURI(jobTitle.trim()));
    }

    if (state) {
      searchParams.push("state=" + encodeURI(state.trim()));
    }

    navigate(url + `?${searchParams.join("&")}`);
  };

  const handleChangeJobTitle = (ev) => {
    const newValue = ev.target.value;

    setJobTitle(newValue);
  };

  const handleChangeState = (ev) => {
    const newValue = ev.target.value;

    setState(newValue);
  };

  return (
    <Box p={3}>
      <Box display="flex" justifyContent="center">
        <Stack
          alignItems="center"
          display="flex"
          justifyContent="center"
          spacing={3.5}
          width="400px"
        >
          <TextField
            label="Job Title"
            type="search"
            onChange={handleChangeJobTitle}
          />
          <Typography>OR</Typography>
          <TextField label="State" type="search" onChange={handleChangeState} />
          <Button onClick={handleSearch} variant="contained">
            Search in Map
          </Button>
          <Box paddingTop={2}>
            Weather
            <WeatherFilter />
          </Box>
        </Stack>
      </Box>
    </Box>
  );
};

export default Main;
