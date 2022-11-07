import { Box, FormGroup, Stack, Typography } from "@mui/material";

const FilterList = (props) => {
  const { children } = props;

  return (
    <Box>
      <Typography mb="2">Filters</Typography>
      <FormGroup>
        <Stack spacing={1}>{children}</Stack>
      </FormGroup>
    </Box>
  );
};

export default FilterList;
