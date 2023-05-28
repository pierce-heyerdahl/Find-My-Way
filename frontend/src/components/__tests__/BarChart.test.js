import { render, screen } from '@testing-library/react'
import BarChart from '../BarChart'
import { BrowserRouter } from 'react-router-dom'

it('should render BarChart component', () => {
    render(<BrowserRouter><BarChart/></BrowserRouter>);
});