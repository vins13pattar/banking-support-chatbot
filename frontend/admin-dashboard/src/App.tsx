import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Tickets from './pages/Tickets';

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Navigate to="/approvals" replace />} />
            <Route path="/approvals" element={<Dashboard />} />
            <Route path="/tickets" element={<Tickets />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
