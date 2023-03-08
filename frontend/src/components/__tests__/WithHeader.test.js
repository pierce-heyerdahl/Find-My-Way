import { render, screen } from '@testing-library/react'
import WithHeader from '../WithHeader'
import { BrowserRouter } from 'react-router-dom'

it('should render WithHeader component', () => {
    render(<BrowserRouter><WithHeader/></BrowserRouter>);
    screen.getByText(/Find My Way/i);
});