import { render, screen } from '@testing-library/react'
import Map from '../Map'
import { BrowserRouter } from 'react-router-dom'

jest.mock("../Map", () => {
    return function DummyMap(props) {
        return (
            <div data-testid="map">
                {props.center.lat}:{props.center.long}
            </div>
        );
    };
});

it('should render Map component', () => {
    const center = { lat: 0, long: 0 };
    render(<BrowserRouter><Map center={center}/></BrowserRouter>);
});