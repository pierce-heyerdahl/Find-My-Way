import { useState, useEffect } from "react";
import { TextField, Box, Button, Stack, Typography } from "@mui/material";
import FilterList from "../components/FilterList";
import FilterItem from "../components/FilterItem";
import { Link } from "react-router-dom";

const Main = () => {
  const [data, setData] = useState([{}]);

  useEffect(() => {
    fetch("/test")
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        console.log(data);
      });
  }, []);

  return (
    <Box p={2}>
      <Box display="flex" justifyContent="center">
        <Stack
          alignItems="center"
          display="flex"
          justifyContent="center"
          spacing={2}
          width="400px"
        >
          <TextField label="Job Title" type="search" />
          <Typography>OR</Typography>
          <TextField label="City" type="search" />
          <Link to="/mapview">
            <Button variant="contained">
              Search in Map
            </Button>
          </Link>
          <FilterList>
            <FilterItem label="Avg. Rent Amount" />
            <FilterItem label="Big Mac Price" />
            <FilterItem label="Avg. Utility Cost" />
          </FilterList>
        </Stack>
      </Box>

      <Box>
        {typeof data.numbers === "undefined" ? (
          <p>Loading...</p>
        ) : (
          data.numbers.map((number, i) => <p key={i}>{number}</p>)
        )}
      </Box>
    </Box>
  );
};

export default Main;
