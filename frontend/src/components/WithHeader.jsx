import React from "react";
import { Outlet } from "react-router-dom";
import { Box, Button, Tooltip, Icon, ClickAwayListener } from "@mui/material";
import { NavLink } from "react-router-dom";

const hideComponentStyle = {
  display: "none",
};

function WithHeader() {
  const [isTooltipOpen, setIsTooltipOpen] = React.useState(false);

  const handleTooltipClose = function () {
    setIsTooltipOpen(false);
  };

  const handleTooltipOpen = function () {
    setIsTooltipOpen(true);
  };

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
          <Box>
            <NavLink
              to="/"
              style={({ isActive }) =>
                isActive ? hideComponentStyle : undefined
              }
            >
              <Button>Back</Button>
            </NavLink>
          </Box>
          <Button
            size="large"
            href="/"
            variant="text"
            sx={{ fontSize: 25, ml: 2.5 }}
            color="primary"
          >
            Find My Way
          </Button>
          <Box>
            <NavLink
              to="/"
              style={({ isActive }) =>
                isActive ? undefined : hideComponentStyle
              }
            >
              <ClickAwayListener onClickAway={handleTooltipClose}>
                <Tooltip
                  title="Disclaimer: Find My Way is designed to help users find future careers and locations to live. The data used by Find My Way is sourced directly from the United States Bureau of Labor Statistics."
                  open={isTooltipOpen}
                >
                  <Icon onClick={handleTooltipOpen}>priority_high</Icon>
                </Tooltip>
              </ClickAwayListener>
            </NavLink>
          </Box>
        </Box>
      </header>
      <Outlet />
    </Box>
  );
}

export default WithHeader;
