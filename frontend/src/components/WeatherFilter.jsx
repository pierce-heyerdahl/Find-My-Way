import { Box, Slider } from "@mui/material";

const marks = [
  {
    value: 0,
    label: "0°C",
  },
  {
    value: 35,
    label: "35°C",
  },
  {
    value: 70,
    label: "70°C",
  },
  {
    value: 100,
    label: "100°C",
  },
];

const WeatherFilter = () => {
  return (
    <Box sx={{ width: 300 }}>
      <Slider
        defaultValue={70}
        step={5}
        valueLabelDisplay="auto"
        marks={marks}
      />
    </Box>
  );
};

export default WeatherFilter;
