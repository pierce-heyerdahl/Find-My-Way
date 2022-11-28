import { useState, useEffect, useRef } from "react";
import { TextField, Box, Button, Stack, Typography } from "@mui/material";
import FilterList from "../components/FilterList";
import FilterItem from "../components/FilterItem";
import { Link, useNavigate } from "react-router-dom";

const Main = () => {
  const inputRef = useRef(null);
  const [data, setData] = useState([{}]);
  const [searchInput, setSearchInput] = useState([{}]);

  const navigate = useNavigate();

  useEffect(() => {
    fetch("/test")
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        console.log(data);
      });
  }, []);

  const handleClick = () => {
    setSearchInput(inputRef.current.value);
    console.log(searchInput);
    console.log(inputRef.current.value);
    navigate('/mapview', { state: { job_title: inputRef.current.value } });
  };

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
          <TextField inputRef={inputRef} label="Job Title" type="search" />
          <Typography>OR</Typography>
          <TextField label="State" type="search" />
          
            <Button variant="contained" onClick={handleClick}>
              Search in Map
            </Button>
          
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
