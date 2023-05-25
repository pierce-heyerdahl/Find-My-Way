import React from "react";
import { TextField, Box, Button, Stack, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import backgroundImage from "./images/test2.jpg";
import RangeSlider from "../components/RangeSlider";
import Autocomplete from "@mui/material/Autocomplete";
import { US_STATES, JOB_TITLE_PLACEHOLDERS } from "../constants/place_holders";

const Main = () => {
  const [jobTitle, setJobTitle] = React.useState("");
  const [state, setState] = React.useState("");
  const [city, setCity] = React.useState("");
  const [salaryRange, setSalaryRange] = React.useState([200000, 600000]);
  const [stateSuggestions, setStateSuggestions] = React.useState(US_STATES);
  const [jobTitleSuggestions, setJobTitleSuggestions] = React.useState([]);
  const [citySuggestions, setCitySuggestions] = React.useState([]);

  const navigate = useNavigate();

  const handleSearch = () => {
    // if (!jobTitle.trim() && !state.trim() && !city.trim() && !salaryRange) {
    //   alert("You must enter either Job Title or State or City!");
    //   return;
    // }

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

  // const handleChangeJobTitle = (ev) => {
  //   const newValue = ev.target.value;

  //   setJobTitle(newValue);
  // };

  const handleChangeJobTitle = (event, newValue) => {
    setJobTitle(newValue);
  };

  const handleJobTitleSearch = async (event, newValue) => {
    if (newValue) {
      try {
        const response = await fetch(`/JobsList/${newValue}`);
        const data = await response.json();
        console.log(data);
        setJobTitleSuggestions(data);
      } catch (error) {
        console.error(error);
      }
    }
  };

  // const handleChangeState = (ev) => {
  //   const newValue = ev.target.value;
  //   setState(newValue);
  // };
  const handleChangeState = (event, newValue) => {
    setState(newValue);
  };

  const handleChangeCity = (event, newValue) => {
    setCity(newValue);
  };

  const handleCitySearch = async (event, newValue) => {
    if (newValue) {
      try {
        const response = await fetch(`/CitiesList/${newValue}`);
        const data = await response.json();
        console.log(data);
        setCitySuggestions(data);
      } catch (error) {
        console.log(error);
      }
    }
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
          <Autocomplete
            label="Job Title"
            options={jobTitleSuggestions}
            onChange={handleChangeJobTitle}
            onInputChange={handleJobTitleSearch}
            sx={{ backgroundColor: "snow" }}
            renderInput={(params) => (
              <TextField
                {...params}
                label="Job Title"
                type="search"
                sx={{
                  backgroundColor: "snow",
                  width: "210px",
                  "& .MuiAutocomplete-inputRoot": {
                    paddingRight: "30px",
                  },
                  "& .MuiAutocomplete-endAdornment": {
                    paddingRight: "9px",
                    justifyContent: "flex-end",
                  },
                  "& .MuiAutocomplete-popupIndicator": {
                    marginLeft: "30px",
                  },
                  "& .MuiAutocomplete-clearIndicator": {
                    display: "none",
                  },
                }}
                onKeyPress={(ev) => {
                  if (ev.key === "Enter") {
                    ev.preventDefault();
                    handleSearch();
                  }
                }}
              />
            )}
          />
          <Typography>OR</Typography>
          <Autocomplete
            options={stateSuggestions}
            value={state}
            onChange={handleChangeState}
            renderInput={(params) => (
              <TextField
                {...params}
                label="State"
                type="search"
                sx={{
                  backgroundColor: "snow",
                  width: "210px",
                  "& .MuiAutocomplete-inputRoot": {
                    paddingRight: "30px",
                  },
                  "& .MuiAutocomplete-endAdornment": {
                    paddingRight: "9px",
                    justifyContent: "flex-end",
                  },
                  "& .MuiAutocomplete-popupIndicator": {
                    marginLeft: "30px",
                  },
                  "& .MuiAutocomplete-clearIndicator": {
                    display: "none",
                  },
                }}
                onKeyPress={(ev) => {
                  if (ev.key === "Enter") {
                    ev.preventDefault();
                    handleSearch();
                  }
                }}
              />
            )}
          />

          <Typography>OR</Typography>
          <Autocomplete
            label="City Title"
            options={citySuggestions}
            //value={city}
            onChange={handleChangeCity}
            onInputChange={handleCitySearch}
            sx={{ backgroundColor: "snow" }}
            renderInput={(params) => (
              <TextField
                {...params}
                label="City"
                type="search"
                sx={{
                  backgroundColor: "snow",
                  width: "210px",
                  "& .MuiAutocomplete-inputRoot": {
                    paddingRight: "30px",
                  },
                  "& .MuiAutocomplete-endAdornment": {
                    paddingRight: "9px",
                    justifyContent: "flex-end",
                  },
                  "& .MuiAutocomplete-popupIndicator": {
                    marginLeft: "30px",
                  },
                  "& .MuiAutocomplete-clearIndicator": {
                    display: "none",
                  },
                }}
                onKeyPress={(ev) => {
                  if (ev.key === "Enter") {
                    ev.preventDefault();
                    handleSearch();
                  }
                }}
              />
            )}
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
