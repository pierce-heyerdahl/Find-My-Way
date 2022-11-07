import React from "react";
import { Outlet } from "react-router-dom";
import { Box, Typography, Button } from "@mui/material";

function Header() {
  return (
    <header>
      <Box>
        <Box
          alignItems="center"
          boxSizing="border-box"
          display="flex"
          height={40}
          width="100%"
          px={2}
          py={1}
        >
          <Typography>TEST</Typography>
          <Button size="large" href="/" variant="text">
            Find My Way
          </Button>
        </Box>
        <Outlet />
      </Box>
    </header>
  );
}

export default Header;
