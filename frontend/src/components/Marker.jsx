import React from "react";

const Marker = ({ position, map }) => {
    console.log({position});

    const [marker, setMarker] = React.useState();

    React.useEffect(() => {
      setMarker(new window.google.maps.Marker({}));  
    }, []);

    if (marker) {
        marker.setMap(map);
        marker.setPosition(position);
    }
  
    return null;
  };
  
  export default Marker;