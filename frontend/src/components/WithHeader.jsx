import React from "react";
import { Outlet } from "react-router-dom";
import { Box, Typography, Button } from "@mui/material";

function WithHeader() {
  return (
    <Box sx={{ height: "100vh" }}>
      <header>
        <Box
          //CSS prop.
          sx={{
            alignItems: "center",
            boxSizing: "border-box",
            display: "flex",
            height: 58,
            justifyContent: "space-between",
            px: 2,
            py: 1,
            width: "100%",
          }}
        >
          <Box sx={{ background: "red", height: "100%", width: "100px" }}>
            Back
          </Box>
          <Button size="large" href="/" variant="text" sx={{ fontSize: 24 }}>
            Find My Way
          </Button>
          <Box sx={{ background: "blue", height: "100%", width: "100px" }}>
            Disclaimer
          </Box>
        </Box>
      </header>
      <Outlet />
    </Box>
  );
}

export default WithHeader;
