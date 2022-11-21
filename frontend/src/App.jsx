import { BrowserRouter, Route, Routes } from "react-router-dom";
//import './index.css';
import WithHeader from "./components/WithHeader";
import Main from "./pages/Main";
import MapView from "./pages/MapView";
import NotFoundPage from "./pages/NotFoundPage";

import "./index.css";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<WithHeader />}>
          <Route index element={<Main />} />
          <Route path="mapview" element={<MapView />} />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
