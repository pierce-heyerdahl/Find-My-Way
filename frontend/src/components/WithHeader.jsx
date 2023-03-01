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

  const handleTooltipOpen = function (event) {
    event.preventDefault();
    setIsTooltipOpen(true);
  };

  return (
    <Box sx={{ height: "100vh" }}>
      <header
        style={{
          backgroundColor: "snow",
          filter: "drop-shadow(0px 4px 8px rgba(0, 0, 0, 0.1))",
          zIndex: 1,
        }}
      >
        <Box
          //CSS prop.
          sx={{
            alignItems: "center",
            boxSizing: "border-box",
            display: "flex",
            height: 56,
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
            sx={{ fontSize: 30, ml: 2.5 }}
            color="primary"
          >
            Find My Way
          </Button>
          <Box>
            <ClickAwayListener onClickAway={handleTooltipClose}>
              <Tooltip
                title="Disclaimer: Find My Way is designed to help users find future careers and locations to live. The data used by Find My Way is sourced directly from the United States Bureau of Labor Statistics."
                open={isTooltipOpen}
              >
                <Icon onClick={handleTooltipOpen}>priority_high</Icon>
              </Tooltip>
            </ClickAwayListener>
          </Box>
        </Box>
      </header>
      <Outlet />
    </Box>
  );
}

/*style{({ isActive }) =>
                isActive ? undefined : hideComponentStyle}*/

export default WithHeader;
