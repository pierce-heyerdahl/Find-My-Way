import React, { useState } from "react";
import { Checkbox, FormControlLabel } from "@mui/material";

const FilterItem = (props) => {
  const [isChecked, setIsChecked] = useState(false);
  const { label } = props;

  const handleChange = (event) => {
    console.log(`Checkbox ${label} is clicked!, ${event.target.checked}`);
    setIsChecked(event.target.checked);
  };

  return (
    <FormControlLabel
      control={
        <Checkbox
          checked={isChecked}
          onChange={handleChange}
          sx={{ marginRight: "10px" }}
        />
      }
      label={label}
      sx={{ marginLeft: 0 }}
    />
  );
};

export default FilterItem;
