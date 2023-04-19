import * as React from "react";
import Box from "@mui/material/Box";
import Slider from "@mui/material/Slider";

const DEFAULT_MAX_VALUE = 1000000;
const DEFAULT_MIN_VALUE = 0;
const DEFAULT_VALUE = [300000, 500000];

function valuetext(value) {
  return `${value}`;
}

function numberWithCommas(value) {
  return "$" + value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

const RangeSlider = ({
  value = DEFAULT_VALUE,
  max = DEFAULT_MAX_VALUE,
  min = DEFAULT_MIN_VALUE,
  onChange,
}) => {
  const handleChange = (event, newValue) => {
    onChange && onChange(newValue);
  };

  return (
    <Box sx={{ width: 300 }}>
      <Slider
        getAriaLabel={() => "Salary range"}
        value={value}
        onChange={handleChange}
        valueLabelDisplay="auto"
        getAriaValueText={valuetext}
        valueLabelFormat={numberWithCommas}
        min={min}
        max={max}
        step={1000}
      />
    </Box>
  );
};

export default RangeSlider;