import { Route, Routes, Link } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Kanban from './pages/Kanban'
import DealDetail from './pages/DealDetail'
import Stats from './pages/Stats'
import Offline from './pages/Offline'

export default function App() {
  return (
    <div>
      <nav style={{ padding: 8, borderBottom: '1px solid #ddd' }}>
        <Link to="/">Kanban</Link> | <Link to="/stats">Stats</Link> | <Link to="/offline">Offline</Link>
      </nav>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<Kanban />} />
        <Route path="/deals/:id" element={<DealDetail />} />
        <Route path="/stats" element={<Stats />} />
        <Route path="/offline" element={<Offline />} />
      </Routes>
    </div>
  )
}

