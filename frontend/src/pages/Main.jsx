import React from "react";
import { TextField, Box, Button, Stack, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import backgroundImage from "./images/test2.jpg";

const Main = () => {
  const [jobTitle, setJobTitle] = React.useState("");
  const [state, setState] = React.useState("");
  const navigate = useNavigate();

  const handleSearch = () => {
    if (!jobTitle.trim() && !state.trim()) {
      alert("You must enter either Job Title or State!");
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
    <Box
      p={3}
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        boxSizing: "border-box",
        height: "calc(100% - 56px)",
        zIndex: 0,
      }}
    >
      <Box display="flex" justifyContent="center" sx={{ marginTop: "16px" }}>
        <Stack
          alignItems="center"
          display="flex"
          justifyContent="center"
          spacing={2.5}
          width="400px"
        >
          <TextField
            label="Job Title"
            type="search"
            onChange={handleChangeJobTitle}
            sx={{ backgroundColor: "snow" }}
            onKeyPress={(ev) => {
              if (ev.key === "Enter") {
                ev.preventDefault();
                handleSearch();
              }
            }}
          />
          <Typography>OR</Typography>
          <TextField
            label="State"
            type="search"
            onChange={handleChangeState}
            sx={{ backgroundColor: "snow" }}
            onKeyPress={(ev) => {
              if (ev.key === "Enter") {
                ev.preventDefault();
                handleSearch();
              }
            }}
          />
          <Button
            onClick={handleSearch}
            variant="contained"
            style={{ marginTop: "40px" }}
          >
            Search in Map
          </Button>
        </Stack>
      </Box>
      <Box position="absolute" bottom="20px" left={15}>
        <Button
          variant="contained"
          color="primary"
          style={{ backgroundColor: "transparent" }}
          href="/adminLogin"
        >
          Admin
        </Button>
      </Box>
    </Box>
  );
};

export default Main;
