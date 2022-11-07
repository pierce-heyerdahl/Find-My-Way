import { BrowserRouter, Route, Routes } from "react-router-dom";
//import './index.css';
import Header from "./components/Header";
import Main from "./pages/Main";
import MapView from "./pages/MapView";
import NotFoundPage from "./pages/NotFoundPage";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Header />}>
          <Route index element={<Main />} />
          <Route path="mapview" element={<MapView />} />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
