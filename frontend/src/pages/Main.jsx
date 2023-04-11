import React from "react";
import { TextField, Box, Button, Stack, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import backgroundImage from "./images/test2.jpg";
import RangeSlider from "../components/RangeSlider";

const Main = () => {
  const [jobTitle, setJobTitle] = React.useState("");
  const [state, setState] = React.useState("");
  const [city, setCity] = React.useState("");
  const [salaryRange, setSalaryRange] = React.useState([200000, 600000]);
  const navigate = useNavigate();

  const handleSearch = () => {
    if (!jobTitle.trim() && !state.trim() && !city.trim()) {
      alert("You must enter either Job Title or State or City!");
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

    if (city) {
      searchParams.push("city=" + encodeURI(city.trim()));
    }

    if (salaryRange) {
      searchParams.push(`minSalary=${salaryRange[0]}`);
      searchParams.push(`maxSalary=${salaryRange[1]}`);
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

  const handleChangeCity = (ev) => {
    const newValue = ev.target.value;

    setCity(newValue);
  };

  const handleChangeSalaryRange = (newSalaryRange) => {
    if (Array.isArray(newSalaryRange) && newSalaryRange.length === 2) {
      setSalaryRange(newSalaryRange);
    }
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
          <Typography>OR</Typography>
          <TextField
            label="City"
            type="search"
            onChange={handleChangeCity}
            sx={{ backgroundColor: "snow" }}
            onKeyPress={(ev) => {
              if (ev.key === "Enter") {
                ev.preventDefault();
                handleSearch();
              }
            }}
          />
          <Stack>
            <Typography>Salary Range</Typography>
            <RangeSlider
              min={5000}
              onChange={handleChangeSalaryRange}
              value={salaryRange}
            />
            <Typography
              textAlign="center"
              width="100%"
            >{`$${salaryRange[0].toLocaleString()} - $${salaryRange[1].toLocaleString()}`}</Typography>
          </Stack>
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
